from dash import html, dcc
import pandas as pd
from jbi100_app.modified_data import *
from variables import data_folder
from create_player_data import *
from dash import Dash
df_teams = pd.read_csv(f'{data_folder}/group_stats.csv')
team_data_csv = f'{data_folder}/team_data.csv'

app = Dash('FIFA World Cup 2022')


def create_accordion(df_teams):
    accordion = []
    for group in sorted(df_teams['group'].unique()):
        teams_in_group = df_teams[df_teams['group'] == group]
        details = html.Details([
            html.Summary(f'Group {group}', style={
                'fontSize': '24px',
                'fontWeight': 'bold',
                'color': 'blue'
            }),
            html.Div([
                # Ensure each team is a clickable button with a unique id
                html.Button(team, id={'type': 'team-button', 'index': team}, style={
                    'display': 'block',  # Changed to block to ensure full width
                    'padding': '5px',
                    'borderBottom': '1px solid blue',
                    'fontSize': '20px',
                    'color': 'black',
                    'textAlign': 'center',  
                    'background-color': 'transparent',  
                    'border': 'none',  
                    'width': '100%', 
                    'text-align': 'center' 
                }) for team in teams_in_group['team']
            ], style={'padding': '10px'})
        ], style={
            'width': '100%',
            'marginBottom': '10px',
            'border': '1px solid blue'
        })
        accordion.append(details)
    return accordion


def top_scoring_players_modified():
    df = df_players 
    top_scorers = df.sort_values(by='goals', ascending=False).head(10)
    # Create a bar chart using Plotly
    fig = px.bar(top_scorers, x='player', y='goals', 
                 title="Top 10 Scoring Players", 
                 labels={'player': 'Player', 'goals': 'Goals Scored'})
    fig.update_layout(xaxis_title="Player",
                      yaxis_title="Goals Scored",
                      xaxis={'categoryorder':'total descending'},)
    return fig



group_accordions = create_accordion(df_teams)
initial_app_content = html.Div([
    html.H1("FIFA World Cup 2022", style={'textAlign': 'center'}),
    html.H2("Teams", style={'textAlign': 'center'}),
    html.Div([
        html.Div(group_accordions[:4], style={
            'text-align': 'center',
            'width': '48%',
            'float': 'left',  
            'display': 'inline-block',
            'paddingRight': '10px',
        }),
        html.Div(group_accordions[4:], style={
            'text-align': 'center',
            'width': '48%',
            'float': 'right',
            'display': 'inline-block',
            'paddingLeft': '10px',
        }),
    ], style={'padding': '20px'}),
    
    html.Div([
        html.Button('Player Comparison Dashboard', id='player-comparison-dashboard-button', style={
            'border': '1px solid blue',
            'fontSize': '20px',
            'color': 'blue',
            'width': '48%',  # Set width to 50%
            'margin': '10px auto',  # Auto margins horizontally to center the button
            'cursor': 'pointer',
    })], style={'width': '96%','text-align': 'center', 'display': 'inline-block', }),
    html.Div([
        html.Button('Playoff Bracket', id='playoff-bracket-button', style={
            'border': '1px solid blue',
            'fontSize': '20px',
            'color': 'blue',
            'width': '48%',  # Set width to 50%
            'margin': '10px auto',  # Auto margins horizontally to center the button
            'cursor': 'pointer',
    })], style={'width': '96%','text-align': 'center', 'display': 'inline-block', }),
    # New row for the three graphs
    html.Div([
        html.Div([
            dcc.Graph(figure=top_scoring_teams(load_team_data(team_data_csv)))
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            dcc.Graph(figure=best_defensive_teams(load_team_data(team_data_csv)))
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '5px'}),
        html.Div([
            dcc.Graph(figure=top_scoring_players_modified())
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '5px'}),
    ], style={'width': '100%', 'display': 'flex', 'justify-content': 'space-between'}),
])

#df = pd.read_csv('player_stats.csv').groupby('club', as_index=False).sum().sort_values('minutes_90s')
#px.bar(df.tail(10), x='club', y='minutes_90s')