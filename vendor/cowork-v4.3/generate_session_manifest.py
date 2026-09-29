#!/usr/bin/env python3
"""
generate_session_manifest.py — Buat _SESSION-MANIFEST.json di awal Task 01.

Manifest mencatat daftar file yang ADA di 00-input/ folder penugasan aktif,
beserta hash SHA-256 dan timestamp. Manifest ini WAJIB di-validate setiap
kali Claude akan baca file untuk analisis (Task 03 / Task 04).

Tujuan: cegah Claude membaca file dari folder penugasan LAIN, dari wiki/,
dari pattern-library/, atau dari memori percakapan sesi sebelumnya.

Aturan whitelist:
  - File yang boleh dipakai sebagai SUMBER FAKTA: hanya yang tercantum di manifest
  - Wiki, pattern-library, references: hanya boleh dipakai untuk KRITERIA/regulasi
    (Perpres, PMK, dll) dan untuk pattern temuan — TIDAK untuk fakta/data/angka

CLI:
  python3 scripts/generate_session_manifest.py --penugasan penugasan/2026-001-xxx
  python3 scripts/generate_session_manifest.py --penugasan penugasan/2026-001-xxx --force
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

WIB = timezone(timedelta(hours=7))


def _now_iso():
    return datetime.now(WIB).isoformat(timespec="seconds")


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _scan_input(input_dir: Path) -> list:
    """Scan 00-input/ recursively, return list of file metadata."""
    out = []
    for p in sorted(input_dir.rglob("*")):
        if p.is_file() and not p.name.startswith("."):
            try:
                stat = p.stat()
                out.append({
                    "path": str(p.relative_to(input_dir.parent)),
                    "name": p.name,
                    "size_bytes": stat.st_size,
                    "sha256": _hash_file(p),
                    "mtime": datetime.fromtimestamp(stat.st_mtime, WIB).isoformat(timespec="seconds"),
                })
            except OSError as e:
                sys.stderr.write(f"WARN: gagal hash {p}: {e}\n")
    return out


def main():
    ap = argparse.ArgumentParser(description="Generate session manifest untuk isolasi data per penugasan.")
    ap.add_argument("--penugasan", required=True, help="Path folder penugasan")
    ap.add_argument("--force", action="store_true", help="Timpa manifest yang sudah ada")
    args = ap.parse_args()

    pdir = Path(args.penugasan).resolve()
    if not pdir.is_dir():
        sys.stderr.write(f"ERROR: folder penugasan tidak ditemukan: {pdir}\n")
        sys.exit(1)

    input_dir = pdir / "00-input"
    if not input_dir.is_dir():
        sys.stderr.write(f"ERROR: folder 00-input/ tidak ditemukan di {pdir}\n")
        sys.stderr.write("       Pastikan ST, KP, PKP, dan dokumen pendukung sudah di-upload.\n")
        sys.exit(2)

    manifest_path = pdir / "_SESSION-MANIFEST.json"
    if manifest_path.exists() and not args.force:
        sys.stderr.write(f"ERROR: {manifest_path.name} sudah ada. Pakai --force untuk timpa.\n")
        sys.exit(3)

    files = _scan_input(input_dir)
    if not files:
        sys.stderr.write(f"ERROR: tidak ada file di 00-input/. Upload dokumen dulu.\n")
        sys.exit(2)

    manifest = {
        "schema_version": "v1.0",
        "penugasan_dir": str(pdir.name),
        "generated_at": _now_iso(),
        "input_dir": str(input_dir.relative_to(pdir)),
        "total_files": len(files),
        "files": files,
        "whitelist_rules": {
            "fakta_sumber": "Hanya file di array 'files' di atas yang boleh dipakai sebagai SUMBER FAKTA (kondisi, angka, tanggal, nama, dll) di temuan KKP.",
            "wiki_allowed_for": ["pattern_temuan", "kriteria_regulasi", "best_practice"],
            "wiki_forbidden_for": ["fakta_kondisi", "fakta_data", "fakta_angka", "fakta_nama"],
            "pattern_library_allowed_for": ["referensi_pattern_temuan"],
            "pattern_library_forbidden_for": ["fakta_temuan_baru"],
            "memori_chat_forbidden": "Fakta dari percakapan/sesi sebelumnya DILARANG masuk ke temuan baru, kecuali secara eksplisit ada di file di array 'files' sesi ini."
        }
    }

    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: manifest di-generate di {manifest_path}")
    print(f"     {len(files)} file ter-cantum sebagai whitelist sumber fakta.")
    for f in files:
        print(f"     - {f['name']} ({f['size_bytes']:,} bytes)")
    sys.exit(0)


if __name__ == "__main__":
    main()
