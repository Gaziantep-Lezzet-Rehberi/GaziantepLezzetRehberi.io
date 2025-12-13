from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app, db, Recipe

with app.app_context():
    if Recipe.query.filter_by(slug='kulbasti').first():
        print('Recipe "kulbasti" already exists')
        sys.exit(0)

    r = Recipe(
        name='Külbastı',
        slug='kulbasti',
        category='Kebaplar',
        is_meat=True,
        cook_time=20,
        difficulty='Orta',
        servings=2,
        description='Klasik külbastı; etin kısa sürede yüksek ısıda pişirilmesiyle hazırlanan lezzetli kebap.',
        ingredients='Külbastı eti (kuzu veya dana), tuz, karabiber, isteğe bağlı zeytinyağı',
        steps='1. Etleri temizleyip tuzlayın.\n2. Yüksek ateşte mühürleyin ve kısa sürede pişirin.',
        image_url='/static/images/kulbasti.jpg'
    )
    db.session.add(r)
    db.session.commit()
    print('Added recipe id=', r.id)
