from PIL import Image, ImageOps
from pathlib import Path
p = Path(__file__).resolve().parent.parent / 'static' / 'images' / 'beyran.jpg'
if not p.exists():
    print('FILE_NOT_FOUND', p)
    raise SystemExit(1)
with Image.open(p) as im:
    print('Original size:', im.size)
    target = (1200, 800)
    # Use ImageOps.fit to crop to aspect ratio and resize
    new = ImageOps.fit(im, target, Image.LANCZOS)
    new.save(p, quality=85)
    print('Saved new size:', new.size)
