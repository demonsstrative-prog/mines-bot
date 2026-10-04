# grid.py
# Mines Grid Engine — always exactly 3 safe stars

import random
from config import SAFE_STARS, MIN_BOMBS, MAX_BOMBS

def make_grid(stars: int = SAFE_STARS) -> str:
    """
    Generate a 5x5 grid.
    Exactly `stars` positions are marked as safe (⭐).
    All other positions are 🔵.
    """
    cells = ["🔵"] * 25
    safe_positions = random.sample(range(25), stars)
    for pos in safe_positions:
        cells[pos] = "⭐"

    rows = []
    for r in range(5):
        row = "".join(cells[r*5 : (r+1)*5])
        rows.append(row)
    return "\n".join(rows)

def random_mines() -> int:
    """Return a random bomb count between MIN_BOMBS and MAX_BOMBS."""
    return random.randint(MIN_BOMBS, MAX_BOMBS)

def get_mines_signal_data():
    """
    Return everything needed for one Mines signal.
    """
    mines = random_mines()
    grid = make_grid(SAFE_STARS)
    return {
        "mines": mines,
        "stars": SAFE_STARS,
        "grid": grid
    }
