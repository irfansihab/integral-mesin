# ⚠️ ATURAN ISOLASI SUMBER — Wajib Patuhi di Setiap Skill

> **Status:** Aturan global ekosistem audit-system-v4 (v4.3, Mei 2026).
> **Berlaku untuk:** SEMUA skill di folder `skills/` saat menjalankan Task 03 (KKP) maupun Task 04 (LHP).
> **Pelanggaran aturan ini setara dengan fabrikasi bukti audit.**

---

## Prinsip Inti

**Fakta di KKP/LHP HANYA boleh berasal dari dokumen yang di-upload auditor ke folder `00-input/` pada penugasan aktif.**

Tidak ada pengecualian. Tidak boleh ambil fakta dari:

- ❌ Folder penugasan lain (mis. `penugasan/2026-XXX/`)
- ❌ Percakapan/sesi sebelumnya (memori chat)
- ❌ Wiki (`wiki/`) untuk fakta data spesifik
- ❌ Pattern library (`pattern-library/`) untuk fakta data spesifik
- ❌ Templates (`templates/`) — itu hanya kerangka, bukan data
- ❌ Hasil ekstraksi reviu sebelumnya yang masih tersangkut di context
- ❌ Asumsi/inferensi yang "tampak relevan" tapi tidak tertulis di dokumen sesi ini

---

## Yang BOLEH dari Sumber Selain `00-input/`

| Sumber | Boleh untuk | TIDAK boleh untuk |
|---|---|---|
| **Wiki** (`wiki/`) | Pattern temuan historis sebagai referensi metodologi; lookup nomor regulasi/Perpres/PMK/Permenpan-RB sebagai **Kriteria** | Fakta Kondisi (angka, tanggal, nama, nominal, kejadian) |
| **Pattern library** (`pattern-library/`) | Referensi pola temuan dari penugasan lama untuk inspirasi struktur | Sumber data temuan baru |
| **Shared references** (`skills/shared-*-references/`) | Perbandingan skill, mapping kapan pakai yang mana | Fakta auditi |
| **Pengetahuan umum Claude** | Pemahaman regulasi/peraturan umum sebagai Kriteria (dengan catatan verifikasi nomor) | Klaim sebagai fakta dari dokumen |
| **References folder** (`references/permenpan-42-2011-kode.json`) | Lookup kodefikasi temuan & rekomendasi sesuai PermenPAN 42/2011 (89 kode temuan + 14 kode rekomendasi) untuk diisi di `kodefikasi_temuan` dan `kodefikasi_rekomendasi` per temuan | Tidak dipakai untuk fakta Kondisi/Sebab/Akibat |

**Aturan emas:** wiki dan pattern library dipakai untuk **METODOLOGI dan KRITERIA**, BUKAN untuk **DATA dan FAKTA**.

---

## Cara Memastikan Setiap Sebelum Menulis Temuan

Sebelum menuliskan kalimat di kolom **Kondisi**, **Sebab**, **Akibat** untuk satu temuan, lakukan 4 cek wajib ini:

### Cek 1 — Cek Sumber Fakta
*Apakah kalimat/angka/nomor ini ada di hasil ekstraksi dokumen `00-input/` pada sesi ini?*
- Ya → lanjut Cek 2
- Tidak → **HAPUS** kalimat tersebut

### Cek 2 — Cek Atribusi Dokumen
*Dari file mana persis fakta ini berasal?*
- Setiap fakta WAJIB sebut nama file (mis. "Berdasarkan KAK_2026.pdf..."). Field `dokumen_sumber.file` di JSON temuan tidak boleh kosong.
- File tersebut HARUS ada di `_SESSION-MANIFEST.json`. Kalau tidak ada → kontaminasi.

### Cek 3 — Cek Isolasi Sesi
*Apakah ini bukan fakta dari reviu/percakapan/sesi sebelumnya?*
- Pertanyaan diri: "Kalau saya hanya punya file di `00-input/` sesi ini dan tidak ingat apa-apa, masih bisakah saya tulis kalimat ini?"
- Kalau ragu sedikit pun → **HAPUS** atau tulis "Tidak ditemukan informasi mengenai hal ini dalam dokumen yang tersedia."

### Cek 4 — Cek Bukan Asumsi
*Apakah ini fakta eksplisit yang tertulis, bukan kesimpulan/inferensi yang dikarang?*
- Fakta eksplisit (ada angka, kalimat, nama) → boleh
- Inferensi/perkiraan → **HAPUS**, atau tulis dengan flag *"(catatan: kesimpulan analitik, bukan fakta langsung dari dokumen)"*

---

## Penanganan Multi-Dokumen di Sesi yang Sama

Kalau ada >1 dokumen di `00-input/`, setiap dokumen di-label `[DOC-N]` (DOC-1, DOC-2, dst). Setiap fakta di Kondisi WAJIB sebut label, contoh:

> "Berdasarkan [DOC-1: KAK_2026.pdf] disebutkan target SLA 99,9%, namun berdasarkan [DOC-2: Kontrak.pdf] target SLA 99,99% — terdapat inkonsistensi."

Label `[DOC-N]` mencegah pencampuran fakta antar dokumen di SATU sesi.

---

## Penanganan Kriteria (Regulasi)

Kolom **Kriteria** boleh berisi referensi regulasi yang TIDAK ada di `00-input/`. Tapi:

1. Verifikasi nomor & tahun regulasi sebelum dicantumkan
2. Kalau tidak yakin → tambah catatan: *"(Catatan: Harap verifikasi apakah regulasi ini masih berlaku)"*
3. Lebih baik tulis generik (*"sesuai ketentuan PBJ yang berlaku, nomor regulasi harap dilengkapi auditor"*) daripada mengarang nomor

Wiki boleh dipakai untuk lookup regulasi yang sering dipakai. Pattern library boleh dipakai untuk pola Kriteria yang serupa.

---

## Pre-Flight & Post-Flight Check

Dua script otomatis yang menjaga isolasi:

| Script | Kapan Dipanggil | Fungsi |
|---|---|---|
| `scripts/generate_session_manifest.py` | Awal Task 01 | Generate `_SESSION-MANIFEST.json` berisi daftar file `00-input/` + hash SHA-256. Lock-in scope sesi. |
| `scripts/check_isolation.py` | Akhir Task 03 (sebelum gate auditor); awal Task 04 (sebelum konsumsi temuan); sebelum `integral_inject.py` | Verifikasi setiap temuan punya `dokumen_sumber.file` yang ADA di manifest. Block kalau ada kontaminasi. |

**Jika `check_isolation.py` exit code 3 (kontaminasi terdeteksi):**
- Inject ke INTEGRAL DIBLOKIR
- LHP DIBLOKIR
- Auditor harus revisi temuan dulu sampai semua sumber tervalidasi

---

## Konsekuensi Pelanggaran

Kontaminasi data lintas-sesi tidak hanya menghasilkan KKP yang tidak akurat, tapi juga:

- Akuntabilitas auditor terganggu (KKP dibuat atas nama auditor padahal isinya dari penugasan lain)
- Berisiko menyebar fakta penugasan A ke laporan penugasan B (kebocoran informasi)
- Bisa dianggap fabrikasi bukti audit oleh standar SAIPI 2300

Setiap skill SKILL.md WAJIB merefer ke file ini di section "Aturan Isolasi". Tidak boleh ada skill yang menjalankan analisis tanpa patuh aturan di sini.

---

## Referensi Schema

Field di `temuan.json` yang terkait isolasi:

| Field | Wajib | Kegunaan |
|---|---|---|
| `dokumen_sumber` (array) | ✅ | Daftar file di `00-input/` yang menjadi sumber fakta. Minimal 1 entry. |
| `dokumen_sumber[].file` | ✅ | Nama file. HARUS ada di `_SESSION-MANIFEST.json`. |
| `dokumen_sumber[].halaman` | optional | Halaman/pasal/bagian dalam file. |
| `dokumen_sumber[].kutipan` | optional | Kutipan singkat (≤200 char) untuk audit trail. |

Lihat `schemas/kkp-temuan.schema.json` untuk validasi format.
