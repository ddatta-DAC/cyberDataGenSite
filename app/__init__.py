from flask import Flask
from flask_bootstrap import Bootstrap
import os
import sys
sys.path.append('./../..')

app = Flask(__name__)
bootstrap = Bootstrap(app)


from app import routes