#!/usr/bin/env python3
"""
Download images for Buku Ajar Pemrograman Game - Roll a Ball.
Tries Unity Learn URLs first; creates placeholder if download fails.
Run: python download_images.py
"""
import os
import sys
import urllib.request
import ssl
import base64

# Create figures directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(SCRIPT_DIR, "..", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Minimal 2x2 gray PNG (base64) for placeholder
_PLACEHOLDER_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAEklEQVQImWP4z8AwwjDCAAB"
    "gAAG/U0bBAAAAAElFTkSuQmCC"
)


def create_placeholder(filepath: str, label: str) -> bool:
    """Create a simple placeholder PNG when download fails."""
    try:
        # Try PIL if available
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (800, 400), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 790, 390], outline=(150, 150, 150), width=2)
        draw.text((400, 200), label, fill=(100, 100, 100), anchor="mm")
        img.save(filepath)
        return True
    except ImportError:
        with open(filepath, "wb") as f:
            f.write(_PLACEHOLDER_PNG)
        return True
    except Exception:
        return False


# Unity Learn image URLs (educational use) - may need manual screenshot if 404
IMAGES = {
    "unity-editor-overview.png": "https://connect-mediagw.unity.com/h1/20230920/learn/images/84183f6a-0905-4d4d-be59-5b5db508ab2b_0-setting-up-the-game-final.png",
    "create-project.png": "https://connect-mediagw.unity.com/h1/20230920/learn/images/9d56ea42-9138-4a3a-ad4f-440fd59ee5d6_1-create-a-new-project.png",
    "rename-minigame.png": "https://connect-mediagw.unity.com/h1/20230920/learn/images/5e2fea6a-e480-4b49-a4df-0ed83da2c3ce_2-rename-minigame.png",
    "ground-plane.png": "https://connect-mediagw.unity.com/h1/20230920/learn/images/dff45d10-e46e-422a-ac57-5fc6ab178846_3-ground-plane.png",
    "scale-ground.png": "https://connect-mediagw.unity.com/h1/20230920/learn/images/205669cf-5b59-4eb8-9291-7f1813734491_4-increase-scale.png",
    "player-sphere.png": "https://connect-mediagw.unity.com/h1/20230920/learn/images/d3fae6fc-4a29-4e7e-a791-90a1d61c6582_5-add-player-sphere.png",
    "add-materials.png": "https://connect-mediagw.unity.com/h1/20230920/learn/images/555e74fe-3de4-4ccd-8d2c-7a7b462db8b7_7-add-materials.png",
    "project-introduction.png": "https://connect-mediagw.unity.com/h1/20200716/learn/images/b7964159-e07f-45d4-bffb-953c7f3c9109_Project_introduction.png",
    "moving-player.png": "https://connect-mediagw.unity.com/h1/20200716/learn/images/bcdda2f6-1c83-4c62-9f05-bd3d9ca62b5e_Moving_the_player.png",
    "moving-camera.png": "https://connect-mediagw.unity.com/h1/20200716/learn/images/d88b1a3e-2937-4166-875c-3d1254473d80_Movingthecamera.png",
    "play-area.png": "https://connect-mediagw.unity.com/h1/20200716/learn/images/03a125a3-b691-4bff-8eb7-aedeba83bbb3_Setting_Up_the_Play_area.png",
    "collectibles.png": "https://connect-mediagw.unity.com/h1/20200716/learn/images/efc386c4-8acb-4410-8bb8-b39287df866b_CreatingCollectibles.png",
    "counting-points.png": "https://connect-mediagw.unity.com/h1/20200716/learn/images/96fb9c76-043a-4606-96da-284a083ca218_CountingPoints.png",
    "display-score.png": "https://connect-mediagw.unity.com/h1/20200716/learn/images/86ca8892-dfd7-4cbc-9069-ec0d9e7789ca_DisplayScoreAndText.png",
    "build-game.png": "https://connect-mediagw.unity.com/h1/20200716/learn/images/c0267697-fb48-4378-ad1b-14886e2c8625_Buildthegame.png",
}


def download_image(url: str, filepath: str, retries: int = 3) -> bool:
    """Download image with retry logic."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                with open(filepath, "wb") as f:
                    f.write(resp.read())
            return True
        except Exception as e:
            print(f"  Attempt {attempt + 1}/{retries} failed: {e}")
    return False


def main():
    placeholder_only = "--placeholder-only" in sys.argv
    if placeholder_only:
        print("Creating placeholder images (skip download)...")
    else:
        print("Downloading images for Buku Ajar Pemrograman Game...")
    print(f"Output directory: {FIGURES_DIR}\n")
    
    success = 0
    failed = []
    
    for filename, url in IMAGES.items():
        filepath = os.path.join(FIGURES_DIR, filename)
        print(f"{'Creating' if placeholder_only else 'Downloading'} {filename}...", end=" ")
        if placeholder_only:
            ok = create_placeholder(filepath, filename.replace(".png", "").replace("-", " ").title())
            print("OK" if ok else "FAILED")
            success += 1 if ok else 0
            if not ok:
                failed.append(filename)
        elif download_image(url, filepath):
            print("OK")
            success += 1
        else:
            label = filename.replace(".png", "").replace("-", " ").title()
            if create_placeholder(filepath, label):
                print("(placeholder)")
                success += 1
            else:
                print("FAILED")
                failed.append(filename)
    
    print(f"\nDone: {success}/{len(IMAGES)} images ready.")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
