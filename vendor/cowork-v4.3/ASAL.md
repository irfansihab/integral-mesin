# Asal berkas di folder ini

Disalin **apa adanya** dari repo Cowork `marchelianaba/audit-system-cowork` (audit-system v4.4,
1 Juni 2026; komit awal `d499dc6`, 29 Sep 2026) — Aturan Isolasi Sumber v4.3 (11 Mei 2026).

| Berkas | Asal |
|---|---|
| `generate_session_manifest.py` | `scripts/generate_session_manifest.py` |
| `check_isolation.py` | `scripts/check_isolation.py` |
| `ATURAN-ISOLASI-SUMBER.md` | `skills/ATURAN-ISOLASI-SUMBER.md` (diadaptasi ke `payung/integral-mesin/references/05-isolasi-sumber.md`) |

Kedua skrip disalin `bangun.py` ke dalam paket tanpa diubah. INTEGRAL FULL tidak memilikinya —
di server tiap penugasan terisolasi oleh arsitektur; di Cowork (memori lintas sesi) pengaman ini
dibutuhkan. Jangan sunting di sini; bila perlu mengubah perilaku, bungkus di `mesin.py`.
