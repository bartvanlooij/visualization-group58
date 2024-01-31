from dash import html, dcc, dash_table, Input, Output, State, callback_context
import dash_daq as daq
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from shotmap import show_shot_on_map
from variables import data_folder
from initial_content import app
from momentum_distribution import *
#import matplotlib.pyplot as plt


shots1 = [2,4,7,20,25,40,59,62,89]
shots2 = [34,45,48,69,74,77,79,81,85]

df_shots = pd.DataFrame(data={'team1': shots1, 'team2': shots2})

def create_match_dashboard(home, away):
    # function generating the match dashboard 
    # match_data = process_match_data(home_team, away_team, match_data_csv)
    dashboard = html.Div([
        html.H2(f"{home} vs. {away}", style={'display': 'inline-block', 'margin-right': '10px', 'margin-top': '10px', 'margin-bottom': '10px'}),
        html.Div([column_match_statistics(shots1, shots2),
                  column_shot_dynamics(shots1, shots2)], 
                  style={'display': 'grid', 'grid-template-columns': '1fr 1fr'})])
    return dashboard

def column_match_statistics(home, away):
    return html.Div("hello")

def column_shot_dynamics(home, away):
    shotmap = create_shotmap(home, away)
    momentum_dist = create_momentum_distribution(False)
    return html.Div([dcc.Graph(figure=shotmap), dcc.Graph(figure=momentum_dist)])

#def create_momentum_distribution(home, away):
    fig = px.line(df_shots, x= 'team1', y= 'team2')
    return fig

def create_shotmap(home, away):
    fig = show_shot_on_map(False)
    return fig 

def create_match_stats(home, away):
    hi = 'hello'
    return hi

# @app.callback(
#     Output('home-switch-output', 'children'),
#     Input('home-away-switch', 'on')
# )
# def update_output(on):
#     return f'The switch is {on}.'

# daq.BooleanSwitch(id='home-away-switch', on=True, label='Home/Away'),
# html.Div(id='home-switch-output'),


#def process_match_data(team1, team2, match_data_csv):
    match_data = pd.read_csv(match_data_csv)
    selected_match = match_data[(match_data['home_team'] == team1) & (match_data['away_team'] == team2)]
    return selected_match

#def create_match_stats(home, away, match):
    match_stats = match[(match['home_team'] == home) & (match['away_team'] == away)].iloc[0]
    home_form = match_stats['home_formation']
    away_form = match_stats['away_formation']

    return home_form, away_form

#df_match = pd.read_csv(f'{data_folder}/match_data.csv')

#print(create_match_stats('Qatar', 'Ecuador', df_match))