import sys
sys.path.append('./..')
sys.path.append('./../..')

from flask import render_template
def render():
    _dict = {
        'value_1' : 'A',
        'value_2': 'B'
    }
    return render_template('index.html', **_dict)
