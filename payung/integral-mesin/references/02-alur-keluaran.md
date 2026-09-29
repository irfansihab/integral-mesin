# Alur keluaran — folder, urutan, dan isi tiap dokumen

## Folder penugasan

Auditor hanya menyiapkan `00-input/`. Sisanya dibuat skill dan `mesin.py`:

```
<penugasan>/
├── 00-input/                 ← DISIAPKAN AUDITOR: semua dokumen (subfolder boleh)
├── _SESSION-MANIFEST.json    mesin.py mulai — SHA-256 tiap berkas 00-input
├── context.md                skill — identitas, Tujuan, Ruang Lingkup, Tim
├── _PERENCANAAN/             skill: DPP.md, Laporan-PIA.md → mesin.py perencanaan: .docx
├── _PKP/sasaran-assignment.json   skill — sasaran dari DPP
├── _KKP/temuan.json          skill — SUMBER KEBENARAN; mesin.py kkp: KKP-<nama>.docx
├── _KKP/penilaian-aspek.json skill — penutupan butir checklist (opsional tetapi dianjurkan)
├── _LHP/                     skill: rekomendasi.json | saran.json | penilaian-rb.json |
│                             kegiatan-pendampingan.json → mesin.py lhp: LHA/LHR/LHE/LP/LHP-*.docx
├── _QA-SAIPI/                mesin.py — hasil QC SAIPI tahap kkp & lhp
├── _AUDIT-TRAIL/             mesin.py — jejak QC
└── Paket-Analisis.md         mesin.py paket + skill mengisi bagian penilaian
```

Dokumen wajib per skill tercantum di SKILL.md masing-masing. Yang wajib tetapi tak ada →
keterbatasan, bukan deviasi.

## 1 · DPP

Template `wiki/templates/dpp/dpp-default.md` (lihat `field_required`). Field yang tak bisa diisi
dari bahan → `[BELUM DIISI]`, jangan dikarang. Sumber berurutan: entri PKPT (`wiki/pkpt/`) bila
penugasan terencana → Surat Tugas/sasaran di `00-input/` → `wiki/konteks/risiko-penugasan.md` →
pola temuan (hipotesis awal) → `wiki/templates/pkp/pkp-<slug>.md` (langkah pengujian).
Sasaran DPP juga ditulis ke `_PKP/sasaran-assignment.json` (format di rujukan 04).
**Berhenti**: auditor membaca DPP sebelum lanjut — titik koreksi pertama.

## 2 · Laporan PIA

Template `wiki/templates/pia/pia-default.md`, sembilan bagian resmi. §6 menilai empat kriteria
kelayakan (`wiki/konteks/kriteria-kelayakan.md`); bila tak layak → hentikan, katakan alasannya.
Blok surat (nomor, lampiran, hal, tujuan) `[DIISI AUDITOR]`. Lalu `mesin.py perencanaan`.

## 3 · Analisis → `_KKP/temuan.json`

Ikuti gate/alur skill. Baca dokumen inti **seluruhnya**; untuk dokumen pendukung yang besar, catat
bagian yang dibaca. Kutip saat menemukan. Skill ber-objek jamak (RO, paket, program) → isi `ro`.
Evaluasi ber-LKE: isi kolom APIP/PK, jangan menimpa PM; selisih PM vs PK = catatan/AoI (tanpa
Sebab). PK SPIP di aplikasi web: ikuti `skills/evaluasi-spip/references/aplikasi-spip/` — pengaman
di sana (ACC di batas KKE, larangan Hapus dan "Copy ke data APIP") mengalahkan instruksi lain.
Lalu `mesin.py kkp`.

## 4 · LHP awal

Profil laporan ditentukan `format_laporan` di frontmatter skill: **kksa** (kebanyakan),
**memo** (konsultansi-umum), **pendampingan** (konsultasi-pengadaan), **rb-4dim** (RB).
Data profil ditulis dulu (rujukan 04), lalu `mesin.py lhp`. Mesin: kerangka resmi
`templates/_skeleton-lhp/template-lhp-<slug>.docx` → penyesuaian judul/istilah per rumpun
(LHA audit · LHR reviu · LHE evaluasi · LP pemantauan) → bab wajib QC (Tujuan, Ruang Lingkup,
Simpulan) → pernyataan kesesuaian SAIPI 2430 → QC.

Bagian bertanda **`[DIISI — …]`** adalah substansi yang tak bisa diturunkan dari temuan (profil
paket, logika intervensi program, tabel rekap nilai LKE, status per tanggal cut-off, …). Isi dari
dokumen `00-input/` lewat `--isian`; yang tak didukung bukti tetap kosong dan masuk Keterbatasan.
Penanda **`[DIISI AUDITOR]`** (nomor surat, tanggal ND, tanda tangan, penerima) memang untuk auditor.

## 5 · Paket

`mesin.py paket` membangkitkan `Paket-Analisis.md` dari `temuan.json`, rekomendasi, dan manifest.
Skill mengisi Ringkasan, Catatan & klarifikasi, Usulan perluasan, Keterbatasan, penilaian per
butir checklist (bila `penilaian-aspek.json` tak ada), dan jawaban daftar periksa.
