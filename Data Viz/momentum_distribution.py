from turtle import color, home
from mobfot import MobFot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from variables import data_folder
client = MobFot()
 
def get_momentum(momentum):
    momentum_list = []
    momentum_minutes = []
    momentum = momentum['main']['data']
    for x in momentum:
        momentum_list.append(x['value'])
        momentum_minutes.append(x['minute'])
       
    return momentum_list, momentum_minutes


def create_momentum_distribution(match, match_id):
    momentum_list, momentum_minutes = get_momentum(match['content']['momentum'])
    df_matches = pd.read_csv(f'{data_folder}/match_data.csv')
    home_team = df_matches[df_matches['match_id'] == match_id]['home_team'].values[0]
    away_team = df_matches[df_matches['match_id'] == match_id]['away_team'].values[0]
    df = pd.DataFrame({'minutes': momentum_minutes, 'momentum': momentum_list})
    fig = go.Figure()
    fig.add_trace(go.Line(x=df['minutes'], y=df['momentum'], 
                          mode='lines', name='Momentum', showlegend=False,
                          hoverinfo='none'))
    fig.add_trace(go.Line(x=[0, df.minutes.max()], y=[0, 0], mode='lines', 
                          line={'color': 'black'}, 
                          showlegend=False,
                          hoverinfo='none'))
    # add the horizontal line at 0
    fig.update_yaxes(range = [-100, 100],
                     title_text = 'Momentum',
                     title_font = {"size": 20},
                     title_standoff = 25)
    fig.update_xaxes(title_text = 'Minutes',
                        title_font = {"size": 20},
                        title_standoff = 25)
    fig.update_yaxes(tickvals = [-100, -50, 0, 50, 100],
                     title_text = 'Momentum',
                        title_font = {"size": 20},
                        title_standoff = 25)
    fig.update_layout(title = 'Momentum Distribution',
                      title_font = {"size": 20},
                      title_x = 0.5,
                      plot_bgcolor = 'white',
                      xaxis = {"showgrid": False},
                      yaxis = {"showgrid": False},
                      template = 'simple_white')
    df_above_zero = df.copy()
    df_above_zero['momentum'] = df_above_zero['momentum'].apply(lambda x: x if x > 0 else 0)
    df_below_zero = df.copy()
    df_below_zero['momentum'] = df_below_zero['momentum'].apply(lambda x: x if x < 0 else 0)
    above_text_list = [f'{home_team} advantage' if x > 0 else '' for x in df_above_zero['momentum']]
    below_text_list = [f'{away_team} advantage' if x < 0 else '' for x in df_below_zero['momentum']]
    area_above_trace = go.Scatter(x=df_above_zero['minutes'], 
                                  y=df_above_zero['momentum'], 
                                  fill='tozeroy', fillcolor='green', 
                                  mode='none', name=f'{home_team} advantage',
                                  text=above_text_list)
    area_below_trace = go.Scatter(x=df_below_zero['minutes'], 
                                  y=df_below_zero['momentum'], 
                                  fill='tozeroy', fillcolor='red', 
                                  mode='none', name=f'{away_team} advantage',
                                  text=below_text_list)
    fig.add_trace(area_above_trace)
    fig.add_trace(area_below_trace)


    return fig
