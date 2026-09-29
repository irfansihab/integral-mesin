#!/usr/bin/env python3
"""
check_isolation.py — Pre-flight check anti-kontaminasi lintas-sesi.

Dipanggil OTOMATIS di akhir Task 03 (sebelum gate auditor SETUJU) dan
di awal Task 04 (sebelum konsumsi temuan.json). Tujuan: cegah temuan
yang berisi fakta dari folder penugasan LAIN atau dari memori chat
sesi sebelumnya.

Cek yang dilakukan:
  1. _SESSION-MANIFEST.json ada dan valid.
  2. Hash file di 00-input/ masih sesuai manifest (file tidak berubah/
     dihapus tanpa regenerate manifest).
  3. Setiap temuan di temuan.json punya field 'dokumen_sumber' yang
     non-kosong, dan file yang dirujuk ADA di whitelist manifest.
  4. Tidak ada nama file dokumen_sumber yang berasal dari folder lain
     (mis. nama file penugasan lain).

Exit codes:
  0  Semua cek OK, aman lanjut.
  1  Error setup (manifest tidak ada, folder salah).
  2  Manifest invalid (hash file tidak match — file berubah/hilang).
  3  Temuan terkontaminasi (referensi file di luar whitelist).

CLI:
  python3 scripts/check_isolation.py --penugasan penugasan/2026-001-xxx
  python3 scripts/check_isolation.py --penugasan penugasan/2026-001-xxx --strict
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_manifest(pdir: Path) -> dict:
    p = pdir / "_SESSION-MANIFEST.json"
    if not p.exists():
        sys.stderr.write(f"ERROR: _SESSION-MANIFEST.json tidak ditemukan di {pdir}.\n")
        sys.stderr.write("       Jalankan: python3 scripts/generate_session_manifest.py --penugasan ...\n")
        sys.exit(1)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"ERROR: manifest rusak: {e}\n")
        sys.exit(1)


def _verify_hashes(pdir: Path, manifest: dict, strict: bool) -> list:
    """Re-hash file di 00-input/ dan cocokkan dengan manifest. Return list of anomalies."""
    anomalies = []
    for fmeta in manifest.get("files", []):
        relpath = fmeta["path"]
        full = pdir.parent / relpath
        # Resolve relative to penugasan parent (manifest path is relative to pdir.name/00-input/...)
        if not full.exists():
            # try relative to pdir
            full = pdir / Path(relpath).relative_to(pdir.name) if relpath.startswith(pdir.name) else pdir / relpath
        if not full.exists():
            anomalies.append(f"FILE HILANG: {relpath} tercantum di manifest tapi tidak ada di disk.")
            continue
        actual_hash = _hash_file(full)
        if actual_hash != fmeta["sha256"]:
            msg = f"HASH MISMATCH: {fmeta['name']} berubah sejak manifest dibuat."
            if strict:
                anomalies.append(msg)
            else:
                sys.stderr.write(f"WARN: {msg} (di-skip karena tidak strict)\n")
    return anomalies


def _check_temuan_sources(pdir: Path, manifest: dict) -> list:
    """Cek setiap temuan punya dokumen_sumber yang valid (ada di manifest)."""
    temuan_path = pdir / "_KKP" / "temuan.json"
    if not temuan_path.exists():
        return []  # Task 03 belum jalan, no temuan to check

    try:
        data = json.loads(temuan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"temuan.json rusak: {e}"]

    whitelist_names = {f["name"] for f in manifest.get("files", [])}
    whitelist_paths = {f["path"] for f in manifest.get("files", [])}

    anomalies = []
    for i, t in enumerate(data.get("temuan", []), start=1):
        id_t = t.get("id_temuan", f"#{i}")
        sumber = t.get("dokumen_sumber", [])
        if not sumber:
            anomalies.append(f"{id_t}: TIDAK ADA dokumen_sumber. Setiap temuan WAJIB cite dokumen dari 00-input/.")
            continue
        for s in sumber:
            fname = s.get("file", "")
            if not fname:
                anomalies.append(f"{id_t}: dokumen_sumber.file kosong.")
                continue
            # Cek apakah file ada di whitelist (by name atau by path)
            if fname not in whitelist_names and fname not in whitelist_paths \
               and not any(fname.endswith(w) for w in whitelist_names):
                anomalies.append(
                    f"{id_t}: dokumen_sumber merujuk file '{fname}' yang TIDAK ADA "
                    f"di whitelist manifest. Kemungkinan kontaminasi dari folder lain "
                    f"atau memori sesi sebelumnya."
                )
    return anomalies


def main():
    ap = argparse.ArgumentParser(description="Cek isolasi sesi: pastikan temuan tidak terkontaminasi sumber luar.")
    ap.add_argument("--penugasan", required=True)
    ap.add_argument("--strict", action="store_true",
                    help="Fail kalau hash file di 00-input/ tidak match manifest")
    ap.add_argument("--skip-hash", action="store_true",
                    help="Skip verifikasi hash (hanya cek temuan vs whitelist)")
    args = ap.parse_args()

    pdir = Path(args.penugasan).resolve()
    if not pdir.is_dir():
        sys.stderr.write(f"ERROR: folder tidak ditemukan: {pdir}\n")
        sys.exit(1)

    manifest = _load_manifest(pdir)
    print(f"Manifest loaded: {manifest.get('total_files', 0)} file di whitelist (generated {manifest.get('generated_at')})")

    # Cek 1: hash file (Lapis 3)
    hash_anomalies = []
    if not args.skip_hash:
        hash_anomalies = _verify_hashes(pdir, manifest, strict=args.strict)
        if hash_anomalies:
            sys.stderr.write("\n=== ANOMALI HASH (Lapis 3) ===\n")
            for a in hash_anomalies:
                sys.stderr.write(f"  ✗ {a}\n")
            if args.strict:
                sys.exit(2)

    # Cek 2: temuan sumber (Lapis 5)
    src_anomalies = _check_temuan_sources(pdir, manifest)
    if src_anomalies:
        sys.stderr.write("\n=== KONTAMINASI TEMUAN (Lapis 5) ===\n")
        for a in src_anomalies:
            sys.stderr.write(f"  ✗ {a}\n")
        sys.stderr.write(f"\nTotal anomali: {len(src_anomalies)}\n")
        sys.stderr.write("Inject ke INTEGRAL DIBLOKIR. Perbaiki temuan dulu — pastikan setiap\n")
        sys.stderr.write("fakta cite dokumen yang ada di 00-input/ sesi ini.\n")
        sys.exit(3)

    print(f"OK: semua cek isolasi PASSED.")
    print(f"     - Hash file 00-input/: {'OK' if not hash_anomalies else 'WARN (non-strict)'}")
    print(f"     - Temuan vs whitelist: OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
