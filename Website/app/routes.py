import sys
sys.path.append('./../..')
sys.path.append('./..')
from flask import current_app as app
import os
from flask import Flask, flash, jsonify, render_template, request, send_from_directory, send_file
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

# @app.route("/download/<path:path>")
# def download(path):
#     """Serve a file from the upload directory."""
#     SRC_DIR = './../data/MainData/Generated'
#     return send_from_directory(SRC_DIR, path, as_attachment=True)

# @app.route('/dash/<path:path>')
# def download(path):
#     SRC_DIR = './../data/MainData/Generated'
#     file = os.apth.join(SRC_DIR, path)
#     import io
#     import pandas as pd
#     str_io = io.BytesIO()
#     df = pd.read_csv(file)
#     df.to_csv(str_io)
#
#     mem = io.BytesIO()
#     mem.write(str_io.getvalue().encode('utf-8'))
#     mem.seek(0)
#     str_io.close()
#
#     return send_file(mem,
#                      mimetype='text/csv',
#                      attachment_filename='downloadFile.csv',
#                      as_attachment=True)
