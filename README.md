# nerd-life

A tiny terminal toy that runs Conway's Game of Life with random per-run cell glyphs.

It can render with:
- Nerd Font icons (downloaded glyph list)
- block-style characters
- plain `x`

## Features

- Auto-fits to your terminal size
- Adapts when you resize the terminal window
- Randomly picks a glyph each run cycle for visual variety
- Optional Nerd Font glyph mode with local cache at `~/.cache/nerd-life/`
- Zero third-party Python dependencies

## Requirements

- Python 3.14+
- `uv`
- A terminal that supports ANSI escape codes
- (Optional) a Nerd Font for best results with `--icons nerd`

## Quick Start

```bash
uv run nerd_life.py
```

Stop anytime with `Ctrl+C`.

## Usage

```bash
uv run nerd_life.py [--icons {nerd,blocks,plain}] [--refresh-icons] [--speed SECONDS] [--density 0.0-1.0] [--iterations N]
```

### Options

- `--icons`: icon mode for alive cells (`blocks` default)
- `--refresh-icons`: re-download the Nerd Font glyph metadata cache
- `--speed`: seconds between frames (default: `0.08`)
- `--density`: initial live-cell density from `0.0` to `1.0` (default: `0.3`)
- `--iterations`: number of frames per cycle (default: `10000`, use `0` for endless)

## Examples

Run with block characters (default):

```bash
uv run nerd_life.py --icons blocks
```

Run forever with plain ASCII and slower updates:

```bash
uv run nerd_life.py --icons plain --iterations 0 --speed 0.12
```

Use Nerd Font icons and refresh glyph cache first:

```bash
uv run nerd_life.py --icons nerd --refresh-icons
```

## Notes

- The grid wraps at edges (toroidal world).
- The app clears the screen and hides the cursor while running, then restores it on exit.

## Roadmap Ideas

- Add a `--seed` flag for reproducible runs
- Add pattern presets (glider gun, pulsar, etc.)
- Package as an installable CLI (`pipx install ...`)

## License

Add a license file before publishing (MIT is a common choice for small utilities).
