#!/usr/bin/env python3
"""
Mines 1Win Signals — Advanced Multi-File Channel Bot
24/7 • 3-star entries • Affiliate push
"""

import time
import requests
from datetime import datetime

from config import (
    BOT_TOKEN, CHANNEL_ID, CYCLE_SECONDS,
    COUNTDOWN_5, COUNTDOWN_1, DELAY_AFTER_SIGNAL,
    DELAY_AFTER_GREEN, PROMO_EVERY, TIP_EVERY, STATS_EVERY
)
from grid import make_grid, random_mines
from messages import (
    countdown, signal, green, promo, tip, stats, startup
)

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def send(text: str) -> bool:
    for attempt in range(1, 4):
        try:
            r = requests.post(f"{API}/sendMessage", json={
                "chat_id": CHANNEL_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }, timeout=20)
            if r.json().get("ok"):
                return True
        except Exception as e:
            log(f"Send error ({attempt}): {e}")
            time.sleep(2 * attempt)
    return False

def main():
    log("=" * 55)
    log("Mines 1Win Signals — Advanced Engine Started")
    log(f"Channel : {CHANNEL_ID}")
    log("=" * 55)

    send(startup())
    time.sleep(8)

    count = 0

    while True:
        try:
            # Countdown
            send(countdown(5))
            log("5-min countdown")
            time.sleep(COUNTDOWN_5 - COUNTDOWN_1)

            send(countdown(1))
            log("1-min countdown")
            time.sleep(COUNTDOWN_1)

            # Signal
            count += 1
            mines = random_mines()
            grid = make_grid()
            send(signal(count, mines, grid))
            log(f"Signal #{count} sent")
            time.sleep(DELAY_AFTER_SIGNAL)

            # Green
            send(green(count))
            log("Green sent")

            # Promo
            if count % PROMO_EVERY == 0:
                time.sleep(DELAY_AFTER_GREEN)
                send(promo())
                log("Promo sent")

            # Tip
            if count % TIP_EVERY == 0:
                time.sleep(12)
                send(tip())

            # Stats
            if count % STATS_EVERY == 0:
                time.sleep(10)
                send(stats(count))

            # Remaining sleep
            used = COUNTDOWN_5 + DELAY_AFTER_SIGNAL + DELAY_AFTER_GREEN
            remaining = max(45, CYCLE_SECONDS - used)
            log(f"Sleeping {remaining}s")
            time.sleep(remaining)

        except Exception as e:
            log(f"Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
