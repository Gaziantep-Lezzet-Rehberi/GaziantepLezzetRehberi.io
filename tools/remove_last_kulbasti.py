from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import app, db, Recipe

with app.app_context():
    items = Recipe.query.filter((Recipe.name.ilike('%külbast%')) | (Recipe.name.ilike('%kulbast%'))).order_by(Recipe.id.desc()).all()
    if not items:
        print('No Külbastı recipes found')
        sys.exit(0)

    to_delete = items[0]
    print(f"Deleting recipe id={to_delete.id} name='{to_delete.name}' slug='{to_delete.slug}'")
    db.session.delete(to_delete)
    db.session.commit()
    print('Deleted.')
