# LiveSpec

Otomatik **OpenAPI + Swagger** üretimi, iste​k–yanıt loglama ve kolay CI contract-test entegrasyonu.

## Kurulum
```bash
pip install -e .  # proje klasöründe
```

## Hızlı Başlangıç
```python
from flask import Flask
from livespec import init_docs, request_logger

app = Flask(__name__)
init_docs(app, title="My API")
app.wsgi_app = request_logger(app)  # opsiyonel

@app.route("/hello")
def hello():
    return {"msg": "hi"}

if __name__ == "__main__":
    app.run()
```
- `/docs` → Swagger-UI
- `/openapi.json` → makine-okunur şema

## CLI: OpenAPI üretimi
```bash
python -m livespec.generate_openapi example.app openapi.json
```

## Özellikler (MVP)
- Flask `url_map` introspection → OpenAPI 3.0
- Swagger-UI dâhil
- Basit WSGI middleware ile istek / süre log’u

## Yol Haritası
- JSON-Schema çıkarımı (marshmallow destekli)
- PostgreSQL `request_log` tablosu
- GitHub Actions contract-test şablonu
- Prometheus exporter
