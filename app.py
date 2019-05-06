import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go

# import dataframe class from data.py
from data import NBAData

# get data source
nba = NBAData()
data = nba.data

# dash setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# dash layout


if __name__ == '__main__':
    app.run_server(debug=True)
