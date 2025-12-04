import sys
from pathlib import Path

# Ensure project root is on sys.path so `from app import ...` works when running from tools/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app, db, Recipe

def update_categories(mapping):
    with app.app_context():
        changed = False
        for slug, new_cat in mapping.items():
            r = Recipe.query.filter_by(slug=slug).first()
            if not r:
                print(f"Not found: slug={slug}")
                continue
            old = r.category
            if old != new_cat:
                r.category = new_cat
                db.session.add(r)
                print(f"Updated: {r.name} ({slug})  {old} -> {new_cat}")
                changed = True
            else:
                print(f"No change: {r.name} ({slug}) already {new_cat}")
        if changed:
            db.session.commit()
            print("Database commit complete.")
        else:
            print("No updates needed.")

if __name__ == '__main__':
    mapping = {
        'alinazik': 'Kebaplar',
        'patlican-kebabi': 'Kebaplar',
        'fistikli-kebap': 'Kebaplar',
        'kusleme': 'Kebaplar',
        'simit-kebabi': 'Kebaplar',
    }
    update_categories(mapping)
