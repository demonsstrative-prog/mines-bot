# messages.py
# All message templates + strong ALLEYSIGNALS warning system

import random
from datetime import datetime, timezone
from config import AFFILIATE, PROMO_CODE, MIN_DEPOSIT, SAFE_STARS

def _warning_block() -> str:
    return (
        f"⚠️ <b>WARNING</b>\n"
        f"Signals only work if you registered with promo code <b>{PROMO_CODE}</b> "
        f"and deposited at least {MIN_DEPOSIT}.\n"
        f"Without the promo code the entry is not valid."
    )

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
            f"⏳ <b>Final minute</b>\n\nBe ready.",
            f"⏳ <b>60 seconds</b> until next entry...",
        ]
    return random.choice(options)

def mines_signal(num: int, mines: int, grid: str) -> str:
    now = datetime.now(timezone.utc).strftime("%H:%M UTC")
    notes = [
        "Low-risk pattern detected",
        "Safe entry zone identified",
        "Controlled risk profile",
        "High probability path",
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
        f"{_warning_block()}\n\n"
        f"⏰ {now}"
    )

def aviator_signal(num: int, target: float, confidence: int) -> str:
    now = datetime.now(timezone.utc).strftime("%H:%M UTC")
    return (
        f"✈️💎 <b>AVIATOR / CRASH SIGNAL</b> 💎✈️\n"
        f"────────────────────\n"
        f"✅ <b>LOW-RISK ENTRY</b>\n"
        f"Target: <b>{target:.2f}x</b>\n"
        f"Confidence: <b>{confidence}%</b>\n"
        f"Signal #{num}\n"
        f"────────────────────\n"
        f"👆 <b><a href=\"{AFFILIATE}\">Play Here — Open 1Win</a></b>\n\n"
        f"✅ <b>How to play</b>\n"
        f"1. Click the link & register\n"
        f"2. Enter promo code: <b>{PROMO_CODE}</b>\n"
        f"3. Deposit minimum {MIN_DEPOSIT}\n"
        f"4. Open Aviator / LuckyJet / JetX\n"
        f"5. Cash
