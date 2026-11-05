import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import jadwal
import requests
from fastapi import FastAPI, Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent
CAL_ID = os.getenv("CALENDAR_ID", "tumbalkontol069@gmail.com")
WAHA = os.getenv("WAHA_URL", "http://localhost:3000")
ALLOWED = {
    "199883734700266@lid",
    "17119840362715@lid",
    "92462190227502@lid",
    "6282265468133@c.us",
    "6289688361696@c.us",
}
SEMUA_BOLEH = os.getenv("SEMUA_BOLEH", "true").lower() in {"1", "true", "yes", "on"}
TZ = ZoneInfo("Asia/Jakarta")

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)
_terakhir = {}

try:
    creds = service_account.Credentials.from_service_account_file(
        BASE_DIR / "key.json",
        scopes=["https://www.googleapis.com/auth/calendar.readonly"],
    )
    cal = build("calendar", "v3", credentials=creds)
except Exception:
    cal = None
    logger.warning("Google Calendar credentials (key.json) not loaded. Deadline feature will be disabled.")

app = FastAPI()


def terlalu_cepat(sender, jeda=5):
    now = time.time()
    terakhir = _terakhir.get(sender)
    if terakhir is not None and now - terakhir < jeda:
        return True
    _terakhir[sender] = now
    if len(_terakhir) > 1000:
        batas = now - 300
        for key, timestamp in list(_terakhir.items()):
            if timestamp < batas:
                del _terakhir[key]
    return False


def get_events(start, end):
    if not cal:
        return []
    try:
        res = cal.events().list(
            calendarId=CAL_ID,
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        return res.get("items", [])
    except Exception:
        logger.exception("Failed to fetch Google Calendar events")
        return []


def fmt(ev):
    title = ev.get("summary", "(Tanpa judul)")
    start = ev.get("start", {})
    if "dateTime" in start:
        try:
            waktu = datetime.fromisoformat(start["dateTime"]).astimezone(TZ)
            return f"• {waktu:%d/%m %H:%M} - *{title}*"
        except (TypeError, ValueError):
            pass
    return f"• {start.get('date', 'Waktu tidak tersedia')} - *{title}*"


def deadline_14_hari():
    if not cal:
        return "⚠️ Fitur deadline non-aktif (Google Calendar belum dikonfigurasi/key.json tidak valid)."
    now = datetime.now(TZ)
    evs = get_events(now, now + timedelta(days=14))
    if not evs:
        return "✨ Tidak ada deadline dalam 14 hari ke depan."
    return "📌 *Deadline Terdekat (14 Hari):*\n" + "\n".join(fmt(e) for e in evs)


def kirim(chat_id, text):
    response = requests.post(
        f"{WAHA}/api/sendText",
        json={"session": "default", "chatId": chat_id, "text": text},
        headers={"X-Api-Key": os.environ.get("WAHA_API_KEY", "")},
        timeout=15,
    )
    response.raise_for_status()


@app.post("/webhook")
async def webhook(req: Request):
    try:
        data = await req.json()
        payload = data.get("payload")
        if not isinstance(payload, dict):
            return {"ok": True}

        sender = payload.get("from")
        message = payload.get("body", "")
        if not isinstance(sender, str) or not isinstance(message, str):
            return {"ok": True}
        if payload.get("fromMe") or sender == "status@broadcast":
            return {"ok": True}
        if not (SEMUA_BOLEH or sender in ALLOWED):
            return {"ok": True}

        logger.info("Webhook message received")
        msg = message.strip().lower()
        balasan = jadwal.perintah(msg, deadline_14_hari)
        if balasan and not terlalu_cepat(sender):
            kirim(sender, balasan)
    except (ValueError, KeyError, requests.RequestException):
        logger.exception("Webhook processing failed")
    except Exception:
        logger.exception("Unexpected webhook failure")
    return {"ok": True}
