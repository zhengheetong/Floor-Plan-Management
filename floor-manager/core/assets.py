"""
core/assets.py
Handles all sprite sheet generation logic.
Pure business logic — no Tkinter dependency.
"""

import os
import json
from PIL import Image

# ===========================================
# SPRITE SHEET GENERATION
# ===========================================

ICON_SIZE = 120
COLUMNS = 10
VALID_EXTENSIONS = {'.png', '.jpg', '.jpeg'}


def generate_sprite_sheet(sprite_dir, base_dir, floor_config):
    """
    Stitches all logos in `sprite_dir` into a single master sprite sheet.
    Updates each floor's data.json with the precise (x, y) CSS coordinates.

    Returns a tuple: (success: bool, message: str, updated_count: int)
    """
    images = [
        f for f in os.listdir(sprite_dir)
        if os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
    ]

    if not images:
        return False, "The Sprite Library is empty. Upload some logos first!", 0

    rows = (len(images) + COLUMNS - 1) // COLUMNS
    sprite_w = COLUMNS * ICON_SIZE
    sprite_h = rows * ICON_SIZE

    master_img = Image.new("RGBA", (sprite_w, sprite_h), (255, 255, 255, 0))
    logo_mapping = {}

    for idx, filename in enumerate(images):
        filepath = os.path.join(sprite_dir, filename)
        try:
            img = Image.open(filepath).convert("RGBA")
            img = img.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)

            col = idx % COLUMNS
            row = idx // COLUMNS
            x = col * ICON_SIZE
            y = row * ICON_SIZE

            master_img.paste(img, (x, y))

            name_without_ext = os.path.splitext(filename)[0].lower().strip()
            logo_mapping[name_without_ext] = {"x": x, "y": y}
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    # Save to the local public folder so the staging React app can preview it
    sprite_path = os.path.join("public", "icons-sprite.png")
    master_img.save(sprite_path)

    # Inject coordinates into each floor's data.json
    updated_count = 0
    for floor in floor_config:
        data_path = os.path.join(base_dir, floor['folder'], "data.json")
        if not os.path.exists(data_path):
            continue

        with open(data_path, "r") as f:
            floor_stores = json.load(f)

        changed = False
        for store in floor_stores:
            store_name_lower = store['name'].lower().strip()
            if store_name_lower in logo_mapping:
                store['spriteX'] = logo_mapping[store_name_lower]['x']
                store['spriteY'] = logo_mapping[store_name_lower]['y']
                changed = True
                updated_count += 1

        if changed:
            with open(data_path, "w") as f:
                json.dump(floor_stores, f, indent=2)

    msg = f"Sprite Sheet generated!\n\nLinked {updated_count} logos to stores on the map."
    return True, msg, updated_count
