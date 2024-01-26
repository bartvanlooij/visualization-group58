from dash import html, dcc, dash_table, Input, Output, State, callback_context
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modified_data import *

def create_team_dashboard(team_name):
    
    # Function that creates and returns the team-specific dashboard
    team_data = process_team_data(team_name, match_data_csv)
    team_performance_chart = create_team_performance_chart(team_data, team_name)
    home_chart, away_chart = create_average_specifics_chart(team_data)
    
    if team_name not in df_teams['team'].unique():
        print(f"Invalid team name: {team_name}")
        return html.Div("Invalid team selection.")
    
    else:
        return html.Div([
            # Modified section to include the home button
    html.Div([
        html.H2(f"{team_name} Dashboard", style={'display': 'inline-block', 'margin-right': '10px', 'margin-top': '10px', 'margin-bottom': '10px'}),
        html.A(html.Button('Home', id='home-button-team-dashboard', 
                    style={'display': 'inline-block', 'float': 'right', 'border': '1px solid black', 
                           'color': 'black', 'backgroundColor': '#f9f9f9', 'margin-top': '10px', 'margin-bottom': '10px'}),href='/'),
    ], style={'width': '100%', 'textAlign': 'left', 'display': 'flex', 'justifyContent': 'space-between', 'position': '-webkit-sticky', 'top': '0', 'backgroundColor': 'white', 'zIndex': '1000'}),
            dcc.Graph(figure=team_performance_chart),
            html.H3("Home Statistics"),
            dcc.Graph(figure=home_chart),
            html.H3("Away Statistics"),
            dcc.Graph(figure=away_chart)
        ])
    
def extract_team_name(prop_id):
    try:
        # Attempt to extract the team name
        team_name = prop_id.split('index":"')[1].split('"')[0]
        return team_name
    except IndexError:
        # Handle the case where extraction fails
        print("Error extracting team name from prop_id:", prop_id)
        return None



def load_and_merge_player_data():
    # Read the CSV files into Pandas dataframes
    df_defense = pd.read_csv('data_new/player_defense.csv')
    df_gca = pd.read_csv('data_new/player_gca.csv')
    df_keepers = pd.read_csv('data_new/player_keepers.csv')
    df_keepersadv = pd.read_csv('data_new/player_keepersadv.csv')
    df_misc = pd.read_csv('data_new/player_misc.csv')
    df_passing = pd.read_csv('data_new/player_passing.csv')
    df_passing_types = pd.read_csv('data_new/player_passing_types.csv')
    df_playingtime = pd.read_csv('data_new/player_playingtime.csv')
    df_possesion = pd.read_csv('data_new/player_possession.csv')
    df_shooting = pd.read_csv('data_new/player_shooting.csv')
    df_stats = pd.read_csv('data_new/player_stats.csv')

    # Merge dataframes
    df_combined = df_defense.merge(df_gca, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_keepers, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_keepersadv, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_misc, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_passing, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_passing_types, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_playingtime, on=['player', 'position', 'team', 'age', 'birth_year'], how='outer')
    df_combined = df_combined.merge(df_possesion, on=['player', 'position', 'team', 'age', 'birth_year'], how='outer')
    df_combined = df_combined.merge(df_shooting, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_stats, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')

    df_combined.drop_duplicates(subset=['player'], keep='first', inplace=True)
    return df_combined


df_players = load_and_merge_player_data()
# Function to display player information
def display_player_info(player_name):
    player_info = df_players[df_players['player'] == player_name].iloc[0]
    return html.Div([
        html.H4(player_info['player']),
        html.P(f"Team: {player_info['team']}"),
        html.P(f"Position: {player_info['position']}"),
        html.P(f"Age: {player_info['age']}")
    ])


def create_player_stats_table(player_name):
    # Extracting relevant data for the player
    player_data = df_players[df_players['player'] == player_name][['games', 'minutes_per_game', 'xg', 'fouls', 'cards_yellow', 'cards_red', 'offsides', 'own_goals']].iloc[0]

    # Creating a DataFrame for the DataTable
    data_df = pd.DataFrame([player_data])

    # Creating the DataTable
    table = dash_table.DataTable(
        data=data_df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in data_df.columns],
        style_as_list_view=True,
        style_cell={'padding': '5px', 'textAlign': 'center'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'},
             'backgroundColor': 'rgb(220, 220, 220)'},
            {'if': {'row_index': 'even'},
             'backgroundColor': 'rgb(240, 240, 240)'}
        ]
    )
    
    return table

def remove_outliers(df, column, num_std_dev=3):
    mean = df[column].mean()
    std_dev = df[column].std()
    filtered_df = df[(df[column] >= mean - num_std_dev * std_dev) & (df[column] <= mean + num_std_dev * std_dev)]
    return filtered_df




# Adjusted Function to create a radar chart for two players
def create_radar_chart(player_name_1, player_name_2):
    # Initialize the radar chart figure
    fig = go.Figure()

    # Remove outliers and then calculate the max values for scaling
    max_aerial = remove_outliers(df_players, 'aerials_won_pct').max()['aerials_won_pct']
    dribbling = df_players['dribbles_completed_pct'] - df_players['dispossessed'] - df_players['miscontrols']
    max_dribbling = remove_outliers(df_players.assign(dribbling=dribbling), 'dribbling').max()['dribbling']
    passing = df_players['passes_pct'] - df_players['passes_offsides']
    max_passing = remove_outliers(df_players.assign(passing=passing), 'passing').max()['passing']
    shooting = df_players['shots_on_target_pct'] + df_players['goals']
    max_shooting = remove_outliers(df_players.assign(shooting=shooting), 'shooting').max()['shooting']
    defense = df_players['tackles'] + df_players['blocked_shots'] + df_players['interceptions'] + df_players['clearances'] - df_players['errors']
    max_defense = remove_outliers(df_players.assign(defense=defense), 'defense').max()['defense']

    # Function to scale the values
    def scale_value(value, max_value):
        return (value / max_value) * 100 if max_value != 0 else 0
    # Add traces for each player if they have been selected
    for player_name, color in zip([player_name_1, player_name_2], ['blue', 'red']):
        if player_name:
            player_stats = df_players[df_players['player'] == player_name].iloc[0]

            # Calculating the stats
            aerial_score = scale_value(player_stats['aerials_won_pct'], max_aerial)
            dribbling_score = scale_value(player_stats['dribbles_completed_pct'] - player_stats['dispossessed'] - player_stats['miscontrols'], max_dribbling)
            passing_score = scale_value(player_stats['passes_pct'] - player_stats['passes_offsides'], max_passing)
            shooting_score = scale_value(player_stats['shots_on_target_pct'] + player_stats['goals'], max_shooting)
            defense_score = scale_value(player_stats['tackles'] + player_stats['blocked_shots'] + player_stats['interceptions'] + player_stats['clearances'] - player_stats['errors'], max_defense)

            stats = [shooting_score, defense_score, passing_score, aerial_score, dribbling_score]

            fig.add_trace(go.Scatterpolar(
                r=stats,
                theta=['shooting', 'defending', 'passing', 'aerial', 'dribbling'],
                fill='toself',
                name=player_name,
                line=dict(color=color)
            ))

    # Set the radar chart layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Scale range set to 0-100
            )),
        showlegend=True
    )

    return fig

def create_defense_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Define the list of defense stats to compare
    defense_stats = ['tackles', 'blocked_shots', 'interceptions', 'clearances', 'errors']

    # Extract player stats and number of games
    player_stats = df_players[df_players['player'] == player_name].iloc[0]
    player_games = player_stats['games'] 

    # Normalize player stats per game
    player_values = [player_stats[stat] / player_games if player_games else 0 for stat in defense_stats]

    # Calculate and normalize average stats per game
    total_games = df_players['games'].sum()
    avg_stats = df_players[defense_stats].sum() / total_games

    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in defense_stats]

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=defense_stats, y=player_values),
        go.Scatter(name='Average', x=defense_stats, y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(title='Defense Stats Comparison', xaxis_title='Stats', yaxis_title='Value per Game')
    
    return fig

def create_shooting_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Extract player stats and number of matches
    player_stats = df_players[df_players['player'] == player_name].iloc[0]
    player_matches = player_stats['games'] 

    # Normalize player stats per match
    player_values = [player_stats[stat] / player_matches for stat in ['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot']]

    # Calculate and normalize average stats per match
    total_matches = df_players['games'].sum()
    avg_stats = df_players[['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot']].sum() / total_matches

    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in ['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot']]

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot'], y=player_values),
        go.Scatter(name='Average', x=['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot'], y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(title='Shooting Stats Comparison', xaxis_title='Stats', yaxis_title='Value per Match')
    
    return fig

def create_attacking_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Extract player stats and number of matches
    player_stats = df_players[df_players['player'] == player_name].iloc[0]
    player_matches = player_stats['games'] 

    # Normalize player stats per match
    player_values = [player_stats[stat] / player_matches for stat in ['sca', 'gca', 'assists']]

    # Calculate and normalize average stats per match
    total_matches = df_players['games'].sum()
    avg_stats = df_players[['sca', 'gca', 'assists']].sum() / total_matches

    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in ['sca', 'gca', 'assists']]

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=['sca', 'gca', 'assists'], y=player_values),
        go.Scatter(name='Average', x=['sca', 'gca', 'assists'], y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(title='Attacking Stats Comparison', xaxis_title='Stats', yaxis_title='Value per Match')
    
    return fig

def create_dribbling_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Extract player stats and number of matches
    player_stats = df_players[df_players['player'] == player_name].iloc[0]
    player_matches = player_stats['games']  # Use 'games' as the number of matches played

    # Normalize player stats per match, divide 'touches' by 10
    player_values = [player_stats[stat] / player_matches for stat in ['dribbles', 'dribbles_completed', 'dispossessed', 'miscontrols']]
    player_values.insert(2, (player_stats['touches'] / player_matches) / 10)  # Insert adjusted 'touches' at the correct position

    # Calculate and normalize average stats per match, divide average 'touches' by 10
    total_matches = df_players['games'].sum()
    avg_stats = df_players[['dribbles', 'dribbles_completed', 'dispossessed', 'miscontrols']].sum() / total_matches
    avg_touches = (df_players['touches'].sum() / total_matches) / 10  # Adjusted average 'touches'
    
    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in ['dribbles', 'dribbles_completed', 'dispossessed', 'miscontrols']]
    avg_values.insert(2, avg_touches)  # Insert adjusted average 'touches' at the correct position

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=['dribbles', 'dribbles_completed', 'touches (scaled /10)', 'dispossessed', 'miscontrols'], y=player_values),
        go.Scatter(name='Average', x=['dribbles', 'dribbles_completed', 'touches (scaled /10)', 'dispossessed', 'miscontrols'], y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(
        title='Dribbling Stats Comparison',
        xaxis_title='Stats',
        yaxis_title='Value per Match',
    )
    
    return fig

def create_passing_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Extract player stats and number of games
    player_stats = df_players[df_players['player'] == player_name].iloc[0] 
    player_games = player_stats['games'] 

    # Normalize player stats per game
    player_values = [player_stats[stat] / player_games for stat in ['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct']]

    # Calculate and normalize average stats per game
    total_games = df_players['games'].sum()
    avg_stats = df_players[['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct']].sum() / total_games

    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in ['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct']]

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct'], y=player_values),
        go.Scatter(name='Average', x=['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct'], y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(title='Passing Stats Comparison', xaxis_title='Stats', yaxis_title='Value per Game')
    
    return fig


def update_player_comparison(n_clicks_1, n_clicks_2, selected_player_1, selected_player_2):
    # Initialize empty containers for player info and tables
    player_1_display = html.Div()
    player_2_display = html.Div()
    player_1_table = html.Div()
    player_2_table = html.Div()

    # Initialize an empty radar chart
    radar_chart = go.Figure()

    # Check if player 1 is selected and update info and table
    if selected_player_1:
        player_1_display = display_player_info(selected_player_1)
        player_1_table = create_player_stats_table(selected_player_1)
        radar_chart = create_radar_chart(selected_player_1, selected_player_2)  # Update to include both players

    # Check if player 2 is selected and update info and table
    if selected_player_2:
        player_2_display = display_player_info(selected_player_2)
        player_2_table = create_player_stats_table(selected_player_2)
        # No need to call create_radar_chart again if player 1 was selected, it already includes both players
        if not selected_player_1:
            radar_chart = create_radar_chart(selected_player_1, selected_player_2)
            
    player_1_defense_chart = create_defense_stats_chart(selected_player_1) if selected_player_1 else go.Figure()
    player_2_defense_chart = create_defense_stats_chart(selected_player_2) if selected_player_2 else go.Figure()
    
    player_1_attacking_chart = create_attacking_stats_chart(selected_player_1) if selected_player_1 else go.Figure()
    player_2_attacking_chart = create_attacking_stats_chart(selected_player_2) if selected_player_2 else go.Figure()

    player_1_shooting_chart = create_shooting_stats_chart(selected_player_1) if selected_player_1 else go.Figure()
    player_2_shooting_chart = create_shooting_stats_chart(selected_player_2) if selected_player_2 else go.Figure()
    
    player_1_passing_chart = create_passing_stats_chart(selected_player_1) if selected_player_1 else go.Figure()
    player_2_passing_chart = create_passing_stats_chart(selected_player_2) if selected_player_2 else go.Figure()
    
    player_1_dribbling_chart = create_dribbling_stats_chart(selected_player_1) if selected_player_1 else go.Figure()
    player_2_dribbling_chart = create_dribbling_stats_chart(selected_player_2) if selected_player_2 else go.Figure()

    # Additional logic to filter options for player-selector-2 based on the selected player in player-selector-1
    if selected_player_1 is None:
        # If no player is selected in player-selector-1, return all options for player-selector-2
        player_2_options = player_options
    else:
        # Extract the position of the selected player
        selected_player_position = next(
            (player['position'] for player in player_options if player['value'] == selected_player_1),
            None
        )

        # Filter options for player-selector-2 based on the position of player-selector-1
        player_2_options = [
            {'label': p['label'], 'value': p['value']} for p in player_options
            if p['position'] == selected_player_position and p['value'] != selected_player_1
        ]

    # Return the updated values for the components
    return player_1_display, player_2_display, player_1_table, player_2_table, \
           radar_chart, player_1_defense_chart, player_2_defense_chart, \
           player_1_attacking_chart, player_2_attacking_chart, \
           player_1_shooting_chart, player_2_shooting_chart, \
           player_1_passing_chart, player_2_passing_chart, \
           player_1_dribbling_chart, player_2_dribbling_chart, player_2_options
           
           
           
# Function to display player information
def display_player_info(player_name):
    player_info = df_players[df_players['player'] == player_name].iloc[0]
    return html.Div([
        html.H4(player_info['player']),
        html.P(f"Team: {player_info['team']}"),
        html.P(f"Position: {player_info['position']}"),
        html.P(f"Age: {player_info['age']}")
    ])


def create_player_stats_table(player_name):
    # Extracting relevant data for the player
    player_data = df_players[df_players['player'] == player_name][['games', 'minutes_per_game', 'xg', 'fouls', 'cards_yellow', 'cards_red', 'offsides', 'own_goals']].iloc[0]

    # Creating a DataFrame for the DataTable
    data_df = pd.DataFrame([player_data])

    # Creating the DataTable
    table = dash_table.DataTable(
        data=data_df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in data_df.columns],
        style_as_list_view=True,
        style_cell={'padding': '5px', 'textAlign': 'center'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'},
             'backgroundColor': 'rgb(220, 220, 220)'},
            {'if': {'row_index': 'even'},
             'backgroundColor': 'rgb(240, 240, 240)'}
        ]
    )
    
    return table

# Adjusted Function to create a radar chart for two players
def create_radar_chart(player_name_1, player_name_2):
    # Initialize the radar chart figure
    fig = go.Figure()

    # Remove outliers and then calculate the max values for scaling
    max_aerial = remove_outliers(df_players, 'aerials_won_pct').max()['aerials_won_pct']
    dribbling = df_players['dribbles_completed_pct'] - df_players['dispossessed'] - df_players['miscontrols']
    max_dribbling = remove_outliers(df_players.assign(dribbling=dribbling), 'dribbling').max()['dribbling']
    passing = df_players['passes_pct'] - df_players['passes_offsides']
    max_passing = remove_outliers(df_players.assign(passing=passing), 'passing').max()['passing']
    shooting = df_players['shots_on_target_pct'] + df_players['goals']
    max_shooting = remove_outliers(df_players.assign(shooting=shooting), 'shooting').max()['shooting']
    defense = df_players['tackles'] + df_players['blocked_shots'] + df_players['interceptions'] + df_players['clearances'] - df_players['errors']
    max_defense = remove_outliers(df_players.assign(defense=defense), 'defense').max()['defense']

    # Function to scale the values
    def scale_value(value, max_value):
        return (value / max_value) * 100 if max_value != 0 else 0
    # Add traces for each player if they have been selected
    for player_name, color in zip([player_name_1, player_name_2], ['blue', 'red']):
        if player_name:
            player_stats = df_players[df_players['player'] == player_name].iloc[0]

            # Calculating the stats
            aerial_score = scale_value(player_stats['aerials_won_pct'], max_aerial)
            dribbling_score = scale_value(player_stats['dribbles_completed_pct'] - player_stats['dispossessed'] - player_stats['miscontrols'], max_dribbling)
            passing_score = scale_value(player_stats['passes_pct'] - player_stats['passes_offsides'], max_passing)
            shooting_score = scale_value(player_stats['shots_on_target_pct'] + player_stats['goals'], max_shooting)
            defense_score = scale_value(player_stats['tackles'] + player_stats['blocked_shots'] + player_stats['interceptions'] + player_stats['clearances'] - player_stats['errors'], max_defense)

            stats = [shooting_score, defense_score, passing_score, aerial_score, dribbling_score]

            fig.add_trace(go.Scatterpolar(
                r=stats,
                theta=['shooting', 'defending', 'passing', 'aerial', 'dribbling'],
                fill='toself',
                name=player_name,
                line=dict(color=color)
            ))

    # Set the radar chart layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Scale range set to 0-100
            )),
        showlegend=True
    )

    return fig

def create_defense_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Define the list of defense stats to compare
    defense_stats = ['tackles', 'blocked_shots', 'interceptions', 'clearances', 'errors']

    # Extract player stats and number of games
    player_stats = df_players[df_players['player'] == player_name].iloc[0]
    player_games = player_stats['games'] 

    # Normalize player stats per game
    player_values = [player_stats[stat] / player_games if player_games else 0 for stat in defense_stats]

    # Calculate and normalize average stats per game
    total_games = df_players['games'].sum()
    avg_stats = df_players[defense_stats].sum() / total_games

    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in defense_stats]

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=defense_stats, y=player_values),
        go.Scatter(name='Average', x=defense_stats, y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(title='Defense Stats Comparison', xaxis_title='Stats', yaxis_title='Value per Game')
    
    return fig

def create_shooting_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Extract player stats and number of matches
    player_stats = df_players[df_players['player'] == player_name].iloc[0]
    player_matches = player_stats['games'] 

    # Normalize player stats per match
    player_values = [player_stats[stat] / player_matches for stat in ['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot']]

    # Calculate and normalize average stats per match
    total_matches = df_players['games'].sum()
    avg_stats = df_players[['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot']].sum() / total_matches

    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in ['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot']]

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot'], y=player_values),
        go.Scatter(name='Average', x=['goals', 'shots', 'shots_on_target_pct', 'goals_per_shot'], y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(title='Shooting Stats Comparison', xaxis_title='Stats', yaxis_title='Value per Match')
    
    return fig

def create_attacking_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Extract player stats and number of matches
    player_stats = df_players[df_players['player'] == player_name].iloc[0]
    player_matches = player_stats['games'] 

    # Normalize player stats per match
    player_values = [player_stats[stat] / player_matches for stat in ['sca', 'gca', 'assists']]

    # Calculate and normalize average stats per match
    total_matches = df_players['games'].sum()
    avg_stats = df_players[['sca', 'gca', 'assists']].sum() / total_matches

    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in ['sca', 'gca', 'assists']]

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=['sca', 'gca', 'assists'], y=player_values),
        go.Scatter(name='Average', x=['sca', 'gca', 'assists'], y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(title='Attacking Stats Comparison', xaxis_title='Stats', yaxis_title='Value per Match')
    
    return fig

def create_dribbling_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Extract player stats and number of matches
    player_stats = df_players[df_players['player'] == player_name].iloc[0]
    player_matches = player_stats['games']  # Use 'games' as the number of matches played

    # Normalize player stats per match, divide 'touches' by 10
    player_values = [player_stats[stat] / player_matches for stat in ['dribbles', 'dribbles_completed', 'dispossessed', 'miscontrols']]
    player_values.insert(2, (player_stats['touches'] / player_matches) / 10)  # Insert adjusted 'touches' at the correct position

    # Calculate and normalize average stats per match, divide average 'touches' by 10
    total_matches = df_players['games'].sum()
    avg_stats = df_players[['dribbles', 'dribbles_completed', 'dispossessed', 'miscontrols']].sum() / total_matches
    avg_touches = (df_players['touches'].sum() / total_matches) / 10  # Adjusted average 'touches'
    
    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in ['dribbles', 'dribbles_completed', 'dispossessed', 'miscontrols']]
    avg_values.insert(2, avg_touches)  # Insert adjusted average 'touches' at the correct position

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=['dribbles', 'dribbles_completed', 'touches (scaled /10)', 'dispossessed', 'miscontrols'], y=player_values),
        go.Scatter(name='Average', x=['dribbles', 'dribbles_completed', 'touches (scaled /10)', 'dispossessed', 'miscontrols'], y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(
        title='Dribbling Stats Comparison',
        xaxis_title='Stats',
        yaxis_title='Value per Match',
    )
    
    return fig

def create_passing_stats_chart(player_name):
    if player_name is None:
        return go.Figure()

    # Extract player stats and number of games
    player_stats = df_players[df_players['player'] == player_name].iloc[0] 
    player_games = player_stats['games'] 

    # Normalize player stats per game
    player_values = [player_stats[stat] / player_games for stat in ['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct']]

    # Calculate and normalize average stats per game
    total_games = df_players['games'].sum()
    avg_stats = df_players[['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct']].sum() / total_games

    # Data for bar chart
    avg_values = [avg_stats[stat] for stat in ['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct']]

    # Create figure
    fig = go.Figure(data=[
        go.Bar(name=player_name, x=['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct'], y=player_values),
        go.Scatter(name='Average', x=['passes', 'passes_short', 'passes_medium', 'passes_long', 'passes_offsides', 'passes_pct'], y=avg_values, mode='lines', line=dict(color='red', dash='dot'))
    ])

    # Update layout
    fig.update_layout(title='Passing Stats Comparison', xaxis_title='Stats', yaxis_title='Value per Game')
    
    return fig



primary_color = "#007BFF"
secondary_color = "#FFC107"
background_color = "#F8F9FA"
text_color = "#212529"

header_style = {"textAlign": "center", "color": text_color}
subheader_style = {"textAlign": "left", "color": text_color, "padding": "5px 0px"}

# File paths for the CSV files
team_data_csv = 'data_new/team_data.csv'
player_data_csv = 'data_new/Player_stats.csv'
match_data_csv = 'data_new/match_data.csv'
df_teams = pd.read_csv('data_new/group_stats.csv')

# Read and merge player data
def load_and_merge_player_data():
    # Read the CSV files into Pandas dataframes
    df_defense = pd.read_csv('data_new/player_defense.csv')
    df_gca = pd.read_csv('data_new/player_gca.csv')
    df_keepers = pd.read_csv('data_new/player_keepers.csv')
    df_keepersadv = pd.read_csv('data_new/player_keepersadv.csv')
    df_misc = pd.read_csv('data_new/player_misc.csv')
    df_passing = pd.read_csv('data_new/player_passing.csv')
    df_passing_types = pd.read_csv('data_new/player_passing_types.csv')
    df_playingtime = pd.read_csv('data_new/player_playingtime.csv')
    df_possesion = pd.read_csv('data_new/player_possession.csv')
    df_shooting = pd.read_csv('data_new/player_shooting.csv')
    df_stats = pd.read_csv('data_new/player_stats.csv')

    # Merge dataframes
    df_combined = df_defense.merge(df_gca, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_keepers, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_keepersadv, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_misc, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_passing, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_passing_types, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_playingtime, on=['player', 'position', 'team', 'age', 'birth_year'], how='outer')
    df_combined = df_combined.merge(df_possesion, on=['player', 'position', 'team', 'age', 'birth_year'], how='outer')
    df_combined = df_combined.merge(df_shooting, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')
    df_combined = df_combined.merge(df_stats, on=['player', 'position', 'team', 'age', 'birth_year', 'minutes_90s'], how='outer')

    df_combined.drop_duplicates(subset=['player'], keep='first', inplace=True)
    return df_combined

# Load and merge player data
df_players = load_and_merge_player_data()

# Drop columns with "_y" suffix
df_players.drop([col for col in df_players.columns if col.endswith('_y')], axis=1, inplace=True)

# Rename columns with "_x" suffix by removing "_x"
df_players.rename(columns={col: col.rstrip('_x') for col in df_players.columns if col.endswith('_x')}, inplace=True)

# Fill NaN values with 0 for all columns
df_players = df_players.fillna(0)

# Normalize statistics function
def normalize_statistic(df, column_name):
    min_val = df[column_name].min()
    max_val = df[column_name].max()
    df[column_name] = 100 * (df[column_name] - min_val) / (max_val - min_val)
    return df

# Normalize statistics
df_players = normalize_statistic(df_players, 'goals_per_shot')
df_players = normalize_statistic(df_players, 'tackles_won')
df_players = normalize_statistic(df_players, 'passes_completed')

# Function to extract the year part from the age string
def extract_year(age_str):
    return age_str.split('-')[0]

# Apply the function to the 'age' column
df_players['age'] = df_players['age'].apply(extract_year)

# Convert the 'age' column to integers
df_players['age'] = df_players['age'].astype(int)

def remove_outliers(df, column, num_std_dev=3):
    mean = df[column].mean()
    std_dev = df[column].std()
    filtered_df = df[(df[column] >= mean - num_std_dev * std_dev) & (df[column] <= mean + num_std_dev * std_dev)]
    return filtered_df

def get_player_names():
    df = df_players
    df.drop_duplicates(subset=['player'], inplace=True)
    player_names = df['player'].sort_values().unique()
    return [{'label': player, 'value': player} for player in player_names]


# Function to create team dropdowns
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
                    'textAlign': 'center',  # Align text to the left
                    'background-color': 'transparent',  # Transparent background
                    'border': 'none',  # No border
                    'width': '100%',  # Full width
                    'text-align': 'center'  # Align text to the left
                }) for team in teams_in_group['team']
            ], style={'padding': '10px'})
        ], style={
            'width': '100%',
            'marginBottom': '10px',
            'border': '1px solid blue'
        })
        accordion.append(details)
    return accordion

group_accordions = create_accordion(df_teams)




def top_scoring_players_modified():
    df = df_players
    
    top_scorers = df.sort_values(by='goals', ascending=False).head(10)

    # Create a bar chart using Plotly
    fig = px.bar(top_scorers, x='player', y='goals', 
                 title="Top 10 Scoring Players", 
                 labels={'player': 'Player', 'goals': 'Goals Scored'})

    # Optional: Customize the layout
    fig.update_layout(xaxis_title="Player",
                      yaxis_title="Goals Scored",
                      xaxis={'categoryorder':'total descending'},
                     )
    return fig