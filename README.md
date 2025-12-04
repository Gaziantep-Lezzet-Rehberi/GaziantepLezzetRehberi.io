## Gaziantep Lezzet Rehberi — Local Kurulum

Bu proje tam başlangıç (SQLite + Flask-SQLAlchemy + Flask-WTF) içerir.

Kurulum (PowerShell):

```powershell
# 1) Sanal ortam oluştur
python -m venv .venv

# 2) Sanal ortamı etkinleştir
.venv\Scripts\Activate.ps1

# 3) Paketleri yükle
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4) Veritabanını oluşturup seed et
python seed.py

# 5) Uygulamayı çalıştır
python app.py

# Tarayıcıda aç: http://127.0.0.1:5000
```

PowerShell yürütme politikası izinleriyle ilgili sorun yaşarsanız:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Notlar:
- İlk başta örnek veriler `seed.py` ile eklenir.
- Geliştirme sırasında `app.py` debug modunda çalışır.

