# crash.py — Low-Risk Crash Engine (Aviator / LuckyJet / JetX)

import random
from config import CRASH_MIN, CRASH_MAX

def generate_target(mode: str = "safe") -> float:
    if mode == "safe":
        # Very conservative
        target = round(random.uniform(1.32, 1.68), 2)
    else:
        # Normal low-risk
        target = round(random.uniform(1.45, 2.05), 2)

    target = max(CRASH_MIN, min(CRASH_MAX, target))
    return target

def get_crash_data(mode: str = "safe"):
    target = generate_target(mode)
    confidence = random.randint(74, 93) if mode == "safe" else random.randint(68, 88)
    games = ["Aviator", "LuckyJet", "JetX"]
    game = random.choice(games)
    return {
        "target": target,
        "confidence": confidence,
        "game": game,
        "mode": mode
    }
