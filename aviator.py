# aviator.py
# Low-Risk Crash Game Engine (Aviator / LuckyJet / JetX style)

import random
from config import AVIATOR_MIN, AVIATOR_MAX

def generate_low_risk_target() -> float:
    """
    Generate a safe low-risk cashout target.
    Focused on high probability small multipliers.
    """
    # Weighted towards safer (lower) values
    weights = [0.35, 0.30, 0.20, 0.10, 0.05]
    ranges = [
        (1.35, 1.55),
        (1.55, 1.75),
        (1.75, 1.95),
        (1.95, 2.10),
        (2.10, 2.25),
    ]
    
    chosen_range = random.choices(ranges, weights=weights, k=1)[0]
    target = round(random.uniform(chosen_range[0], chosen_range[1]), 2)
    
    # Hard limits
    target = max(AVIATOR_MIN, min(AVIATOR_MAX, target))
    return target

def get_aviator_signal_data():
    """
    Return data for one low-risk crash signal.
    """
    target = generate_low_risk_target()
    confidence = random.randint(72, 91)
    
    return {
        "target": target,
        "confidence": confidence,
        "style": "low-risk"
    }

def format_target(target: float) -> str:
    return f"{target:.2f}x"
