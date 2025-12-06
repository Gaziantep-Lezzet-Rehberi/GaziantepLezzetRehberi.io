import os
import sys
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, db, Recipe

URL = os.environ.get('IMAGE_URL')
OUT_DIR = os.path.join(ROOT, 'static', 'images')
OUT_NAME = 'simit_kebabi.jpg'
OUT_PATH = os.path.join(OUT_DIR, OUT_NAME)

def download(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
    except Exception as e:
        print('İndirme hatası:', e)
        return None
    if r.status_code != 200:
        print('HTTP hata:', r.status_code)
        return None
    ctype = r.headers.get('Content-Type', '')
    if ctype.startswith('image'):
        return r.content

    # If HTML, try to extract an image URL (og:image, twitter:image, link rel=image_src)
    text = r.text
    import re
    patterns = [r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
                r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
                r'<link[^>]+rel=["\']image_src["\'][^>]+href=["\']([^"\']+)["\']',
                r'(https?:\\/\\/[^"\'>]+\\.(?:jpg|jpeg|png|webp))']
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            img_url = m.group(1).replace('\\/','/')
            print('Bulunan görsel URLsi:', img_url)
            try:
                r2 = requests.get(img_url, headers=headers, timeout=20)
                if r2.status_code == 200 and r2.headers.get('Content-Type','').startswith('image'):
                    return r2.content
                else:
                    print('Bulunan görsel indirilemedi, durum:', r2.status_code, r2.headers.get('Content-Type'))
            except Exception as e:
                print('Görsel indirirken hata:', e)
    print('Sayfa içinde görsel bulunamadı veya erişim engellenmiş (Content-Type:', ctype, ')')
    return None

def save_and_update(data):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_PATH, 'wb') as f:
        f.write(data)
    print('Görsel kaydedildi:', OUT_PATH)
    with app.app_context():
        r = Recipe.query.filter((Recipe.slug == 'simit-kebabi') | (Recipe.name.ilike('%simit%'))).first()
        if not r:
            print('Simit Kebabı bulunamadı, fakat görsel kaydedildi.')
            return
        old = r.image_url
        r.image_url = '/static/images/' + OUT_NAME
        db.session.add(r)
        db.session.commit()
        print('Veritabanı güncellendi: {} -> {}'.format(old, r.image_url))

if __name__ == '__main__':
    if not URL:
        print('IMAGE_URL environment variable not set')
        sys.exit(2)
    data = download(URL)
    if not data:
        print('Görsel indirilemedi.')
        sys.exit(1)
    save_and_update(data)
