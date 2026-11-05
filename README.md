# WhatsApp Academic & Schedule Bot (wabot 2)

Bot WhatsApp otomatis untuk notifikasi jadwal perkuliahan dan integrasi *deadline* tugas akademik dari Google Calendar. Bot ini berjalan menggunakan Python, FastAPI, WAHA (WhatsApp HTTP API), dan SQLite.

---

## 🚀 Fitur Utama

- 📅 **Jadwal Kuliah Automatis**: Cek jadwal hari ini, besok, atau seluruh minggu (Senin - Jumat).
- 📌 **Integrasi Google Calendar**: Penarikan otomatis batas waktu / *deadline* tugas 14 hari ke depan.
- ⚡ **Command Dispatcher Fleksibel**: Mendukung sintaks dengan prefix maupun tanpa prefix (`/jadwal`, `jadwal`, `!jadwal`, `besok`, `tugas`, dll).
- 🛡️ **Rate Limiting & Safety**: Mencegah pemanggilan webhook berlebihan (*spamming*).
- 🔧 **Daemon Management**: Manajemen proses daemon mudah dengan skrip `bot.sh`.

---

## 🛠️ Tech Stack

- **Runtime**: Python 3.14 / FastAPI / Uvicorn
- **Messaging Gateway**: [WAHA (WhatsApp HTTP API)](https://waha.devlike.pro/)
- **External API**: Google Calendar API v3
- **Database**: SQLite (`jadwal.db`)

---

## 📌 Perintah Bot

| Perintah | Alias | Keterangan |
| :--- | :--- | :--- |
| `jadwal` | `/jadwal`, `hariini`, `today` | Menampilkan jadwal perkuliahan hari ini |
| `besok` | `/besok`, `tomorrow` | Menampilkan jadwal perkuliahan besok |
| `minggu` | `/minggu`, `/semua`, `full` | Menampilkan jadwal lengkap Senin–Jumat |
| `tugas` | `/tugas`, `/deadline`, `deadline` | Menampilkan deadline tugas 14 hari ke depan |
| `help` | `/help`, `menu`, `pilihan` | Menampilkan menu bantuan perintah |

---

## ⚙️ Konfigurasi Environment Variable

Bot menggunakan variabel lingkungan berikut (opsional):

| Variable | Default Value | Keterangan |
| :--- | :--- | :--- |
| `CALENDAR_ID` | `tumbalkontol069@gmail.com` | ID Google Calendar |
| `WAHA_URL` | `http://localhost:3000` | URL service WAHA |
| `SEMUA_BOLEH` | `true` | Mengizinkan semua pengirim merespons |
| `WAHA_API_KEY` | `""` | API Key WAHA (jika dikonfigurasi) |
| `LOG_LEVEL` | `INFO` | Level log Python (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## 📦 Jalankan Bot

1. Inisialisasi database SQLite:
   ```bash
   python3 jadwal.py
   ```

2. Kelola daemon bot menggunakan `bot.sh`:
   ```bash
   ./bot.sh start   # Jalankan bot
   ./bot.sh status  # Cek status bot
   ./bot.sh log     # Lihat log real-time
   ./bot.sh stop    # Hentikan bot
   ```
