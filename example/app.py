from flask import Flask, jsonify
from livespec import init_docs, request_logger

app = Flask(__name__)

# attach docs & logger
init_docs(app, title="Example API")
app.wsgi_app = request_logger(app)


@app.route("/hello")
def hello():
    """Basit hello endpoint"""
    return jsonify(message="Hello, LiveSpec!")


if __name__ == "__main__":
    app.run(debug=True)
