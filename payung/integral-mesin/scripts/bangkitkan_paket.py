#!/usr/bin/env python3
"""Bangkitkan `Paket-Analisis.md` dari `_KKP/temuan.json` — bukan ditulis bebas.

KKP, LHP, dan Paket dibangkitkan dari berkas yang sama, sehingga isinya tak bisa
saling berbeda. Bagian yang butuh penilaian (Ringkasan, Catatan & klarifikasi,
Usulan perluasan, Keterbatasan, jawaban Daftar periksa) ditandai `<!-- DIISI SKILL -->`
dan diisi skill payung setelahnya.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


def _ctx(p: Path) -> dict:
    out: dict = {}
    if not p.exists():
        return out
    for b in p.read_text(encoding="utf-8").splitlines():
        if b.startswith("|"):
            sel = [c.strip() for c in b.strip().strip("|").split("|")]
            if len(sel) >= 2 and sel[0] and not set(sel[0]) <= set("-: "):
                out.setdefault(sel[0].lower(), sel[1])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--penugasan", required=True)
    ap.add_argument("--versi", default="integral-mesin")
    ap.add_argument("--daftar-periksa", default=None)
    a = ap.parse_args()
    d = Path(a.penugasan).resolve()
    data = json.loads((d / "_KKP" / "temuan.json").read_text(encoding="utf-8"))
    rek_p = d / "_LHP" / "rekomendasi.json"
    rek = json.loads(rek_p.read_text(encoding="utf-8")) if rek_p.exists() else {}
    man_p = d / "_SESSION-MANIFEST.json"
    man = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {"files": []}
    ctx = _ctx(d / "context.md")
    jenis = data["penugasan"].get("jenis_pengawasan", "")
    temuan = data.get("temuan", [])

    dibaca: dict[str, set] = defaultdict(set)
    for t in temuan:
        for s in t.get("dokumen_sumber", []) or []:
            dibaca[Path(str(s.get("file", ""))).name].add(str(s.get("halaman", "")))

    L = [f"DRAF — belum disetujui. Persetujuan dilakukan di INTEGRAL. Dihasilkan {a.versi}.", "",
         f"# Paket Analisis — {ctx.get('objek') or ctx.get('obyek') or d.name}", "",
         f"- Skill: `{jenis}` · Nomor ST: {ctx.get('nomor st', '[DIISI AUDITOR]')} · Tanggal ST: {ctx.get('tanggal st', '[DIISI AUDITOR]')}",
         f"- Dibangkitkan: {date.today():%d %B %Y} · Temuan: {len(temuan)} · Dokumen di manifest: {len(man.get('files', []))}", "",
         "## Ringkasan", "", "<!-- DIISI SKILL: 3–5 kalimat — apa yang diperiksa, hal terpenting, keterbatasan utama -->", "",
         f"## Temuan ({len(temuan)})", ""]
    for t in temuan:
        tid = t.get("id_temuan", "?")
        L += [f"### {tid} · {t.get('judul_temuan', '')}", "",
              f"- Sasaran: {t.get('sasaran_id', '')}" + (f" · Unit/RO/paket: {t['ro']}" if t.get("ro") else "")
              + f" · Kode kondisi: {t.get('kode_kondisi', '') or '—'} · Kode penyebab: {t.get('kode_penyebab', '') or '—'}",
              f"- **Kondisi:** {t.get('kondisi', '')}", f"- **Kriteria:** {t.get('kriteria', '')}"]
        if "sebab" in t and t.get("sebab") is not None:
            L.append(f"- **Sebab:** {t.get('sebab')}")
        L += [f"- **Akibat:** {t.get('akibat', '')}", f"- **Rekomendasi (untuk LHP):** {rek.get(tid, '[belum ada]')}"]
        for s in t.get("dokumen_sumber", []) or []:
            L.append(f"- Sumber: `{s.get('file', '')}`, hal. {s.get('halaman', '')} — \"{s.get('kutipan', '')}\"")
        L.append(f"- Langkah kerja: {t.get('langkah_kerja_terkait') or '—'} · Pola: {t.get('pattern_id') or '—'} · Asal: {t.get('origin', 'AI')}")
        L.append("")
    pa = d / "_KKP" / "penilaian-aspek.json"
    L += ["## Penilaian per butir checklist", ""]
    if pa.exists():
        L += ["| Butir | Status | Dasar |", "|---|---|---|"]
        try:
            for b in json.loads(pa.read_text(encoding="utf-8")).get("aspek", []):
                L.append(f"| {b.get('butir', b.get('aspek', ''))} | {b.get('status', '')} | {b.get('dasar', '')} |")
        except (json.JSONDecodeError, AttributeError):
            L.append("| _penilaian-aspek.json rusak_ | | |")
    else:
        L.append("<!-- DIISI SKILL: tutup tiap butir checklist skill — SESUAI / TIDAK_SESUAI / TIDAK_CUKUP_DATA + dasar -->")
    L += ["", "## Catatan & permintaan klarifikasi", "", "<!-- DIISI SKILL -->", "",
          "## Usulan perluasan lingkup", "", "<!-- DIISI SKILL -->", "",
          "## Keterbatasan", "", "<!-- DIISI SKILL: dokumen wajib yang tak ada · bagian tak dibaca · kriteria belum terverifikasi -->", "",
          "## Dokumen (dari manifest 00-input)", "", "| Berkas | Dikutip di halaman | SHA-256 (awal) |", "|---|---|---|"]
    for f in man.get("files", []):
        L.append(f"| `{f.get('path', f.get('name'))}` | {', '.join(sorted(dibaca.get(f.get('name'), []))) or '—'} | {f.get('sha256', '')[:12]} |")
    L += ["", "## Daftar periksa", ""]
    if a.daftar_periksa and Path(a.daftar_periksa).exists():
        isi = Path(a.daftar_periksa).read_text(encoding="utf-8")
        L += [b for b in isi.splitlines() if b.startswith(("- [ ]", "## "))]
    L.append("")
    (d / "Paket-Analisis.md").write_text("\n".join(L), encoding="utf-8")
    print(f"✓ Paket-Analisis.md — {len(temuan)} temuan, {len(man.get('files', []))} dokumen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
