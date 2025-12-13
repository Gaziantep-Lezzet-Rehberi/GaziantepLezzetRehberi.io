from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app, Recipe

with app.app_context():
    items = Recipe.query.filter((Recipe.name.ilike('%külbast%')) | (Recipe.name.ilike('%kulbast%'))).order_by(Recipe.id.asc()).all()
    if not items:
        print('No Külbastı recipes found')
    else:
        for r in items:
            print(r.id, r.name, r.slug, r.image_url)
