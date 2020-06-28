import sys
sys.path.append('./../..')
sys.path.append('./..')
from flask import current_app as app


@app.route('/')
@app.route('/home')
def home():
    from .pages import home
    return home.render()

