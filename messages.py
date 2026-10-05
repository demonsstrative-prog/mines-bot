# messages.py — AI Engine v4 Messages

import random
from datetime import datetime, timezone
from config import AFFILIATE, PROMO_CODE, MIN_DEPOSIT, SAFE_STARS

def warning() -> str:
    return (
        f"⚠️ <b>WARNING</b>\n"
        f"Signals only work if you registered with promo code <b>{PROMO_CODE}</b> "
        f"and deposited at least {MIN_DEPOSIT}.\n"
        f"Without the promo code the entry is not valid."
    )

def countdown(mins: int) -> str:
    if mins >= 4:
        opts = [
            f"⏳ <b>{mins} minutes left</b> for next AI signal...\n\nPrepare balance.",
            f"⏳ Next signal in <b>{mins} minutes</b>\n\nStay ready.",
        ]
    else:
        opts = [
            f"⏳ <b>{mins} minute left</b>...\n\nSignal loading.",
            f"⏳ <b>Final seconds</b>\n\nGet ready.",
        ]
    return random.choice(opts)

def mines_signal(num: int, data: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%H:%M UTC")
    mode = data.get("mode", "safe").upper()
    return (
        f"🤖💎 <b>AI MINES SIGNAL</b> 💎🤖\n"
        f"────────────────────\n"
        f"✅ <b>CONFIRMED ENTRY</b>\n"
        f"Mode: <b>{mode}</b>\n"
        f"Bombs: <b>{data['mines']}</b> 💣\n"
        f"Attempts: <b>{data['stars']}</b>\n"
        f"Signal #{num}\n"
        f"────────────────────\n"
        f"<code>{data['grid']}</code>\n"
        f"────────────────────\n"
        f"👆 <b><a href=\"{AFFILIATE}\">Play Here — Open 1Win</a></b>\n\n"
        f"✅ <b>How to play</b>\n"
        f"1. Register with the link\n"
        f"2. Promo code: <b>{PROMO_CODE}</b>\n"
        f"3. Deposit min {MIN_DEPOSIT}\n"
        f"4. Open Mines → bombs = <b>{data['mines']}</b>\n"
        f"5. Click only the <b>3 ⭐</b>\n"
        f"6. Cash out\n\n"
        f"{warning()}\n\n"
        f"⏰ {now}"
    )

def crash_signal(num: int, data: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%H:%M UTC")
    mode = data.get("mode", "safe").upper()
    return (
        f"✈️💎 <b>AI {data['game'].upper()} SIGNAL</b> 💎✈️\n"
        f"────────────────────\n"
        f"✅ <b>LOW-RISK ENTRY</b>\n"
        f"Mode: <b>{mode}</b>\n"
        f"Target: <b>{data['target']:.2f}x</b>\n"
        f"Confidence: <b>{data['confidence']}%</b>\n"
        f"Signal #{num}\n"
        f"────────────────────\n"
        f"👆 <b><a href=\"{AFFILIATE}\">Play Here — Open 1Win</a></b>\n\n"
        f"✅ <b>How to play</b>\n"
        f"1. Register with the link\n"
        f"2. Promo code: <b>{PROMO_CODE}</b>\n"
        f"3. Deposit min {MIN_DEPOSIT}\n"
        f"4. Open {data['game']}\n"
        f"5. Cash out at <b>{data['target']:.2f}x</b>\n\n"
        f"{warning()}\n\n"
        f"⏰ {now}"
    )

def green(num: int, game: str = "MINES") -> str:
    opts = [
        f"✅✅✅ <b>GREEEEEEEENNNNN!!!</b> ✅✅✅\n\n💰 {game} Signal #{num} secured!",
        f"✅✅✅ <b>WIN LOCKED</b> ✅✅✅\n\n🔥 Signal #{num} closed successfully.",
        f"✅✅✅ <b>GREEEEN!</b> ✅✅✅\n\n💎 Clean low-risk entry.",
    ]
    return random.choice(opts)

def promo() -> str:
    return (
        f"🎁 <b>IMPORTANT</b>\n\n"
        f"Signals only work if you:\n\n"
        f"1. Register → {AFFILIATE}\n"
        f"2. Use promo code <b>{PROMO_CODE}</b>\n"
        f"3. Deposit minimum <b>{MIN_DEPOSIT}</b>\n\n"
        f"Without this, signals are not valid for your account."
    )

def tip() -> str:
    tips = [
        "📌 <b>Tip</b>\nOnly click the 3 stars on Mines.",
        "📌 <b>Tip</b>\nOn crash games cash out at the exact target.",
        "📌 <b>Tip</b>\nNever increase bet after a loss.",
        f"📌 <b>Tip</b>\nPromo <b>{PROMO_CODE}</b> + {MIN_DEPOSIT} is mandatory.",
    ]
    return random.choice(tips)

def stats(total, mines, crash, mode, intensity) -> str:
    return (
        f"📊 <b>AI Engine Stats</b>\n\n"
        f"Total signals: <b>{total}</b>\n"
        f"Mines: <b>{mines}</b> | Crash: <b>{crash}</b>\n"
        f"Mode: <b>{mode.upper()}</b>\n"
        f"Intensity: <b>{intensity.upper()}</b>\n"
        f"Status: 🟢 Online 24/7\n\n"
        f"⚠️ {PROMO_CODE} + {MIN_DEPOSIT} required"
    )

def startup(mode: str, intensity: str) -> str:
    return (
        f"🤖 <b>AI ENGINE v4 ONLINE</b>\n\n"
        f"Low-Risk Automatic Engine started.\n"
        f"Mode: <b>{mode.upper()}</b>\n"
        f"Intensity: <b>{intensity.upper()}</b>\n\n"
        f"⚠️ Promo <b>{PROMO_CODE}</b> + {MIN_DEPOSIT} required\n\n"
        f"🔗 {AFFILIATE}"
    )
