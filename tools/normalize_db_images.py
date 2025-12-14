"""
Normalize image_url values in instance/gaziantep.db for Recipe and Place tables.
Rules applied:
 - If image_url is NULL/empty -> leave as None
 - If image_url starts with 'http://' or 'https://' -> leave as-is
 - If image_url starts with '/static/' -> strip leading '/static/' and store that (e.g. 'images/x.jpg' or 'uploads/x.jpg')
 - If image_url already contains a slash but not starting with '/static/', assume it's a relative static path and keep as-is
 - If image_url is a bare filename (no slash), assume it's an upload and store as 'uploads/<filename>' (so templates can use url_for('static', filename=image_url))

This script prints a short summary of changes and updates the DB in-place.
"""
import os
import sqlite3

DB = os.path.join('instance', 'gaziantep.db')
if not os.path.exists(DB):
    print('Instance DB not found at', DB)
    raise SystemExit(1)

con = sqlite3.connect(DB)
cur = con.cursor()

changed = 0

# helper
def normalize(val):
    if val is None:
        return None
    v = val.strip()
    if v == '':
        return None
    if v.startswith('http://') or v.startswith('https://'):
        return v
    if v.startswith('/static/'):
        return v[len('/static/'):]
    if '/' in v:
        # already a relative path like 'images/x.jpg' or 'uploads/x.jpg'
        return v
    # bare filename -> assume uploads
    return f'uploads/{v}'

# Process Recipe.image_url
try:
    cur.execute("SELECT id, image_url FROM recipe")
except Exception as e:
    print('Error querying recipe table:', e)
    con.close()
    raise SystemExit(1)

rows = cur.fetchall()
for rid, img in rows:
    new = normalize(img) if img is not None else None
    if new != img:
        cur.execute("UPDATE recipe SET image_url = ? WHERE id = ?", (new, rid))
        changed += 1

# Process Place.image_url if present
try:
    cur.execute("SELECT id, image_url FROM place")
    rows = cur.fetchall()
    for pid, img in rows:
        new = normalize(img) if img is not None else None
        if new != img:
            cur.execute("UPDATE place SET image_url = ? WHERE id = ?", (new, pid))
            changed += 1
except Exception:
    # table may not exist, ignore
    pass

con.commit()
con.close()
print(f'Done. Normalized {changed} image_url entries in {DB}')
