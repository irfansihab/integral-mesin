#!/usr/bin/env python3
"""Bangun plugin Cowork `integral-mesin` dari `knowledge/` milik INTEGRAL FULL.

    python3 bangun.py                       # FULL diasumsikan di ../sistem audit v10
    python3 bangun.py --full /jalur/ke/repo-full --versi 2026.9.28
    python3 bangun.py --dengan-pdf          # ikutkan PDF mentah regulasi (+±50 MB)
    python3 bangun.py --hanya-uji           # bangun & uji, jangan bungkus

FULL HANYA DIBACA. Folder ini berdiri sendiri: yang berubah di sini tidak
menyentuh repo FULL, dan sebaliknya perubahan pengetahuan tetap dikerjakan di
FULL — plugin dibangun ulang darinya.

Yang dilakukan, berurutan, dan tiap langkah punya cara gagalnya sendiri:
 1. salin knowledge/ ke build/, kecuali draf, arsip, tasks/, PDF mentah
 2. tulis `description` ke frontmatter tiap SKILL.md — Cowork memicu skill dari
    kalimat itu; INTEGRAL tidak memakainya, jadi belum ada
 3. sisipkan skill payung `integral-mesin` (orkestrasi & doktrin) dari payung/
 4. tulis .claude-plugin/plugin.json, README.md, VERSI.txt (versi + sidik isi)
 5. jalankan uji penjaga FULL pada ISI PAKET (bukan pada repo):
    uji_doktrin_bersama.py & uji_kutipan_pola.py lewat APP_SKILLS_PATH/APP_WIKI_PATH,
    ditambah uji format plugin di sini
 6. bungkus menjadi keluaran/integral-mesin-<versi>.plugin (zip) + catatan sidik

Paket yang gagal uji TIDAK dibungkus — bukan dibungkus dengan peringatan.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

DI_SINI = Path(__file__).resolve().parent
NAMA = "integral-mesin"

# Folder/berkas yang TIDAK ikut. `_draft` = skill yang belum layak dipakai agen;
# `_ARSIP*` = template lama; `tasks/` = catatan kerja pengembang.
_KECUALI_DIR = {"_draft", "tasks", "__pycache__", ".git"}
_KECUALI_DIR_AWALAN = ("_ARSIP",)
_KECUALI_BERKAS = {".DS_Store", "pengetahuan-bawaan.json"}

# Frasa pemicu per skill — Cowork memutuskan skill mana yang dimuat dari sini.
# Yang tak ada di peta memakai jenis-nya saja (masih berfungsi, kurang tajam).
_PEMICU = {
    "reviu-rka-kl": '"reviu TOR", "reviu KAK", "reviu RKA-K/L", "periksa RAB", "cek TOR ini"',
    "reviu-pengadaan": '"reviu pengadaan", "reviu RUP", "reviu HPS", "reviu dokumen tender", "cek SIRUP"',
    "audit-pengadaan": '"audit pengadaan", "audit PBJ", "audit kontrak", "periksa kelebihan bayar", "audit BAST"',
    "pemantauan-pengadaan": '"pemantauan pengadaan", "pantau kontrak", "progres fisik keuangan", "monitoring PBJ"',
    "konsultasi-pengadaan": '"konsultasi pengadaan", "pendampingan PBJ", "tanya aturan pengadaan", "boleh tidak … dalam pengadaan"',
    "audit-kinerja": '"audit kinerja", "audit efektivitas", "audit program", "3E", "2E"',
    "audit-umum": '"audit umum", "audit dengan kriteria ini", "audit kepatuhan", "audit ketaatan"',
    "evaluasi-sakip": '"evaluasi SAKIP", "evaluasi AKIP", "LKE SAKIP", "nilai akuntabilitas kinerja"',
    "evaluasi-spip": '"kerjakan PK SPIP", "isi KKLEAD", "buka aplikasi SPIP", "PK level kementerian/K-L", "penjaminan kualitas SPIP", "LKE SPIP", "maturitas SPIP"',
    "evaluasi-reformasi-birokrasi": '"evaluasi RB", "evaluasi reformasi birokrasi", "LKE RB", "zona integritas"',
    "evaluasi-manajemen-risiko": '"evaluasi manajemen risiko", "evaluasi MR", "register risiko", "piagam risiko"',
    "evaluasi-umum": '"evaluasi dengan kriteria ini", "evaluasi program", "evaluasi kebijakan"',
    "reviu-laporan-keuangan": '"reviu laporan keuangan", "reviu LK", "reviu LRA/Neraca/LO/LPE/CaLK", "reviu LK semester"',
    "reviu-pipk": '"reviu PIPK", "pengendalian intern pelaporan keuangan", "reviu PIPK satker"',
    "reviu-pnbp": '"reviu PNBP", "reviu penerimaan negara bukan pajak", "piutang PNBP", "tarif PNBP"',
    "reviu-umum": '"reviu dengan kriteria ini", "reviu dokumen", "reviu juklak"',
    "pemantauan-tindak-lanjut": '"pemantauan tindak lanjut", "TLHP", "status rekomendasi", "tindak lanjut BPK"',
    "pemantauan-umum": '"pemantauan", "pantau realisasi", "monitoring rencana aksi"',
    "konsultansi-umum": '"konsultansi", "minta pendapat", "advisory", "pertanyaan tertulis"',
}


# Skrip yang ikut paket. Perender & QC dari FULL (turunan Cowork v4 yang sudah mengikuti
# doktrin 17 Jun 2026 dan placeholder per skill); isolasi sumber dari Cowork v4.3 (FULL tak punya).
_DARI_FULL = ("backend/v6/scripts/render_kkp.py", "backend/v6/scripts/render_lhp.py",
              "backend/v6/scripts/qc_saipi.py", "backend/v6/scripts/audit_trail.py",
              "backend/app/perencanaan_docx.py", "backend/app/export_perencanaan.py",
              "backend/app/lapisan_lhp.py")
_DARI_VENDOR = ("vendor/cowork-v4.3/generate_session_manifest.py", "vendor/cowork-v4.3/check_isolation.py")
# Tambalan minimal. Build GAGAL bila teks sumber berubah — tambalan tak pernah diam-diam hilang.
_TAMBAL = {
    "qc_saipi.py": ('CHECKLIST_PATH = ROOT / "skills" / "kepatuhan-saipi" / "references" / "checklist-saipi-per-penugasan.json"',
                    'CHECKLIST_PATH = Path(__import__("os").environ.get("INTEGRAL_CHECKLIST_SAIPI") or '
                    'ROOT / "skills" / "kepatuhan-saipi" / "references" / "checklist-saipi-per-penugasan.json")'),
    # Server membaca akar wiki dari app.config; di paket, wiki ada di AKAR/wiki.
    # Yang dipakai mesin hanya resolve_template/template_fields/render_template —
    # write_perencanaan (gerbang PIA server) tak pernah dipanggil di Cowork.
    "export_perencanaan.py": ('    from app.config import get_settings\n    return get_settings().wiki_path / "templates"',
                              '    import os\n    return Path(os.environ["INTEGRAL_AKAR"]) / "wiki" / "templates"'),
}


def _frontmatter(teks: str) -> tuple[dict, int, int]:
    """(peta, awal_isi, akhir_frontmatter) — akhir = indeks baris '---' penutup."""
    baris = teks.splitlines()
    if not baris or baris[0].strip() != "---":
        return {}, 0, -1
    peta: dict = {}
    kunci_lipat: str | None = None  # kunci ber-nilai `>` / `|` — barisnya menyusul, menjorok
    for i in range(1, len(baris)):
        if baris[i].strip() == "---":
            return peta, i + 1, i
        if kunci_lipat and (baris[i].startswith("  ") or not baris[i].strip()):
            peta[kunci_lipat] = (peta[kunci_lipat] + " " + baris[i].strip()).strip()
            continue
        kunci_lipat = None
        m = re.match(r"^([A-Za-z_][\w\-]*):\s*(.*)$", baris[i])
        if m:
            nilai = m.group(2).strip()
            if nilai in (">", "|", ">-", "|-"):
                kunci_lipat, nilai = m.group(1), ""
            peta[m.group(1)] = nilai.strip('"')
    return {}, 0, -1


def _description(slug: str, fm: dict) -> str:
    jenis = fm.get("jenis", slug).strip()
    pemicu = _PEMICU.get(slug, f'"{slug.replace("-", " ")}"')
    return (
        f"Gunakan skill ini saat auditor Inspektorat mengerjakan penugasan {jenis} — "
        f"menyusun DPP, Laporan PIA, KKP (Kondisi–Kriteria–Sebab–Akibat), dan LHP awal dari "
        f"dokumen penugasan. Pemicu: {pemicu}, atau folder berisi Surat Tugas jenis ini. "
        f"Dimuat oleh skill payung integral-mesin; ikuti gate/alur di dalamnya."
    )


def _salin(sumber: Path, tujuan: Path, dengan_pdf: bool) -> list[str]:
    dilewati: list[str] = []
    for akar, dirs, files in os.walk(sumber):
        rel = Path(akar).relative_to(sumber)
        dirs[:] = [d for d in dirs if d not in _KECUALI_DIR and not d.startswith(_KECUALI_DIR_AWALAN)]
        for f in files:
            if f in _KECUALI_BERKAS or f.endswith((".pyc",)):
                continue
            if f.lower().endswith(".pdf") and not dengan_pdf:
                dilewati.append(str(rel / f))
                continue
            (tujuan / rel).mkdir(parents=True, exist_ok=True)
            shutil.copy2(Path(akar) / f, tujuan / rel / f)
    return dilewati


def _sidik_isi(folder: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in folder.rglob("*") if x.is_file()):
        h.update(str(p.relative_to(folder)).encode())
        h.update(hashlib.file_digest(p.open("rb"), "sha256").digest())
    return h.hexdigest()[:16]


def bangun(full: Path, versi: str, dengan_pdf: bool) -> tuple[Path, list[str]]:
    pengetahuan = full / "knowledge"
    if not (pengetahuan / "skills").is_dir() or not (pengetahuan / "wiki").is_dir():
        sys.exit(f"GAGAL: {pengetahuan} bukan folder knowledge/ INTEGRAL (tak ada skills/ atau wiki/)")
    build = DI_SINI / "build" / NAMA
    if build.exists():
        shutil.rmtree(build)
    catatan: list[str] = []

    # 1 · salin
    dilewati = _salin(pengetahuan, build, dengan_pdf)
    catatan.append(f"disalin dari {pengetahuan}; PDF dilewati: {len(dilewati)}" if not dengan_pdf else "PDF mentah ikut")

    # 2 · description
    n_desc = 0
    for md in sorted((build / "skills").glob("*/SKILL.md")):
        slug = md.parent.name
        teks = md.read_text(encoding="utf-8")
        fm, awal, akhir = _frontmatter(teks)
        if akhir < 0:
            sys.exit(f"GAGAL: {md} tanpa frontmatter — tak bisa jadi skill Cowork")
        if fm.get("name", slug) != slug:
            catatan.append(f"PERINGATAN {slug}: name '{fm.get('name')}' ≠ nama folder; disamakan")
        baris = teks.splitlines()
        # buang name/description lama, tulis ulang di atas agar Cowork membacanya lebih dulu
        isi_fm = [b for b in baris[1:akhir] if not re.match(r"^(name|description):", b)]
        desc = fm.get("description") or _description(slug, fm)
        n_desc += 0 if fm.get("description") else 1
        desc_yaml = "description: >\n  " + "\n  ".join(_bungkus(desc, 90))
        md.write_text("\n".join(["---", f"name: {slug}", desc_yaml, *isi_fm, "---", *baris[akhir + 1:]]) + "\n",
                      encoding="utf-8")
    catatan.append(f"description dibangkitkan untuk {n_desc} skill")

    # 3 · payung + skrip mesin (perender & QC dari FULL, isolasi dari Cowork v4.3)
    payung = DI_SINI / "payung" / NAMA
    if not (payung / "SKILL.md").is_file():
        sys.exit(f"GAGAL: skill payung tak ada di {payung}")
    shutil.copytree(payung, build / "skills" / NAMA, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    tujuan_skrip = build / "skills" / NAMA / "scripts"
    for sumber in [full / s for s in _DARI_FULL] + [DI_SINI / s for s in _DARI_VENDOR]:
        if not sumber.is_file():
            sys.exit(f"GAGAL: skrip sumber tak ada: {sumber}")
        teks = sumber.read_text(encoding="utf-8")
        asal = sumber.relative_to(full) if full in sumber.parents else sumber.relative_to(DI_SINI)
        tanda = f"# Disalin bangun.py dari {asal} — jangan disunting di paket; ubah di sumbernya.\n"
        teks = (teks.split("\n", 1)[0] + "\n" + tanda + teks.split("\n", 1)[1]) if teks.startswith("#!") else tanda + teks
        for nama, (a, b) in _TAMBAL.items():
            if sumber.name == nama:
                if a not in teks:
                    sys.exit(f"GAGAL: teks yang ditambal di {nama} sudah berubah di hulu — periksa ulang tambalan")
                teks = teks.replace(a, b)
        (tujuan_skrip / sumber.name).write_text(teks, encoding="utf-8")
    catatan.append(f"skrip mesin: {len(_DARI_FULL)} dari FULL, {len(_DARI_VENDOR)} dari vendor/cowork-v4.3")

    # 4 · manifest, README, VERSI
    sidik = _sidik_isi(build)
    (build / ".claude-plugin").mkdir()
    (build / ".claude-plugin" / "plugin.json").write_text(json.dumps({
        "name": NAMA,
        "version": versi,
        "description": ("Mesin substansi pengawasan Inspektorat II Komdigi: 19 skill jenis pengawasan + "
                        "pengetahuan (pola temuan, regulasi terverifikasi, template) untuk menyusun draf "
                        "DPP, Laporan PIA, KKP, dan LHP awal yang diunggah ke INTEGRAL."),
        "author": {"name": "Inspektorat II — Itjen Komdigi"},
        "keywords": ["apip", "audit", "reviu", "evaluasi", "pemantauan", "komdigi", "integral"],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (build / "VERSI.txt").write_text(f"{NAMA} {versi}\nsidik-isi {sidik}\ndibangun {dt.datetime.now():%Y-%m-%d %H:%M}\n", encoding="utf-8")
    (build / "README.md").write_text(_readme(versi, sidik, dengan_pdf), encoding="utf-8")
    catatan.append(f"versi {versi} · sidik isi {sidik}")
    return build, catatan


def _bungkus(teks: str, lebar: int) -> list[str]:
    kata, baris, sekarang = teks.split(), [], ""
    for k in kata:
        if len(sekarang) + len(k) + 1 > lebar and sekarang:
            baris.append(sekarang); sekarang = k
        else:
            sekarang = f"{sekarang} {k}".strip()
    if sekarang:
        baris.append(sekarang)
    return baris


def _readme(versi: str, sidik: str, dengan_pdf: bool) -> str:
    return f"""# Plugin: INTEGRAL Mesin — versi {versi}

Plugin Cowork untuk auditor **Inspektorat II — Itjen Komdigi**. Berisi 19 skill jenis
pengawasan INTEGRAL beserta pengetahuannya (pola temuan, teks regulasi terverifikasi,
template DPP/PIA/LHP) — dibangun otomatis dari repo INTEGRAL, sidik isi `{sidik}`.

## Cara pakai
1. Pasang plugin ini di Cowork (Customize → Plugins → pasang dari berkas).
2. Susun folder penugasan: `00-input/` (Surat Tugas, sasaran) · `01-objek/` (dokumen yang
   diperiksa) · `02-kriteria/` (regulasi tambahan, bila ada) · `03-bukti-lapangan/` (bila ada).
3. Buka folder itu di Cowork dan minta: **"kerjakan penugasan ini"**. Skill `integral-mesin`
   memilih skill jenis pengawasan yang sesuai, menyusun DPP dan Laporan PIA lebih dulu,
   lalu KKP dan LHP awal ke `90-keluaran/`.
4. Semua keluaran berlabel **DRAF**. Periksa dengan daftar periksa di akhir
   `Paket-Analisis.md`, lalu unggah ke INTEGRAL untuk persetujuan dan laporan final.

## Versi
Versi tampak di nama berkas plugin dan di `VERSI.txt`; skill payung mencetaknya di tiap
keluaran. Bila ada versi baru, pasang ulang — pengetahuan tak diperbarui dengan cara lain.
{"PDF mentah regulasi ikut disertakan." if dengan_pdf else "PDF mentah regulasi tidak disertakan (ringkasannya ada di `references/*.md`)."}
"""


# ── uji ────────────────────────────────────────────────────────────────────
def uji(build: Path, full: Path) -> list[str]:
    gagal: list[str] = []

    def cek(nama: str, ok: bool, rinci: str = "") -> None:
        print(f"  {'✓' if ok else '✗'} {nama}" + (f" — {rinci}" if rinci else ""))
        if not ok:
            gagal.append(nama)

    print("── format plugin")
    try:
        m = json.loads((build / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        cek("plugin.json valid & name kebab-case", re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", m.get("name", "")) is not None)
        cek("version semver (tanpa nol di depan)", re.fullmatch(r"\d+\.\d+\.\d+", m.get("version", "")) is not None and not re.search(r"(^|\.)0\d", m["version"]))
    except Exception as e:  # noqa: BLE001
        cek("plugin.json terbaca", False, str(e))
    skills = sorted(d for d in (build / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").is_file())
    cek("20 skill (19 + payung) punya SKILL.md", len(skills) == 20, f"{len(skills)}")
    for d in skills:
        fm, _, _ = _frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
        # ≥ 80: description satu-dua kata (atau ">" yang salah baca) tak cukup untuk memicu skill
        cek(f"{d.name}: description 80–700 karakter", 80 <= len(fm.get("description", "")) <= 700, f"{len(fm.get('description', ''))} karakter")
        cek(f"{d.name}: name = folder", fm.get("name") == d.name, fm.get("name"))
    cek("tak ada folder _draft / _ARSIP / tasks", not any(p.name in _KECUALI_DIR or p.name.startswith(_KECUALI_DIR_AWALAN) for p in build.rglob("*") if p.is_dir()))
    besar = sum(p.stat().st_size for p in build.rglob("*") if p.is_file()) / 1e6
    cek("ukuran ≤ 200 MB (batas unggah Cowork)", besar <= 200, f"{besar:.1f} MB")
    for wajib in ("skills/integral-mesin/scripts/mesin.py", "skills/integral-mesin/scripts/render_lhp.py",
                  "skills/integral-mesin/scripts/check_isolation.py", "meta/kepatuhan-saipi/references/checklist-saipi-per-penugasan.json",
                  "skills/evaluasi-spip/references/aplikasi-spip/00-mode-aplikasi.md",
                  "wiki/konteks/regulasi", "wiki/temuan-patterns", "templates/_skeleton-lhp",
                  "skills/panduan-format-umum/PANDUAN.md", "skills/panduan-format-umum/kodefikasi-temuan.md",
                  "skills/integral-mesin/references"):
        cek(f"ada: {wajib}", (build / wajib).exists())

    print("── uji penjaga FULL pada ISI PAKET")
    py = full / "backend" / ".venv" / "bin" / "python"
    if not py.exists():
        py = full / "backend" / ".venv" / "Scripts" / "python.exe"
    # Frontmatter SKILL.md harus YAML sah menurut parser SUNGGUHAN (PyYAML di venv FULL).
    # Parser buatan di bangun.py dan di server memaafkan apa saja; Cowork tidak — metadata
    # dibuang diam-diam dan skill tak terpicu (8–9 Okt 2026, 18 dari 19 skill).
    r = subprocess.run([str(py), "-c", "import re,sys,yaml,pathlib\n"
                        "g=[]\n"
                        "for f in sorted(pathlib.Path(sys.argv[1]).glob('skills/*/SKILL.md')):\n"
                        "    m=re.match(r'^---\\n(.*?)\\n---', f.read_text(encoding='utf-8'), re.S)\n"
                        "    try: assert isinstance(yaml.safe_load(m.group(1)), dict)\n"
                        "    except Exception as e: g.append(f'{f.parent.name}: {getattr(e, \"problem\", e)}')\n"
                        "print('\\n'.join(g)); sys.exit(1 if g else 0)", str(build)], capture_output=True, text=True)
    cek("frontmatter semua SKILL.md sah menurut PyYAML", r.returncode == 0, r.stdout.strip()[:300])
    # Validator resmi, bila CLI `claude` ada di mesin pembangun.
    if shutil.which("claude"):
        r = subprocess.run(["claude", "plugin", "validate", str(build)], capture_output=True, text=True)
        galat = [b.strip() for b in (r.stdout + r.stderr).splitlines() if "❯" in b]
        cek("`claude plugin validate` tanpa galat", r.returncode == 0 and not galat, (galat[0][:200] if galat else (r.stdout + r.stderr).strip()[-200:]))
    env = dict(os.environ, PYTHONPATH=str(full / "backend"),
               APP_SKILLS_PATH=str(build / "skills"), APP_WIKI_PATH=str(build / "wiki"))
    for skrip in ("uji_doktrin_bersama.py", "uji_kutipan_pola.py"):
        r = subprocess.run([str(py), str(full / "backend" / "scripts" / skrip)], env=env,
                           cwd=full / "backend", capture_output=True, text=True)
        akhir = (r.stdout.strip().splitlines() or ["(tanpa keluaran)"])[-1]
        cek(f"{skrip}: {akhir[:80]}", r.returncode == 0 and akhir.startswith("LULUS"))
        if r.returncode != 0:
            print("\n".join("      " + b for b in (r.stdout + r.stderr).strip().splitlines()[-12:]))
    print("── ujung ke ujung mesin.py pada ISI PAKET")
    r = subprocess.run([str(py), str(DI_SINI / "uji" / "uji_mesin.py"), "--akar", str(build)], capture_output=True, text=True)
    print("\n".join("    " + b for b in (r.stdout + r.stderr).strip().splitlines()))
    cek("uji_mesin.py", r.returncode == 0)
    return gagal


def bungkus(build: Path, versi: str) -> Path:
    keluaran = DI_SINI / "keluaran"
    keluaran.mkdir(exist_ok=True)
    tujuan = keluaran / f"{NAMA}-{versi}.plugin"
    with zipfile.ZipFile(tujuan, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(x for x in build.rglob("*") if x.is_file()):
            z.write(p, p.relative_to(build))
    sidik = hashlib.file_digest(tujuan.open("rb"), "sha256").hexdigest()
    (keluaran / f"{NAMA}-{versi}.sha256").write_text(f"{sidik}  {tujuan.name}\n", encoding="utf-8")
    return tujuan


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", default=str(DI_SINI.parent / "sistem audit v10"))
    ap.add_argument("--versi", default=f"{dt.date.today():%Y}.{dt.date.today().month}.{dt.date.today().day}")
    ap.add_argument("--dengan-pdf", action="store_true")
    ap.add_argument("--hanya-uji", action="store_true")
    a = ap.parse_args()
    full = Path(a.full).expanduser().resolve()
    print(f"═══ bangun {NAMA} {a.versi} dari {full}")
    build, catatan = bangun(full, a.versi, a.dengan_pdf)
    for c in catatan:
        print("  ·", c)
    gagal = uji(build, full)
    if gagal:
        print(f"\nGAGAL — {len(gagal)} pemeriksaan; paket TIDAK dibungkus.")
        return 1
    if a.hanya_uji:
        print("\nLULUS — tidak dibungkus (--hanya-uji).")
        return 0
    tujuan = bungkus(build, a.versi)
    print(f"\nLULUS — {tujuan} ({tujuan.stat().st_size / 1e6:.1f} MB); sidik di {tujuan.with_suffix('.sha256').name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
