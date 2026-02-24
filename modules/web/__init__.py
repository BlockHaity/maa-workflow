import flask
from .api import api_bp
from modules.tools import Config

def main():
    app = flask.Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.run(host=Config.get("webui.address", "0.0.0.0"),port=Config.get("webui.port", 12023), debug=True)