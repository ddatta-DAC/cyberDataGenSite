"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import os
import sys
from pandarallel import pandarallel
from dash.dependencies import Input, Output, State
import glob

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
        if pathname is not None:
            _ip = validate_ip(pathname.split('/')[-1])
        else:
            _ip = None

        if _ip is None:
            return html.Div([
                html.Div('Set IP ')
            ])
        else:
            return build_page(_ip)

    return dash_app.server


# ==========================
# Main layout creator
# ==========================
def build_page(IP):
    df_r, df_g = read_data(IP)


    time_series_div_r_P = get_TS_fig(
        figure_id = IP + '_ts_P_' + str(1),
        df = df_r,
        x_value='TimeStamp',
        y_value='Packets',
        label = 'Real Data'
    )

    time_series_div_g_P = get_TS_fig(
        figure_id= IP + '_ts_P_' +  str(2),
        df=df_g,
        x_value='TimeStamp',
        y_value='Packets',
        label='Generated Data'
    )

    time_series_div_r_B = get_TS_fig(
        figure_id=IP + '_ts_B_' + str(1),
        df=df_r,
        x_value='TimeStamp',
        y_value='Bytes',
        label='Real Data',
        line_color = 'blue'
    )

    time_series_div_g_B = get_TS_fig(
        figure_id=IP + '_ts_B_' + str(2),
        df=df_g,
        x_value='TimeStamp',
        y_value='Bytes',
        label='Generated Data',
        line_color='blue'
    )
    viz_tab = get_viz_tab(df_r, df_g, IP)

    page_content = html.Div([
        html.Div('User IP {}'.format(IP)),
        time_series_div_r_P,
        time_series_div_g_P,
        time_series_div_r_B,
        time_series_div_g_B,
        viz_tab
    ])
    return page_content

# ====
# Auxillary functions
# ====
def validate_ip(_str):
    import re
    pattern = '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
    res = re.search(pattern, _str)
    if res is None:
        return None
    else:
        return res[0]


def read_data(
        IP
):
    DATA_LOC = './../data/MainData/Processed/'
    file_r = list(glob.glob(os.path.join(DATA_LOC, 'real', IP + '.csv')))[0]
    file_g = list(glob.glob(os.path.join(DATA_LOC, 'generated', IP + '.csv')))[0]

    df_g = pd.read_csv(file_g, index_col=None)
    df_r = pd.read_csv(file_r, index_col=None)

    df_g = df_g.rename(columns={
        'TS': 'TimeStamp',
        'sp': 'Source Port',
        'dp': 'Destination Port',
        'sa': 'Source Address',
        'da': 'Destination Address',
        'pr': 'Protocol',
        'byt': 'Bytes',
        'pkt': 'Packets',
        'td': 'Time Duration',

    })
    df_r = df_r.rename(columns={
        'TS': 'TimeStamp',
        'sp': 'Source Port',
        'dp': 'Destination Port',
        'sa': 'Source Address',
        'da': 'Destination Address',
        'pr': 'Protocol',
        'byt': 'Bytes',
        'pkt': 'Packets',
        'td': 'Time Duration',
    })
    columns = [
        'TimeStamp',
        'Source Address',
        'Source Port',
        'Destination Port',
        'Destination Address',
        'Protocol',
        'Bytes',
        'Packets',
        'Time Duration'
    ]
    df_r = df_r[columns]
    df_g = df_g[columns]
    print( ' {}   {}  '.format(len(df_r),len(df_g)),file=sys.stdout)
    # df_r = df_r.sample(1000)
    # df_g = df_g.sample(1000)

    return df_r, df_g

def get_TS_fig(
        figure_id,
        df,
        x_value='TimeStamp',
        y_value='Packets',
        label = None,
        line_color = 'red'
):
    fig = plotly_utils.fetch_figure(figure_id)
    if fig is None:
        print('Figure not saved', file=sys.stdout)
        df = df.copy()

        fig = px.line(
            df,
            x=x_value,
            y=y_value
        )
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
        plotly_utils.save_figure(fig, figure_name=figure_id)

    time_series_viz = dcc.Graph(figure=fig)
    label_div = html.Div(
        [html.H3(label)]
    )
    time_series_div = html.Div([
        label_div,
        time_series_viz
    ],
        className='container-fluid justify-content-center'
    )
    return time_series_div

# ============================
# Visualize Tab
# ============================
def get_viz_tab(df_r, df_g ,IP):

    # List to store each Tab specific data in the  Tabs container
    tab_list = []

    # =====
    # 2. Source Port to Destination Port
    # =====
    fig_1 = get_pie_chart(df_r, column='Protocol')
    fig_2 = get_pie_chart(df_g, column='Protocol')
    fig_1_div = html.Div(
        [html.H4('Real Data'), dcc.Graph(figure=fig_1) ],
        className="col"
    )
    fig_2_div = html.Div(
        [html.H4('Generated Data'),  dcc.Graph(figure=fig_2)],
        className="col"
    )
    fig_div = html.Div(
        [
            fig_1_div, fig_2_div
        ],
        className="row"
    )

    tab_1 = dcc.Tab(
        label='Protocol Distribution',
        children=[ fig_div ]
    )
    # ------------------------------------
    # Violin plot of Time duration
    # ------------------------------------
    fig_1 = get_violin_plot_div(df_r, y_column='Time Duration')
    fig_2 = get_violin_plot_div(df_g, y_column='Time Duration')

    fig_1_div = html.Div(
        [html.H4('Real Data'), fig_1],
        className="col"
    )

    fig_2_div = html.Div(
        [html.H4('Generated Data'),fig_2],
        className="col"
    )
    fig_div = html.Div(
        [ fig_1_div, fig_2_div ],
        className="row"
    )

    tab_2 = dcc.Tab(
        label='Time duration of connections',
        children=[fig_div]
    )

    # -------------------------------------
    # tab_4 = dcc.Tab(
    #     label='# of Packets',
    #     children=[get_violin_plot_div(data, y_column='Packets')]
    # )
    # tab_5 = dcc.Tab(
    #     label='# of Bytes',
    #     children=[get_violin_plot_div(data, y_column='Bytes')]
    # )

    # ===================================
    # 1. Source Port to Destination Port
    # ===================================
    # Group ports
    df_r_port_modified = modify_ports(df_r, port_columns=['Source Port', 'Destination Port'])
    df_g_port_modified = modify_ports(df_g, port_columns=['Source Port', 'Destination Port'])

    figure_id = 'source_dest_port_R_' + IP
    fig_obj_r = plotly_utils.fetch_figure(figure_id)
    if fig_obj_r is None:
        columns = ['Source Port', 'Destination Port']
        fig_obj_r = get_cat_plot(df_r_port_modified, columns)
        plotly_utils.save_figure(fig_obj_r, figure_id)

    figure_id = 'source_dest_port_G_' + IP
    fig_obj_g = plotly_utils.fetch_figure(figure_id)

    if fig_obj_g is None:
        columns = ['Source Port', 'Destination Port']
        fig_obj_g = get_cat_plot(df_g_port_modified, columns)
        plotly_utils.save_figure(fig_obj_g, figure_id)
    fig_1 = dcc.Graph(figure=fig_obj_r)
    fig_2 = dcc.Graph(figure=fig_obj_g)

    fig_1_div = html.Div(
        [html.H4('Real Data'), fig_1],
        className="col"
    )

    fig_2_div = html.Div(
        [html.H4('Generated Data'), fig_2],
        className="col"
    )

    fig_div = html.Div(
        [fig_1_div, fig_2_div],
        className="row"
    )

    tab_3 = dcc.Tab(
        label='Port Communication',
        children=[fig_div]
    )

    # tab_list.append(tab_3)
    # tab_list.append(tab_4)
    # tab_list.append(tab_5)
    tab_list.append(tab_1)
    tab_list.append(tab_2)
    tab_list.append(tab_3)

    header_label = ' Data Statistics '
    header = html.Div(
        html.P(header_label),
        className="text-center h3"
    )

    tab_container = dcc.Tabs(tab_list)
    tab_container = html.Div(
        tab_container,
        id="viz_tabs",
        className="mx-auto"
    )

    tab_container = html.Div(
        [html.Hr(), header, tab_container],
        className="dash_table text-center"
    )

    return tab_container


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


def get_violin_plot_div(df, y_column='Time Duration', x_col='Protocol'):
    fig = px.violin(
        df, y=y_column, x=x_col,
        box=True, points="all",
        hover_data=df.columns
    )

    return dcc.Graph(figure=fig)

def modify_ports(df, port_columns):
    df = df.copy()

    def aux(val):
        val = int(val)
        if val <= 1023:
            return 'System Port'
        if val <= 49151:
            return "Reg. Port"
        else:
            return "Dynamic"

    for pc in port_columns:
        df[pc] = df[pc].parallel_apply(aux)
    df = df.sort_values(by=port_columns, ascending=True)
    return df


# =================================
# Sankey like categorical parallel axis plot
# =================================
def get_cat_plot(df, columns):
    df = df.copy()
    df_1 = df[columns]
    df_1 = df_1.groupby(columns).size().reset_index(name='count')

    fig = px.parallel_categories(
        df_1,
        dimensions=columns,
        color="count",
        color_continuous_scale=px.colors.sequential.Pinkyl,

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