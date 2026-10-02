#!/usr/bin/env python3
"""
Mines 1Win Signals — Advanced 24/7 Channel Bot
------------------------------------------------
- Continuous countdown + signal + green cycle
- Always 3 safe stars (Attempts: 3)
- Affiliate link on every signal
- Rotating promo messages
- Multiple message styles
- Auto recovery on errors
- Detailed logging
"""

import requests
import random
import time
import sys
from datetime import datetime, timezone, timedelta

# ═══════════════════════════════════════════════════════════════
#                        CONFIGURATION
# ═══════════════════════════════════════════════════════════════

BOT_TOKEN   = "8702447245:AAH9tm7f2rqppiziufL2CUeZWe7n14uYZEE"
CHANNEL_ID  = "-1004331688852"
AFFILIATE   = "https://lkql.cc/6ac160"

# Timing (in seconds)
SIGNAL_INTERVAL     = 8 * 60        # full cycle every 8 minutes
COUNTDOWN_5_MIN     = 5 * 60
COUNTDOWN_1_MIN     = 60
AFTER_SIGNAL_DELAY  = 35
AFTER_GREEN_DELAY   = 20
PROMO_EVERY_N       = 3             # send promo every N signals

# Grid settings
SAFE_STARS          = 3             # always 3 safe clicks
MIN_MINES           = 3
MAX_MINES           = 5

# ═══════════════════════════════════════════════════════════════
#                        TELEGRAM CORE
# ═══════════════════════════════════════════════════════════════

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def send(text: str, disable_preview: bool = False) -> bool:
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_preview
    }
    for attempt in range(1, 4):
        try:
            r = requests.post(f"{API}/sendMessage", json=payload, timeout=20)
            data = r.json()
            if data.get("ok"):
                return True
            log(f"Telegram error: {data}")
        except Exception as e:
            log(f"Send failed (try {attempt}): {e}")
            time.sleep(2 * attempt)
    return False

# ═══════════════════════════════════════════════════════════════
#                        GRID GENERATOR
# ═══════════════════════════════════════════════════════════════

def generate_grid(stars: int = SAFE_STARS) -> str:
    """Create 5x5 grid with exactly `stars` safe positions."""
    cells = ["🔵"] * 25
    positions = random.sample(range(25), stars)
    for pos in positions:
        cells[pos] = "⭐"
    rows = []
    for r in range(5):
        rows.append("".join(cells[r*5 : (r+1)*5]))
    return "\n".join(rows)

# ═══════════════════════════════════════════════════════════════
#                        MESSAGE TEMPLATES
# ═══════════════════════════════════════════════════════════════

def msg_countdown(minutes: int) -> str:
    if minutes >= 5:
        return (
            f"⏳ <b>{minutes} minutes left</b> for the next signal...\n\n"
            f"Get ready. Prepare your balance."
        )
    return (
        f"⏳ <b>{minutes} minute left</b> for the next signal...\n\n"
        f"Almost time. Stay focused."
    )

def msg_signal(signal_number: int) -> str:
    mines = random.randint(MIN_MINES, MAX_MINES)
    grid = generate_grid(SAFE_STARS)
    now = datetime.now(timezone.utc).strftime("%H:%M UTC")

    tips = [
        "Click only the stars. Do not open any other tile.",
        "Set the exact bomb count shown above before starting.",
        "Cash out immediately after the 3 safe clicks.",
        "Never chase after a loss. Wait for the next signal.",
    ]
    tip = random.choice(tips)

    return (
        f"💣💎 <b>Mines 1Win Signals</b> 💎💣\n"
        f"────────────────────\n"
        f"✅ <b>CONFIRMED ENTRY</b>\n"
        f"Bombs: <b>{mines}</b> 💣\n"
        f"Attempts: <b>{SAFE_STARS}</b>\n"
        f"Signal #{signal_number}\n"
        f"────────────────────\n"
        f"<code>{grid}</code>\n"
        f"────────────────────\n"
        f"👆 <b><a href=\"{AFFILIATE}\">Play Here — Open 1Win</a></b>\n\n"
        f"✅ <b>How to play this signal</b>\n"
        f"1. Click the link above & login\n"
        f"2. Go to Mines game\n"
        f"3. Set bombs = <b>{mines}</b>\n"
        f"4. Click only the <b>3 ⭐ stars</b>\n"
        f"5. Cash out after 3 safe tiles\n\n"
        f"💡 {tip}\n\n"
        f"⏰ {now}"
    )

def msg_green(signal_number: int) -> str:
    variants = [
        f"✅✅✅ <b>GREEEEEEEENNNNN!!!</b> ✅✅✅\n\n"
        f"💰 Signal #{signal_number} secured!\n"
        f"Another clean win. Stay with us.",

        f"✅✅✅ <b>GREEEEN!</b> ✅✅✅\n\n"
        f"🔥 Perfect entry.\n"
        f"Next signal coming soon. Get ready.",

        f"✅✅✅ <b>WIN SECURED</b> ✅✅✅\n\n"
        f"💎 Signal #{signal_number} closed in profit.\n"
        f"Keep following the stars only.",
    ]
    return random.choice(variants)

def msg_promo() -> str:
    variants = [
        f"🎁 <b>500% First Deposit Bonus</b>\n\n"
        f"Register with my partner link and unlock the bonus:\n"
        f"{AFFILIATE}\n\n"
        f"Minimum deposit $10 to activate.\n"
        f"Fast withdrawals • Daily signals",

        f"💎 <b>Don't play without the bonus</b>\n\n"
        f"Use this link to get up to 500% on your first deposit:\n"
        f"{AFFILIATE}\n\n"
        f"This is the only link that supports the channel.",

        f"🚀 <b>New players bonus still available</b>\n\n"
        f"Click → {AFFILIATE}\n"
        f"Register → Deposit → Activate 500% bonus\n\n"
        f"Then come back and follow the live signals.",
    ]
    return random.choice(variants)

def msg_tip() -> str:
    tips = [
        "📌 <b>Pro tip</b>\nNever increase bet size after a loss. Stick to the signal.",
        "📌 <b>Pro tip</b>\nOnly click the 3 stars shown. Opening extra tiles is the fastest way to lose.",
        "📌 <b>Pro tip</b>\nWait for the next confirmed entry if you missed the current one.",
        "📌 <b>Pro tip</b>\nPlay only with money you can afford to lose. Signals are guidance, not guarantees.",
    ]
    return random.choice(tips)

def msg_stats(total_signals: int) -> str:
    return (
        f"📊 <b>Channel Stats</b>\n\n"
        f"Total signals sent: <b>{total_signals}</b>\n"
        f"Mode: 3 safe stars only\n"
        f"Status: 🟢 Online 24/7\n\n"
        f"Thank you for staying with Mines 1Win Signals."
    )

# ═══════════════════════════════════════════════════════════════
#                        MAIN LOOP
# ═══════════════════════════════════════════════════════════════

def main():
    log("=" * 50)
    log("Mines 1Win Signals — Advanced Channel Bot")
    log(f"Channel : {CHANNEL_ID}")
    log(f"Affiliate: {AFFILIATE}")
    log(f"Stars   : {SAFE_STARS} safe clicks every signal")
    log("=" * 50)

    # startup message
    send(
        "🟢 <b>Bot is online</b>\n\n"
        "24/7 Mines signals starting now.\n"
        f"Affiliate: {AFFILIATE}"
    )

    signal_count = 0

    while True:
        try:
            # ── 5 minute countdown
            send(msg_countdown(5))
            log("Sent 5-min countdown")
            time.sleep(COUNTDOWN_5_MIN - COUNTDOWN_1_MIN)

            # ── 1 minute countdown
            send(msg_countdown(1))
            log("Sent 1-min countdown")
            time.sleep(COUNTDOWN_1_MIN)

            # ── Main signal
            signal_count += 1
            send(msg_signal(signal_count))
            log(f"Signal #{signal_count} sent")

            time.sleep(AFTER_SIGNAL_DELAY)

            # ── Green / win message
            send(msg_green(signal_count))
            log("Green message sent")

            # ── Promo every N signals
            if signal_count % PROMO_EVERY_N == 0:
                time.sleep(AFTER_GREEN_DELAY)
                send(msg_promo())
                log("Promo message sent")

            # ── Occasional tip
            if signal_count % 5 == 0:
                time.sleep(15)
                send(msg_tip())

            # ── Occasional stats
            if signal_count % 10 == 0:
                time.sleep(10)
                send(msg_stats(signal_count))

            # ── Wait remaining time until next full cycle
            elapsed = (COUNTDOWN_5_MIN + AFTER_SIGNAL_DELAY + AFTER_GREEN_DELAY)
            remaining = max(30, SIGNAL_INTERVAL - elapsed)
            log(f"Sleeping {remaining}s until next cycle")
            time.sleep(remaining)

        except KeyboardInterrupt:
            log("Stopped by user")
            send("🔴 Bot temporarily stopped.")
            break
        except Exception as e:
            log(f"Loop error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
