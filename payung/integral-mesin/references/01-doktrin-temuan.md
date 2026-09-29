# Doktrin temuan — rincian untuk skill payung

Diturunkan dari prompt orkestrator INTEGRAL (`anggota_tim.md`, `ketua_tim.md`) dan
`skills/panduan-format-umum/PANDUAN.md`. Bila keduanya berbeda, PANDUAN.md menang untuk
format, dokumen ini untuk pelaksanaan.

## Unsur temuan (KKSA) dan siapa yang memakainya

| Jenis | Unsur | Sebab? |
|---|---|---|
| audit (kinerja, pengadaan, umum) | Kondisi · Kriteria · Sebab · Akibat · Rekomendasi (di LHP) | wajib — RCA; kerugian negara dihitung bila relevan |
| reviu (RKA-K/L, pengadaan, LK, PIPK, PNBP, umum) | K · K · S · A · Rekomendasi (di LHR) | diisi bila terbukti; "tidak cukup data" wajar karena lingkup terbatas |
| evaluasi non-LKE (MR, umum) | K · K · S · A · Rekomendasi | diisi bila terbukti |
| pemantauan (pengadaan, TLHP, umum) | K · K · S · A · Rekomendasi | diisi bila terbukti |
| evaluasi ber-LKE (SAKIP, SPIP, RB) | LKE kolom APIP + catatan/AoI: Kondisi · Kriteria · Akibat | **tidak ada** unsur Sebab |
| konsultansi | Pertanyaan · Dasar hukum · Pendapat/Saran | tidak menghasilkan temuan |

## Sumber dokumen — wajib, per kondisi

Setiap kondisi menyebut `{file, halaman, kutipan}`; `file` = jalur berkas di `00-input/` persis
seperti tercatat di `_SESSION-MANIFEST.json`; `halaman` = nomor halaman PDF/Word atau nama sheet Excel;
`kutipan` = teks apa adanya (≤ 2 kalimat). Tanpa ini, kondisi itu bukan temuan.

Dokumen besar: jangan menyimpulkan dari bagian awal. Bila tak sanggup membaca seluruhnya,
tulis bagian mana yang dibaca dan **jangan** membuat klaim ketiadaan atas bagian yang tak dibaca.

## Kriteria — presisi & anti-mengarang

1. Urutan sumber: kriteria yang diunggah auditor di `00-input/` → `wiki/konteks/regulasi/*.md`
   (teks pasal terverifikasi, status TERVERIFIKASI di frontmatter) → `skills/<slug>/references/`.
2. Kutip **nomor pasal/ayat/huruf dan bunyinya**. Pasal yang bunyinya tidak ada di sumber
   mana pun → tulis "belum terverifikasi — perlu dicek auditor". Nomor yang terdengar masuk
   akal adalah jebakan: 38 dari 85 pola temuan pernah salah pasal karena itu.
3. Kriteria tambahan yang diunggah auditor (SOP, juklak, SBK khusus) diikutkan; tandai mana
   baku dan mana tambahan; bila bertentangan, laporkan konflik + hierarki.
4. Pola temuan (`wiki/temuan-patterns/`) memberi *bentuk* kondisi dan kriteria yang lazim —
   ambil strukturnya, verifikasi ulang pasalnya ke teks. Setiap pola mencantumkan catatan
   verifikasi; pola tanpa catatan itu belum tentu benar.

## Temuan = deviasi terkonfirmasi

Sebelum menulis temuan, tanyakan: apakah deviasi di Kondisi × Kriteria **pasti**? Bila masih
"perlu diverifikasi": (a) selesaikan verifikasinya dari berkas/kriteria yang ada; (b) bila tak
bisa, sampaikan sebagai **catatan/permintaan klarifikasi** atau **usulan langkah verifikasi**,
bukan temuan. Akibat boleh menyebut risiko *potensial*; deviasinya tidak.

## Sebab — RCA tanpa mengarang

- 5 Whys dari Kondisi, 3–5 lapis; atau fishbone (SDM · proses/SOP · sistem · kebijakan ·
  anggaran · pengawasan). Berhenti pada lapisan terakhir yang **masih didukung bukti**.
- Sertakan dasarnya (berkas/halaman) seperti kondisi.
- Tidak terbukti → **"Tidak cukup data untuk menyimpulkan penyebab"**, dan kode penyebab
  dikosongkan. Jangan menebak "kurangnya koordinasi" atau "kelalaian" tanpa bukti.

## Checklist skill — nilai dan tutup tiap butir

Untuk tiap butir checklist/aspek di SKILL.md: kesimpulan eksplisit **SESUAI /
TIDAK_SESUAI / TIDAK_CUKUP_DATA** + dasar (berkas/halaman atau "dokumen X tidak tersedia").
Butir yang SESUAI tetap didokumentasikan di KKP — bukan hanya yang menyimpang. Terapkan
judgment substansi (spesifikasi terukur? kebutuhan terkuantifikasi? jadwal masuk akal?),
bukan hanya diskrepansi yang mudah.

## Scoping dari sasaran

Sasaran generik → dekomposisi ke checklist penuh. Sasaran spesifik → dalami aspek yang
disasar; aspek lain cukup lintasan ringan; sinyal material di luar sasaran → catatan +
usulan perluasan lingkup, bukan temuan penuh. Cakupan objek tetap; yang menyempit adalah
aspek/kedalaman.

## Kondisi kronologis, bahasa formal

Kondisi: runtutan fakta urut waktu/tahapan (apa, kapan, nomor/tanggal dokumen, nilai, pihak,
sumber), lalu deviasinya. Kalimat lengkap, baku, formal; tanpa fragmen telegrafis; istilah
asing diberi padanan Indonesia; singkatan diperkenalkan pada penyebutan pertama; rupiah
"Rp29.000.000,00 (dua puluh sembilan juta rupiah)" pada penyebutan kunci.

## Kodefikasi

Tiap temuan diberi kode dari `skills/panduan-format-umum/kodefikasi-temuan.md`: kode
kondisi (wajib), kode penyebab (hanya bila Sebab terbukti), kode rekomendasi (di LHP).

## Ketertelusuran

Tiap temuan menyebut langkah kerja PKP yang memunculkannya (atau "dari standar skill, di
luar lantai PKP") dan id pola temuan bila dipakai.

## Rekomendasi (LHP awal)

Satu rekomendasi konkret per temuan: siapa melakukan apa, menyasar Sebab bila terbukti, atau
Kondisi bila tidak. Tanpa fakta baru. Untuk evaluasi ber-LKE: diarahkan pada pemenuhan unsur
yang selisih. Pakai `pola-temuan-berulang.md` agar rekomendasi tidak terisolasi dari akar
masalah lintas-LHP.

## Bahasa keyakinan

Reviu (terbatas): "Berdasarkan hasil reviu, tidak terdapat hal-hal yang membuat kami yakin
bahwa [objek] tidak [kondisi] sesuai dengan [kriteria], kecuali hal-hal yang kami sampaikan
pada bagian hasil reviu di atas." Audit (memadai) dan lainnya: lihat "Bahasa Standar per
Tingkat Keyakinan" di PANDUAN.md. Pernyataan baku SAIPI 2430 dan placeholder administratif
dibiarkan `[DIISI AUDITOR]`.
