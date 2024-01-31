from dash import html, dcc, Input, Output, State
from variables import playoff_right, playoff_top, data_folder, field_length, field_width, field_spacing
from initial_content import app
import plotly.graph_objects as go


def generate_field(spoilers=False, initialize=False):
    fig = go.Figure()
    
    goal_width = 7.32
    goal_depth = 2
    goal_box_length = 5.5
    goal_box_width = goal_width + 5.5*2
    strafschopgebied_length = 16.5
    strafschopgebied_width = 40.32
    penalty_spot_distance = 11
    penalty_spot_size = 0.5
    goal_circle_arc_radius = 9.15
    spacing = field_spacing
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_xaxes(range=[0-spacing, field_length+spacing])
    fig.update_yaxes(range=[0-spacing, field_width+spacing])
    
    fig.add_shape(type="rect",
                  x0=0, y0=0, x1=field_length, y1=field_width,
                  line=dict(color="black", width=2),
                  fillcolor="green",
                  layer="below",
                  )
    # add circle around the penalty spot
    fig.add_shape(type="circle",
                    x0=penalty_spot_distance - goal_circle_arc_radius,
                    y0=field_width/2 - goal_circle_arc_radius,
                    x1= penalty_spot_distance + goal_circle_arc_radius,
                    y1=field_width/2 + goal_circle_arc_radius,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    fig.add_shape(type="circle",
                    x0=field_length - penalty_spot_distance - goal_circle_arc_radius,
                    y0=field_width/2 - goal_circle_arc_radius,
                    x1= field_length - penalty_spot_distance + goal_circle_arc_radius,
                    y1=field_width/2 + goal_circle_arc_radius,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    
    fig.add_shape(type="rect",
                    x0=0, 
                    y0=(field_width/2)+(strafschopgebied_width/2), 
                    x1=strafschopgebied_length, 
                    y1=(field_width/2)-(strafschopgebied_width/2),
                    line=dict(color="black", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    fig.add_shape(type="rect",
                    x0=field_length, 
                    y0=(field_width/2)+(strafschopgebied_width/2), 
                    x1=field_length-strafschopgebied_length, 
                    y1=(field_width/2)-(strafschopgebied_width/2),
                    line=dict(color="black", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    fig.add_shape(type="rect",
                    x0=0, 
                    y0=(field_width/2)+(goal_box_width/2), 
                    x1=0+goal_box_length, 
                    y1=(field_width/2)-(goal_box_width/2),
                    line=dict(color="black", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    fig.add_shape(type="rect",
                    x0=field_length, 
                    y0=(field_width/2)+(goal_box_width/2), 
                    x1=field_length-goal_box_length, 
                    y1=(field_width/2)-(goal_box_width/2),
                    line=dict(color="black", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    # Add the six yard box
    # fig.add_shape(type="line",
    #                 x0=field_length/2, y0=0, x1=field_length/2, y1=field_width,
    #                 line=dict(color="black", width=2),
    #                 layer="below",
    #                 )
    # Add the centre circle
    fig.add_shape(type="circle",
                    x0=field_length/2-9.15, 
                    y0=field_width/2-9.15,
                    x1=field_length/2+9.15, 
                    y1=field_width/2+9.15,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    # Add the penalty spots
    fig.add_shape(type="circle",
                    x0=penalty_spot_distance - penalty_spot_size, 
                    y0=field_width/2 - penalty_spot_size, 
                    x1=penalty_spot_distance + penalty_spot_size, 
                    y1=field_width/2 + penalty_spot_size,
                    line=dict(color="black", width=2),
                    fillcolor="black",
                    layer="below",
                    )
    fig.add_shape(type="circle",
                    x0=field_length - penalty_spot_distance - penalty_spot_size, 
                    y0=field_width/2 - penalty_spot_size, 
                    x1=field_length - penalty_spot_distance + penalty_spot_size, 
                    y1=field_width/2 + penalty_spot_size,
                    line=dict(color="black", width=2),
                    fillcolor="black",
                    layer="below",
                    )
    # Add the corner arcs
    fig.add_shape(type="circle",
                    x0=-0.5, 
                    y0=-0.5, 
                    x1=0.5, 
                    y1=0.5,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    fig.add_shape(type="circle",
                    x0=-0.5, 
                    y0=field_width - 0.5, 
                    x1=0.5, 
                    y1=field_width+0.5,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    fig.add_shape(type="circle",
                    x0=field_length - 0.5, 
                    y0=-0.5, 
                    x1=field_length + 0.5, 
                    y1=0.5,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    fig.add_shape(type="circle",
                    x0=field_length - 0.5, 
                    y0=field_width - 0.5, 
                    x1=field_length + 0.5, 
                    y1=field_width + 0.5,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    # Add the half circle
    fig.add_shape(type="path",
                    path="M 52.5 54 C 52.5 54 52.5 14 52.5 14",
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    # Add the centre spot
    fig.add_shape(type="circle",
                    x0=field_length/2-penalty_spot_size, 
                    y0=field_width/2-penalty_spot_size, 
                    x1=field_length/2+penalty_spot_size, 
                    y1=field_width/2+penalty_spot_size,
                    line=dict(color="black", width=2),
                    fillcolor="black",
                    layer="below",
                    )
    # add center line
    fig.add_shape(type="line",
                    x0=field_length/2, 
                    y0=0, 
                    x1=field_length/2, 
                    y1=field_width,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    
    # add coloring for the spacing at the border
    fig.add_shape(type="rect",
                    x0=-spacing, 
                    y0=-spacing, 
                    x1=0, 
                    y1=field_width,
                    line=dict(color="green", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    fig.add_shape(type="rect",
                    x0=field_length, 
                    y0=-spacing, 
                    x1=field_length+spacing, 
                    y1=field_width,
                    line=dict(color="green", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    fig.add_shape(type="rect",
                    x0=-spacing, 
                    y0=-spacing, 
                    x1=field_length, 
                    y1=0,
                    line=dict(color="green", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    fig.add_shape(type="rect",
                    x0=-spacing, 
                    y0=field_width, 
                    x1=field_length, 
                    y1=field_width+spacing,
                    line=dict(color="green", width=2),
                    fillcolor="green",
                    
                    layer="below",
                    )
    fig.add_shape(type="rect",
                    x0=field_length, 
                    y0=field_width, 
                    x1=field_length+spacing, 
                    y1=field_width+spacing,
                    line=dict(color="green", width=2),
                    fillcolor="green",
                    
                    layer="below",
                    )
    
    #draw field border lines
    fig.add_shape(type="line",
                    x0=0, 
                    y0=0, 
                    x1=field_length, 
                    y1=0,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    fig.add_shape(type="line",
                    x0=0, 
                    y0=field_width, 
                    x1=field_length, 
                    y1=field_width,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    fig.add_shape(type="line",
                    x0=0, 
                    y0=0, 
                    x1=0, 
                    y1=field_width,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    fig.add_shape(type="line",
                    x0=field_length, 
                    y0=0, 
                    x1=field_length, 
                    y1=field_width,
                    line=dict(color="black", width=2),
                    layer="below",
                    )
    
    fig.add_shape(type="rect",
                    x0=-goal_depth, 
                    y0=(field_width/2)+(goal_width/2), 
                    x1=0, 
                    y1=(field_width/2)-(goal_width/2),
                    line=dict(color="black", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    fig.add_shape(type="rect",
                    x0=field_length, 
                    y0=(field_width/2)+(goal_width/2), 
                    x1=field_length+goal_depth, 
                    y1=(field_width/2)-(goal_width/2),
                    line=dict(color="black", width=2),
                    fillcolor="green",
                    layer="below",
                    )
    
    return fig


def show_shot_on_map(players, initialize = False):
    shot_size = 20
    colors = {'Miss' : 'red', 'Goal' : 'blue', 'Post' : 'orange', 'AttemptSaved' : 'red'}
    fig, _ = generate_field(initialize=initialize)
    x = {}
    y = {}
    player_name = {}
    shot_time = {}
    for shottype in colors.keys():
        x[shottype] = []
        y[shottype] = []
        player_name[shottype] = []
        shot_time[shottype] = []
    event_type = []
    for player in players:
        if 'shotmaps' in player.keys():
            for shotmap in player['shotmaps']:
                player_name[shotmap['eventType']].append(player['name'])
                shot_time[shotmap['eventType']].append(shotmap['min'])
                x[shotmap['eventType']].append(int(shotmap['x']))
                y[shotmap['eventType']].append(int(shotmap['y']))
                event_type.append(colors[shotmap['eventType']])
    text_list = {shottype: [f'{player_name[shottype][i]}<br>{shot_time[shottype][i]} min' 
                            for i in range(len(player_name[shottype]))] 
                 for shottype in colors.keys()}
    
    for shottype in colors.keys():
        fig.add_trace(go.Scatter(x=x[shottype], 
                                 y=y[shottype], 
                                 mode='markers', 
                                 marker=dict(color=[colors[shottype] for _ in range(len(x[shottype]))], 
                                             size=shot_size),
                                 text=text_list[shottype], 
                                 name=shottype))
    return fig