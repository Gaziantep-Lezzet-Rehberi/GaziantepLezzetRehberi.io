import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app, db, Place


def add_place_if_missing(data):
    with app.app_context():
        if Place.query.filter_by(name=data['name']).first():
            print(f"Already exists: {data['name']}")
            return False
        p = Place(**data)
        db.session.add(p)
        db.session.commit()
        print(f"Added: {data['name']}")
        return True


if __name__ == '__main__':
    places = [
        {
            'name': 'Tudyahan 1874',
            'address': 'Şahinbey, Akyol Mah. (Tarihi Tütün Hanı içinde, şık bir atmosfer.)',
            'category': 'Kebaplar',
            'lat': None,
            'lng': None,
            'description': 'Küşleme ve Simit Kebabı sunan, tarihi tütün hanı içinde yer alan şık mekan.',
            'rating': 4.4,
            'image_url': ''
        },
        {
            'name': 'Metanet Lokantası (Beyran Efsane)',
            'address': 'Şahinbey, Tepebaşı Mah. (Tarihi mekanlara yakın, sabah saatlerinde çok yoğun.)',
            'category': 'Çorbalar',
            'lat': None,
            'lng': None,
            'description': 'Uzun yıllardır Beyran ile özdeşleşmiş lokanta; sabahları özellikle yoğundur.',
            'rating': 4.5,
            'image_url': ''
        }
    ]

    for p in places:
        add_place_if_missing(p)
