---
name: integral-mesin
description: >
  Gunakan skill ini setiap kali auditor Inspektorat II Komdigi meminta mengerjakan penugasan
  pengawasan dari sebuah folder — "kerjakan penugasan ini", "susun DPP", "buat Laporan PIA",
  "susun KKP", "buat LHP awal", "analisis dokumen penugasan ini", atau saat folder berisi
  Surat Tugas/sasaran pengawasan. Skill ini adalah orkestrator: memilih skill jenis pengawasan
  INTEGRAL yang tepat, menegakkan doktrin anti-mengarang, kutipan sumber, dan isolasi sumber,
  lalu menghasilkan draf DPP, Laporan PIA, KKP, dan LHP awal lewat mesin.py untuk diunggah ke
  INTEGRAL. Untuk PK SPIP langsung di aplikasi spip.komdigi.go.id, lihat skill evaluasi-spip.
metadata:
  version: "0.2.0"
  author: "Inspektorat II — Itjen Komdigi"
---

# INTEGRAL Mesin — orkestrator penugasan pengawasan

Skill ini menggantikan orkestrator server INTEGRAL. Skill jenis pengawasan (`reviu-rka-kl`,
`audit-pengadaan`, …) berisi **substansi**; urutan kerja, gerbang, dan doktrin ada **di sini**.
Semua keluaran adalah **DRAF** — persetujuan dilakukan auditor di INTEGRAL, bukan di Cowork.

**Akar plugin** = dua tingkat di atas folder skill ini (berisi `skills/`, `wiki/`, `templates/`,
`meta/`, `VERSI.txt`). Semua dokumen keluaran dibuat oleh **`mesin.py`**:
`python3 <akar>/skills/integral-mesin/scripts/mesin.py <perintah> <folder-penugasan>`. Bila `python3` tidak ada (Windows), pakai `python` atau `py -3` — skripnya sama; ia memakai interpreter yang menjalankannya untuk semua langkah berikutnya.
Jangan merangkai skrip lain sendiri, dan jangan menyunting `.docx` hasil mesin dengan tangan.

## 0 · Mulai — auditor cukup menyiapkan `00-input/`

1. Folder penugasan hanya perlu berisi **`00-input/`** dengan semua dokumen (Surat Tugas,
   sasaran, dokumen objek, kriteria tambahan, bukti lapangan — subfolder boleh, tidak wajib).
   Bila dokumen ada di akar folder tanpa `00-input/`, **minta izin** auditor sebelum memindahkannya.
   **Folder yang tersinkron Google Drive:** berkas `.gdoc`/`.gsheet`/`.gslides` hanyalah penunjuk
   tanpa isi — `mesin.py mulai` menolaknya (keluar 4). Minta auditor mengunduhnya sebagai
   `.docx`/`.xlsx`/PDF ke `00-input/`; jangan mencoba membaca dokumen itu lewat tautannya, karena
   isinya tidak masuk manifest dan tak bisa dikutip dengan halaman.
2. `mesin.py cek` — memeriksa `python-docx`, `openpyxl`, kerangka LHP, dan teks regulasi.
   Keluar 6 → coba `pip install python-docx openpyxl`; bila tetap gagal, katakan terus terang
   dan pakai skill docx sebagai cadangan dengan catatan "format tidak dijamin".
3. `mesin.py mulai <folder>` — membuat folder kerja dan **manifest** (SHA-256 tiap berkas
   `00-input/`). Baca `references/05-isolasi-sumber.md` **sekarang**: fakta hanya dari berkas di
   manifest. Bila auditor menambah dokumen kemudian: `mesin.py ulang-manifest` — hanya atas
   sepengetahuan auditor.

## 1 · Pilih skill jenis pengawasan

Tentukan jenisnya dari Surat Tugas/sasaran, muat `skills/<slug>/SKILL.md`, ikuti gate/alurnya.
reviu TOR/RAB → `reviu-rka-kl` · reviu RUP/HPS/tender → `reviu-pengadaan` · audit siklus PBJ →
`audit-pengadaan` · pantau kontrak → `pemantauan-pengadaan` · pertanyaan/pendampingan PBJ →
`konsultasi-pengadaan` · audit program (2E) → `audit-kinerja` · LKE SAKIP → `evaluasi-sakip` ·
PK SPIP → `evaluasi-spip` (**dua jalur**: isi langsung di aplikasi spip.komdigi.go.id bila Claude
in Chrome tersedia, atau LKE Excel — skill itu yang memilih) · RB → `evaluasi-reformasi-birokrasi` ·
MR → `evaluasi-manajemen-risiko` · LK/PIPK/PNBP → `reviu-laporan-keuangan`/`reviu-pipk`/`reviu-pnbp` ·
TLHP → `pemantauan-tindak-lanjut` · kriteria dari auditor tanpa skill khusus → `audit-umum`/
`reviu-umum`/`evaluasi-umum`/`pemantauan-umum`/`konsultansi-umum`. **Tidak jelas → tanyakan.**
**Skill jenis ditulis untuk server INTEGRAL.** Bila ia menyebut *digest* TOR/RAB/dokumen, `read_digest`,
`read_ingested_digest`, atau melarang membaca PDF ulang — di Cowork tak ada digest: **baca dokumen
di `00-input/` langsung**, halaman demi halaman, dan catat halamannya untuk kutipan. Alat tulisnya
diganti berkas: `append_temuan` → `_KKP/temuan.json`, `write_penilaian_aspek` →
`_KKP/penilaian-aspek.json`, `write_perencanaan` → `_PERENCANAAN/dpp.json`/`pia.json`.
Lalu baca doktrin bersama yang dirujuknya: `skills/panduan-format-umum/PANDUAN.md`,
`kodefikasi-temuan.md`, dan `shared-pbj-references/` atau `shared-kinerja-references/` bila disebut.

## 2 · Sumber arahan — perannya berbeda

- **Sasaran = gerbang lingkup.** Hal material di luar sasaran → *usulan perluasan lingkup*, bukan temuan.
- **Langkah kerja PKP = lantai, bukan plafon.** Cakup semuanya, lalu analisis sampai standar skill penuh.
- **Standar skill + pola temuan + regulasi = tulang punggung mutu.** Pola temuan
  (`wiki/temuan-patterns/<slug>/`) adalah hipotesis dan contoh bentuk — **bukan sumber kutipan**.
- **Bukti dokumen = penentu.** Bukti mengalahkan pola, selalu.

## 3 · Doktrin — rinciannya di `references/01-doktrin-temuan.md`

Fakta hanya dari berkas di manifest, dengan berkas + halaman + kutipan · kriteria dikutip dari
teksnya (`00-input/` kriteria auditor → `wiki/konteks/regulasi/*.md` → `references/`); yang tak ada
teksnya ditulis **"belum terverifikasi"** · temuan = deviasi **pasti**, dugaan menjadi catatan
klarifikasi · Sebab lewat RCA dari bukti, bila tak terbukti **"Tidak cukup data untuk menyimpulkan
penyebab"** · klaim ketiadaan hanya bila seluruh dokumen dibaca · tiap butir checklist ditutup
SESUAI/TIDAK_SESUAI/TIDAK_CUKUP_DATA · kondisi kronologis, bahasa formal baku.

## 4 · Urutan kerja — setiap langkah diakhiri perintah mesin

Format tiap berkas ada di `references/04-kontrak-berkas.md`; alur rinci di `references/02-alur-keluaran.md`.

1. **`context.md`** — identitas, Tujuan, Ruang Lingkup, tabel Tim (format wajib di rujukan 04).
2. **DPP** → `_PERENCANAAN/dpp.json` (daftar field: `mesin.py perencanaan --field dpp`; tabel berupa
   daftar objek) dan sasarannya ke `_PKP/sasaran-assignment.json`. Field yang merupakan keputusan
   auditor dibiarkan kosong — mesin mencetaknya `[BELUM DIISI]`. **Berhenti — minta auditor membaca
   DPP** sebelum lanjut.
3. **Laporan PIA** → `_PERENCANAAN/pia.json` (`--field pia`; §6 empat kriteria kelayakan — bila tak
   layak, hentikan). Lalu `mesin.py perencanaan <folder>` → `DPP.md`/`Laporan-PIA.md` + `.docx`.
4. **Analisis** → `_KKP/temuan.json` + `_KKP/penilaian-aspek.json` — **tiap** butir checklist
   ditutup, termasuk yang SESUAI (wajib untuk KKSA; kunci `aspek`/`kesimpulan`/`dasar`).
   Lalu `mesin.py kkp <folder>`: kontrak → isolasi → KKP → QC. Keluar 5/2/3 → perbaiki sumbernya.
5. **LHP awal** → tulis data profilnya (KKSA: `_LHP/rekomendasi.json`; memo: `_LHP/saran.json`;
   RB: `_LHP/penilaian-rb.json`; pendampingan: `_LHP/kegiatan-pendampingan.json`), lalu
   `mesin.py lhp <folder> --judul "…" --auditi "…" --gambaran-umum "3–5 kalimat dari 00-input"`
   (+ `--simpulan "…"` bila diminta). Mesin melaporkan **bagian "[DIISI — …]"** yang harus diisi
   dari dokumen: tulis JSON `{"<teks penanda persis>": "isi" | {"tabel": [[…]]}}`, jalankan ulang
   dengan `--isian <berkas>`, sampai tak ada yang tersisa. Yang **tak bisa** diisi dari bukti
   dibiarkan dan dicatat di Paket → Keterbatasan — jangan dikarang.
6. **`mesin.py paket <folder>`** → `Paket-Analisis.md`; isi bagian `<!-- DIISI SKILL -->` dan
   jawab **daftar periksa** (`references/03-daftar-periksa.md`) dengan jujur.

Keluar **7** = QC SAIPI menemukan KRITIS: baca `_QA-SAIPI/laporan-qa-*.md`, perbaiki **data
sumbernya**, jalankan ulang. Kode lain: 0 beres · 2 `00-input` berubah · 3 sumber di luar
manifest · 4 prasyarat kurang · 5 kontrak dilanggar · 6 pustaka Python tak ada.

## 5 · Yang tidak boleh

- Fakta, angka, atau kutipan yang tak ditelusuri ke berkas di manifest; pasal dari ingatan;
  Sebab tanpa bukti.
- Menyunting `.docx` hasil mesin dengan tangan, atau melewati `mesin.py` untuk KKP/LHP.
- Membuat ulang manifest untuk "meloloskan" perubahan `00-input/` tanpa sepengetahuan auditor.
- Menandai apa pun "final", mengisi nomor surat/tanggal/tanda tangan, menyusun Nota Dinas.
- Melewati DPP/PIA, kecuali auditor menyatakan keduanya sudah ada (baca dari `00-input/`).
- Menyembunyikan keterbatasan — dokumen yang tak terbaca, bagian yang tak dibuka, kriteria
  belum terverifikasi, bagian LHP yang tak bisa diisi: semuanya ke Paket.
