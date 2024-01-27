from variables import data_folder
import pandas as pd
player_data_csv = f'{data_folder}/Player_stats.csv'
match_data_csv = f'{data_folder}/match_data.csv'
df_teams = pd.read_csv(f'{data_folder}/group_stats.csv')

# Read merge n fix player data
def load_and_merge_player_data():
    df_defense = pd.read_csv(f'{data_folder}/player_defense.csv')
    df_gca = pd.read_csv(f'{data_folder}/player_gca.csv')
    df_keepers = pd.read_csv(f'{data_folder}/player_keepers.csv')
    df_keepersadv = pd.read_csv(f'{data_folder}/player_keepersadv.csv')
    df_misc = pd.read_csv(f'{data_folder}/Player_misc.csv')
    df_passing = pd.read_csv(f'{data_folder}/Player_passing.csv')
    df_passing_types = pd.read_csv(f'{data_folder}/Player_passing_types.csv')
    df_playingtime = pd.read_csv(f'{data_folder}/Player_playingtime.csv')
    df_possesion = pd.read_csv(f'{data_folder}/player_possession.csv')
    df_shooting = pd.read_csv(f'{data_folder}/Player_shooting.csv')
    df_stats = pd.read_csv(f'{data_folder}/Player_stats.csv')

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