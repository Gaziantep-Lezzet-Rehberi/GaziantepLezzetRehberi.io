#!/usr/bin/env python3
"""Copy a local image into `static/images/<slug>.jpg`, optionally resize it,
and update a Recipe record in the app's database to point to the new image.

Usage:
  py tools\set_recipe_image.py <local_path> "Recipe Name" [slug]

Example:
  py tools\set_recipe_image.py static\images\muhammara_src.jpg "Muhammara" muhammara
"""
from pathlib import Path
import sys
import shutil

try:
    from PIL import Image
except Exception:
    Image = None

ROOT = Path(__file__).resolve().parents[1]
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
        new_w = int(target_ratio * src_h)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)


def main():
    if len(sys.argv) < 3:
        print('Usage: py tools\\set_recipe_image.py <local_path> "Recipe Name" [slug]')
        sys.exit(1)

    src_path = Path(sys.argv[1]).expanduser()
    recipe_name = sys.argv[2]
    slug = sys.argv[3] if len(sys.argv) > 3 else recipe_name.lower().replace(' ', '_')

    if not src_path.exists():
        print('Source file not found:', src_path)
        sys.exit(1)

    dest_dir = ROOT / 'static' / 'images'
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / f'{slug}.jpg'

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

    # Update DB
    with app.app_context():
        recipe = Recipe.query.filter(Recipe.name.ilike(f'%{recipe_name}%')).first()
        if not recipe:
            print(f'Could not find recipe with name containing "{recipe_name}"')
            sys.exit(1)

        old = recipe.image_url
        recipe.image_url = f'/static/images/{slug}.jpg'
        db.session.commit()
        print(f"Updated recipe id={recipe.id} name='{recipe.name}'\n  Old: {old}\n  New: {recipe.image_url}")


if __name__ == '__main__':
    main()
