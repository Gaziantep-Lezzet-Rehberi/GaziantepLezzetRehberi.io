import os
import sys
import requests

# make project importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, db, Recipe

URL = os.environ.get('GEMINI_URL', 'https://gemini.google.com/share/5fcb94d5ec48')
OUT_DIR = os.path.join(ROOT, 'static', 'images')
OUT_NAME = 'simit_kebabi.jpg'
OUT_PATH = os.path.join(OUT_DIR, OUT_NAME)

def download_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        resp = requests.get(url, headers=headers, allow_redirects=True, timeout=15)
    except Exception as e:
        print('İstek başarısız:', e)
        return False, None

    if resp.status_code != 200:
        print('HTTP hata:', resp.status_code)
        return False, None

    ctype = resp.headers.get('Content-Type', '')
    if not ctype.startswith('image'):
        # try to find an image URL in HTML
        text = resp.text
        # naive search for jpg/png urls
        import re
        m = re.search(r'(https?:\\/\\/[^"\'>]+\\.(?:jpg|jpeg|png|webp))', text, re.IGNORECASE)
        if m:
            img_url = m.group(1).replace('\\/','/')
            print('Sayfa içinde bulunmuş görsel URLsi:', img_url)
            try:
                r2 = requests.get(img_url, headers=headers, timeout=15)
                if r2.status_code == 200 and r2.headers.get('Content-Type','').startswith('image'):
                    return True, r2.content
                else:
                    print('İkinci istekte görsel alınamadı, durum:', r2.status_code)
                    return False, None
            except Exception as e:
                print('İkinci istek hata:', e)
                return False, None
        print('İndirilen içerik görsel değil veya erişim engellenmiş (Content-Type:', ctype, ')')
        return False, None

    return True, resp.content

def save_and_update(data_bytes):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_PATH, 'wb') as f:
        f.write(data_bytes)
    print('Görsel kaydedildi:', OUT_PATH)

    with app.app_context():
        r = Recipe.query.filter((Recipe.slug == 'simit-kebabi') | (Recipe.name.ilike('%simit%'))).first()
        if not r:
            print('Simit Kebabı tarifi bulunamadı, fakat görsel kaydedildi.')
            return
        old = r.image_url
        r.image_url = '/static/images/' + OUT_NAME
        db.session.add(r)
        db.session.commit()
        print('Veritabanı güncellendi: eski ->', old, 'yeni ->', r.image_url)

if __name__ == '__main__':
    ok, data = download_image(URL)
    if not ok:
        print('Görsel indirilemedi.')
        sys.exit(1)
    save_and_update(data)
