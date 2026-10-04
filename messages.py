# messages.py
import random
from datetime import datetime, timezone
from config import AFFILIATE, SAFE_STARS

PROMO_CODE = "ALLEYSIGNALS"
MIN_DEPOSIT = "$3"

def countdown(mins: int) -> str:
    if mins >= 5:
        options = [
            f"⏳ <b>{mins} minutes left</b> for the next signal...\n\nPrepare your balance.",
            f"⏳ Next entry in <b>{mins} minutes</b>\n\nStay ready.",
            f"⏳ <b>{mins} minutes remaining</b>\n\nGet in position.",
        ]
    else:
        options = [
            f"⏳ <b>{mins} minute left</b>...\n\nSignal loading.",
            f"⏳ <b>Final minute</b>\n\nBe ready to follow the stars only.",
            f"⏳ <b>60 seconds</b> until next entry...",
        ]
    return random.choice(options)

def signal(num: int, mines: int, grid: str) -> str:
    now = datetime.now(timezone.utc).strftime("%H:%M UTC")
    notes = [
        "Pattern strength: Strong",
        "Entry quality: High",
        "Risk level: Controlled",
        "Model agreement: Positive",
    ]
    note = random.choice(notes)

    return (
        f"🤖💎 <b>MINES SIGNAL</b> 💎🤖\n"
        f"────────────────────\n"
        f"✅ <b>CONFIRMED ENTRY</b>\n"
        f"Bombs: <b>{mines}</b> 💣\n"
        f"Attempts: <b>{SAFE_STARS}</b>\n"
        f"Signal #{num}\n"
        f"────────────────────\n"
        f"<code>{grid}</code>\n"
        f"────────────────────\n"
        f"👆 <b><a href=\"{AFFILIATE}\">Play Here — Open 1Win</a></b>\n\n"
        f"✅ <b>How to play</b>\n"
        f"1. Click the link & register\n"
        f"2. Enter promo code: <b>{PROMO_CODE}</b>\n"
        f"3. Deposit minimum {MIN_DEPOSIT}\n"
        f"4. Open Mines → set bombs = <b>{mines}</b>\n"
        f"5. Click only the <b>3 ⭐ stars</b>\n"
        f"6. Cash out\n\n"
        f"🧠 {note}\n\n"
        f"⚠️ <b>WARNING</b>\n"
        f"Signals only work if you registered with promo code <b>{PROMO_CODE}</b> "
        f"and deposited at least {MIN_DEPOSIT}.\n"
        f"Without the promo code the entry is not valid.\n\n"
        f"⏰ {now}"
    )

def green(num: int) -> str:
    options = [
        f"✅✅✅ <b>GREEEEEEEENNNNN!!!</b> ✅✅✅\n\n💰 Signal #{num} secured!\nNext one loading...",
        f"✅✅✅ <b>WIN LOCKED</b> ✅✅✅\n\n🔥 Signal #{num} closed.\nStay disciplined.",
        f"✅✅✅ <b>GREEEEN!</b> ✅✅✅\n\n💎 Clean entry.\nFollow the next signal.",
    ]
    return random.choice(options)

def promo() -> str:
    return (
        f"🎁 <b>IMPORTANT — READ THIS</b>\n\n"
        f"To receive working signals you MUST:\n\n"
        f"1. Register with this link:\n{AFFILIATE}\n\n"
        f"2. Enter promo code: <b>{PROMO_CODE}</b>\n\n"
        f"3. Deposit minimum <b>{MIN_DEPOSIT}</b>\n\n"
        f"Without the promo code + {MIN_DEPOSIT} deposit, signals will not work for your account.\n\n"
        f"Do it once and all future signals become active."
    )

def tip() -> str:
    tips = [
        "📌 <b>Tip</b>\nOnly click the 3 stars. Never open extra tiles.",
        "📌 <b>Tip</b>\nIf you miss a signal, wait for the next one.",
        "📌 <b>Tip</b>\nKeep the same bet size. Do not chase losses.",
        "📌 <b>Tip</b>\nCash out immediately after the 3 safe clicks.",
        f"📌 <b>Tip</b>\nMake sure you used promo code <b>{PROMO_CODE}</b> or signals won’t work.",
    ]
    return random.choice(tips)

def stats(total: int) -> str:
    return (
        f"📊 <b>Channel Stats</b>\n\n"
        f"Total signals: <b>{total}</b>\n"
        f"Mode: 3-star entries\n"
        f"Status: 🟢 Online 24/7\n\n"
        f"⚠️ Remember: Promo code <b>{PROMO_CODE}</b> + {MIN_DEPOSIT} required."
    )

def startup() -> str:
    return (
        f"🤖 <b>ENGINE ONLINE</b>\n\n"
        f"Mines 1Win Signals is now running.\n"
        f"24/7 automatic entries active.\n\n"
        f"⚠️ Signals only work with promo code <b>{PROMO_CODE}</b> + minimum {MIN_DEPOSIT} deposit.\n\n"
        f"🔗 {AFFILIATE}"
    )
