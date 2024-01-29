import dash
from dash import html, dcc
from dash.dependencies import Input, Output, MATCH, State, ALL
from dash.exceptions import PreventUpdate
from dash import html, dcc, callback_context
from match_dashboard import *
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table
from helper import *
from modified_data import *
#Style 



app = dash.Dash(__name__)



# Initial layout for 'right-column' with general home page content
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
    }),
    html.Button('button for sophie', id='match_dashboard_button', style={
            'border': '1px solid blue',
            'fontSize': '20px',
            'color': 'blue',
            'width': '48%',  # Set width to 50%
            'margin': '10px auto',  # Auto margins horizontally to center the button
            'cursor': 'pointer',
    })], style={'width': '100%','text-align': 'center', 'display': 'flex', 'justify-content': 'space-between' }),
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


# Define the layout of the app with a 50% transparent background
app.layout = html.Div(
    id="app-container",
    children=initial_app_content,
    style={
        "fontFamily": "Arial, sans-serif",
        "width": "100%",
        "background": "rgba(255, 255, 255, 0.5) url('/fifa.jpg') no-repeat center center",
        "backgroundSize": "cover"
    }
)


# Main callback to update content
@app.callback(
    Output('app-container', 'children'),
    [Input({'type': 'team-button', 'index': ALL}, 'n_clicks'),
     Input('player-comparison-dashboard-button', 'n_clicks'),
     Input('match_dashboard_button', 'n_clicks')],
    prevent_initial_call=True)

def update_dashboard(team_button_clicks, player_comparison_dashboard_clicks, match_dashboard_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return initial_app_content

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'player-comparison-dashboard-button':
        player_options = get_player_names()
        return create_player_comparison_dashboard(player_options)
    
    if button_id == 'match_dashboard_button':
        return create_match_dashboard("Senegal", "Netherlands")



    elif 'team-button' in button_id:
        clicked_team = extract_team_name(ctx.triggered[0]['prop_id'])
        return create_team_dashboard(clicked_team)

    return initial_app_content



if __name__ == '__main__':
    app.run_server(debug=True)