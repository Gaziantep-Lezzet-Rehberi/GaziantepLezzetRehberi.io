#!/usr/bin/env python3
"""Copy a local image into `static/images/patlican_kebabi.jpg`, optionally resize it,
and update the `Recipe` record in the app's database to point to the new image.

Usage:
  py tools\set_patlican_image.py C:\path\to\downloaded\image.jpg

After running, the recipe whose name contains 'Patlıcan' (case-insensitive)
will be updated to use `/static/images/patlican_kebabi.jpg`.
"""
from pathlib import Path
import sys
import shutil

try:
    from PIL import Image
except Exception:
    Image = None

ROOT = Path(__file__).resolve().parents[1]
APP_PY = ROOT / 'app.py'
if not APP_PY.exists():
    print('Error: could not find app.py in workspace root; run this from the project root.')
    sys.exit(1)

# make sure we can import the Flask app
sys.path.insert(0, str(ROOT))
try:
    from app import app, db, Recipe
except Exception as e:
    print('Failed to import app:', e)
    sys.exit(1)


def center_crop_and_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h
    if src_ratio > target_ratio:
        # source is wider -> crop left/right
        new_w = int(target_ratio * src_h)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        # source is taller -> crop top/bottom
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)


def main():
    if len(sys.argv) < 2:
        print('Usage: py tools\\set_patlican_image.py C:\\path\\to\\image.jpg')
        sys.exit(1)

    src_path = Path(sys.argv[1]).expanduser()
    if not src_path.exists():
        print('Source file not found:', src_path)
        sys.exit(1)

    dest_dir = ROOT / 'static' / 'images'
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / 'patlican_kebabi.jpg'

    # If Pillow is available, resize/crop to 1200x800 for consistent layout
    if Image is not None:
        try:
            with Image.open(src_path) as im:
                im = im.convert('RGB')
                im2 = center_crop_and_resize(im, 1200, 800)
                im2.save(dest_path, format='JPEG', quality=85)
                print('Saved resized image to', dest_path)
        except Exception as e:
            print('Pillow failed to process image, falling back to raw copy:', e)
            shutil.copy2(src_path, dest_path)
            print('Copied image to', dest_path)
    else:
        shutil.copy2(src_path, dest_path)
        print('Copied image to', dest_path)

    # Update DB record
    with app.app_context():
        # find recipe with name containing 'Patlıcan' or exact 'Patlıcan Kebabı'
        recipe = Recipe.query.filter(Recipe.name.ilike('%patlıcan%')).first()
        if not recipe:
            # try english fallback
            recipe = Recipe.query.filter(Recipe.name.ilike('%patlican%')).first()

        if not recipe:
            print('Warning: Could not find a recipe with name containing "Patlıcan".')
            print('You may need to update the DB manually or run the seed script again.')
            sys.exit(0)

        old = recipe.image_url
        recipe.image_url = '/static/images/patlican_kebabi.jpg'
        db.session.commit()
        print(f"Updated recipe id={recipe.id} name='{recipe.name}'\n  Old image: {old}\n  New image: {recipe.image_url}")


if __name__ == '__main__':
    main()
