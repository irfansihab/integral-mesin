# Kontrak berkas — format yang dibaca mesin.py

Bentuknya sama dengan server INTEGRAL, sehingga perender INTEGRAL membacanya apa adanya.
`mesin.py kkp` menolak (keluar 5) `temuan.json` yang melanggar kontrak — pesan galatnya menyebut
field persisnya.

## `context.md`

```markdown
# Konteks Penugasan

## Identitas Penugasan

| Kolom | Isi |
|---|---|
| Kode | 2026-10-reviu-rka-ditjen-x |
| Objek | Ditjen X — RKA-K/L TA 2027 |
| Skill | reviu-rka-kl |
| Nomor ST | ST-123/IJ.3/PW.04.04/10/2026 |
| Tanggal ST | 1 Oktober 2026 |
| Tahun Anggaran | 2027 |
| Periode Pelaksanaan | 1–10 Oktober 2026 |
| Dasar Penugasan | Nota Dinas Sekretaris Ditjen X Nomor … |

Tujuan: <satu kalimat — dari DPP/Surat Tugas>

Ruang Lingkup: <dokumen yang diperiksa + TA>

## Tim

| Peran | Nama | NIP | Jabfung |
|---|---|---|---|
| Ketua Tim | … | … | Auditor Madya |
| Anggota | … | … | Auditor Pertama |
```

`Tujuan:` dan `Ruang Lingkup:` ditulis **inline** (bukan judul). Yang tak diketahui → `[DIISI AUDITOR]`.

## `_PKP/sasaran-assignment.json`

```json
{"skill": "reviu-rka-kl", "sasaran": [
  {"sasaran_id": "S-01", "deskripsi": "…dari DPP…", "assigned_to": ["Nama Auditor"],
   "status": "DISETUJUI_KT", "langkah_kerja": ["…", "…"]}]}
```

## `_KKP/temuan.json`

```json
{
  "schema_version": "v4.0.0",
  "generated_at": "2026-10-05T14:00:00+07:00",
  "penugasan": {"id": "<kode>", "nomor_st": "…", "tanggal_st": "2026-10-01",
                "obyek": "…", "jenis_pengawasan": "<slug skill>"},
  "temuan": [{
    "id_temuan": "T-001", "sasaran_id": "S-01",
    "judul_temuan": "…singkat dan tegas…",
    "anggota_tim": {"nama_lengkap": "Nama Auditor"},
    "kondisi": "…kronologis dulu, lalu deviasi…",
    "kriteria": "Perpres 16/2018 Pasal 26 ayat (1): \"…bunyi…\" (sumber: wiki/konteks/regulasi/…)",
    "sebab": "…akar via RCA dari bukti… | Tidak cukup data untuk menyimpulkan penyebab",
    "akibat": "…",
    "kode_kondisi": "4.402", "kode_penyebab": "", "kode_rekomendasi": "4.401",
    "dokumen_sumber": [{"file": "00-input/TOR-RO-01.pdf", "halaman": 3, "kutipan": "…apa adanya…"}],
    "langkah_kerja_terkait": "…langkah PKP… | di luar lantai PKP — dari standar skill",
    "pattern_id": "RKA-01", "ro": "", "origin": "AI", "status": "DRAFT"
  }]
}
```

Aturan yang ditegakkan: `schema_version` = `v4.0.0` · kelima field `penugasan` terisi · `id_temuan`
berbentuk `T-001`, unik · `sasaran_id` ada di sasaran-assignment · jenis ber-KKSA **wajib** memuat
kunci `sebab` berisi teks (bila tak terbukti, `kode_penyebab` kosong) · evaluasi ber-LKE dan
konsultansi tanpa Sebab · `dokumen_sumber` tak kosong, tiap butir punya `file`, `halaman`,
`kutipan` · `file` harus berkas di manifest (dicek `check_isolation`) · `kode_kondisi` terisi ·
tak ada `{{…}}`.

## `_KKP/penilaian-aspek.json` (dianjurkan)

```json
{"aspek": [{"butir": "Kelengkapan KAK/TOR", "status": "TIDAK_SESUAI", "dasar": "00-input/TOR.pdf hal. 2"}]}
```

## Data LHP per profil

- **kksa** — `_LHP/rekomendasi.json`: `{"T-001": "Kepala … agar …", "T-002": "…"}`, satu per temuan.
- **memo** — `_LHP/saran.json`: `[{"pertanyaan": "…", "dasar_hukum": ["…"], "telaah": "…",
  "pendapat": "…", "saran": "…", "asumsi_batasan": "…"}]`. `telaah` dan `dasar_hukum` wajib.
- **rb-4dim** — `_LHP/penilaian-rb.json`: `{"komponen": [{"nama": "…", "ketepatan": "Sesuai",
  "ketercapaian": "…", "kualitas": "Tidak Sesuai", "kesesuaian": "…", "catatan": "…"}],
  "analisis_dampak": "…", "aoi": ["Agar …"]}`.
- **pendampingan** — `_LHP/kegiatan-pendampingan.json`: `[{"tanggal": "2026-10-02",
  "jenis_kegiatan": "Rapat", "deskripsi": "…", "hasil": "…", "pihak_didampingi": "PPK",
  "dokumen_pendukung": ["…"], "tindak_lanjut": "…"}]`.

## `--isian` untuk bagian `[DIISI — …]`

```json
{"[DIISI — Komposisi tim audit kinerja]": "Ketua Tim …; Anggota …",
 "[DIISI — Tabel rekapitulasi nilai per komponen LKE]": {"tabel": [["Komponen", "Bobot", "Nilai PM", "Nilai PK"],
                                                                   ["Perencanaan Kinerja", "30", "22,5", "20,1"]]}}
```

Kunci = teks penanda persis seperti dicetak mesin (awalannya cukup). Paragraf dipisah baris kosong.
