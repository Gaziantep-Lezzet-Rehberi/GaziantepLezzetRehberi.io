"""
Small test script to verify the admin edit flow.
It:
 - GETs /login to fetch CSRF token
 - POSTs credentials (admin / 234356na)
 - GETs /recipes and /recipes/1 to check for status 200 and presence of 'Düzenle' or '/admin/edit/'

Run with the project's venv python.
"""
import re
import sys
from urllib.parse import urljoin

try:
    import requests
except Exception as e:
    print("requests not available in this python environment:", e)
    sys.exit(2)

BASE = 'http://127.0.0.1:5001'
LOGIN = urljoin(BASE, '/login')
RECIPES = urljoin(BASE, '/recipes')
RECIPE1 = urljoin(BASE, '/recipes/1')
USERNAME = 'admin'
PASSWORD = '234356na'

s = requests.Session()

print('GET', LOGIN)
r = s.get(LOGIN, timeout=5)
print('status:', r.status_code)
if r.status_code != 200:
    print('Failed to GET /login')
    sys.exit(3)

# try to find a CSRF token in the login page (order-agnostic attribute search)
m = re.search(r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']', r.text)
csrf = m.group(1) if m else None
print('csrf token found:', bool(csrf))

post_data = {'username': USERNAME, 'password': PASSWORD}
if csrf:
    post_data['csrf_token'] = csrf

print('POST /login (attempting to sign in)')
r = s.post(LOGIN, data=post_data, allow_redirects=True, timeout=5)
print('login status:', r.status_code)
if r.status_code != 200 and r.status_code != 302:
    print('Login may have failed. Response body (truncated):')
    print(r.text[:1000])

# check recipes
print('\nGET', RECIPES)
r = s.get(RECIPES, timeout=5)
print('status:', r.status_code)
contains_edit = ('Düzenle' in r.text) or ('/admin/edit/' in r.text)
print('contains edit link/text on /recipes:', contains_edit)

# check recipe 1
print('\nGET', RECIPE1)
r = s.get(RECIPE1, timeout=5)
print('status:', r.status_code)
contains_edit_1 = ('Düzenle' in r.text) or ('/admin/edit/' in r.text)
print('contains edit link/text on /recipes/1:', contains_edit_1)

if r.status_code == 200 and (contains_edit or contains_edit_1):
    print('\nTEST RESULT: PASS')
    sys.exit(0)
else:
    print('\nTEST RESULT: FAIL')
    sys.exit(4)
