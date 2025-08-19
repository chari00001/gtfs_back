# FastAPI Boilerplate

Bu proje, hızlıca üretime hazır bir FastAPI uygulamasına başlamak için minimal fakat genişletilebilir bir iskele sunar.

## Özellikler

- Sağlık kontrolü (`GET /api/health`)
- Ortam değişkenleriyle yapılandırma (Pydantic Settings)
- CORS yapılandırması
- Basit logging kurulumu
- Pytest ile örnek test

## Başlangıç

Önkoşullar: Python 3.10+

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Uygulama açıldıktan sonra:

- API Dokümantasyonu: `http://127.0.0.1:8000/docs`
- Sağlık Kontrolü: `http://127.0.0.1:8000/api/health`

## Ortam Değişkenleri

`cp .env.example .env` komutuyla örnek dosyadan `.env` oluşturun. Başlıca değişkenler:

- `PROJECT_NAME`: Uygulama adı
- `DEBUG`: Hata ayıklama modu (true/false)
- `API_V1_PREFIX`: API prefix (örn. `/api`)
- `BACKEND_CORS_ORIGINS`: CORS izinli origin listesi (JSON array)

## Testler

```bash
pytest -q
```

## Proje Yapısı

```
app/
  api/
    routes/
      health.py
    router.py
  core/
    config.py
    logging_config.py
  __init__.py
  main.py
tests/
  test_health.py
requirements.txt
README.md
.env.example
```


