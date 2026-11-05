# WhatsApp Academic & Schedule Bot (wabot 2)

## Overview
Bot WhatsApp otomatis untuk notifikasi jadwal kuliah dan deadline tugas dari Google Calendar, dibangun menggunakan Python, FastAPI, WAHA (WhatsApp HTTP API), dan SQLite.

## Stack
- **Runtime**: Python 3.14 + FastAPI + Uvicorn
- **Messaging API**: WAHA (`/api/sendText`)
- **Calendar API**: Google Calendar API v3 (`key.json`)
- **Database**: SQLite (`jadwal.db`)
- **Process Manager**: Shell daemon (`bot.sh`)

## Structure
- `bot.py`: Webhook FastAPI, rate limiter, & integrasi WAHA/Google Calendar
- `jadwal.py`: Database query & command dispatcher jadwal kuliah
- `bot.sh`: Daemon runner (start/stop/status/restart/log)
- `jadwal.db`: SQLite database jadwal
- `key.json`: Kredensial Google Cloud Service Account
- `Context.md`: Dokumentasi sistem

