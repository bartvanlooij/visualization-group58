from dash import html, dcc, dash_table, Input, Output, State, callback_context
import dash_daq as daq
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from shotmap import show_shot_on_map
from variables import data_folder
from initial_content import app
from momentum_distribution import *
from api_connection import * 

#import matplotlib.pyplot as plt


shots1 = [2,4,7,20,25,40,59,62,89]
shots2 = [34,45,48,69,74,77,79,81,85]

df_shots = pd.DataFrame(data={'team1': shots1, 'team2': shots2})

def create_match_dashboard(match_id):
    match = client.get_match_details(match_id)
    # function generating the match dashboard 
    # match_data = process_match_data(home_team, away_team, match_data_csv)
    dashboard = html.Div([
        html.H2(f"{match['general']['homeTeam']['name']} vs. {match['general']['awayTeam']['name']}", style={'display': 'inline-block', 'margin-right': '10px', 'margin-top': '10px', 'margin-bottom': '10px'}),
        html.Div([column_match_statistics(match),
                  column_shot_dynamics(match)], 
                  style={'display': 'grid', 'grid-template-columns': '3fr 2fr', 'grid-gap': '50px'})],
        style={'padding': '0 80px'})
    return dashboard

def column_match_statistics(match):
    stats = create_match_stats(match)
    return html.Div([html.H3("Match statistics"),
                     stats])

def column_shot_dynamics(match, on=True):
    momentum_dist = create_momentum_distribution(match)
    return html.Div([html.Div([# hack to store match state
                               dcc.Input(id="match", type="text", value=match, style={"display": "none"}),
                               html.H3("Shotmap"), 
                               html.Div(id="shotmap"),
                               daq.BooleanSwitch(id="home-away-shotmap", on=True, style={"width": "min-content"})]),
                     html.Div([html.H3("Momentum"), dcc.Graph(figure=momentum_dist)])])


@app.callback(
    Output('shotmap', 'children'),
    State('match', 'value'),
    Input('home-away-shotmap', 'on')
)
def update_output(match, on):
    label = 'Home' if on else 'Away'
    return [dcc.Graph(figure=create_shotmap(match, on)),
            html.Span(label, style={'font-size': '14px'})]
   
#def create_momentum_distribution(home, away):
    #fig = px.line(df_shots, x= 'team1', y= 'team2')
    #return fig

def create_shotmap(match, on):
    homePlayers, awayPlayers = get_player_data(match)
    homePlayers = [parse_api_results(x) for x in homePlayers]
    awayPlayers = [parse_api_results(x) for x in awayPlayers]
    
    if on:
        fig = show_shot_on_map(homePlayers)
    
    else:
        fig = show_shot_on_map(awayPlayers)

    return fig 

def create_match_stats(match):
    df1 = pd.json_normalize(match['content']['stats']['Periods']['All']['stats'][0]['stats'])
    df1[['home', 'away']] = pd.DataFrame(df1['stats'].tolist(), index= df1.index)
    df = df1[['title', 'home', 'away']]

    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    return table

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