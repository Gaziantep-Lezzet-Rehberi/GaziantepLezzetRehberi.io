import urllib.request
import sys

url = 'http://127.0.0.1:5000/static/images/patlican_kebabi.jpg'
try:
    req = urllib.request.Request(url, method='HEAD')
    with urllib.request.urlopen(req, timeout=5) as res:
        print('STATUS:', res.status)
        print('CONTENT-TYPE:', res.getheader('Content-Type'))
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
