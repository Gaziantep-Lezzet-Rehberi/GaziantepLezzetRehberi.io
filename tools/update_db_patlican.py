#!/usr/bin/env python3
"""Update the Recipe.image_url for the Patlıcan recipe to point to
`/static/images/patlican_kebabi.jpg` without touching the file system.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from app import app, db, Recipe
except Exception as e:
    print('Failed to import app:', e)
    sys.exit(1)

with app.app_context():
    recipe = Recipe.query.filter(Recipe.name.ilike('%patlıcan%')).first()
    if not recipe:
        recipe = Recipe.query.filter(Recipe.name.ilike('%patlican%')).first()

    if not recipe:
        print('Could not find a recipe with "patlıcan" in the name.')
        sys.exit(1)

    old = recipe.image_url
    recipe.image_url = '/static/images/patlican_kebabi.jpg'
    db.session.commit()
    print(f"Updated recipe id={recipe.id} name='{recipe.name}'\n  Old: {old}\n  New: {recipe.image_url}")
