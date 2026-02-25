from flask import Blueprint
from flask_apispec import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import doc
from werkzeug.wrappers import Response
from datetime import datetime

__all__ = ["init_docs", "request_logger"]

_docs_blueprint = Blueprint("livespec_docs", __name__, url_prefix="/docs")

def init_docs(app, title: str = "API", version: str = "1.0.0"):
    """Attach Swagger-UI with auto-generated spec to given Flask app."""
    app.config.update({
        "APISPEC_TITLE": title,
        "APISPEC_VERSION": version,
        "APISPEC_SWAGGER_UI_URL": "/docs/",
    })

    docs = FlaskApiSpec(app)

    # expose swagger.json
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
