import sys
import os

# Ensure project root is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import db, Recipe, app

GEMINI_URL = 'https://gemini.google.com/share/52b70c2bc679'

def set_image():
    with app.app_context():
        r = Recipe.query.filter((Recipe.slug == 'simit-kebabi') | (Recipe.name.ilike('%simit%'))).first()
        if not r:
            print('Simit Kebabı tarifi bulunamadı.')
            return
        old = r.image_url
        r.image_url = GEMINI_URL
        db.session.add(r)
        db.session.commit()
        print(f'Güncellendi: {r.name} ({r.slug})')
        print(f'Önceki image_url: {old}')
        print(f'Yeni image_url: {r.image_url}')

if __name__ == '__main__':
    set_image()
