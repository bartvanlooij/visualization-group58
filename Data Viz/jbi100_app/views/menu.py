from dash import dcc, html
import pandas as pd

# Assuming team_data.csv is in the same directory as your script
team_data_csv = 'team_data.csv'

def generate_description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Select a Team:"),
        ],
    )

def generate_control_card():
    team_data = pd.read_csv(team_data_csv)
    teams = team_data['team'].unique()

    return html.Div(
        id="control-card",
        children=[
            dcc.Dropdown(
                id='team-selector',
                options=[{'label': team, 'value': team} for team in teams],
                value=teams[0]
            ),
            html.Button('Select', id='select-team-button'),
            html.Button('Player Comparison', id='player-comparison-button'),
            html.Button('Home', id='home-button')  # New Home button
        ], style={"textAlign": "float-left"}
    )

def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
