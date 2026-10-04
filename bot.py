#!/usr/bin/env python3
"""
bot.py
Advanced Automatic Low-Risk Engine
Mines + Aviator style • 24/7 • Admin control • ALLEYSIGNALS protection
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
    DELAY_AFTER_GREEN, MIN_SLEEP, RANDOM_DELAY_MIN, RANDOM_DELAY_MAX,
    PROMO_EVERY, TIP_EVERY, STATS_EVERY,
    MINES_ENABLED, AVIATOR_ENABLED,
    MAX_RETRIES, TIMEOUT, STATS_FILE
)
from grid import get_mines_signal_data
from aviator import get_aviator_signal_data
from messages import (
    countdown, mines_signal, aviator_signal,
    green, promo, tip, stats, startup, admin_status
)
from admin import AdminController

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

class Engine:
    def __init__(self):
        self.admin = AdminController()
        self.total_signals = 0
        self.mines_count = 0
        self.aviator_count = 0
        self.offset = 0
        self.load_stats()

    def log(self, msg: str):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def load_stats(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r") as f:
                    data = json.load(f)
                    self.total_signals = data.get("total", 0)
                    self.mines_count = data.get("mines", 0)
                    self.aviator_count = data.get("aviator", 0)
            except:
                pass

    def save_stats(self):
        try:
            with open(STATS_FILE, "w") as f:
                json.dump({
                    "total": self.total_signals,
                    "mines": self.mines_count,
                    "aviator": self.aviator_count,
                    "updated": datetime.now(timezone.utc).isoformat()
                }, f)
        except Exception as e:
            self.log(f"Stats save error: {e}")

    def send(self, text: str, chat_id: str = None) -> bool:
        target = chat_id or CHANNEL_ID
        for attempt in range(1, MAX_RETRIES + 1):
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
                self.log(f"Send fail ({attempt}): {e}")
                time.sleep(1.5 * attempt)
        return False

    def random_delay(self):
        delay = random.randint(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX)
        time.sleep(delay)

    def process_admin_updates(self):
        """Check for admin commands."""
        try:
            r = requests.get(f"{API}/getUpdates", params={
                "offset": self.offset,
                "timeout": 1
            }, timeout=10)
            data = r.json()
            if not data.get("ok"):
                return
            for upd in data.get("result", []):
                self.offset = upd["update_id"] + 1
                msg = upd.get("message")
                if not msg:
                    continue
                user_id = msg.get("from", {}).get("id")
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")
                if not text:
                    continue
                reply = self.admin.handle_command(user_id, text)
                if reply:
                    self.send(reply, chat_id=str(chat_id))
        except Exception as e:
            self.log(f"Admin update error: {e}")

    def send_mines_signal(self):
        data = get_mines_signal_data()
        self.total_signals += 1
        self.mines_count += 1
        self.save_stats()
        text = mines_signal(self.total_signals, data["mines"], data["grid"])
        self.send(text)
        self.log(f"Mines signal #{self.total_signals} sent")
        time.sleep(DELAY_AFTER_SIGNAL)
        self.send(green(self.total_signals, "MINES"))

    def send_aviator_signal(self):
        data = get_aviator_signal_data()
        self.total_signals += 1
        self.aviator_count += 1
        self.save_stats()
        text = aviator_signal(self.total_signals, data["target"], data["confidence"])
        self.send(text)
        self.log(f"Aviator signal #{self.total_signals} sent")
        time.sleep(DELAY_AFTER_SIGNAL)
        self.send(green(self.total_signals, "CRASH"))

    def choose_and_send_signal(self):
        # Force commands have priority
        if self.admin.consume_force_mines() and MINES_ENABLED:
            self.send_mines_signal()
            return
        if self.admin.consume_force_aviator() and AVIATOR_ENABLED:
            self.send_aviator_signal()
            return

        # Normal rotation
        options = []
        if MINES_ENABLED:
            options.append("mines")
        if AVIATOR_ENABLED:
            options.append("aviator")

        if not options:
            return

        choice = random.choice(options)
        if choice == "mines":
            self.send_mines_signal()
        else:
            self.send_aviator_signal()

    def run_cycle(self):
        if not self.admin.running:
            self.log("Engine paused by admin")
            time.sleep(30)
            return

        # Countdown phase
        self.send(countdown(5))
        self.log("5-min countdown")
        time.sleep(COUNTDOWN_5 - COUNTDOWN_1)

        self.send(countdown(1))
        self.log("1-min countdown")
        time.sleep(COUNTDOWN_1)

        # Main signal
        self.choose_and_send_signal()
        self.random_delay()

        # Promo
        if self.total_signals % PROMO_EVERY == 0:
            time.sleep(DELAY_AFTER_GREEN)
            self.send(promo())
            self.log("Promo sent")

        # Tip
        if self.total_signals % TIP_EVERY == 0:
            time.sleep(10)
            self.send(tip())

        # Stats
        if self.total_signals % STATS_EVERY == 0:
            time.sleep(8)
            self.send(stats(self.total_signals, self.mines_count, self.aviator_count))

        # Remaining sleep
        used = COUNTDOWN_5 + DELAY_AFTER_SIGNAL + DELAY_AFTER_GREEN
        remaining = max(MIN_SLEEP, CYCLE_SECONDS - used)
        self.log(f"Sleeping {remaining}s until next cycle")
        time.sleep(remaining)

    def start(self):
        self.log("=" * 60)
        self.log("ADVANCED LOW-RISK ENGINE STARTED")
        self.log(f"Channel: {CHANNEL_ID}")
        self.log("=" * 60)

        self.send(startup())
        time.sleep(8)

        while True:
            try:
                self.process_admin_updates()
                self.run_cycle()
            except Exception as e:
                self.log(f"Cycle error: {e}")
                time.sleep(30)

if __name__ == "__main__":
    engine = Engine()
    engine.start()
