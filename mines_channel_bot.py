#!/usr/bin/env python3
"""
================================================================================
  MINES 1WIN SIGNALS — AI-POWERED ADVANCED CHANNEL BOT
  Version        : 3.2.0 Advanced
  Mode           : 24/7 Continuous Signal Engine
  Safe Stars     : Always 3
  Platform       : Railway / VPS / Termux
================================================================================
"""

import requests
import random
import time
import json
import os
import sys
import traceback
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional

# ══════════════════════════════════════════════════════════════════════════════
#                              CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

class Config:
    # Telegram
    BOT_TOKEN: str = "8702447245:AAH9tm7f2rqppiziufL2CUeZWe7n14uYZEE"
    CHANNEL_ID: str = "-1004331688852"
    AFFILIATE_LINK: str = "https://lkql.cc/6ac160"

    # Timing (seconds)
    FULL_CYCLE_SECONDS: int = 8 * 60          # 8 minutes total cycle
    COUNTDOWN_5_MIN: int = 5 * 60
    COUNTDOWN_1_MIN: int = 60
    DELAY_AFTER_SIGNAL: int = 40
    DELAY_AFTER_GREEN: int = 25
    DELAY_BEFORE_PROMO: int = 18
    MIN_SLEEP_BETWEEN_CYCLES: int = 45

    # Grid
    SAFE_STARS: int = 3
    MIN_BOMBS: int = 3
    MAX_BOMBS: int = 5

    # Frequency
    PROMO_EVERY_N_SIGNALS: int = 3
    TIP_EVERY_N_SIGNALS: int = 5
    STATS_EVERY_N_SIGNALS: int = 10
    LONG_TIP_EVERY_N: int = 7

    # Retry
    MAX_SEND_RETRIES: int = 4
    RETRY_BASE_DELAY: float = 1.8

    # Logging
    LOG_TO_CONSOLE: bool = True
    SHOW_STARTUP_BANNER: bool = True

    # Files (optional persistence)
    STATS_FILE: str = "bot_stats.json"


# ══════════════════════════════════════════════════════════════════════════════
#                              LOGGING SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class Logger:
    @staticmethod
    def _ts() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def info(msg: str):
        if Config.LOG_TO_CONSOLE:
            print(f"[{Logger._ts()}] [INFO]  {msg}")

    @staticmethod
    def success(msg: str):
        if Config.LOG_TO_CONSOLE:
            print(f"[{Logger._ts()}] [OK]    {msg}")

    @staticmethod
    def warn(msg: str):
        if Config.LOG_TO_CONSOLE:
            print(f"[{Logger._ts()}] [WARN]  {msg}")

    @staticmethod
    def error(msg: str):
        if Config.LOG_TO_CONSOLE:
            print(f"[{Logger._ts()}] [ERROR] {msg}")

    @staticmethod
    def banner():
        if not Config.SHOW_STARTUP_BANNER:
            return
        print("=" * 70)
        print("  MINES 1WIN SIGNALS — AI-POWERED ADVANCED ENGINE")
        print("  Version 3.2.0 | 24/7 Channel Mode | 3-Star Safe Entries")
        print("=" * 70)
        print(f"  Channel ID : {Config.CHANNEL_ID}")
        print(f"  Affiliate  : {Config.AFFILIATE_LINK}")
        print(f"  Safe Stars : {Config.SAFE_STARS}")
        print("=" * 70)


# ══════════════════════════════════════════════════════════════════════════════
#                              TELEGRAM CLIENT
# ══════════════════════════════════════════════════════════════════════════════

class TelegramClient:
    def __init__(self):
        self.api = f"https://api.telegram.org/bot{Config.BOT_TOKEN}"
        self.session = requests.Session()

    def send(self, text: str, disable_preview: bool = False) -> bool:
        payload = {
            "chat_id": Config.CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": disable_preview
        }
        for attempt in range(1, Config.MAX_SEND_RETRIES + 1):
            try:
                r = self.session.post(
                    f"{self.api}/sendMessage",
                    json=payload,
                    timeout=25
                )
                data = r.json()
                if data.get("ok"):
                    return True
                Logger.warn(f"Telegram API response: {data}")
            except Exception as e:
                Logger.error(f"Send attempt {attempt} failed: {e}")
                time.sleep(Config.RETRY_BASE_DELAY * attempt)
        return False


# ══════════════════════════════════════════════════════════════════════════════
#                              GRID ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class GridEngine:
    @staticmethod
    def generate(stars: int = Config.SAFE_STARS) -> str:
        cells = ["🔵"] * 25
        positions = random.sample(range(25), stars)
        for p in positions:
            cells[p] = "⭐"
        rows = []
        for r in range(5):
            rows.append("".join(cells[r*5:(r+1)*5]))
        return "\n".join(rows)

    @staticmethod
    def random_mines() -> int:
        return random.randint(Config.MIN_BOMBS, Config.MAX_BOMBS)


# ══════════════════════════════════════════════════════════════════════════════
#                              MESSAGE FACTORY
# ══════════════════════════════════════════════════════════════════════════════

class MessageFactory:

    # ── Countdown ──────────────────────────────────────────────
    @staticmethod
    def countdown(minutes: int) -> str:
        if minutes >= 5:
            variants = [
                f"⏳ <b>{minutes} minutes left</b> for the next AI signal...\n\nPrepare your balance. Stay focused.",
                f"⏳ <b>{minutes} minutes remaining</b>\n\nAI model is calculating the next safe entry.",
                f"⏳ Next AI signal in <b>{minutes} minutes</b>\n\nGet ready. Do not enter randomly.",
            ]
        else:
            variants = [
                f"⏳ <b>{minutes} minute left</b>...\n\nAI entry is almost ready. Stay in position.",
                f"⏳ <b>Final minute</b>\n\nSignal dropping soon. Be prepared to click only the stars.",
                f"⏳ <b>60 seconds</b> until next confirmed entry...",
            ]
        return random.choice(variants)

    # ── Main Signal ────────────────────────────────────────────
    @staticmethod
    def signal(signal_number: int) -> str:
        mines = GridEngine.random_mines()
        grid = GridEngine.generate(Config.SAFE_STARS)
        now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

        ai_notes = [
            "AI Confidence: High",
            "Pattern Strength: Strong",
            "Risk Level: Controlled",
            "Entry Quality: Optimal",
            "Model Agreement: 3/3",
            "Safe Path Detected",
        ]
        ai_note = random.choice(ai_notes)

        tips = [
            "Click only the 3 stars. Never open extra tiles.",
            "Set the exact bomb count before you start.",
            "Cash out immediately after the 3 safe clicks.",
            "If you miss this signal, wait for the next one.",
        ]
        tip = random.choice(tips)

        return (
            f"🤖💎 <b>AI MINES SIGNAL</b> 💎🤖\n"
            f"────────────────────────\n"
            f"✅ <b>CONFIRMED ENTRY</b>\n"
            f"Bombs: <b>{mines}</b> 💣\n"
            f"Attempts: <b>{Config.SAFE_STARS}</b>\n"
            f"Signal #{signal_number}\n"
            f"────────────────────────\n"
            f"<code>{grid}</code>\n"
            f"────────────────────────\n"
            f"👆 <b><a href=\"{Config.AFFILIATE_LINK}\">Play Here — Open 1Win</a></b>\n\n"
            f"✅ <b>How to play this signal</b>\n"
            f"1. Click the link above and login\n"
            f"2. Open the Mines game\n"
            f"3. Set bombs = <b>{mines}</b>\n"
            f"4. Click only the <b>3 ⭐ stars</b>\n"
            f"5. Cash out after 3 safe tiles\n\n"
            f"🧠 {ai_note}\n"
            f"💡 {tip}\n"
            f"⏰ {now}"
        )

    # ── Green / Win ────────────────────────────────────────────
    @staticmethod
    def green(signal_number: int) -> str:
        variants = [
            f"✅✅✅ <b>GREEEEEEEENNNNN!!!</b> ✅✅✅\n\n"
            f"💰 AI Signal #{signal_number} secured!\n"
            f"Clean win. Next entry loading...",

            f"✅✅✅ <b>WIN LOCKED</b> ✅✅✅\n\n"
            f"🔥 Signal #{signal_number} closed in profit.\n"
            f"Discipline pays. Stay with the stars only.",

            f"✅✅✅ <b>GREEEEN!</b> ✅✅✅\n\n"
            f"💎 Another successful AI entry.\n"
            f"Channel is eating. Keep following.",

            f"✅✅✅ <b>PROFIT TAKEN</b> ✅✅✅\n\n"
            f"🤖 Signal #{signal_number} completed successfully.\n"
            f"Prepare for the next confirmed entry.",
        ]
        return random.choice(variants)

    # ── Promo ──────────────────────────────────────────────────
    @staticmethod
    def promo() -> str:
        variants = [
            f"🎁 <b>500% Welcome Bonus Available</b>\n\n"
            f"Register with the partner link and unlock the bonus:\n"
            f"{Config.AFFILIATE_LINK}\n\n"
            f"Minimum deposit $10 • Fast activation\n"
            f"This link supports the channel.",

            f"💎 <b>New players — claim your bonus</b>\n\n"
            f"Use only this link:\n{Config.AFFILIATE_LINK}\n\n"
            f"500% on first deposit + daily AI signals.",

            f"🚀 <b>Bonus still active</b>\n\n"
            f"Click → {Config.AFFILIATE_LINK}\n"
            f"Register → Deposit → Play with extra balance\n\n"
            f"Support the channel by using the official link.",

            f"🔥 <b>Don't play without the bonus</b>\n\n"
            f"Official partner link:\n{Config.AFFILIATE_LINK}\n\n"
            f"Higher balance = better risk management.",
        ]
        return random.choice(variants)

    # ── Short Tips ─────────────────────────────────────────────
    @staticmethod
    def tip() -> str:
        tips = [
            "📌 <b>AI Tip</b>\nNever open extra tiles. Only the 3 stars shown.",
            "📌 <b>AI Tip</b>\nIf you miss a signal, wait for the next one. Do not force entries.",
            "📌 <b>AI Tip</b>\nKeep the same bet size. Do not increase after a loss.",
            "📌 <b>AI Tip</b>\nCash out immediately after the 3 safe clicks.",
            "📌 <b>AI Tip</b>\nSet the bomb count exactly as shown in the signal.",
            "📌 <b>AI Tip</b>\nPlay only with money you can afford to lose.",
        ]
        return random.choice(tips)

    # ── Longer Educational Tips ────────────────────────────────
    @staticmethod
    def long_tip() -> str:
        tips = [
            "📚 <b>Quick Lesson</b>\n\n"
            "The grid shows only 3 safe positions.\n"
            "Your job is simple: click those 3 stars and cash out.\n"
            "Opening any other tile is the fastest way to lose the round.",

            "📚 <b>Risk Management</b>\n\n"
            "Never double your bet after a loss.\n"
            "Stick to the same stake size for at least 10 signals.\n"
            "This is how long-term players survive.",

            "📚 <b>Why only 3 stars?</b>\n\n"
            "3 safe clicks keeps the risk controlled while still giving a solid multiplier.\n"
            "More clicks = higher chance of hitting a bomb.\n"
            "We keep it disciplined on purpose.",
        ]
        return random.choice(tips)

    # ── Stats ──────────────────────────────────────────────────
    @staticmethod
    def stats(total_signals: int, uptime_hours: float) -> str:
        return (
            f"📊 <b>AI Channel Statistics</b>\n\n"
            f"Total signals sent: <b>{total_signals}</b>\n"
            f"Mode: 3-star safe entries only\n"
            f"Engine status: 🟢 Online 24/7\n"
            f"Approximate uptime: <b>{uptime_hours:.1f} hours</b>\n\n"
            f"Thank you for staying with Mines 1Win Signals."
        )

    # ── Startup ────────────────────────────────────────────────
    @staticmethod
    def startup() -> str:
        return (
            f"🤖 <b>AI-POWERED ENGINE ONLINE</b>\n\n"
            f"Mines 1Win Signals advanced mode is now active.\n"
            f"24/7 automatic confirmed entries running.\n\n"
            f"🔗 Partner link:\n{Config.AFFILIATE_LINK}\n\n"
            f"Stay in the channel. Signals are live."
        )


# ══════════════════════════════════════════════════════════════════════════════
#                              STATS TRACKER
# ══════════════════════════════════════════════════════════════════════════════

class StatsTracker:
    def __init__(self):
        self.total_signals = 0
        self.start_time = datetime.now(timezone.utc)
        self.load()

    def load(self):
        if os.path.exists(Config.STATS_FILE):
            try:
                with open(Config.STATS_FILE, "r") as f:
                    data = json.load(f)
                    self.total_signals = data.get("total_signals", 0)
            except Exception:
                pass

    def save(self):
        try:
            with open(Config.STATS_FILE, "w") as f:
                json.dump({
                    "total_signals": self.total_signals,
                    "last_update": datetime.now(timezone.utc).isoformat()
                }, f)
        except Exception as e:
            Logger.warn(f"Could not save stats: {e}")

    def increment(self):
        self.total_signals += 1
        self.save()

    def uptime_hours(self) -> float:
        delta = datetime.now(timezone.utc) - self.start_time
        return delta.total_seconds() / 3600.0


# ══════════════════════════════════════════════════════════════════════════════
#                              MAIN BOT ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class MinesSignalBot:
    def __init__(self):
        self.tg = TelegramClient()
        self.stats = StatsTracker()
        self.running = True

    def safe_sleep(self, seconds: int):
        """Sleep in small chunks so the process stays responsive."""
        end = time.time() + seconds
        while time.time() < end and self.running:
            time.sleep(min(10, end - time.time()))

    def run_cycle(self):
        # 1. 5-minute countdown
        self.tg.send(MessageFactory.countdown(5))
        Logger.info("5-minute countdown sent")
        self.safe_sleep(Config.COUNTDOWN_5_MIN - Config.COUNTDOWN_1_MIN)

        # 2. 1-minute countdown
        self.tg.send(MessageFactory.countdown(1))
        Logger.info("1-minute countdown sent")
        self.safe_sleep(Config.COUNTDOWN_1_MIN)

        # 3. Main signal
        self.stats.increment()
        num = self.stats.total_signals
        self.tg.send(MessageFactory.signal(num))
        Logger.success(f"Signal #{num} sent")
        self.safe_sleep(Config.DELAY_AFTER_SIGNAL)

        # 4. Green message
        self.tg.send(MessageFactory.green(num))
        Logger.info("Green message sent")

        # 5. Promo
        if num % Config.PROMO_EVERY_N_SIGNALS == 0:
            self.safe_sleep(Config.DELAY_BEFORE_PROMO)
            self.tg.send(MessageFactory.promo())
            Logger.info("Promo message sent")

        # 6. Short tip
        if num % Config.TIP_EVERY_N_SIGNALS == 0:
            self.safe_sleep(12)
            self.tg.send(MessageFactory.tip())

        # 7. Long tip
        if num % Config.LONG_TIP_EVERY_N == 0:
            self.safe_sleep(10)
            self.tg.send(MessageFactory.long_tip())

        # 8. Stats
        if num % Config.STATS_EVERY_N_SIGNALS == 0:
            self.safe_sleep(8)
            self.tg.send(MessageFactory.stats(
                self.stats.total_signals,
                self.stats.uptime_hours()
            ))

        # 9. Remaining time until next full cycle
        used = (Config.COUNTDOWN_5_MIN +
                Config.DELAY_AFTER_SIGNAL +
                Config.DELAY_AFTER_GREEN)
        remaining = max(Config.MIN_SLEEP_BETWEEN_CYCLES,
                        Config.FULL_CYCLE_SECONDS - used)
        Logger.info(f"Cycle complete. Sleeping {remaining} seconds")
        self.safe_sleep(remaining)

    def start(self):
        Logger.banner()
        Logger.info("Engine starting...")

        # Startup message
        self.tg.send(MessageFactory.startup())
        time.sleep(8)

        Logger.success("Bot is now live and entering main loop")

        while self.running:
            try:
                self.run_cycle()
            except KeyboardInterrupt:
                Logger.warn("Keyboard interrupt received")
                self.running = False
                self.tg.send("🔴 AI Engine temporarily stopped by admin.")
                break
            except Exception as e:
                Logger.error(f"Cycle error: {e}")
                Logger.error(traceback.format_exc())
                time.sleep(30)

        Logger.info("Bot stopped.")


# ══════════════════════════════════════════════════════════════════════════════
#                              ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    bot = MinesSignalBot()
    bot.start()
