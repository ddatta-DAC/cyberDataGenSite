"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import os
import sys
from pandarallel import pandarallel

pandarallel.initialize()

sys.path.append('./../../..')
sys.path.append('./../..')
sys.path.append('./..')
from cyberDataGenSite.data.common_utils import utils
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from .data import create_dataframe
from .layout import html_layout
import plotly.express as px


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
            dbc.themes.LUX,
            '/static/dashapp_1.css',
        ]
    )

    # Load DataFrame
    data = fetch_network_data_v1()
    # Custom HTML layout
    dash_app.index_string = html_layout

    # ========================================
    # Create a Time series plot
    # ========================================

    tab_obj = get_viz_tab_1(data)
    time_series_Packets = get_TS_fig(data)
    time_series_Bytes = get_TS_fig(data, y_value='Bytes')
    # ========================================
    # Create a visualization tab
    # ========================================

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            time_series_Packets,
            time_series_Bytes,
            tab_obj,
            create_data_table(data)
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
        page_size=25,
        style_data={'border': '1px solid blue'},
        style_header = {'border': '2px solid green', 'fontsize' : '2rem'}
    )
    table = html.Div(
        table,
        className='border border-100'
    )
    header = html.Div(
        html.P('Data Table'),
        className="text-center h3"
    )
    table = html.Div(
        [header,table],
        className="dash_table text-center"
    )
    return table


def fetch_network_data_v1():
    print(os.getcwd())
    DATA_LOC = './../data/Processed/data_2016-04-12.csv'
    df = pd.read_csv(DATA_LOC, index_col=None)
    df = df.rename(columns={
        'sp': 'Source Port',
        'dp': 'Destination Port',
        'pr': 'Protocol',
        'byt': 'Bytes',
        'pkt': 'Packets',
        'td': 'Time Duration'
    })
    return df


# ==================================
# Create Pie chart
# ==================================
def get_pie_chart(df, column):
    df = df.copy()
    df = df.groupby([column]).size().reset_index(name='count')
    fig = px.pie(df, values='count', names='Protocol')
    fig.update_layout(
        autosize=True,
        font=dict(
            family="Courier New",
            size=18,
            color="#7f7f7f"
        ),
        title_text=''
    )
    return fig


# =================================
# Sankey like categorical parallel axis plot
# =================================
def get_cat_plot(df, columns):
    df = df.copy()
    df_1 = df[columns]
    df_1 = df_1.groupby(columns).size().reset_index(name='count')

    fig = px.parallel_categories(
        df_1, dimensions=columns,
        color="count",
        color_continuous_scale=px.colors.sequential.Pinkyl
    )
    fig.update_layout(
        autosize=False,
        margin=dict(l=150, r=100, t=40, b=40),

        paper_bgcolor="#ffffff",
        font=dict(
            family="Courier New",
            size=15,
            color="#7f7f7f"
        ),
        title_text='',
        legend_orientation="h"
    )
    return fig


# ===============================
# Violin plot
# ===============================
def get_violin_plot_div(df, y_column='Time Duration', x_col='Protocol'):
    fig = px.violin(
        df, y=y_column, x=x_col,
        box=True, points="all",
        hover_data=df.columns
    )
    div = html.Div(dcc.Graph(figure=fig), className='d-flex justify-content-center')
    return div


# ===============================
# Time Serioes plot
# ===============================
def get_TS_fig(df, x_value='TS', y_value='Packets', group_by='Protocol'):
    df = df.copy()
    fig = px.line(df, x=x_value, y=y_value, color=group_by)
    fig.update_xaxes(
        rangeslider_visible=True,
         rangeselector=dict(
             buttons=list([
                 dict(count=3, label="3h", step="hour", stepmode="backward"),
                 dict(count=6, label="6h", step="hour", stepmode="backward"),
                 dict(count=12, label="12h", step="hour", stepmode="backward"),
                 dict(count=1, label="1d", step="day", stepmode="backward"),
                 dict(count=1, label="TD", step="day", stepmode="todate"),
                 dict(step="all")
             ])
         )
    )
    fig.update_layout(
        font=dict(
            family="Courier New",
            size=12,
            color="#7f7f7f"
        ),
        title_text=y_value)
    time_series_viz = dcc.Graph(figure=fig)
    time_series_div = html.Div(

        time_series_viz,
        className='container-fluid justify-content-center'
    )
    return time_series_div


def modify_ports(df, port_columns):
    df = df.copy()
    def aux(val):
        val = int(val)
        if val <= 1023:
            return val
        if val <= 49151:
            return "Reg. Port"
        else:
            return "Dynamic"

    for pc in port_columns:
        df[pc] = df[pc].parallel_apply(aux)
    df = df.sort_values(by=port_columns, ascending = True)
    return df


def get_viz_tab_1(data):
    df = data.copy()
    # List to store each Tab specific data in the  Tabs container
    tab_list = []
    # ===================================
    # 1. Source Port to Destination Port
    # ===================================
    # Group ports
    df_port_modified = modify_ports( df, port_columns=['Source Port', 'Destination Port'])
    columns = ['Source Port', 'Destination Port']
    fig = get_cat_plot(df_port_modified, columns)
    tab_1 = dcc.Tab(
        label='Port Communication',
        children=[html.Div(dcc.Graph(figure=fig), className='d-flex justify-content-center')]
    )
    tab_list.append(tab_1)
    # =====
    # 2. Source Port to Destination Port
    # =====
    fig = get_pie_chart(df, column='Protocol')
    tab_2 = dcc.Tab(
        label='Protocol Distribution',
        children=[html.Div(dcc.Graph(figure=fig), className='d-flex justify-content-center')]
    )
    tab_list.append(tab_2)

    tab_3 = dcc.Tab(
        label='Time duration of connections',
        children=[get_violin_plot_div(data)]
    )
    tab_4 = dcc.Tab(
        label='# of Packets',
        children=[get_violin_plot_div(data, y_column='Packets')]
    )
    tab_5 = dcc.Tab(
        label='# of Bytes',
        children=[get_violin_plot_div(data, y_column='Bytes')]
    )
    tab_list.append(tab_3)
    tab_list.append(tab_4)
    tab_list.append(tab_5)
    tab_container = dcc.Tabs(tab_list)
    tab_container = html.Div(
        tab_container,
        id="viz_tabs",
        className="mx-auto"
    )
    return tab_container
