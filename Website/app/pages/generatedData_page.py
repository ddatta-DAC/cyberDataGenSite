import sys
import csv
import plotly
import plotly.graph_objs as go

import pandas as pd
import plotly.express as px
import math
import pandas as pd
import numpy as np
import json

from flask import Flask, render_template

app = Flask(__name__)

sys.path.append('./..')
sys.path.append('./../..')

from flask import render_template


def create_scatter_sa_da(df):
    data0 = [
        go.Scatter(
            x=df['sa'],
            y=df['da'],
            text=df['IP'],
            mode='markers'
        )
    ]
    fig0 = go.Figure(data0)
    fig0.update_xaxes(title_text='Count as Starting Address')
    fig0.update_yaxes(title_text='Count as Destination Address')

    fig0.update_layout(
        autosize=False,
        height=1000,
        width=1000,
        title_text='Count of NetFlows for Each User as Starting Address and Destination Address'
        )
    
    graphJSON = json.dumps(fig0, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_horizontal_barchart_gr(df):
    data1 = [
        go.Bar(
            name='TCP',
            y=df["IP"],
            x=df["TCP"],
            orientation='h'),
        go.Bar(
            name='UDP',
            y=df["IP"],
            x=df["UDP"],
            orientation='h'),
        go.Bar(
            name='ICMP',
            y=df["IP"],
            x=df["ICMP"],
            orientation='h')
    ]
    fig1 = go.Figure(data1)
    fig1.update_layout(
        barmode='stack',
        autosize=False,
        height=1800,
        width=1200,
        title_text='Count of NetFlows for Each User in Each Transport Protocol'
        )
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON1


def create_hist(l_tcp, l_udp, l_icmp, text, text1):
    data2 = [
        go.Histogram(
            name='TCP',
            x=[math.log10(float(a)) for a in l_tcp]
        ),
        go.Histogram(
            name='UDP',
            x=[math.log10(float(a)) for a in l_udp]
        ),
        go.Histogram(
            name='ICMP',
            x=[math.log10(float(a)) for a in l_icmp]
        )
    ]
    fig2 = go.Figure(data2)
    fig2.update_layout(
        autosize=False,
        barmode='overlay',
        height=1000,
        width=1000,
        title_text=text
        )
    fig2.update_traces(opacity=0.75)
    fig2.update_yaxes(title_text='Count of NetFlows')
    fig2.update_xaxes(title_text=text1)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON2



def render():
    # --------------------
    # read in List of IPs
    # --------------------
    with open("./../data/MainData/Processed/VALID_IP_LIST.txt", "r") as fh:
        ip_list = fh.readlines()
    ip_list = [ip.strip('\n') for ip in ip_list]
    sys.stdout.flush()

    _dict = {
        'IP_List': ip_list
    }
    
    with open("./../data/MainData/Processed/VALID_IP_LIST.txt", "r") as fh:
        ip_list = fh.readlines()
    ip_list = [ip.strip('\n') for ip in ip_list]
    df_gen_da = pd.read_csv('./../data/MainData/Processed/summarized/gen_da.csv',
                            names=["IP", "da"])
    df_gen_da = df_gen_da[df_gen_da["IP"].isin(ip_list)]
    df_gen_sa = pd.read_csv('./../data/MainData/Processed/summarized/gen_sa.csv',
                            names=["IP", "sa"])
    df_gen_sa = df_gen_sa[df_gen_sa["IP"].isin(ip_list)]
    df0 = df_gen_da.join(df_gen_sa .set_index('IP'), on='IP')
    
#    bar_ts_byt = create_bar_ts_byt(df)
#    pie_pr = create_pie_pr(df)
#    scatter_teDelta_td = create_scatter_teDelta_td(df) 
    scatter_sa_da = create_scatter_sa_da(df0)


    df_gen_pr_tcp = pd.read_csv('./../data/MainData/Processed/summarized/gen_pr_tcp.csv',
                                names=["IP", "TCP"])
    df_gen_pr_tcp = df_gen_pr_tcp[df_gen_pr_tcp["IP"].isin(ip_list)]
    df_gen_pr_udp = pd.read_csv('./../data/MainData/Processed/summarized/gen_pr_udp.csv',
                                names=["IP", "UDP"])
    df_gen_pr_udp = df_gen_pr_udp[df_gen_pr_udp["IP"].isin(ip_list)]
    df_gen_pr_icmp = pd.read_csv('./../data/MainData/Processed/summarized/gen_pr_icmp.csv',
                                 names=["IP", "ICMP"])
    df_gen_pr_icmp = df_gen_pr_icmp[df_gen_pr_icmp["IP"].isin(ip_list)]
    df1 = df_gen_pr_tcp.join(
        df_gen_pr_udp.set_index('IP'), on='IP').join(
            df_gen_pr_icmp.set_index('IP'), on='IP')

    horizontal_barchart_gr = create_horizontal_barchart_gr(df1)


    with open('./../data/MainData/Processed/summarized/gen_td_tcp.csv', newline='') as f:
        reader = csv.reader(f)
        l_td_tcp = next(reader)
    with open('./../data/MainData/Processed/summarized/gen_td_udp.csv', newline='') as f:
        reader = csv.reader(f)
        l_td_udp = next(reader)
    with open('./../data/MainData/Processed/summarized/gen_td_icmp.csv', newline='') as f:
        reader = csv.reader(f)
        l_td_icmp = next(reader)
    hist_td = create_hist(l_td_tcp, l_td_udp, l_td_icmp,
                          'Distribution of Time Duration (Stacked Histogram)', 'Time Duration in Log10 of Seconds')


    with open('./../data/MainData/Processed/summarized/gen_byt_tcp.csv', newline='') as f:
        reader = csv.reader(f)
        l_byt_tcp = next(reader)
    with open('./../data/MainData/Processed/summarized/gen_byt_udp.csv', newline='') as f:
        reader = csv.reader(f)
        l_byt_udp = next(reader)
    with open('./../data/MainData/Processed/summarized/gen_byt_icmp.csv', newline='') as f:
        reader = csv.reader(f)
        l_byt_icmp = next(reader)
    hist_byt = create_hist(l_byt_tcp, l_byt_udp, l_byt_icmp,
                           'Distribution of Bytes Transferred (Stacked Histogram)','Log10 of Bytes')
    
    with open('./../data/MainData/Processed/summarized/gen_pkt_tcp.csv', newline='') as f:
        reader = csv.reader(f)
        l_pkt_tcp = next(reader)
    with open('./../data/MainData/Processed/summarized/gen_pkt_udp.csv', newline='') as f:
        reader = csv.reader(f)
        l_pkt_udp = next(reader)
    with open('./../data/MainData/Processed/summarized/gen_pkt_icmp.csv', newline='') as f:
        reader = csv.reader(f)
        l_pkt_icmp = next(reader)
    hist_pkt = create_hist(l_pkt_tcp, l_pkt_udp, l_pkt_icmp,
                           'Distribution of Packets Transferred (Stacked Histogram)','Log10 of Packets')
    
    return render_template('generatedData_page.html', **_dict,
                           plot0=scatter_sa_da,
                           plot1=horizontal_barchart_gr,
                           plot2=hist_td,
                           plot3=hist_byt,
                           plot4=hist_pkt)

