from flask import Blueprint, jsonify
from werkzeug.wrappers import Response
from datetime import datetime

try:
    from flask_apispec import FlaskApiSpec
    FLASK_APISPEC_AVAILABLE = True
except ImportError:
    FLASK_APISPEC_AVAILABLE = False

__all__ = ["init_docs", "request_logger"]

def init_docs(app, title: str = "API", version: str = "1.0.0"):
    """Attach Swagger-UI with auto-generated spec to given Flask app.
    
    Falls back to basic route listing if flask-apispec not installed.
    """
    if not FLASK_APISPEC_AVAILABLE:
        # Fallback: manual route listing
        @app.route("/docs")
        def docs_fallback():
            routes = []
            for rule in app.url_map.iter_rules():
                if rule.endpoint != "static":
                    routes.append({
                        "path": str(rule.rule),
                        "methods": list(rule.methods - {"HEAD", "OPTIONS"}),
                        "endpoint": rule.endpoint
                    })
            return jsonify({
                "title": title,
                "version": version,
                "routes": sorted(routes, key=lambda x: x["path"])
            })
        
        @app.route("/openapi.json")
        def openapi_fallback():
            return docs_fallback()
        
        return None
    
    # Full flask-apispec integration
    app.config.update({
        "APISPEC_TITLE": title,
        "APISPEC_VERSION": version,
        "APISPEC_SWAGGER_UI_URL": "/docs/",
    })
    
    docs = FlaskApiSpec(app)
    
    @app.route("/openapi.json")
    def openapi_json():
        return app.apispec.to_dict()
    
    return docs


def request_logger(app):
    """WSGI middleware: her istek/yanıt meta bilgisini stdout'a yazar.
    Kolay entegrasyon; prod'da Postgres insert yapılabilir."""

    def _middleware(environ, start_response):
        start_time = datetime.utcnow()
        method = environ.get("REQUEST_METHOD")
        path = environ.get("PATH_INFO")

        def _sr(status, headers, exc_info=None):
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            print(f"[LiveSpec] {method} {path} -> {status} {duration:.1f}ms")
            return start_response(status, headers, exc_info)

        return app.wsgi_app(environ, _sr)

    return _middleware
