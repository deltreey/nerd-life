from pathlib import Path
from urllib.request import urlretrieve
import json

GLYPH_URL = "https://raw.githubusercontent.com/ryanoasis/nerd-fonts/master/glyphnames.json"
CACHE_DIR = Path.home() / ".cache" / "nerd-life"
GLYPH_FILE = CACHE_DIR / "glyphnames.json"

def ensure_glyph_file(refresh=False):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if refresh or not GLYPH_FILE.exists():
        urlretrieve(GLYPH_URL, GLYPH_FILE)

    return GLYPH_FILE

def get_icons(refresh=False):
    glyph_file = ensure_glyph_file(refresh)

    with open(glyph_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.pop("METADATA", None)

    return [
        entry["char"]
        for entry in data.values()
        if isinstance(entry, dict) and entry.get("char")
    ]
