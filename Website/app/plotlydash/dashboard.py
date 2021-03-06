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
from .dash_G1_layout import html_layout
import plotly.express as px

try:
    from . import plotly_fig_utils as plotly_utils
except:
    import plotly_fig_utils as plotly_utils


# =================================
# Main function
# =================================
def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/bootstrap_lux.min.css',
            dbc.themes.BOOTSTRAP,
            dbc.themes.LUX,
            '/static/dashapp_1.css',
        ],
        assets_folder='/static/assets',
        external_scripts=['/static/js/jquery-3.5.1.min.js','/static/js/dashapp_1.js']

    )

    # Custom HTML layout
    dash_app.index_string = html_layout

    # ========================================
    # Create  Time series plots
    # ========================================

    tab_list = []
    time_series_tab_dict = {
        'background': 'Background Data',
        'sshscan' : 'SSH Scan Netflows',
        'spam'  : 'Spam Attack Netflows '
    }

    ts_header_str = 'Time Series Visualization'
    ts_header = html.Div(
        children=ts_header_str,
        className='header text-center h3'
    )
    ts_data_str = "Time Series visualization of network flow helps understand the volume, frequency and velocity of traffic. " \
                " The X axis shows the time line of traffic and Y-axis shows the number of unidirectional network flows. " \
                " The 3 protocols that are present are TCP (Tranfer Control Protocol), UDP (User Datagram Protocol) and ICMP (Internet Control Message Protocol)."

    ts_preamble =  html.Div(
        html.P(children=ts_data_str),
        className='preamble',
        id="ts_header_desc"
    )

    fig_idx = 1
    for _type,_label in time_series_tab_dict.items():
        data = read_data(_type)
        time_series_count = get_TS_fig_v2(figure_id=fig_idx, df=data, group_by='Protocol')
        fig_idx += 1

        tab_element = dcc.Tab(
            label= _label,
            children=[
                time_series_count
            ]
        )
        tab_list.append(tab_element)

    ts_header_div = html.Div([ts_header, ts_preamble])
    tab_container = dcc.Tabs(tab_list)


    TimeSeries_tab_container = html.Div(
        [ts_header_div, tab_container],
        id="ts_tabs",
        className="mx-auto"
    )

    data_stats_str = "SSH stands for Secure Socket Shell." \
                     " SSH Scan attacks are brute force attacks where attackers try to guess the victims credentials. It is a brute force attack." \
                     " Spam is any kind of unwanted, unsolicited digital communication that gets sent out in bulk." \
                     " Spam attacks are include sttacks such as phising and SMTP email attacks." \
                     " Data statistics can help understand the characteristics of flow traffic. " \
                     " Traffic patterns pertaining to attacks have signatures which need to be understood to help in detecting such attacks."

    data_stats_preamble = html.Div(html.P(children=data_stats_str), className='preamble')


    # ========================================
    # Create a visualization tab
    # ========================================
    tab_obj_1 = get_viz_tab_1(_type='background')
    tab_obj_2 = get_viz_tab_1(_type='sshscan')
    tab_obj_3 = get_viz_tab_1(_type='spam')
    dash_app.layout = html.Div(
        children=[

            TimeSeries_tab_container,
            html.Hr(),
            data_stats_preamble,
            tab_obj_1,
            tab_obj_2,
            tab_obj_3,
            create_data_table(_type='background'),
            create_data_table(_type='sshscan'),
            create_data_table(_type='spam')
        ],
        id='dash-container',
        className="container-fluid mr-4"
    )
    # ===========
    #
    # ============



    return dash_app.server

def read_data(
        _type = 'background',
        _size = 100000
):
    DATA_LOC = './../data/Processed'
    if type is None:
        pass
    import glob

    files = list(glob.glob( os.path.join( DATA_LOC, _type + '**','**.csv') ))
    files += list(glob.glob( os.path.join( DATA_LOC, _type + '*.csv')))

    df = None

    for file in sorted(files):
        _df = pd.read_csv(file, index_col=None)
        if df is None:
            df =_df
        else:
            df = df.append(_df, ignore_index=True)

    df = df.rename(columns={
        'sp': 'Source Port',
        'dp': 'Destination Port',
        'pr': 'Protocol',
        'byt': 'Bytes',
        'pkt': 'Packets',
        'td': 'Time Duration',
        'TS': 'TimeStamp',
        'sa': 'Source Address',
        'da': 'Destination Address',
        'label': 'Label'
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
        'Time Duration',
        'Label'
    ]
    df = df[columns]
    if _size < len(df):
        df = df.sample( _size )
    return df

def create_data_table(_type):
    """
    Create Dash datatable from Pandas DataFrame.
    """
    columns = [
        'TimeStamp',
        'Source Address',
        'Source Port',
        'Destination Port',
        'Destination Address',
        'Protocol',
        'Bytes',
        'Packets',
        'Time Duration',
        'Label'
    ]
    # -----------------
    # Read in data
    # -----------------

    df = read_data(_type)
    df = df[columns]

    table = dash_table.DataTable(
        id='database-table_'+_type,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        page_size=25,
        style_table={'height': '300px', 'overflowY': 'auto','overflowX': 'auto'},
        style_data={'border': '1px solid blue'},
        fixed_rows={'headers': True},
        style_header={
            'border': '2px solid',
            'fontsize': '2.5rem',
            'backgroundColor': 'rgb(1, 36, 34)',
            'color': 'rgb(255, 255, 255)'
        },
        style_cell={
            'minWidth': 50, 'maxWidth': 55, 'width': 52
        },
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Label} = background',
                    'column_id': 'Label'
                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                      'filter_query': '{Label} = anomaly-sshscan',
                      'column_id': 'Label'
                },
                'backgroundColor': 'red',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{Label} = anomaly-spam',
                    'column_id': 'Label'
                },
                'backgroundColor': 'red',
                'color': 'white'
            }
        ]
    )
    table = html.Div(
        table,
        className='border border-100'
    )
    type_str = get_display_string(_type)
    header_label = ' Data Table :: ' + type_str
    header = html.Div(
        html.P(header_label),
        className="text-center h3"
    )
    table = html.Div(
        [header, table],
        className="dash_table text-center"
    )
    return table


def fetch_network_data_v1():
    DATA_LOC = './../data/Processed/data_2016-04-12.csv'
    df = pd.read_csv(DATA_LOC, index_col=None)
    df = df.rename(columns={
        'sp': 'Source Port',
        'dp': 'Destination Port',
        'pr': 'Protocol',
        'byt': 'Bytes',
        'pkt': 'Packets',
        'td': 'Time Duration',
        'TS': 'TimeStamp',
        'sa': 'Source Address',
        'da': 'Destination Address',
        'label' : 'Label'
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
# Time Series plot
# ===============================

def get_TS_fig(figure_id, df, x_value='TimeStamp', y_value='Packets', group_by='Protocol'):
    fig = plotly_utils.fetch_figure(figure_id)
    if fig is None:
        print('Figure not saved', file=sys.stdout)
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
        plotly_utils.save_figure(fig, figure_name=figure_id)

    time_series_viz = dcc.Graph(figure=fig)
    time_series_div = html.Div(
        time_series_viz,
        className='container-fluid justify-content-center'
    )
    return time_series_div


def get_TS_fig_v2(figure_id, df, x_value='TimeStamp',  group_by='Protocol'):
    fig = plotly_utils.fetch_figure(figure_id)
    if fig is None:
        print('Figure not saved', file=sys.stdout)
        df = df.copy()

        # Modify as count
        df = df.groupby(['TimeStamp',group_by]).size().reset_index(name="count")
        y_value = "count"
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
        plotly_utils.save_figure(fig, figure_name=figure_id)

    time_series_viz = dcc.Graph(figure=fig)

    time_series_div = html.Div([
        time_series_viz],
        className='container-fluid justify-content-center'
    )
    return time_series_div

# =======================
# An utility function
# =======================
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


# =======================================
# Create tabbed entries
# The design is hardcoded
# =======================================
def get_viz_tab_1(_type='background'):

    data = read_data(_type, _size=10000)
    # List to store each Tab specific data in the  Tabs container
    tab_list = []


    # =====
    # 2. Source Port to Destination Port
    # =====
    fig = get_pie_chart(data, column='Protocol')
    tab_2 = dcc.Tab(
        label='Protocol Distribution',
        children=[html.Div(dcc.Graph(figure=fig), className='d-flex justify-content-center')]
    )

    tab_3 = dcc.Tab(
        label='Time duration of connections',
        children=[get_violin_plot_div(data,y_column='Time Duration')]
    )
    tab_4 = dcc.Tab(
        label='# of Packets',
        children=[get_violin_plot_div(data, y_column='Packets')]
    )
    tab_5 = dcc.Tab(
        label='# of Bytes',
        children=[get_violin_plot_div(data, y_column='Bytes')]
    )
    # ===================================
    # 1. Source Port to Destination Port
    # ===================================
    # Group ports
    figure_id = 'source_dest_port_'+_type
    fig_obj = plotly_utils.fetch_figure(figure_id)
    if fig_obj is None:
        df_port_modified = modify_ports(data, port_columns=['Source Port', 'Destination Port'])
        columns = ['Source Port', 'Destination Port']
        fig_obj = get_cat_plot(df_port_modified, columns)
        plotly_utils.save_figure(fig_obj,figure_id)

    tab_1 = dcc.Tab(
        label='Port Communication',
        children=[html.Div(dcc.Graph(figure=fig_obj), className='d-flex justify-content-center')]
    )

    tab_list.append(tab_3)
    tab_list.append(tab_4)
    tab_list.append(tab_5)
    tab_list.append(tab_2)
    tab_list.append(tab_1)

    header_label = ' Data Statistics :: ' + get_display_string(_type)
    header = html.Div(
        html.P(header_label),
        className="text-center h3"
    )

    tab_container = dcc.Tabs(tab_list)
    tab_container = html.Div(
        tab_container,
        id="viz_tabs_"+_type,
        className="mx-auto"
    )

    tab_container = html.Div(
        [html.Hr(), header, tab_container],
        className="dash_table text-center"
    )

    return tab_container


def get_display_string(_type):
    if _type=='background':
        return 'Background Traffic'
    if _type=='sshscan':
        return 'SSH Scan Traffic'
    if _type=='spam':
        return 'Spam Attack Traffic'
