from flask import Flask
from flask_cors import CORS
import config
from dashboard import dashboard_bp

app = Flask(__name__,
            template_folder=config.TEMPLATES_PATH,
            static_folder=config.STATIC_PATH)

CORS(app)

app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=config.DEBUG)