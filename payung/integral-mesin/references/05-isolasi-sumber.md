# Isolasi sumber — fakta hanya dari penugasan ini

> Diadaptasi dari Aturan Isolasi Sumber v4.3 Cowork (11 Mei 2026), dibuat setelah Claude terbukti
> membawa fakta dari penugasan lain dan dari memori sesi sebelumnya ke dalam temuan. Di server
> INTEGRAL tiap penugasan terisolasi oleh arsitektur; di Cowork (memori lintas sesi) aturan ini
> yang menjaganya — ditegakkan `check_isolation.py` lewat `mesin.py kkp/lhp`.

## Prinsip inti

**Fakta di KKP/LHP hanya boleh berasal dari berkas yang tercatat di `_SESSION-MANIFEST.json`**
— yaitu isi `00-input/` penugasan ini saat `mesin.py mulai` dijalankan.

| Sumber | Boleh untuk | Tidak boleh untuk |
|---|---|---|
| `00-input/` (manifest) | fakta: kondisi, angka, tanggal, nama, kutipan | — |
| `wiki/konteks/regulasi/`, `references/`, kriteria dari auditor di `00-input/` | kriteria & bunyi pasal | fakta kondisi |
| `wiki/temuan-patterns/`, `pola-temuan-berulang.md` | bentuk temuan, hipotesis, contoh rekomendasi | fakta, angka, nama — **jangan disalin** |
| memori percakapan / sesi lain / penugasan lain | tidak ada | **semuanya** |

## Empat cek sebelum menulis tiap kalimat Kondisi, Sebab, dan Akibat

1. **Sumber fakta** — kalimat ini bersandar pada berkas di manifest? Sebutkan berkas + halaman.
2. **Atribusi** — angka/nama/tanggal itu benar dari berkas yang disebut, bukan dari berkas lain
   atau dari pola temuan?
3. **Isolasi sesi** — adakah bagian yang "terasa diketahui" tetapi tak bisa ditunjuk di `00-input/`?
   Itu dari memori — hapus.
4. **Bukan asumsi** — bila fakta tak ada, tulis bahwa dokumennya tak tersedia; jangan mengisi celah.

## Penanganan kriteria

Nomor dan bunyi pasal diambil dari teks (kriteria auditor → `wiki/konteks/regulasi/` →
`references/`). Bila ragu atau teks tak ada: tulis "belum terverifikasi — pasal perlu dicek
auditor". Lebih baik kriteria generik yang jujur daripada nomor pasal yang dikarang.

## Bila `mesin.py` keluar 2 atau 3

- **2** — berkas di `00-input/` berubah/hilang sejak manifest. Tanyakan auditor; bila memang
  ditambah/diganti, `mesin.py ulang-manifest` lalu **periksa ulang** temuan yang bersandar padanya.
- **3** — ada `dokumen_sumber` yang menunjuk berkas di luar manifest. Itu kontaminasi: hapus
  temuan/kutipan itu atau ganti dengan berkas yang benar dari `00-input/`. Jangan diakali dengan
  menyalin berkas asing ke `00-input/` tanpa auditor.
