# Alur keluaran — folder, urutan, dan cara mengisi tiap dokumen

## Tata letak folder penugasan

```
<kode-penugasan>/
├── 00-input/            Surat Tugas, sasaran/lingkup (bisa dalam ST), entri PKPT, DPP/PIA
│                        lama bila penugasan lanjutan
├── 01-objek/            dokumen yang diperiksa (TOR/RAB, KAK/HPS/kontrak, LK, LKE, …)
├── 02-kriteria/         regulasi/SOP/juklak tambahan yang diunggah auditor (opsional)
├── 03-bukti-lapangan/   hasil pemeriksaan fisik, observasi, notulen diskusi ahli (opsional —
│                        BILA ADA WAJIB DIANALISIS, lihat PANDUAN.md)
└── 90-keluaran/         semua yang dihasilkan skill ini
    ├── 01-DPP.md / .docx
    ├── 02-Laporan-PIA.md / .docx
    ├── 03-KKP.md / .docx (+ .xlsx untuk reviu-rka-kl / LKE terisi untuk evaluasi ber-LKE)
    ├── 04-LHP-awal.docx
    └── Paket-Analisis.md
```

Dokumen wajib per skill ada di bagian "Kontrak dokumen" `docs/ROADMAP-v10.md` INTEGRAL dan
di masing-masing SKILL.md. Yang wajib tetapi tidak ada → keterbatasan, bukan deviasi.

## 1 · DPP — Desain Penugasan Pengawasan

Template: `wiki/templates/dpp/dpp-default.md` (frontmatter memuat `field_required`). Isi
tiap field; yang tak bisa diisi dari bahan yang ada ditulis `[BELUM DIISI]` — jangan dikarang.
Sumber substansi, berurutan:
- entri PKPT di `wiki/pkpt/` bila penugasan terencana (asal substansi = PKPT; catat tanggal
  entri dan usianya);
- Surat Tugas/sasaran di `00-input/`;
- `wiki/konteks/risiko-penugasan.md` → kolom risiko penugasan;
- `wiki/temuan-patterns/<slug>/` → kolom risiko & hipotesis awal (sebagai hipotesis, bukan
  temuan);
- `wiki/templates/pkp/pkp-<slug>.md` → kolom langkah pengujian.
Tulis `01-DPP.md`, render ke `.docx` (pakai skill docx bila ada; struktur heading & tabel
harus utuh). **Berhenti**: minta auditor membaca DPP sebelum lanjut.

## 2 · Laporan PIA — Pengembangan Informasi Awal

Template: `wiki/templates/pia/pia-default.md` — sembilan bagian resmi: 1 Dasar Penugasan ·
2 Sasaran, Ruang Lingkup, Batasan Tanggung Jawab · 3 Tujuan PIA (kontekstualisasi isu, uji
eksistensi, mitigasi risiko penugasan) · 4 Metodologi · 5 Hasil (profil objek; proses bisnis,
kebijakan, risiko inheren; isu kritis & area berisiko tinggi) · 6 Penilaian empat kriteria
kelayakan (`wiki/konteks/kriteria-kelayakan.md`) · 7–9 simpulan, rekomendasi lanjut/tidak,
penutup. Blok surat (nomor, lampiran, hal, tujuan) dibiarkan `[DIISI AUDITOR]`.
Gerbang: bila §6 menyimpulkan tidak layak → hentikan di sini dan katakan alasannya.

## 3 · Analisis

Ikuti gate/alur SKILL.md skill terpilih. Baca dokumen objek **seluruhnya** untuk yang menjadi
inti (TOR/RAB, KAK/HPS/kontrak, LK); untuk dokumen pendukung yang besar, baca bagian yang
relevan dan catat bagian mana. Kutip saat menemukan, jangan menunda — setiap kondisi butuh
berkas + halaman + kutipan.

Skill ber-objek jamak (RKA-K/L per RO; pengadaan per paket; audit per program/unit):
analisis **per unit**, temuan menyebut unitnya (`ro`/paket).

Evaluasi ber-LKE (SAKIP/SPIP/RB): APIP menilai *self-assessment* auditee — isi kolom
APIP/penjaminan kualitas per unsur dari bukti dukung, jangan menimpa kolom PM; bandingkan
PM vs APIP; selisih menjadi catatan/AoI. LKE SPIP besar → kerjakan per komponen dan katakan
komponen mana yang belum.

## 4 · KKP

`03-KKP.md` (+ `.docx`): identitas penugasan (kode, objek, skill, ST, tim) · ringkasan objek
3–5 kalimat dari dokumen · tabel per butir checklist (butir | status | dasar) · tabel temuan
`No | Judul | Kondisi | Kriteria | Sebab | Akibat | Kode kondisi | Kode penyebab | Sumber
(berkas, hal.) | Langkah kerja | Pola`. Rekomendasi **tidak** di KKP.
`reviu-rka-kl`: isi juga `templates/KKR-Reviu-RKA-KL-template.xlsx` per RO.

## 5 · LHP awal

Kerangka: `templates/_skeleton-lhp/template-lhp-<slug>.docx`; bila tak ada,
`template-lhp-generic.docx`; `templates/Laporan Hasil *.docx` adalah contoh format resmi
per jenis untuk menyamakan struktur bab. Profil laporan mengikuti skill:
- **KKSA** (kebanyakan skill): Nota Dinas `[DIISI AUDITOR]` → cover → pendahuluan (dasar,
  tujuan, ruang lingkup, metodologi, gambaran umum objek 3–5 kalimat substantif) → hasil per
  sasaran/aspek (kondisi kronologis, kriteria, sebab, akibat, rekomendasi) → simpulan dengan
  bahasa keyakinan sesuai jenis → lampiran.
- **Memo** (`konsultansi-umum`): pertanyaan → dasar hukum → pendapat/saran; tanpa temuan.
- **Laporan Pendampingan** (`konsultasi-pengadaan`): log kegiatan yang diselesaikan.
- **RB 4 dimensi** (`evaluasi-reformasi-birokrasi`): tabel komponen × dimensi.
- **LKE** (`evaluasi-sakip`, `evaluasi-spip`): rekap skor/predikat PM vs APIP + AoI.
Nomor surat, tanggal, tanda tangan, Nota Dinas: `[DIISI AUDITOR]`.

## 6 · Paket-Analisis.md

Format di `references/04-format-kkp-paket.md`. Ini yang dibaca auditor pertama kali.
