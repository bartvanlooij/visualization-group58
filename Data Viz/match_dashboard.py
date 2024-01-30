from dash import html, dcc, dash_table, Input, Output, State, callback_context
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from shotmap import show_shot_on_map

def create_match_dashboard(home_team, away_team):
    # function generating the match dashboard 
    # match_data = process_match_data(home_team, away_team, match_data_csv)
    print("hello")
    return html.Div([
        html.H2(f"{home_team} vs. {away_team}", style={'display': 'inline-block', 'margin-right': '10px', 'margin-top': '10px', 'margin-bottom': '10px'}),
        html.Div(dcc.Graph(figure=show_shot_on_map(False)))])

def process_match_data(team1, team2, match_data_csv):
    match_data = pd.read_csv(match_data_csv)
    selected_match = match_data[(match_data['home_team'] == team1) & (match_data['away_team'] == team2)]
    return selected_match
