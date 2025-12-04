import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app

def render_about():
    with app.test_client() as client:
        resp = client.get('/about')
        html = resp.data.decode('utf-8')
        out_path = Path(__file__).resolve().parents[0] / 'about_rendered.html'
        out_path.write_text(html, encoding='utf-8')
        print(f'Wrote {out_path}')

if __name__ == '__main__':
    render_about()
