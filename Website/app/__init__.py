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

        # ---------
        # This is to display the real data
        # ---------
        from .plotlydash.dashboard import create_dashboard as dash1
        app = dash1(app)

        # ---------
        # This is to display cpomparison between Real and generated data per User
        # ---------
        from .plotlydash.dashboard_2 import create_dashboard as dash2
        app = dash2(app)


        # Compile static assets
        # compile_static_assets(assets)
        bootstrap = Bootstrap(app)
        return app


# from app import routes