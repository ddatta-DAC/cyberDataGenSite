from app import app
from flask import render_template 
@app.route('/')
@app.route('/index')

def index():
    from .pages import index
    return index.render()

    #return render_template('index.html')
