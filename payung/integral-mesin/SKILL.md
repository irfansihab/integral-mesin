---
name: integral-mesin
description: >
  Gunakan skill ini setiap kali auditor Inspektorat II Komdigi meminta mengerjakan penugasan
  pengawasan dari sebuah folder — "kerjakan penugasan ini", "susun DPP", "buat Laporan PIA",
  "susun KKP", "buat LHP awal", "analisis dokumen penugasan ini", atau saat folder berisi
  Surat Tugas/sasaran pengawasan. Skill ini adalah orkestrator: memilih skill jenis pengawasan
  INTEGRAL yang tepat, menegakkan doktrin anti-mengarang & kutipan sumber, dan menghasilkan
  draf DPP, Laporan PIA, KKP, dan LHP awal yang siap diunggah ke INTEGRAL untuk disetujui.
metadata:
  version: "0.1.0"
  author: "Inspektorat II — Itjen Komdigi"
---

# INTEGRAL Mesin — orkestrator penugasan pengawasan

Skill ini menggantikan orkestrator server INTEGRAL. Skill jenis pengawasan di plugin ini
(`reviu-rka-kl`, `audit-pengadaan`, `evaluasi-sakip`, …) sengaja berisi **substansi saja**
— apa yang dinilai dan format keluarannya. Urutan kerja, gerbang, dan doktrin ada **di sini**.
Semua keluaran adalah **DRAF**; persetujuan dilakukan auditor di INTEGRAL, bukan di Cowork.

Jalur di bawah relatif terhadap **akar plugin** (dua tingkat di atas folder skill ini):
`skills/`, `wiki/`, `templates/`, `meta/`.

## 0 · Sebelum apa pun: kenali penugasan

1. Baca seluruh isi `00-input/` (Surat Tugas, sasaran/lingkup, entri PKPT bila ada) dan daftar
   nama berkas di `01-objek/`, `02-kriteria/`, `03-bukti-lapangan/`. Bila tata letak folder
   tidak seperti itu, kerjakan dengan apa yang ada dan sebutkan penataan yang disarankan
   (lihat `references/02-alur-keluaran.md`).
2. Tentukan **jenis pengawasan** dari Surat Tugas/sasaran, lalu **muat SKILL.md** skill yang
   sesuai di `skills/<slug>/` dan ikuti gate/alur di dalamnya. Peta pilihan:
   reviu TOR/RAB → `reviu-rka-kl` · reviu RUP/HPS/tender → `reviu-pengadaan` · audit seluruh
   siklus PBJ → `audit-pengadaan` · pantau kontrak berjalan → `pemantauan-pengadaan` ·
   pertanyaan PBJ → `konsultasi-pengadaan` · audit program (2E) → `audit-kinerja` · LKE SAKIP
   → `evaluasi-sakip` · PK SPIP → `evaluasi-spip` · LKE RB → `evaluasi-reformasi-birokrasi` ·
   MR → `evaluasi-manajemen-risiko` · LK/PIPK/PNBP → `reviu-laporan-keuangan` / `reviu-pipk` /
   `reviu-pnbp` · TLHP → `pemantauan-tindak-lanjut` · kriteria diunggah auditor tanpa skill
   khusus → `audit-umum` / `reviu-umum` / `evaluasi-umum` / `pemantauan-umum` /
   `konsultansi-umum`. **Bila jenisnya tidak jelas, tanyakan** — jangan menebak.
3. Baca doktrin bersama yang dirujuk skill itu: `skills/panduan-format-umum/PANDUAN.md`
   (unsur temuan, format laporan, scoping sasaran, kriteria tambahan, bukti lapangan) dan
   `skills/panduan-format-umum/kodefikasi-temuan.md`. Untuk skill PBJ juga
   `skills/shared-pbj-references/PANDUAN.md`; untuk skill kinerja
   `skills/shared-kinerja-references/PANDUAN.md`.
4. Muat konteks organisasi seperlunya dari `wiki/konteks/`: `regulasi-kunci.md`,
   `glossary-komdigi.md`, `pola-temuan-berulang.md`, `risiko-penugasan.md`,
   `kriteria-kelayakan.md`. Istilah yang tidak ada di glosarium **jangan didefinisikan sendiri**.

## 1 · Sumber arahan — perannya berbeda, jangan disamakan

- **Sasaran = gerbang lingkup.** Kerjakan hanya yang masuk sasaran. Hal material di luar
  sasaran tidak dikejar; catat sebagai *usulan perluasan lingkup* di Paket-Analisis.
- **Langkah kerja PKP = lantai minimum, bukan plafon.** Cakup semua langkah, tutup tiap
  langkah dengan status; lalu analisis **sampai standar skill penuh** meski PKP tipis.
- **Standar skill + pola temuan + regulasi = tulang punggung mutu.** Pola temuan
  (`wiki/temuan-patterns/<slug>/`) adalah hipotesis dan contoh format — **bukan sumber
  kutipan**; kutipan diambil dari teks regulasinya.
- **Bukti dokumen = penentu.** Sebuah kondisi menjadi temuan hanya bila didukung
  `berkas + halaman + kutipan` dari `01-objek/`.
- Prioritas saat bertabrakan: lingkup → sasaran menang · kedalaman → standar skill menang ·
  kepatuhan → langkah PKP wajib dicakup · validitas → **bukti mengalahkan pola, selalu**.

## 2 · Doktrin yang tidak boleh dilanggar

Rinciannya di `references/01-doktrin-temuan.md`; ringkasnya:

- **Setiap fakta punya sumber.** Angka, tanggal, nomor dokumen, kutipan — semuanya harus
  bisa ditunjuk ke berkas dan halaman yang benar-benar dibuka. Tidak ada fakta dari ingatan.
- **Kriteria dikutip dari teksnya**, bukan dari ingatan: urutan sumber adalah
  `02-kriteria/` (yang diunggah auditor) → `wiki/konteks/regulasi/*.md` (teks pasal
  terverifikasi) → `skills/<slug>/references/`. Regulasi yang teksnya tidak ada di ketiganya
  ditulis **"belum terverifikasi — pasal perlu dicek auditor"**, jangan ditebak nomornya.
  Bila kriteria tambahan dari auditor bertentangan dengan kriteria baku → laporkan
  konfliknya dan hierarkinya (regulasi lebih tinggi menang).
- **Temuan = deviasi yang sudah terkonfirmasi**, bukan dugaan. Yang masih "perlu
  diverifikasi/diklarifikasi" bukan temuan — selesaikan verifikasinya, atau sampaikan sebagai
  *catatan/permintaan klarifikasi*.
- **Sebab tanpa mengarang.** Cari akar lewat RCA (5 Whys / fishbone) **hanya dari bukti**.
  Bila tak terbukti, tulis eksplisit **"Tidak cukup data untuk menyimpulkan penyebab"** —
  itu jawaban yang benar, bukan kekurangan. Berlaku untuk audit, reviu, evaluasi non-LKE,
  pemantauan. Evaluasi ber-LKE (SAKIP, SPIP, RB) dan konsultansi tidak memuat unsur Sebab.
- **Klaim ketiadaan** ("dokumen tidak memuat X") hanya boleh bila seluruh dokumen dibaca;
  sebutkan halaman/bagian yang dibaca. Dokumen besar tidak boleh disimpulkan dari sampel.
- **Nilai dan tutup tiap butir checklist skill**: SESUAI / TIDAK_SESUAI / TIDAK_CUKUP_DATA
  beserta dasarnya — bukan hanya berburu temuan.
- **Kondisi ditulis kronologis dulu, baru deviasinya.** Gaya bahasa formal, baku, kalimat
  lengkap; istilah asing diberi padanan; rupiah ditulis baku pada penyebutan kunci.
- **Rekomendasi** disusun di LHP awal, bukan di KKP; menyasar Sebab bila terbukti, menyebut
  siapa melakukan apa; tidak menambah fakta baru.
- **Dokumen wajib yang tidak ada** dicatat sebagai keterbatasan ("tidak cukup data"),
  bukan diisi dengan deviasi karangan. LKE hasil pindai yang tak terbaca → predikat
  diturunkan satu tingkat + catat keterbatasan (sesuai PANDUAN umum).

## 3 · Urutan kerja & keluaran

Rincian tiap dokumen di `references/02-alur-keluaran.md`. Urutannya wajib:

1. **DPP** (Desain Penugasan Pengawasan) dari `wiki/templates/dpp/dpp-default.md` —
   substansi dari PKPT bila ada (`wiki/pkpt/`), risiko dari `risiko-penugasan.md`, hipotesis
   awal dari pola temuan. Tulis ke `90-keluaran/01-DPP.md` dan `.docx`. **Berhenti dan
   minta auditor membaca DPP** sebelum lanjut — ini titik koreksi pertama.
2. **Laporan PIA** dari `wiki/templates/pia/pia-default.md` — 9 bagian resmi, termasuk
   §6 penilaian empat kriteria kelayakan (`kriteria-kelayakan.md`). Bila kriteria kelayakan
   tidak terpenuhi, katakan penugasan belum layak dilanjutkan; jangan dipaksakan.
3. **Analisis** per aspek/checklist skill, dengan scoping dari sasaran (§1).
4. **KKP** — tabel temuan `No | Judul | Kondisi | Kriteria | Sebab | Akibat | Kode |
   Sumber (berkas, hal.)`; per butir checklist status SESUAI/TIDAK_SESUAI/TIDAK_CUKUP_DATA.
   Untuk `reviu-rka-kl` isi juga `templates/KKR-Reviu-RKA-KL-template.xlsx`. Untuk evaluasi
   ber-LKE, hasilnya adalah LKE terisi kolom APIP + catatan/AoI (tanpa Sebab).
5. **LHP awal** dari `templates/_skeleton-lhp/template-lhp-<slug>.docx` (bila tidak ada,
   `template-lhp-generic.docx`) — profil laporan mengikuti skill: KKSA, Memo (konsultansi),
   Laporan Pendampingan (konsultasi PBJ), RB 4 dimensi, atau LKE. Bahasa keyakinan sesuai
   `tingkat-keyakinan` di frontmatter skill (reviu = terbatas, frasa baku di PANDUAN).
   Bagian administratif (nomor surat, tanda tangan, Nota Dinas) **dibiarkan `[DIISI AUDITOR]`**.
6. **`90-keluaran/Paket-Analisis.md`** — ringkasan seluruh temuan (format di
   `references/04-format-kkp-paket.md`), daftar dokumen yang dibaca beserta halaman,
   butir checklist yang TIDAK_CUKUP_DATA, usulan perluasan lingkup, dan **daftar periksa**
   dari `references/03-daftar-periksa.md`.

Tiap keluaran diawali baris: **`DRAF — belum disetujui. Persetujuan dilakukan di INTEGRAL.
Dihasilkan integral-mesin <versi dari VERSI.txt di akar plugin>.`**

## 4 · Yang tidak boleh

- Menulis fakta, angka, atau kutipan yang tidak ditelusuri ke berkas dan halaman.
- Mengutip pasal dari ingatan, atau mengisi Sebab tanpa bukti.
- Menandai apa pun sebagai "final", mengisi nomor surat/tanggal/tanda tangan, atau
  menyusun Nota Dinas.
- Melewati DPP/PIA langsung ke temuan, kecuali auditor secara eksplisit menyatakan DPP dan
  PIA sudah ada (maka baca keduanya dari `00-input/` dan pakai sebagai lingkup).
- Menurunkan kedalaman analisis mengikuti PKP yang tipis, atau memperluas lingkup di luar
  sasaran tanpa menandainya sebagai usulan.
- Menyembunyikan keterbatasan: dokumen yang tak terbaca, bagian yang tak dibuka, kriteria
  yang tak terverifikasi — semuanya ditulis di Paket-Analisis.
