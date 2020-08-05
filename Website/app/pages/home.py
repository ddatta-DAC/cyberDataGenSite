import sys
sys.path.append('./..')
sys.path.append('./../..')

from flask import render_template
def render():
    _dict = {
    }
    return render_template('homepage.html', **_dict)
