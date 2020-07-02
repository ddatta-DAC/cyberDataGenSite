
import json
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objs as go
import os
from pathlib import Path

DATA_LOC = './PrefetchSaved/plotly_figures'
path = Path(DATA_LOC)
path.mkdir(exist_ok=True,parents=True)


def save_figure(figure_obj, figure_name=None):
    global DATA_LOC
    redata = json.loads(json.dumps(figure_obj.data, cls=PlotlyJSONEncoder))
    relayout = json.loads(json.dumps(figure_obj.layout, cls=PlotlyJSONEncoder))

    f_path = os.path.join(DATA_LOC, str(figure_name) + '.json')
    fig_json = json.dumps({'data': redata, 'layout': relayout})
    if f_path:
        with open(f_path, 'w') as f:
            f.write(fig_json)
    else:
        return fig_json


def plotlyfromjson(fpath):
    """Render a plotly figure from a json file"""
    with open(fpath, 'rb') as f:
        v = json.loads(f.read())
    fig = go.Figure(data=v['data'], layout=v['layout'])
    return fig


def fetch_figure(
        figure_name
):
    global DATA_LOC

    f_path = os.path.join(DATA_LOC, str(figure_name) + '.json')
    if os.path.exists(f_path):
        return plotlyfromjson(f_path)
    else:
        return None
