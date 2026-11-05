import os
import sqlite3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Jakarta")
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jadwal.db")
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# (hari 0=Senin, mulai, selesai, matkul, kelas, ruang, dosen)
DATA = [
    (0, "08:15", "09:15", "Olah Raga I", "IF-B", "Lapangan M", "Sumintarsih S.Pd., M.Or."),
    (0, "12:30", "14:15", "Algoritma dan Pemrograman", "IF-B", "Patt.I-3A", "Wilis Kaswidjanti S.Si., M.Kom."),
    (0, "15:00", "16:45", "Logika Informatika", "IF-B", "Patt.I-3B", "Agus Sasmito Aribowo S.Kom., M.Cs., Ph.D"),
    (1, "08:00", "10:00", "Praktikum Implementasi Basis Data", "IF-D", "Lab Teknologi Mobile", "Budi Santosa S.Si., M.T."),
    (1, "15:30", "17:30", "Praktikum Algoritma dan Pemrograman", "IF-D", "Lab Internet Of Thing", "Rudi Cahyadi S.Si., M.T."),
    (2, "10:00", "12:30", "Matematika Diskrit", "IF-B", "Patt.I-3D", "Rifki Indra P S.Kom., M.Eng."),
    (2, "15:00", "17:30", "Sistem Teknologi Basis Data", "IF-B", "Patt.I-3D", "Mangaras Yanu F S.T., M.Eng."),
    (3, "07:00", "09:15", "Pendidikan Agama Islam", "IF-B", "Patt.III-3D", "Umar Hidayat M.Ag."),
    (3, "10:00", "11:45", "Konsep Teknologi", "IF-B", "Patt.I-3D", "Aldila Putri Linanzha, S.Kom., M.Cs."),
    (4, "07:30", "09:15", "Pendidikan Pancasila", "IF-B", "Patt.II-3B", "Yunie Herawati Ir., M.Hum."),
    (4, "10:00", "11:45", "Kalkulus", "IF-B", "Patt.II-1A", "Ahmad Taufiq Akbar S.Si., M.Cs."),
]


def init():
    with sqlite3.connect(DB) as con:
        con.execute("DROP TABLE IF EXISTS jadwal")
        con.execute(
            "CREATE TABLE jadwal (id INTEGER PRIMARY KEY, hari INTEGER, mulai TEXT, "
            "selesai TEXT, matkul TEXT, kelas TEXT, ruang TEXT, dosen TEXT)"
        )
        con.executemany(
            "INSERT INTO jadwal (hari, mulai, selesai, matkul, kelas, ruang, dosen) "
            "VALUES (?,?,?,?,?,?,?)",
            DATA,
        )


def _rows(hari):
    with sqlite3.connect(DB) as con:
        return con.execute(
            "SELECT mulai, selesai, matkul, ruang FROM jadwal WHERE hari=? ORDER BY mulai",
            (hari,),
        ).fetchall()


def teks_hari(hari, label=""):
    rows = _rows(hari)
    judul = f"*{HARI[hari]}* {label}".strip()
    if not rows:
        return f"📅 {judul}: tidak ada kuliah"
    baris = [f"• {m}-{s} | *{mk}* ({r})" for m, s, mk, r in rows]
    return f"📅 *Jadwal Kuliah {judul}*\n" + "\n".join(baris)


def perintah(msg, deadline_fn):
    cmd = msg.strip().lower().lstrip("/.!")
    now = datetime.now(TZ)
    if cmd in ("jadwal", "hariini", "today"):
        return teks_hari(now.weekday(), "(Hari ini)")
    if cmd in ("besok", "tomorrow"):
        return teks_hari((now + timedelta(days=1)).weekday(), "(Besok)")
    if cmd in ("minggu", "semua", "full"):
        return "\n\n".join(teks_hari(h) for h in range(5))
    if cmd in ("deadline", "tugas"):
        return deadline_fn()
    if cmd in ("help", "menu", "pilihan"):
        return (
            "📌 *Menu Perintah Bot:*\n"
            "• `jadwal` / `/jadwal` - Jadwal hari ini\n"
            "• `besok` / `/besok` - Jadwal besok\n"
            "• `minggu` / `/semua` - Jadwal 1 minggu (Senin-Jumat)\n"
            "• `tugas` / `/deadline` - Deadline 14 hari ke depan"
        )
    return None


if __name__ == "__main__":
    init()
    print("Database jadwal dibuat:", DB, f"({len(DATA)} matkul)")
