import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, db, Recipe

OUT_PATH = '/static/images/simit_kebabi.jpg'

def update():
    with app.app_context():
        r = Recipe.query.filter((Recipe.slug == 'simit-kebabi') | (Recipe.name.ilike('%simit%'))).first()
        if not r:
            print('Simit Kebabı bulunamadı.')
            return
        old = r.image_url
        r.image_url = OUT_PATH
        db.session.add(r)
        db.session.commit()
        print('Güncellendi: {} -> {}'.format(old, r.image_url))

if __name__ == '__main__':
    update()
