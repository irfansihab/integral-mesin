#!/usr/bin/env python3
"""Periksa kontrak `_KKP/temuan.json` INTEGRAL sebelum apa pun dirender.

Kontrak yang sama dengan `append_temuan` di server INTEGRAL (kkp_tools.py), sehingga
berkas ini bisa dibaca perender INTEGRAL (`render_kkp.py`, `render_lhp.py`) apa adanya.

Doktrin yang ditegakkan di sini — di server ia ditegakkan kode, di Cowork hanya di sini:
  · tiap temuan punya dokumen_sumber [{file, halaman, kutipan}] yang lengkap
  · jenis ber-KKSA WAJIB memuat kunci `sebab` berisi teks — "Tidak cukup data untuk
    menyimpulkan penyebab" sah; kosong/null tidak. Bila tak terbukti, kode_penyebab kosong.
  · evaluasi ber-LKE & konsultansi tidak memakai Sebab (diperingatkan bila diisi)
  · sasaran_id harus ada di `_PKP/sasaran-assignment.json`
  · tak ada placeholder `{{…}}` di isi temuan
  · jenis ber-KKSA WAJIB punya `_KKP/penilaian-aspek.json` berkunci persis seperti
    `write_penilaian_aspek` server — {aspek, kesimpulan, dasar}. Kunci lain tak galat di
    perender; kolomnya tercetak KOSONG tanpa pesan (terjadi 29 Sep 2026: butir/status).

Keluar 0 bila sah, 5 bila ada pelanggaran (dicetak semua, bukan berhenti di yang pertama).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TANPA_SEBAB = {"evaluasi-sakip", "evaluasi-spip", "evaluasi-reformasi-birokrasi", "konsultansi-umum", "konsultasi-pengadaan"}
PROFIL_KHUSUS = {"konsultansi-umum", "konsultasi-pengadaan", "evaluasi-reformasi-birokrasi"}
TIDAK_TERBUKTI = re.compile(r"tidak (cukup data|ditemukan penyebab)", re.I)
ASAL = {"AI", "AI_DARI_CATATAN", "MANUAL"}
KESIMPULAN = {"SESUAI", "TIDAK_SESUAI", "TIDAK_CUKUP_DATA"}


def periksa_aspek(d: Path, jenis: str, ada_temuan: bool) -> list[str]:
    """`_KKP/penilaian-aspek.json` — penutupan tiap butir checklist, termasuk yang SESUAI.

    Dibaca render_kkp.py (tabel "Kesimpulan Penilaian per Aspek") dengan kunci
    aspek/kesimpulan/dasar. Evaluasi ber-LKE punya rekap sendiri; konsultansi tak berchecklist.
    """
    f = d / "_KKP" / "penilaian-aspek.json"
    if jenis in TANPA_SEBAB:
        return []
    if not f.exists():
        return ["_KKP/penilaian-aspek.json tidak ada — tutup TIAP butir checklist skill "
                "(SESUAI/TIDAK_SESUAI/TIDAK_CUKUP_DATA + dasar), bukan hanya yang jadi temuan"]
    try:
        aspek = json.loads(f.read_text(encoding="utf-8")).get("aspek")
    except (json.JSONDecodeError, AttributeError) as e:
        return [f"_KKP/penilaian-aspek.json rusak: {e}"]
    if not isinstance(aspek, list) or not aspek:
        return ["penilaian-aspek.json: 'aspek' harus daftar yang tidak kosong"]
    salah = []
    for i, a in enumerate(aspek, 1):
        if not isinstance(a, dict):
            salah.append(f"penilaian-aspek #{i}: harus objek {{aspek, kesimpulan, dasar}}")
            continue
        asing = sorted(set(a) - {"aspek", "kesimpulan", "dasar"})
        if asing:
            salah.append(f"penilaian-aspek #{i}: kunci {asing} tak dibaca perender — pakai aspek/kesimpulan/dasar")
        if not str(a.get("aspek") or "").strip():
            salah.append(f"penilaian-aspek #{i}: 'aspek' kosong")
        if a.get("kesimpulan") not in KESIMPULAN:
            salah.append(f"penilaian-aspek #{i}: kesimpulan {a.get('kesimpulan')!r} bukan {sorted(KESIMPULAN)}")
        if not str(a.get("dasar") or "").strip():
            salah.append(f"penilaian-aspek #{i}: 'dasar' kosong — satu kalimat bukti dari dokumen")
    if ada_temuan and not any(isinstance(a, dict) and a.get("kesimpulan") == "TIDAK_SESUAI" for a in aspek):
        salah.append("ada temuan, tetapi tak satu pun butir penilaian-aspek TIDAK_SESUAI — keduanya bertentangan")
    return salah


def periksa(d: Path, jenis_sah: set[str] | None = None) -> tuple[list[str], list[str]]:
    salah: list[str] = []
    catatan: list[str] = []
    f = d / "_KKP" / "temuan.json"
    if not f.exists():
        return [f"{f.relative_to(d)} tidak ada"], catatan
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"temuan.json bukan JSON sah: {e}"], catatan
    if not isinstance(data, dict) or not isinstance(data.get("temuan"), list):
        return ["temuan.json harus {\"penugasan\": {...}, \"temuan\": [...]}"], catatan
    if data.get("schema_version") != "v4.0.0":
        salah.append(f"schema_version={data.get('schema_version')!r}, harus 'v4.0.0' (QC SAIPI LAK-006)")
    if not str(data.get("generated_at") or "").strip():
        salah.append("generated_at kosong (tanggal-waktu ISO penyusunan)")
    for k in ("id", "nomor_st", "tanggal_st", "obyek", "jenis_pengawasan"):
        if not str((data.get("penugasan") or {}).get(k) or "").strip():
            salah.append(f"penugasan.{k} kosong (skema kkp-temuan)")
    jenis = (data.get("penugasan") or {}).get("jenis_pengawasan", "")
    if not jenis:
        salah.append("penugasan.jenis_pengawasan kosong")
    elif jenis_sah and jenis not in jenis_sah:
        salah.append(f"jenis_pengawasan '{jenis}' bukan slug skill yang ada")
    sasaran_ids: set[str] | None = None
    sa = d / "_PKP" / "sasaran-assignment.json"
    if sa.exists():
        try:
            sasaran_ids = {s.get("sasaran_id") for s in json.loads(sa.read_text(encoding="utf-8")).get("sasaran", [])}
        except (json.JSONDecodeError, AttributeError) as e:
            salah.append(f"_PKP/sasaran-assignment.json rusak: {e}")
    else:
        salah.append("_PKP/sasaran-assignment.json tidak ada (sasaran dari DPP wajib ditulis)")
    if not data["temuan"]:
        catatan.append("tidak ada temuan — sah bila memang tak ada deviasi; pastikan tiap butir checklist ditutup di Paket")
    dilihat: set[str] = set()
    for i, t in enumerate(data["temuan"], 1):
        tid = t.get("id_temuan") or f"#{i}"
        if not re.fullmatch(r"T-\d{3}", str(t.get("id_temuan", ""))):
            salah.append(f"{tid}: id_temuan harus berbentuk T-001")
        if tid in dilihat:
            salah.append(f"{tid}: id_temuan ganda")
        dilihat.add(tid)
        wajib = ["judul_temuan", "sasaran_id"] + ([] if jenis in PROFIL_KHUSUS else ["kondisi", "kriteria", "akibat"])
        for k in wajib:
            if not str(t.get(k) or "").strip():
                salah.append(f"{tid}: '{k}' kosong")
        if not str((t.get("anggota_tim") or {}).get("nama_lengkap", "")).strip():
            salah.append(f"{tid}: anggota_tim.nama_lengkap kosong (perender KKP memilah per anggota)")
        if sasaran_ids is not None and t.get("sasaran_id") and t["sasaran_id"] not in sasaran_ids:
            salah.append(f"{tid}: sasaran_id '{t['sasaran_id']}' tak ada di sasaran-assignment.json")
        sebab = t.get("sebab")
        if jenis and jenis not in TANPA_SEBAB:
            if "sebab" not in t or not str(sebab or "").strip():
                salah.append(f"{tid}: unsur Sebab wajib DITULIS — bila tak terbukti tulis \"Tidak cukup data untuk menyimpulkan penyebab\"")
            elif TIDAK_TERBUKTI.search(str(sebab)) and str(t.get("kode_penyebab") or "").strip():
                salah.append(f"{tid}: Sebab tak terbukti tetapi kode_penyebab diisi — kosongkan")
        elif str(sebab or "").strip() and not TIDAK_TERBUKTI.search(str(sebab)):
            catatan.append(f"{tid}: jenis '{jenis}' tidak memakai unsur Sebab — isinya diabaikan perender")
        ds = t.get("dokumen_sumber")
        if not isinstance(ds, list) or not ds:
            salah.append(f"{tid}: dokumen_sumber kosong — tiap temuan wajib menunjuk berkas di 00-input/")
        else:
            for j, s in enumerate(ds, 1):
                for k in ("file", "halaman", "kutipan"):
                    if not str((s or {}).get(k, "")).strip():
                        salah.append(f"{tid}: dokumen_sumber[{j}].{k} kosong")
        if not str(t.get("kode_kondisi") or "").strip():
            salah.append(f"{tid}: kode_kondisi kosong (kodefikasi-temuan.md)")
        if t.get("origin") and t["origin"] not in ASAL:
            salah.append(f"{tid}: origin '{t['origin']}' bukan {sorted(ASAL)}")
        for k, v in t.items():
            if isinstance(v, str) and "{{" in v:
                salah.append(f"{tid}: '{k}' memuat placeholder {{{{…}}}}")
    salah += periksa_aspek(d, jenis, bool(data["temuan"]))
    return salah, catatan


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--penugasan", required=True)
    ap.add_argument("--jenis-sah", default="")
    a = ap.parse_args()
    d = Path(a.penugasan).resolve()
    salah, catatan = periksa(d, set(filter(None, a.jenis_sah.split(","))) or None)
    for c in catatan:
        print(f"  · {c}")
    if salah:
        print(f"✗ kontrak berkas _KKP dilanggar (temuan.json · penilaian-aspek.json) — {len(salah)} hal:")
        for s in salah:
            print(f"  ✗ {s}")
        return 5
    n = len(json.loads((d / "_KKP" / "temuan.json").read_text(encoding="utf-8"))["temuan"])
    print(f"✓ temuan.json sah — {n} temuan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
