import sys
sys.path.append('./..')
sys.path.append('./../..')

from flask import render_template
from app import app
import os

def render():
    return render_template('index.html')
