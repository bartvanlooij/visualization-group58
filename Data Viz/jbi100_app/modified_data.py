import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

def load_team_data(csv_file_path):
    return pd.read_csv(csv_file_path)

def load_player_data(csv_file_path):
    return pd.read_csv(csv_file_path)

def top_scoring_teams(team_data):
    # Sorting and selecting top 10 teams based on goals
    top_teams = team_data.sort_values(by='goals', ascending=False).head(10)
    return px.bar(top_teams, x='team', y='goals', title='Top 10 Scoring Teams', template='simple_white')

def best_defensive_teams(team_data):
    # Sorting and selecting top 10 teams based on goalkeeper clean sheets
    top_defensive_teams = team_data.sort_values(by='gk_clean_sheets', ascending=False).head(10)
    return px.bar(top_defensive_teams, x='team', y='gk_clean_sheets', title='Top 10 Defensive Teams', template='simple_white')

def top_scoring_players(player_data):
    # Sorting and selecting top 10 players based on goals
    top_players = player_data.sort_values(by='goals', ascending=False).head(10)
    return px.bar(top_players, x='player', y='goals', title='Top 10 Scoring Players', template='simple_white')

# New functions for team-specific dashboard
def process_team_data(selected_team, match_data_csv):
    match_data = pd.read_csv(match_data_csv)
    team_data = match_data[(match_data['home_team'] == selected_team) | (match_data['away_team'] == selected_team)]
    return team_data

def calculate_team_performance(team, match_data):
    wins = draws = losses = goals_scored = goals_against = 0

    for _, row in match_data.iterrows():
        try:
            # Adjust the split method to match the delimiter in your dataset
            home_goals, away_goals = map(int, row['score'].split('–'))
        except ValueError:
            # Handle cases where score format is not as expected
            print(f"Invalid score format: {row['score']}")
            continue

        if row['home_team'] == team:
            goals_scored += home_goals
            goals_against += away_goals
            if home_goals > away_goals:
                wins += 1
            elif home_goals == away_goals:
                draws += 1
            else:
                losses += 1

        elif row['away_team'] == team:
            goals_scored += away_goals
            goals_against += home_goals
            if away_goals > home_goals:
                wins += 1
            elif away_goals == home_goals:
                draws += 1
            else:
                losses += 1

    return wins, draws, losses, goals_scored, goals_against

def create_team_performance_chart(team_data, selected_team):
    team_performance = calculate_team_performance(selected_team, team_data)
    team_performance_df = pd.DataFrame({
        'Statistic': ['Wins', 'Draws', 'Losses', 'Goals Scored', 'Goals Against'],
        'Total': team_performance
    })

    fig = px.bar(team_performance_df, x='Statistic', y='Total', title=f'Overall Team Performance for {selected_team}', template='simple_white')
    return fig

def normalize_data(data):
    scaler = MinMaxScaler()
    return scaler.fit_transform(data.values.reshape(-1, 1)).flatten()

def create_average_specifics_chart(team_data):
    # Define columns of interest for home and away statistics
    home_columns = ['home_possession', 'home_completed_passes', 'home_sot', 'home_total_shots', 'home_saves', 'home_fouls', 'home_corners', 'home_crosses', 'home_tackles', 'home_interceptions', 'home_offsides']
    away_columns = ['away_possession', 'away_completed_passes', 'away_sot', 'away_total_shots', 'away_saves', 'away_fouls', 'away_corners', 'away_crosses', 'away_tackles', 'away_interceptions', 'away_offsides']

    # Calculate average data for home and away
    home_average_data = team_data[home_columns].mean()
    away_average_data = team_data[away_columns].mean()

    # Normalize the data
    home_normalized = normalize_data(home_average_data)
    away_normalized = normalize_data(away_average_data)

    # Append original average values to variable names
    home_labels = [f"{col} ({round(val, 2)})" for col, val in zip(home_columns, home_average_data)]
    away_labels = [f"{col} ({round(val, 2)})" for col, val in zip(away_columns, away_average_data)]

    # Create radar chart for home statistics
    home_fig = go.Figure(data=go.Scatterpolar(
        r=home_normalized,
        theta=home_labels,
        fill='toself'
    ))
    home_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        title='Normalized Average Home Match Specifics', template='simple_white'
    )

    # Create radar chart for away statistics
    away_fig = go.Figure(data=go.Scatterpolar(
        r=away_normalized,
        theta=away_labels,
        fill='toself'
    ))
    away_fig.update_layout(template='simple_white', 
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        title='Normalized Average Away Match Specifics'
    )

    return home_fig, away_fig