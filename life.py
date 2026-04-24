import os
import random
import shutil
import time
import json

from load_icons import get_icons

def get_size():
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, size.lines - 1

def make_grid(w, h, fill_random=True):
    if fill_random:
        return [[random.choice((0, 1)) for _ in range(w)] for _ in range(h)]
    return [[0 for _ in range(w)] for _ in range(h)]

def resize_grid(grid, new_w, new_h):
    old_h = len(grid)
    old_w = len(grid[0]) if old_h else 0

    new_grid = [[0 for _ in range(new_w)] for _ in range(new_h)]

    for y in range(min(old_h, new_h)):
        for x in range(min(old_w, new_w)):
            new_grid[y][x] = grid[y][x]

    # Optional: sprinkle randomness into newly exposed area
    for y in range(new_h):
        for x in range(new_w):
            if y >= old_h or x >= old_w:
                new_grid[y][x] = random.choice((0, 1, 0, 0, 0))

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
    print("\x1b[H", end="")  # move cursor to top-left
    for row in grid:
        print("".join(icon if cell else " " for cell in row))

def run(iterations=1000, icon="x"):
    w, h = get_size()
    grid = make_grid(w, h)
    duration = 0
    
    while True:
        new_w, new_h = get_size()
        if (new_w, new_h) != (w, h):
            grid = resize_grid(grid, new_w, new_h)
            w, h = new_w, new_h

        draw(grid, icon)
        grid = step(grid)
        duration += 1
        if duration > iterations:
            duration = 0
            break
        time.sleep(0.08)

def main():
    icons = get_icons()
    try:
        while True:
            print("\x1b[2J", end="")   # clear screen once
            print("\x1b[?25l", end="") # hide cursor
            icon = random.choice(icons)
            run(10000, icon)
    except KeyboardInterrupt:
        pass
    finally:
        print("\x1b[?25h", end="") # show cursor
        print("\x1b[0m")           # reset termina

if __name__ == "__main__":
    main()

