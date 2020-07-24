import sys
sys.path.append('./../..')
sys.path.append('./..')
from flask import current_app as app
import os
from flask import Flask, flash, jsonify, render_template, request
import webbrowser


@app.route('/')
@app.route('/home')
def home():
    from .pages import home
    return home.render()

@app.route('/compare')
def compare_page():
    from .pages import compare_page
    return compare_page.render()


@app.route('/compare_updateJumbotron', methods=['POST'])
def compare_updateJumbotron():
    projectpath = request.form['update_value']
    return jsonify(status="success")