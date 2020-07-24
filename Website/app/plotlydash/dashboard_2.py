"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import os
import sys
from pandarallel import pandarallel
from dash.dependencies import Input, Output, State

pandarallel.initialize()

sys.path.append('./../../..')
sys.path.append('./../..')
sys.path.append('./..')
from cyberDataGenSite.data.common_utils import utils as common_utils
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from .data import create_dataframe
from .layout import html_layout
import plotly.express as px
from flask import request

try:
    from . import plotly_fig_utils as plotly_utils
except:
    import plotly_fig_utils as plotly_utils


# =================================
# Main function
# =================================
def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dash_board_2/',
        external_stylesheets=[
            '/static/bootstrap_lux.min.css',
            dbc.themes.BOOTSTRAP,
            dbc.themes.LUX,
            '/static/dashapp_1.css',
        ],
        assets_folder='/static/assets',
        external_scripts=['/static/js/jquery-3.5.1.min.js', '/static/js/dashapp_1.js']
    )

    dash_app.index_string = html_layout
    dash_app.layout = html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
            html.Hr(),
            html.Div(id='page-content')
        ],
        id='dash-container',
        className="container-fluid mr-4"
    )

    @dash_app.callback(dash.dependencies.Output('page-content', 'children'),
                       [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        # =================================
        # Create the main content based on IP
        # =================================
        if validate_ip(pathname.split('/')[-1]):
            ip = pathname.split('/')[-1]
        else:
            ip = None

        if ip is None:
            return html.Div([
                html.H3('Set IP ')
            ])
        else:
            return html.Div([
                html.H3('Valid IP {}'.format(ip))
            ])

    return dash_app.server


# ====
# Auxillary functions
# ====
def validate_ip(_str):
    import re
    pattern = '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
    res = re.search(pattern, _str)
    if res is None:
        return False
    else:
        return True
