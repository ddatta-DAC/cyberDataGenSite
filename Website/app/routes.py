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

@app.route('/generatedData_page')
def compare_page():
    from .pages import generatedData_page
    return generatedData_page.render()
