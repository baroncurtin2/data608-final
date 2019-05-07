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
players = [{'label': p, 'value': p} for p in nba.player_names]

# dash setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# dash layout
app.layout = html.Div(children=[
    html.H1('NBA Best Mid-Range Shooters'),

    html.Div(children=[
        html.H5('Player Name'),

        dcc.Dropdown(
            id='player-selector',
            options=players,
            value=players[0]['value']
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
