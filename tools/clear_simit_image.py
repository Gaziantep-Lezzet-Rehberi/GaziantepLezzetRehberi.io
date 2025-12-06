import sys
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, db, Recipe

def clear_image():
    with app.app_context():
        r = Recipe.query.filter((Recipe.slug == 'simit-kebabi') | (Recipe.name.ilike('%simit%'))).first()
        if not r:
            print('Simit Kebabı kaydı bulunamadı.')
            return
        old = r.image_url
        r.image_url = None
        db.session.add(r)
        db.session.commit()
        print('image_url kaldırıldı.')
        print('Önceki:', old)

if __name__ == '__main__':
    clear_image()
