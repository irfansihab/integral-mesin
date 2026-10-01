#!/usr/bin/env python3
"""mesin.py — pengendali tunggal INTEGRAL Mesin di Cowork.

Skill payung memanggil SATU skrip ini, bukan merangkai belasan skrip sendiri.
Semua perintah bekerja pada satu folder penugasan yang disiapkan auditor:

    <penugasan>/00-input/   ← satu-satunya yang disiapkan auditor (semua dokumen)

Sisanya dibuat di sini: _SESSION-MANIFEST.json, context.md (ditulis skill),
_PERENCANAAN/, _PKP/, _KKP/, _LHP/, _QA-SAIPI/, _AUDIT-TRAIL/, Paket-Analisis.md.

    python3 mesin.py cek
    python3 mesin.py mulai          <penugasan>
    python3 mesin.py ulang-manifest <penugasan>      # setelah auditor menambah dokumen
    python3 mesin.py perencanaan    <penugasan>      # _PERENCANAAN/dpp.json, pia.json → .md → .docx
    python3 mesin.py perencanaan    --field dpp|pia  # daftar field template
    python3 mesin.py periksa        <penugasan>      # kontrak _KKP/temuan.json
    python3 mesin.py kkp            <penugasan>      # periksa → isolasi → KKP → QC
    python3 mesin.py lhp            <penugasan> --judul "…" --auditi "…" [--gambaran-umum "…"]
    python3 mesin.py paket          <penugasan>

Kode keluar (sama untuk semua perintah):
    0 beres · 2 dokumen 00-input berubah sejak manifest · 3 temuan merujuk berkas di luar manifest
    4 prasyarat folder/berkas tak ada · 5 temuan.json melanggar kontrak · 6 pustaka Python tak ada
    7 QC SAIPI menemukan KRITIS (keluaran tetap ditulis; baca laporannya) · 1 galat lain
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SKRIP = Path(__file__).resolve().parent


def akar() -> Path:
    """Akar plugin: scripts/ → integral-mesin/ → skills/ → AKAR."""
    env = os.environ.get("INTEGRAL_AKAR")
    return Path(env) if env else SKRIP.parents[2]


def _env() -> dict:
    e = dict(os.environ)
    e["PYTHONIOENCODING"] = "utf-8"
    e["INTEGRAL_CHECKLIST_SAIPI"] = str(akar() / "meta" / "kepatuhan-saipi" / "references" / "checklist-saipi-per-penugasan.json")
    return e


def _jalan(nama: str, *arg: str) -> int:
    r = subprocess.run([sys.executable, str(SKRIP / nama), *arg], env=_env(), capture_output=True, text=True)
    keluar = (r.stdout + r.stderr).strip()
    if keluar:
        print("\n".join("   " + b for b in keluar.splitlines()))
    return r.returncode


def _versi() -> str:
    v = akar() / "VERSI.txt"
    return v.read_text(encoding="utf-8").splitlines()[0] if v.exists() else "integral-mesin (versi tak diketahui)"


def _penugasan(p: str) -> Path:
    d = Path(p).expanduser().resolve()
    if not d.is_dir():
        print(f"✗ folder penugasan tidak ada: {d}")
        raise SystemExit(4)
    return d


def cmd_cek(_a) -> int:
    print(f"── {_versi()} · Python {sys.version.split()[0]} · akar {akar()}")
    kurang = []
    for modul, pip in (("docx", "python-docx"), ("openpyxl", "openpyxl")):
        try:
            __import__(modul)
            print(f"  ✓ {pip}")
        except ImportError:
            kurang.append(pip)
            print(f"  ✗ {pip} tidak ada")
    a = akar()
    kerangka = list((a / "templates" / "_skeleton-lhp").glob("template-lhp-*.docx"))
    reg = list((a / "wiki" / "konteks" / "regulasi").glob("*.md"))
    print(f"  {'✓' if kerangka else '✗'} {len(kerangka)} kerangka LHP · {'✓' if reg else '✗'} {len(reg)} teks regulasi terverifikasi")
    if kurang:
        print(f"\nPasang dulu: pip install {' '.join(kurang)}  — bila tak bisa, keluaran .docx lewat skill docx (format tak dijamin).")
        return 6
    return 0 if kerangka and reg else 4


def _siapkan(d: Path) -> None:
    for sub in ("_PERENCANAAN", "_PKP", "_KKP", "_LHP", "_QA-SAIPI"):
        (d / sub).mkdir(exist_ok=True)


def cmd_mulai(a) -> int:
    d = _penugasan(a.penugasan)
    masukan = d / "00-input"
    if not masukan.is_dir() or not any(p.is_file() for p in masukan.rglob("*")):
        print(f"✗ {masukan} tidak ada atau kosong. Auditor menaruh SEMUA dokumen penugasan di sana (tanpa subfolder wajib).")
        return 4
    _siapkan(d)
    if (d / "_SESSION-MANIFEST.json").exists():
        print("── manifest sudah ada; memeriksa apakah 00-input berubah")
        r = _jalan("check_isolation.py", "--penugasan", str(d), "--strict")
        if r == 2:
            print("✗ 00-input berubah sejak manifest. Bila perubahan itu disengaja (dokumen ditambah auditor): `mesin.py ulang-manifest`.")
        return r
    return _jalan("generate_session_manifest.py", "--penugasan", str(d))


def cmd_ulang_manifest(a) -> int:
    d = _penugasan(a.penugasan)
    _siapkan(d)
    return _jalan("generate_session_manifest.py", "--penugasan", str(d), "--force")


_PERENCANAAN = (("dpp", "DPP.md"), ("pia", "Laporan-PIA.md"))


def cmd_perencanaan(a) -> int:
    """`<jenis>.json` → `<Nama>.md` lewat template wiki → `.docx`.

    Perendernya SAMA dengan server (export_perencanaan.render_template), jadi
    tabel {{#each}}, blok kondisional, dan `[BELUM DIISI]` berperilaku identik.
    Skill cukup menulis datanya; tata letak dokumen bukan urusan skill.
    """
    os.environ["INTEGRAL_AKAR"] = str(akar())
    sys.path.insert(0, str(SKRIP))
    import export_perencanaan as ep
    if a.field:
        f = ep.template_fields(a.field, a.skill)
        tpl = ep.resolve_template(a.field, a.skill)
        print(f"── template {tpl.relative_to(akar()) if tpl else '(tak ada)'}")
        print("  wajib   : " + ", ".join(f["field_required"]))
        print("  opsional: " + ", ".join(f["field_optional"]))
        return 0 if tpl else 4
    if not a.penugasan:
        print("✗ sebutkan folder penugasan, atau --field dpp|pia untuk melihat daftar field")
        return 4
    d = _penugasan(a.penugasan)
    try:
        from perencanaan_docx import markdown_ke_docx
    except ImportError as e:
        print(f"✗ {e}")
        return 6
    ada = 0
    for jenis, nama in _PERENCANAAN:
        data = d / "_PERENCANAAN" / f"{jenis}.json"
        md = d / "_PERENCANAAN" / nama
        if data.exists():
            try:
                fields = json.loads(data.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                print(f"✗ {data.relative_to(d)} bukan JSON sah: {e}")
                return 5
            tpl = ep.resolve_template(jenis, a.skill or fields.get("skill"))
            if tpl is None:
                print(f"✗ template {jenis} tak ada di paket")
                return 4
            md.write_text(ep.render_template(tpl.read_text(encoding="utf-8-sig"), fields), encoding="utf-8")
            kosong = [k for k in ep.template_fields(jenis, a.skill or fields.get("skill"))["field_required"]
                      if not fields.get(k)]
            print(f"  ✓ {md.relative_to(d)} dari {data.name} · template {tpl.name}")
            if kosong:
                print(f"    [BELUM DIISI] pada field wajib: {', '.join(kosong)}")
        if md.exists():
            out = markdown_ke_docx(md.read_text(encoding="utf-8"), md.with_suffix(".docx"))
            print(f"  ✓ {out.relative_to(d)}")
            ada += 1
        else:
            print(f"  – {jenis}.json / {nama} belum ada")
    return 0 if ada else 4


def cmd_periksa(a) -> int:
    d = _penugasan(a.penugasan)
    jenis = ",".join(sorted(p.parent.name for p in (akar() / "skills").glob("*/SKILL.md")))
    return _jalan("periksa_temuan.py", "--penugasan", str(d), "--jenis-sah", jenis)


def _isolasi(d: Path) -> int:
    print("── isolasi sumber")
    return _jalan("check_isolation.py", "--penugasan", str(d), "--strict")


def _qc(d: Path, tahap: str) -> int:
    print(f"── QC SAIPI tahap {tahap}")
    r = _jalan("qc_saipi.py", "--penugasan", str(d), "--stage", tahap)
    return 7 if r == 2 else r


def cmd_kkp(a) -> int:
    d = _penugasan(a.penugasan)
    print("── kontrak temuan.json")
    for langkah in (lambda: cmd_periksa(a), lambda: _isolasi(d)):
        r = langkah()
        if r:
            return r
    print("── render KKP")
    r = _jalan("render_kkp.py", "--penugasan", str(d), "--all-anggota")
    return r or _qc(d, "kkp")


def cmd_lhp(a) -> int:
    d = _penugasan(a.penugasan)
    r = cmd_periksa(a) or _isolasi(d)
    if r:
        return r
    sys.path.insert(0, str(SKRIP))
    import lapisan_lhp as lap
    temuan = json.loads((d / "_KKP" / "temuan.json").read_text(encoding="utf-8"))
    jenis = temuan["penugasan"]["jenis_pengawasan"]
    prof = lap.profil(akar() / "skills", jenis)
    gu = (a.gambaran_umum or "").strip()
    if prof == "kksa" and (len(gu) < 80 or gu.upper().startswith("[DIISI")):
        print("✗ --gambaran-umum wajib untuk LHP KKSA: 3–5 kalimat substantif (objek, nilai anggaran/HPS, "
              "mekanisme/periode) dari dokumen 00-input — seperti server INTEGRAL, LHP tak dirender tanpa itu")
        return 4
    dasar = a.dasar_permintaan or _ctx_isi(d, "dasar penugasan") or _ctx_isi(d, "nomor st")
    arg = {"judul": a.judul, "auditi": a.auditi, "dasar_permintaan": dasar, "gambaran_umum": gu,
           "tanggal_exit_meeting": a.tanggal_exit_meeting or "", "kesimpulan": None, "simpulan": a.simpulan}
    print(f"── render LHP · profil {prof}")
    if prof == "kksa":
        rek_path = d / "_LHP" / "rekomendasi.json"
        ids = {t["id_temuan"] for t in temuan.get("temuan", [])}
        rek = json.loads(rek_path.read_text(encoding="utf-8")) if rek_path.exists() else None
        if rek is None:
            print(f"✗ {rek_path.relative_to(d)} belum ada — tulis {{\"T-001\": \"…\"}} untuk tiap temuan")
            return 4
        kosong = sorted(i for i in ids if not str(rek.get(i, "")).strip())
        if kosong:
            print(f"✗ rekomendasi belum ada untuk: {', '.join(kosong)}")
            return 5
        kerangka = akar() / "templates" / "_skeleton-lhp" / f"template-lhp-{jenis}.docx"
        if not kerangka.exists():
            kerangka = akar() / "templates" / "_skeleton-lhp" / "template-lhp-generic.docx"
        r = _jalan("render_lhp.py", "--penugasan", str(d), "--template", str(kerangka), "--rekomendasi-file", str(rek_path),
                   "--judul", a.judul, "--auditi", a.auditi, "--dasar-permintaan", dasar or "",
                   "--gambaran-umum", gu, "--tanggal-exit-meeting", arg["tanggal_exit_meeting"])
        if r:
            return r
        try:
            out = lap.finalisasi_kksa(d, jenis, a.simpulan)
        except lap.BabKurang as e:
            print(f"✗ {e}")
            return 4
    else:
        berkas = {"memo": "saran.json", "rb-4dim": "penilaian-rb.json", "pendampingan": "kegiatan-pendampingan.json"}[prof]
        if not (d / "_LHP" / berkas).exists():
            print(f"✗ _LHP/{berkas} belum ada — profil {prof} tidak memakai temuan KKSA untuk laporannya")
            return 4
        try:
            out = {"memo": lap.render_memo, "rb-4dim": lap.render_rb, "pendampingan": lap.render_pendampingan}[prof](d, arg, akar() / "templates")
        except (ValueError, json.JSONDecodeError) as e:
            print(f"✗ {e}")
            return 5
    print(f"   ✓ {out.relative_to(d) if out else '(tak ada berkas)'}")
    if out and a.isian:
        isian = json.loads(Path(a.isian).read_text(encoding="utf-8"))
        terisi, tak_ketemu = lap.isi_bagian(out, isian)
        print(f"   ✓ {len(terisi)} bagian diisi dari {Path(a.isian).name}" + (f"; kunci tak cocok: {tak_ketemu}" if tak_ketemu else ""))
    sisa = lap.sisa_isian(out) if out else []
    if sisa:
        print(f"   ⚠ {len(sisa)} bagian LHP masih perlu diisi — tulis isinya ke JSON {{\"<awal penanda>\": \"teks\" | {{\"tabel\": [[…]]}}}} lalu jalankan ulang dengan --isian:")
        for x in sisa:
            print(f"      · {x}")
    return _qc(d, "lhp")


def _ctx_isi(d: Path, kunci: str) -> str:
    p = d / "context.md"
    if not p.exists():
        return ""
    for b in p.read_text(encoding="utf-8").splitlines():
        if b.startswith("|"):
            sel = [c.strip() for c in b.strip().strip("|").split("|")]
            if len(sel) >= 2 and sel[0].lower() == kunci:
                return sel[1]
    return ""


def cmd_paket(a) -> int:
    d = _penugasan(a.penugasan)
    return _jalan("bangkitkan_paket.py", "--penugasan", str(d), "--versi", _versi(),
                  "--daftar-periksa", str(akar() / "skills" / "integral-mesin" / "references" / "03-daftar-periksa.md"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="perintah", required=True)
    sub.add_parser("cek").set_defaults(f=cmd_cek)
    p = sub.add_parser("perencanaan")
    p.add_argument("penugasan", nargs="?")
    p.add_argument("--field", choices=("dpp", "pia"), help="tampilkan daftar field template, lalu berhenti")
    p.add_argument("--skill", help="template spesifik <jenis>-<skill>.md bila ada (bawaan: -default)")
    p.set_defaults(f=cmd_perencanaan)
    for nama, f in (("mulai", cmd_mulai), ("ulang-manifest", cmd_ulang_manifest),
                    ("periksa", cmd_periksa), ("kkp", cmd_kkp), ("paket", cmd_paket)):
        p = sub.add_parser(nama)
        p.add_argument("penugasan")
        p.set_defaults(f=f)
    p = sub.add_parser("lhp")
    p.add_argument("penugasan")
    p.add_argument("--judul", required=True)
    p.add_argument("--auditi", required=True)
    p.add_argument("--gambaran-umum", default=None, help="WAJIB untuk profil KKSA — 3–5 kalimat substantif")
    p.add_argument("--dasar-permintaan", default=None, help="bawaan: 'Dasar Penugasan' atau 'Nomor ST' di context.md")
    p.add_argument("--tanggal-exit-meeting", default=None)
    p.add_argument("--simpulan", default=None, help="WAJIB bila kerangka tak memuat bab Simpulan")
    p.add_argument("--isian", default=None, help="JSON isi bagian '[DIISI — …]': {\"<awal penanda>\": \"teks\" | {\"tabel\": [[…]]}}")
    p.set_defaults(f=cmd_lhp)
    a = ap.parse_args()
    try:
        return a.f(a)
    except SystemExit as e:
        return int(e.code or 0)
    except ModuleNotFoundError as e:  # pustaka dimuat malas di dalam skrip salinan FULL
        print(f"✗ pustaka Python tak ada: {e.name} — jalankan `mesin.py cek`")
        return 6
    except Exception as e:  # noqa: BLE001 — laporkan, jangan jejak galat panjang
        print(f"✗ galat: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
