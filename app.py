import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

# import dataframe class from data.py
from data import NBAData

# constants
MIN_ATTEMPTS = 50

# get data source
nba = NBAData()
data = nba.mid_range_data
distances = nba.mid_range_distances
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
    ]),

    # graph object
    html.Div(children=[
        dcc.Graph(id='fg-percent'),
        html.Div(),
        dcc.Graph(id='points-per-ten')
    ])
])


@app.callback(
    [Output('fg-percent', 'figure'),
     Output('points-per-ten', 'figure')],
    [Input('player-selector', 'value')]
)
def update_graphs(player):
    # copy data for encapsulation
    my_data = data.copy().set_index('PLAYER_NAME')

    # base trace lists
    traces_fg = []
    traces_pp10 = []

    # layout titles
    titles = {
        'fg': '2018-2019 NBA Mid-Range FG%',
        'pp10': '2018-2019 NBA Expected Point / 10 Shots',
    }

    # generate colors
    colors = [f'hsl({str(h)}, 50%, 50%)' for h in np.linspace(0, 200, len(distances))]

    for c, d in zip(colors, distances):
        # get appropriate columns
        cols = [col for col in my_data.columns if d in col]
        data_ = my_data[my_data[f'FGA: {d}'] > MIN_ATTEMPTS][cols]

        # field goal traces
        traces_fg.append(
            go.Box(
                y=data_[f'FG_PCT: {d}'].to_numpy(),
                name=d,
                # boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=c,
                marker=dict(
                    size=2,
                ),
                line=dict(width=1)
            )
        )

        # points per 10 traces
        traces_pp10.append(
            go.Box(
                y=data_[f'PP10: {d}'].to_numpy(),
                name=d,
                # boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=c,
                marker=dict(
                    size=2,
                ),
                line=dict(width=1)
            )
        )
    layout_fg = go.Layout(
        title=titles['fg'],
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=.05,
            gridcolor='white',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(233,233,233)',
        plot_bgcolor='rgb(233,233,233)',
        showlegend=True
    )

    layout_pp10 = go.Layout(
        title=titles['pp10'],
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=.5,
            gridcolor='white',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(233,233,233)',
        plot_bgcolor='rgb(233,233,233)',
        showlegend=True
    )

    fg = go.Figure(data=traces_fg, layout=layout_fg)
    pp10 = go.Figure(data=traces_pp10, layout=layout_pp10)
    return fg, pp10


if __name__ == '__main__':
    app.run_server(debug=True)
