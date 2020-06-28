from flask import Flask
from flask_bootstrap import Bootstrap
import os
import sys
sys.path.append('./../..')
sys.path.append('./..')
# app = Flask(__name__)
# bootstrap = Bootstrap(app)

def create_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config_flask.Config')

    with app.app_context():
        # Import Flask routes
        from . import routes
        # from .assets import compile_static_assets

        # Import Dash application
        from .plotlydash.dashboard import create_dashboard
        app = create_dashboard(app)

        # Compile static assets
        # compile_static_assets(assets)
        bootstrap = Bootstrap(app)
        return app


# from app import routes