import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Recipe

with app.app_context():
    r = Recipe.query.filter_by(slug='alinazik').first()
    if r:
        print('Before:', r.id, r.name, r.image_url)
        r.image_url = '/static/images/alinazik.jpg'
        db.session.commit()
        print('Updated to:', r.image_url)
    else:
        print('Alinazik recipe not found')
