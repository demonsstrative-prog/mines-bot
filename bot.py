#!/usr/bin/env python3
"""
AI Engine v4 — Advanced Automatic Low-Risk Signal Bot
Mines + Crash games • Admin control • ALLEYSIGNALS protection
"""

import time
import random
import json
import os
from datetime import datetime, timezone
import requests

from config import (
    BOT_TOKEN, CHANNEL_ID, CYCLE_SECONDS,
    COUNTDOWN_5, COUNTDOWN_1, DELAY_AFTER_SIGNAL,
    DELAY_AFTER_GREEN, MIN_SLEEP, RANDOM_MIN, RANDOM_MAX,
    PROMO_EVERY, TIP_EVERY, STATS_EVERY,
    MAX_RETRIES, TIMEOUT, STATS_FILE
)
from grid import get_mines_data
from crash import get_crash_data
from messages import (
    countdown, mines_signal, crash_signal,
    green, promo, tip, stats, startup
)
from admin import AdminController

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

class AIEngine:
    def __init__(self):
        self.admin = AdminController()
        self.total = 0
        self.mines_count = 0
        self.crash_count = 0
        self.offset = 0
        self.load_stats()

    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def load_stats(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE) as f:
                    d = json.load(f)
                    self.total = d.get("total", 0)
                    self.mines_count = d.get("mines", 0)
                    self.crash_count = d.get("crash", 0)
            except:
                pass

    def save_stats(self):
        try:
            with open(STATS_FILE, "w") as f:
                json.dump({
                    "total": self.total,
                    "mines": self.mines_count,
                    "crash": self.crash_count,
                    "updated": datetime.now(timezone.utc).isoformat()
                }, f)
        except Exception as e:
            self.log(f"Stats error: {e}")

    def send(self, text, chat_id=None):
        target = chat_id or CHANNEL_ID
        for i in range(1, MAX_RETRIES+1):
            try:
                r = requests.post(f"{API}/sendMessage", json={
                    "chat_id": target,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False
                }, timeout=TIMEOUT)
                if r.json().get("ok"):
                    return True
            except Exception as e:
                self.log(f"Send fail {i}: {e}")
                time.sleep(1.5 * i)
        return False

    def random_delay(self):
        time.sleep(random.randint(RANDOM_MIN, RANDOM_MAX))

    def check_admin(self):
        try:
            r = requests.get(f"{API}/getUpdates", params={
                "offset": self.offset,
                "timeout": 1
            }, timeout=8)
            data = r.json()
            if not data.get("ok"):
                return
            for u in data.get("result", []):
                self.offset = u["update_id"] + 1
                msg = u.get("message")
                if not msg:
                    continue
                uid = msg.get("from", {}).get("id")
                text = msg.get("text", "")
                cid = msg.get("chat", {}).get("id")
                if text:
                    reply = self.admin.handle(uid, text)
                    if reply:
                        self.send(reply, chat_id=str(cid))
        except Exception as e:
            self.log(f"Admin check error: {e}")

    def send_mines(self):
        data = get_mines_data(self.admin.mode)
        self.total += 1
        self.mines_count += 1
        self.save_stats()
        self.send(mines_signal(self.total, data))
        self.log(f"Mines #{self.total}")
        time.sleep(DELAY_AFTER_SIGNAL)
        self.send(green(self.total, "MINES"))

    def send_crash(self):
        data = get_crash_data(self.admin.mode)
        self.total += 1
        self.crash_count += 1
        self.save_stats()
        self.send(crash_signal(self.total, data))
        self.log(f"Crash #{self.total} ({data['game']})")
        time.sleep(DELAY_AFTER_SIGNAL)
        self.send(green(self.total, data["game"].upper()))

    def choose_signal(self):
        if self.admin.consume_force_mines():
            self.send_mines()
            return
        if self.admin.consume_force_crash():
            self.send_crash()
            return

        # Normal rotation
        if random.random() < 0.55:
            self.send_mines()
        else:
            self.send_crash()

    def run_cycle(self):
        if not self.admin.running or self.admin.maintenance:
            self.log("Engine paused")
            time.sleep(20)
            return

        # Adjust speed if aggressive
        cycle = CYCLE_SECONDS
        if self.admin.intensity == "aggressive":
            cycle = int(CYCLE_SECONDS * 0.7)

        self.send(countdown(4))
        time.sleep(COUNTDOWN_5 - COUNTDOWN_1)

        self.send(countdown(1))
        time.sleep(COUNTDOWN_1)

        self.choose_signal()
        self.random_delay()

        if self.total % PROMO_EVERY == 0:
            time.sleep(DELAY_AFTER_GREEN)
            self.send(promo())

        if self.total % TIP_EVERY == 0:
            time.sleep(9)
            self.send(tip())

        if self.total % STATS_EVERY == 0:
            time.sleep(7)
            self.send(stats(
                self.total, self.mines_count, self.crash_count,
                self.admin.mode, self.admin.intensity
            ))

        used = COUNTDOWN_5 + DELAY_AFTER_SIGNAL + DELAY_AFTER_GREEN
        remaining = max(MIN_SLEEP, cycle - used)
        self.log(f"Sleep {remaining}s")
        time.sleep(remaining)

    def start(self):
        self.log("=" * 60)
        self.log("AI ENGINE v4 STARTED")
        self.log("=" * 60)

        self.send(startup(self.admin.mode, self.admin.intensity))
        time.sleep(6)

        while True:
            try:
                self.check_admin()
                self.run_cycle()
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(25)

if __name__ == "__main__":
    AIEngine().start()
