#!/bin/bash
set -u

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
APP="bot:app"
HOST="${HOST:-172.17.0.1}"
PORT="${PORT:-8000}"
PIDFILE="$BASE_DIR/bot.pid"
LOGFILE="$BASE_DIR/bot.log"

cd "$BASE_DIR"

pid() {
  [ -f "$PIDFILE" ] || return 1
  cat "$PIDFILE"
}

jalan() {
  local process_id
  process_id="$(pid 2>/dev/null)" || return 1
  kill -0 "$process_id" 2>/dev/null || return 1
  ps -p "$process_id" -o args= 2>/dev/null | grep -Fq "uvicorn $APP"
}

start() {
  if jalan; then
    echo "Bot sudah jalan (PID $(pid))"
    return
  fi
  rm -f "$PIDFILE"
  nohup ./venv/bin/uvicorn "$APP" --host "$HOST" --port "$PORT" >> "$LOGFILE" 2>&1 &
  echo $! > "$PIDFILE"
  sleep 2
  if jalan; then
    echo "Bot jalan (PID $(pid)). Log: $LOGFILE"
  else
    echo "Gagal start. Cek: tail -n 30 $LOGFILE"
    rm -f "$PIDFILE"
    return 1
  fi
}

stop() {
  if jalan; then
    kill "$(pid)"
    for _ in 1 2 3 4 5; do
      jalan || break
      sleep 1
    done
  fi
  rm -f "$PIDFILE"
  echo "Bot berhenti"
}

case "${1:-}" in
  start)   start ;;
  stop)    stop ;;
  restart) stop; start ;;
  status)  if jalan; then echo "Jalan (PID $(pid))"; else echo "Mati"; fi ;;
  log)     tail -f "$LOGFILE" ;;
  *)       echo "Pakai: ./bot.sh {start|stop|restart|status|log}"; exit 1 ;;
esac
