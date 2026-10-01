#!/usr/bin/env python3
"""Uji ujung-ke-ujung `mesin.py` pada ISI PAKET plugin — dijalankan bangun.py.

    python3 uji/uji_mesin.py --akar build/integral-mesin

Untuk SETIAP skill jenis pengawasan di paket: susun penugasan contoh (hanya 00-input/
disiapkan "auditor"; sisanya ditulis seperti skill akan menulisnya), lalu jalankan
`mulai → kkp → lhp → paket` dan periksa berkas yang dihasilkan — bukan kode keluar saja.
Lalu lima bukti MERAH: pengaman harus benar-benar menolak.

Satu kegagalan = satu baris vonis; uji tidak berhenti di kegagalan pertama.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

TANPA_SEBAB = {"evaluasi-sakip", "evaluasi-spip", "evaluasi-reformasi-birokrasi", "konsultansi-umum", "konsultasi-pengadaan"}
# Placeholder administratif yang MEMANG diisi auditor (nomor surat, TTD, tautan survei).
ADMIN = re.compile(r"\{\{(NOMOR_[A-Z_]*|TANGGAL_NOTA_DINAS|TTD_[A-Z_]*|NAMA_INSPEKTUR|NIP_INSPEKTUR|LINK_SURVEI|TEMBUSAN_LIST)\}\}")

hasil: list[tuple[str, bool, str]] = []


def cek(nama: str, ok: bool, rinci: str = "") -> None:
    hasil.append((nama, ok, rinci))
    print(f"  {'✓' if ok else '✗'} {nama}" + (f" — {rinci}" if rinci else ""), flush=True)


def mesin(akar: Path, *arg: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(akar / "skills/integral-mesin/scripts/mesin.py"), *arg],
                       capture_output=True, text=True, env={"INTEGRAL_AKAR": str(akar), "PATH": "/usr/bin:/bin",
                                                             "HOME": str(Path.home())})
    return r.returncode, (r.stdout + r.stderr)


def susun(d: Path, jenis: str, *, sebab_hilang: bool = False, sumber_asing: bool = False) -> None:
    (d / "00-input").mkdir(parents=True)
    (d / "00-input" / "Surat-Tugas.md").write_text("Surat Tugas Nomor ST-UJI/2026 tanggal 1 Oktober 2026.\n", encoding="utf-8")
    (d / "00-input" / "Dokumen-Objek.md").write_text("Halaman 1: nilai kontrak Rp100.000.000,00.\nHalaman 3: jadwal.\n", encoding="utf-8")
    (d / "context.md").write_text(f"""# Konteks Penugasan

## Identitas Penugasan

| Kolom | Isi |
|---|---|
| Kode | UJI-{jenis} |
| Objek | Objek Uji {jenis} |
| Skill | {jenis} |
| Nomor ST | ST-UJI/2026 |
| Tanggal ST | 1 Oktober 2026 |
| Tahun Anggaran | 2026 |
| Periode Pelaksanaan | 1–10 Oktober 2026 |

Tujuan: Memberikan keyakinan terbatas atas objek uji sesuai kriteria yang berlaku.

Ruang Lingkup: Dokumen objek uji TA 2026.

## Tim

| Peran | Nama | NIP | Jabfung |
|---|---|---|---|
| Ketua Tim | Auditor Uji | 1990 | Auditor Madya |
| Anggota | Auditor Uji | 1990 | Auditor Pertama |
""", encoding="utf-8")
    (d / "_PKP").mkdir()
    (d / "_PKP" / "sasaran-assignment.json").write_text(json.dumps({"skill": jenis, "sasaran": [
        {"sasaran_id": "S-01", "deskripsi": "Sasaran uji", "assigned_to": ["Auditor Uji"], "status": "DISETUJUI_KT",
         "langkah_kerja": ["Langkah uji 1"]}]}, ensure_ascii=False, indent=2), encoding="utf-8")
    tanpa = jenis in TANPA_SEBAB
    def t(i: int, sebab: str | None) -> dict:
        x = {"id_temuan": f"T-00{i}", "sasaran_id": "S-01", "judul_temuan": f"Temuan uji {i}",
             "anggota_tim": {"nama_lengkap": "Auditor Uji"},
             "kondisi": "Pada 1 Oktober 2026 dokumen objek mencantumkan nilai Rp100.000.000,00 tanpa rincian.",
             "kriteria": "Perpres 16/2018 Pasal 26 ayat (1): \"HPS dihitung secara keahlian dan menggunakan data yang dapat dipertanggungjawabkan.\"",
             "akibat": "Kewajaran nilai tidak dapat diyakini.", "kode_kondisi": "4.402", "kode_penyebab": "",
             "kode_rekomendasi": "4.401", "langkah_kerja_terkait": "Langkah uji 1", "pattern_id": "", "ro": "",
             "origin": "AI", "status": "DRAFT",
             "dokumen_sumber": [{"file": ("penugasan-lain/rahasia.pdf" if sumber_asing and i == 1 else "00-input/Dokumen-Objek.md"),
                                 "halaman": 1, "kutipan": "nilai kontrak Rp100.000.000,00"}]}
        if not sebab_hilang or i != 1:
            x["sebab"] = sebab
        return x
    temuan = [t(1, None if tanpa else "SOP penyusunan HPS belum ditetapkan (bukti: Dokumen-Objek hal. 1)."),
              t(2, None if tanpa else "Tidak cukup data untuk menyimpulkan penyebab")]
    (d / "_KKP").mkdir()
    (d / "_LHP").mkdir()
    (d / "_KKP" / "temuan.json").write_text(json.dumps({
        "schema_version": "v4.0.0", "generated_at": "2026-10-01T09:00:00+07:00",
        "penugasan": {"id": f"UJI-{jenis}", "nomor_st": "ST-UJI/2026", "tanggal_st": "2026-10-01",
                      "obyek": f"Objek Uji {jenis}", "jenis_pengawasan": jenis},
        "temuan": temuan}, ensure_ascii=False, indent=2), encoding="utf-8")
    if not tanpa:
        (d / "_KKP" / "penilaian-aspek.json").write_text(json.dumps({"aspek": [
            {"aspek": "Kewajaran nilai terhadap rincian perhitungan", "kesimpulan": "TIDAK_SESUAI", "dasar": "T-001, T-002; Dokumen-Objek hal. 1"},
            {"aspek": "Kelengkapan jadwal", "kesimpulan": "SESUAI", "dasar": "Dokumen-Objek hal. 3 memuat jadwal"}]},
            ensure_ascii=False), encoding="utf-8")
    (d / "_LHP" / "saran.json").write_text(json.dumps([{"pertanyaan": "Bolehkah paket dipecah?", "telaah": "Pemecahan paket untuk menghindari tender dilarang.", "dasar_hukum": [
        "Perpres 16/2018 Pasal 20 ayat (2) huruf d"], "pendapat": "Tidak boleh untuk menghindari tender.",
        "saran": "Satukan paket."}], ensure_ascii=False), encoding="utf-8")
    (d / "_LHP" / "penilaian-rb.json").write_text(json.dumps({"komponen": [{"nama": "Digitalisasi layanan",
        "ketepatan": "Sesuai", "ketercapaian": "Sesuai", "kualitas": "Tidak Sesuai", "kesesuaian": "Sesuai",
        "catatan": "Bukti uji mutu tak ada"}], "aoi": ["Agar menyusun bukti uji mutu."]}, ensure_ascii=False), encoding="utf-8")
    (d / "_LHP" / "kegiatan-pendampingan.json").write_text(json.dumps([{"tanggal": "2026-10-02", "jenis_kegiatan": "Rapat",
        "deskripsi": "Pembahasan KAK", "hasil": "KAK direvisi", "pihak_didampingi": "PPK"}], ensure_ascii=False), encoding="utf-8")
    (d / "_LHP" / "rekomendasi.json").write_text(json.dumps({"T-001": "Kepala satker agar menetapkan SOP penyusunan HPS.",
                                                             "T-002": "PPK agar melengkapi rincian perhitungan HPS."},
                                                            ensure_ascii=False), encoding="utf-8")


def kolom_aspek_kosong(docx: Path) -> bool | None:
    """True bila tabel 'Kesimpulan Penilaian per Aspek' ada tetapi kolom Aspek/Kesimpulan kosong.
    None bila tabelnya tak ada. Kunci salah TIDAK galat di render_kkp — hanya sel kosong."""
    from docx import Document
    for tb in Document(str(docx)).tables:
        if len(tb.columns) == 4 and "Aspek" in tb.rows[0].cells[1].text:
            return any(not r.cells[1].text.strip() or not r.cells[2].text.strip() for r in tb.rows[1:])
    return None


def sisa_placeholder(docx: Path) -> list[str]:
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8", "replace")
    teks = re.sub(r"<[^>]+>", "", xml)
    return sorted({m for m in re.findall(r"\{\{[A-Z0-9_]+\}\}", teks) if not ADMIN.fullmatch(m)})


GU_ = ("Objek uji berupa kegiatan pada satuan kerja uji Tahun Anggaran 2026 dengan nilai pagu Rp100.000.000,00. "
       "Penugasan dilaksanakan melalui penelaahan dokumen pada 1–10 Oktober 2026.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--akar", required=True)
    akar = Path(ap.parse_args().akar).resolve()
    jenis_semua = sorted(p.parent.name for p in (akar / "skills").glob("*/SKILL.md") if p.parent.name != "integral-mesin")
    kerja = Path(tempfile.mkdtemp(prefix="uji-mesin-"))
    try:
        print(f"── cek lingkungan"); r, o = mesin(akar, "cek"); cek("mesin.py cek", r == 0, o.strip().splitlines()[-1] if r else "")
        print(f"── ujung ke ujung, {len(jenis_semua)} jenis")
        for j in jenis_semua:
            d = kerja / j
            susun(d, j)
            langkah = []
            r1, o1 = mesin(akar, "mulai", str(d)); langkah.append(("mulai", r1, o1))
            r2, o2 = mesin(akar, "kkp", str(d)); langkah.append(("kkp", r2, o2))
            SIMP = "Berdasarkan hasil penugasan, terdapat dua temuan yang perlu ditindaklanjuti sebagaimana diuraikan."
            dasar = ["lhp", str(d), "--judul", f"Uji {j}", "--auditi", "Satker Uji", "--simpulan", SIMP, "--gambaran-umum", GU_]
            r3, o3 = mesin(akar, *dasar)
            # Bagian substansi yang dilaporkan mesin diisi seperti skill mengisinya (JSON --isian), lalu
            # render ulang — membuktikan MEKANISMENYA, bukan isinya.
            penanda = sorted(set(re.findall(r"· (\[DIISI[^\]\n]*)", o3)))
            if penanda:
                isian = {x[:40]: ({"tabel": [["Komponen", "Nilai"], ["Uji", "1"]]} if "Tabel" in x else "Isi uji dari dokumen 00-input hal. 1.") for x in penanda}
                (d / "isian.json").write_text(json.dumps(isian, ensure_ascii=False), encoding="utf-8")
                r3, o3 = mesin(akar, *dasar, "--isian", str(d / "isian.json"))
            langkah.append(("lhp", r3, o3))
            r4, o4 = mesin(akar, "paket", str(d)); langkah.append(("paket", r4, o4))
            kkp = list((d / "_KKP").glob("KKP-*.docx")); lhp = [p for p in (d / "_LHP").glob("*.docx")]
            gagal_l = [f"{n}={r}" for n, r, _ in langkah if r != 0]
            sisa = sisa_placeholder(lhp[0]) if lhp else ["(tak ada LHP)"]
            paket = (d / "Paket-Analisis.md").read_text(encoding="utf-8") if (d / "Paket-Analisis.md").exists() else ""
            qc = [n for n, r, _ in langkah if r == 7]
            isian = sorted({x for _, _, o in langkah for x in re.findall(r"· (\[DIISI[^\]\n]*\])", o)})
            aspek_kosong = [k.name for k in kkp if j not in TANPA_SEBAB and kolom_aspek_kosong(k) is not False]
            ok = not gagal_l and kkp and lhp and not sisa and not aspek_kosong and "T-001" in paket and "DRAF" in paket
            rinci = []
            if gagal_l: rinci.append("keluar " + ", ".join(gagal_l))
            if not kkp: rinci.append("KKP tak ada")
            if aspek_kosong: rinci.append(f"tabel penilaian aspek tak ada/kosong di {aspek_kosong}")
            if sisa: rinci.append(f"placeholder tersisa {sisa[:6]}")
            if qc: rinci.append(f"QC KRITIS di {'/'.join(qc)}")
            if isian: rinci.append(f"{len(isian)} bagian LHP perlu diisi")
            cek(f"{j}", bool(ok), "; ".join(rinci))
            if not ok:
                for n, r, o in langkah:
                    if r != 0:
                        print("\n".join(f"        [{n}] {b}" for b in o.strip().splitlines()[-8:]))
        # ── Penugasan contoh dengan dokumen nyata (uji/contoh): TOR & RAB satu RO, 6 temuan,
        #    penilaian 6 aspek Pasal 61 ayat (2). Membuktikan yang tak terlihat di fixture sintetis:
        #    LHR reviu RKA tak lagi menulis "telah sesuai" untuk aspek yang tak diuji (30 Sep 2026).
        print("── penugasan contoh (uji/contoh)")
        for sumber in sorted((Path(__file__).resolve().parent / "contoh").glob("*/")):
            d = kerja / f"contoh-{sumber.name}"
            shutil.copytree(sumber, d, ignore=shutil.ignore_patterns("_SESSION-MANIFEST.json", "*.docx", "_QA-SAIPI",
                                                                       "_AUDIT-TRAIL", "Paket-Analisis.md", "DPP.md", "Laporan-PIA.md"))
            for sub in ("_QA-SAIPI", "_AUDIT-TRAIL"):
                shutil.rmtree(d / sub, ignore_errors=True)
            GU_C = ("Rincian Output Aplikasi Pemantauan Perlindungan Data Pribadi berada pada Kegiatan 5241, Program 059.GG, "
                    "Direktorat Jenderal Ekosistem Digital, dengan pagu Rp2.450.000.000 dari DIPA TA 2026.")
            urut = [("mulai", ["mulai", str(d)]), ("perencanaan", ["perencanaan", str(d)]), ("kkp", ["kkp", str(d)]),
                    ("lhp", ["lhp", str(d), "--judul", "Reviu RKA-K/L contoh", "--auditi", "Ditjen Ekosistem Digital",
                             "--gambaran-umum", GU_C]), ("paket", ["paket", str(d)])]
            hasil_c = [(n, *mesin(akar, *arg)) for n, arg in urut]
            gagal_c = [f"{n}={r}" for n, r, _ in hasil_c if r != 0]
            lhr = sorted((d / "_LHP").glob("LHR-*.docx"))
            teks = ""
            if lhr:
                from docx import Document
                teks = "\n".join(p.text for p in Document(str(lhr[0])).paragraphs)
            klaim_palsu = [k for k in ("telah sesuai dengan ketentuan", "telah dipatuhi", "telah lengkap", "telah memadai", "telah sesuai arahan")
                           if k in teks]
            ok_c = (not gagal_c and lhr and not klaim_palsu and teks.count("Kesimpulan: Tidak Cukup Data") == 4
                    and teks.count("Kesimpulan: Tidak Sesuai") == 2 and "Susunan tim:\n- " in teks
                    and "LAPORAN HASIL Laporan Hasil" not in teks and "[DIISI — " not in teks)
            rinci_c = []
            if gagal_c: rinci_c.append("keluar " + ", ".join(gagal_c))
            if klaim_palsu: rinci_c.append(f"klaim kepatuhan tanpa dasar: {klaim_palsu}")
            if lhr and "[DIISI — " in teks: rinci_c.append("bagian LHP belum terisi")
            if lhr and ("Kesimpulan: Tidak Cukup Data" not in teks or "Susunan tim:\n- " not in teks):
                rinci_c.append("penilaian aspek / susunan tim tak terbaca di LHR")
            cek(f"{sumber.name}: alur penuh, LHR memuat penilaian 6 aspek, tanpa klaim palsu", bool(ok_c), "; ".join(rinci_c))
            if not ok_c:
                for n, r, o in hasil_c:
                    if r != 0:
                        print("\n".join(f"        [{n}] {b}" for b in o.strip().splitlines()[-8:]))
        print("── bukti MERAH")
        d = kerja / "merah-simpulan"; susun(d, "audit-umum"); mesin(akar, "mulai", str(d))
        r, _ = mesin(akar, "lhp", str(d), "--judul", "x", "--auditi", "y", "--gambaran-umum", GU_)
        cek("kerangka tanpa bab Simpulan & tanpa --simpulan → lhp keluar 4", r == 4, f"keluar {r}")
        d = kerja / "merah-telaah"; susun(d, "konsultansi-umum"); mesin(akar, "mulai", str(d))
        sj = json.loads((d / "_LHP" / "saran.json").read_text(encoding="utf-8")); sj[0].pop("telaah")
        (d / "_LHP" / "saran.json").write_text(json.dumps(sj), encoding="utf-8")
        r, _ = mesin(akar, "lhp", str(d), "--judul", "x", "--auditi", "y", "--simpulan", "s", "--gambaran-umum", GU_)
        cek("memo tanpa telaah → lhp keluar 5", r == 5, f"keluar {r}")
        d = kerja / "merah-ubah"; susun(d, "reviu-pengadaan"); mesin(akar, "mulai", str(d))
        (d / "00-input" / "Dokumen-Objek.md").write_text("isi diganti setelah manifest\n", encoding="utf-8")
        r, _ = mesin(akar, "kkp", str(d)); cek("dokumen 00-input diubah setelah manifest → kkp keluar 2", r == 2, f"keluar {r}")
        d = kerja / "merah-asing"; susun(d, "reviu-pengadaan", sumber_asing=True); mesin(akar, "mulai", str(d))
        r, _ = mesin(akar, "kkp", str(d)); cek("temuan merujuk berkas penugasan lain → kkp keluar 3", r == 3, f"keluar {r}")
        d = kerja / "merah-sebab"; susun(d, "audit-pengadaan", sebab_hilang=True); mesin(akar, "mulai", str(d))
        r, _ = mesin(akar, "kkp", str(d)); cek("kunci `sebab` hilang di jenis KKSA → kkp keluar 5", r == 5, f"keluar {r}")
        d = kerja / "merah-rek"; susun(d, "reviu-rka-kl"); mesin(akar, "mulai", str(d))
        (d / "_LHP" / "rekomendasi.json").write_text('{"T-001": "hanya satu"}', encoding="utf-8")
        r, _ = mesin(akar, "lhp", str(d), "--judul", "x", "--auditi", "y", "--gambaran-umum", "Objek uji berupa kegiatan pada satuan kerja uji Tahun Anggaran 2026 dengan nilai pagu Rp100.000.000,00. Penugasan dilaksanakan melalui penelaahan dokumen pada 1–10 Oktober 2026."); cek("rekomendasi kurang untuk T-002 → lhp keluar 5", r == 5, f"keluar {r}")
        r, _ = mesin(akar, "lhp", str(d), "--judul", "x", "--auditi", "y"); cek("LHP KKSA tanpa gambaran umum → lhp keluar 4", r == 4, f"keluar {r}")
        d = kerja / "merah-skema"; susun(d, "reviu-umum"); mesin(akar, "mulai", str(d))
        t = json.loads((d / "_KKP" / "temuan.json").read_text(encoding="utf-8")); t.pop("schema_version")
        (d / "_KKP" / "temuan.json").write_text(json.dumps(t), encoding="utf-8")
        r, _ = mesin(akar, "kkp", str(d)); cek("temuan.json tanpa schema_version → kkp keluar 5", r == 5, f"keluar {r}")
        d = kerja / "merah-kunci-aspek"; susun(d, "reviu-rka-kl"); mesin(akar, "mulai", str(d))
        (d / "_KKP" / "penilaian-aspek.json").write_text(json.dumps({"aspek": [
            {"butir": "Kelengkapan TOR", "status": "TIDAK_SESUAI", "dasar": "T-001"}]}), encoding="utf-8")
        r, _ = mesin(akar, "kkp", str(d)); cek("penilaian-aspek berkunci butir/status → kkp keluar 5", r == 5, f"keluar {r}")
        d = kerja / "merah-aspek-sesuai"; susun(d, "audit-umum"); mesin(akar, "mulai", str(d))
        (d / "_KKP" / "penilaian-aspek.json").write_text(json.dumps({"aspek": [
            {"aspek": "Semua butir", "kesimpulan": "SESUAI", "dasar": "x"}]}), encoding="utf-8")
        r, _ = mesin(akar, "kkp", str(d)); cek("ada temuan tetapi semua aspek SESUAI → kkp keluar 5", r == 5, f"keluar {r}")
        d = kerja / "merah-tanpa-aspek"; susun(d, "reviu-pengadaan"); mesin(akar, "mulai", str(d))
        (d / "_KKP" / "penilaian-aspek.json").unlink()
        r, _ = mesin(akar, "kkp", str(d)); cek("jenis KKSA tanpa penilaian-aspek.json → kkp keluar 5", r == 5, f"keluar {r}")
        d = kerja / "merah-kosong"; (d / "00-input").mkdir(parents=True)
        r, _ = mesin(akar, "mulai", str(d)); cek("00-input kosong → mulai keluar 4", r == 4, f"keluar {r}")
    finally:
        shutil.rmtree(kerja, ignore_errors=True)
    gagal = [n for n, ok, _ in hasil if not ok]
    print(f"\n{'LULUS' if not gagal else 'GAGAL'} — {len(hasil) - len(gagal)}/{len(hasil)}")
    return 1 if gagal else 0


if __name__ == "__main__":
    raise SystemExit(main())
