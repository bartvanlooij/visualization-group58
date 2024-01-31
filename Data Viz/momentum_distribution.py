from mobfot import MobFot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

client = MobFot()
 
def get_momentum(momentum):
    momentum_list = []
    momentum_minutes = []
    momentum = momentum['main']['data']
    for x in momentum:
        momentum_list.append(x['value'])
        momentum_minutes.append(x['minute'])
       
    return momentum_list, momentum_minutes


def create_momentum_distribution(match):
    match = client.get_match_details(3854556)
    momentum_list, momentum_minutes = get_momentum(match['content']['momentum'])
    df = pd.DataFrame({'minutes': momentum_minutes, 'momentum': momentum_list})
    fig = px.line(df, x='minutes', y='momentum')

    return fig