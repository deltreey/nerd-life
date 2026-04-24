import argparse
import json
import random
import shutil
import time
from pathlib import Path
from urllib.request import urlretrieve


GLYPH_URL = "https://raw.githubusercontent.com/ryanoasis/nerd-fonts/master/glyphnames.json"
CACHE_DIR = Path.home() / ".cache" / "nerd-life"
GLYPH_FILE = CACHE_DIR / "glyphnames.json"

BLOCK_ICONS = ["█", "▓", "▒", "░", "#", "@", "*", "x"]


def ensure_glyph_file(refresh=False):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if refresh or not GLYPH_FILE.exists():
        urlretrieve(GLYPH_URL, GLYPH_FILE)

    return GLYPH_FILE


def get_nerd_icons(refresh=False):
    glyph_file = ensure_glyph_file(refresh)

    with open(glyph_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.pop("METADATA", None)

    return [
        entry["char"]
        for entry in data.values()
        if isinstance(entry, dict) and entry.get("char")
    ]


def get_icons(icon_mode, refresh=False):
    if icon_mode == "nerd":
        return get_nerd_icons(refresh)

    if icon_mode == "blocks":
        return BLOCK_ICONS

    if icon_mode == "plain":
        return ["x"]

    raise ValueError(f"unknown icon mode: {icon_mode}")


def get_size():
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, max(1, size.lines - 1)


def make_grid(w, h, density=0.3):
    return [
        [1 if random.random() < density else 0 for _ in range(w)]
        for _ in range(h)
    ]


def resize_grid(grid, new_w, new_h, density=0.05):
    old_h = len(grid)
    old_w = len(grid[0]) if old_h else 0

    new_grid = [[0 for _ in range(new_w)] for _ in range(new_h)]

    for y in range(min(old_h, new_h)):
        for x in range(min(old_w, new_w)):
            new_grid[y][x] = grid[y][x]

    for y in range(new_h):
        for x in range(new_w):
            if y >= old_h or x >= old_w:
                new_grid[y][x] = 1 if random.random() < density else 0

    return new_grid


def step(grid):
    h = len(grid)
    w = len(grid[0]) if h else 0
    new = [[0] * w for _ in range(h)]

    for y in range(h):
        for x in range(w):
            n = 0

            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue

                    ny = (y + dy) % h
                    nx = (x + dx) % w
                    n += grid[ny][nx]

            new[y][x] = 1 if n == 3 or (grid[y][x] and n == 2) else 0

    return new


def draw(grid, icon="x"):
    print("\x1b[H", end="")

    for row in grid:
        print("".join(icon if cell else " " for cell in row))


def run(iterations, icon, speed, density):
    w, h = get_size()
    grid = make_grid(w, h, density)
    duration = 0

    while True:
        new_w, new_h = get_size()

        if (new_w, new_h) != (w, h):
            grid = resize_grid(grid, new_w, new_h)
            w, h = new_w, new_h

        draw(grid, icon)
        grid = step(grid)

        duration += 1
        if iterations > 0 and duration >= iterations:
            break

        time.sleep(speed)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="nerd-life",
        description="Run Conway's Game of Life in your terminal with optional Nerd Font icons.",
    )

    parser.add_argument(
        "--icons",
        choices=["nerd", "blocks", "plain"],
        default="blocks",
        help="icon set to use for alive cells",
    )

    parser.add_argument(
        "--refresh-icons",
        action="store_true",
        help="download a fresh Nerd Font glyphnames.json file",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=0.08,
        help="seconds between frames",
    )

    parser.add_argument(
        "--density",
        type=float,
        default=0.3,
        help="initial alive-cell density from 0.0 to 1.0",
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=10000,
        help="frames to run before choosing a new icon; use 0 to run forever",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if not 0.0 <= args.density <= 1.0:
        raise ValueError("--density must be between 0.0 and 1.0")

    if args.speed < 0:
        raise ValueError("--speed must be non-negative")

    icons = get_icons(args.icons, refresh=args.refresh_icons)

    try:
        print("\x1b[2J", end="")
        print("\x1b[?25l", end="")

        while True:
            icon = random.choice(icons)
            run(args.iterations, icon, args.speed, args.density)

            if args.iterations == 0:
                break

    except KeyboardInterrupt:
        pass

    finally:
        print("\x1b[?25h", end="")
        print("\x1b[0m", end="")


if __name__ == "__main__":
    main()
