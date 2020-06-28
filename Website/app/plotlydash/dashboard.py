"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import os
import sys
sys.path.append('./../../..')
sys.path.append('./../..')
sys.path.append('./..')
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from .data import create_dataframe
from .layout import html_layout

# =================================
# Main function
# =================================
def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/bootstrap_lux.min.css',
             dbc.themes.BOOTSTRAP,
             dbc.themes.LUX
        ]
    )

    # Load DataFrame
    df = create_dataframe()
    df_2 = fetch_network_data_v1()
    # Custom HTML layout
    dash_app.index_string = html_layout

    histogram_1 = get_histogram()

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            histogram_1,
            create_data_table(df_2)
        ],
        id='dash-container',
        className="container-fluid mr-4"
    )
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id='database-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        page_size=300
    )
    return table

def fetch_network_data_v1():
    print(os.getcwd())
    DATA_LOC = './../data/Processed/data_2016-04-12.csv'
    df = pd.read_csv(DATA_LOC,index_col=None)
    return df

def get_histogram():
    df = fetch_network_data_v1()
    # Aggregate by Protocaol

    df = df.groupby(['pr']).size().reset_index(name='count')
    df['Protocol'] = df['pr']
    histogram_1 = dcc.Graph(
        id='histogram-graph',
        figure={
            'data': [{
                'x': df['Protocol'],
                'customdata': df['count'],
                'name': 'Distribution of Protocols',
                'type': 'bar'
            }],
            'layout': {
                'title': 'Distribution of Protocols',
                'height': 300,
                'padding': 150
            }
        })
    return histogram_1