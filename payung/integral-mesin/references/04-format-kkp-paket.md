# Format Paket-Analisis.md

Strukturnya mengikuti Paket Analisis INTEGRAL (`export_paket.py`) agar kelak bisa dibaca
mesin bila INTEGRAL menyediakan jalur impor. Untuk sekarang ia dibaca auditor.

```markdown
DRAF — belum disetujui. Persetujuan dilakukan di INTEGRAL. Dihasilkan integral-mesin <versi>.

# Paket Analisis — <kode/judul penugasan>

- Objek: …            - Skill: <slug>            - ST: <nomor, tanggal> (dari 00-input)
- Sasaran: …          - Tingkat keyakinan: <dari frontmatter skill>
- Dibuat: <tanggal>   - Dokumen dibaca: <n> berkas (rincian di §Dokumen)

## Ringkasan
<3–5 kalimat: apa yang direviu/diaudit, berapa temuan, hal terpenting, keterbatasan utama>

## Temuan (<n>)
### T-001 · <judul>
- Unit/RO/paket: …                        - Kode kondisi: …   Kode penyebab: … (kosong bila tidak terbukti)
- Kondisi: <kronologis, lalu deviasi>
- Kriteria: <pasal + bunyi; sumber: berkas/halaman atau wiki/konteks/regulasi/<berkas>.md>
- Sebab: <RCA> | "Tidak cukup data untuk menyimpulkan penyebab"
- Akibat: …
- Rekomendasi (untuk LHP): …
- Sumber: <berkas>, hal. <n> — "<kutipan>"
- Langkah kerja: <langkah PKP> | "di luar lantai PKP — dari standar skill"; Pola: <id> | —
(ulangi per temuan)

## Penilaian per butir checklist
| Butir | Status | Dasar |
|---|---|---|
| … | SESUAI / TIDAK_SESUAI / TIDAK_CUKUP_DATA | berkas/hal. atau "dokumen X tidak tersedia" |

## Catatan & permintaan klarifikasi
<hal yang belum bisa dipastikan — bukan temuan>

## Usulan perluasan lingkup
<sinyal material di luar sasaran>

## Keterbatasan
<dokumen wajib yang tidak ada; bagian yang tidak dibaca; kriteria belum terverifikasi>

## Dokumen
| Berkas | Halaman dibaca | Keterangan |

## Daftar periksa
<dari references/03-daftar-periksa.md, terisi>
```

Skill dengan profil non-KKSA (konsultansi, pendampingan, RB 4 dimensi, LKE) mengganti bagian
"Temuan" dengan bagian yang sesuai (Pendapat/Saran; Log kegiatan; Tabel 4 dimensi; Rekap
PM vs APIP + AoI) — sisanya tetap.
