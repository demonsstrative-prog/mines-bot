# grid.py — Mines Engine v4

import random
from config import SAFE_STARS, MIN_BOMBS, MAX_BOMBS

def make_grid(stars: int = SAFE_STARS) -> str:
    cells = ["🔵"] * 25
    for pos in random.sample(range(25), stars):
        cells[pos] = "⭐"
    return "\n".join("".join(cells[i*5:(i+1)*5]) for i in range(5))

def random_mines() -> int:
    return random.randint(MIN_BOMBS, MAX_BOMBS)

def get_mines_data(mode: str = "safe"):
    mines = random_mines()
    # In safe mode we keep stars fixed at 3
    stars = SAFE_STARS
    grid = make_grid(stars)
    return {
        "mines": mines,
        "stars": stars,
        "grid": grid,
        "mode": mode
    }
