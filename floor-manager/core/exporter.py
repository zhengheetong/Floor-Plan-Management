"""
core/exporter.py
Handles all file export / deployment logic.
Pure business logic — no Tkinter dependency.
"""

import os
import shutil

# ===========================================
# PROJECT EXPORT (Local Staging → React Public)
# ===========================================


def export_to_web(base_dir, target_web_dir):
    """
    Copies all local map data and the generated sprite sheet
    from the staging area into the React app's `public` folder.

    Returns a tuple: (success: bool, message: str)
    """
    dest_floor_path = os.path.join(target_web_dir, "Floor")
    dest_sprite_img = os.path.join(target_web_dir, "icons-sprite.png")

    try:
        # Copy all Floor subdirectories (map.png + data.json per floor)
        shutil.copytree(base_dir, dest_floor_path, dirs_exist_ok=True)

        # Copy the generated sprite sheet if it exists
        local_sprite_img = os.path.join("public", "icons-sprite.png")
        if os.path.exists(local_sprite_img):
            shutil.copy(local_sprite_img, dest_sprite_img)

        return True, "All map data and sprites exported!\nRefresh your website to see changes."
    except Exception as e:
        return False, f"An error occurred:\n{str(e)}"
