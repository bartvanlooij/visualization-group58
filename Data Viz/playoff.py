
from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from initial_content import app
import pandas as pd
from match_dashboard import *
from variables import data_folder, playoff_right, playoff_top
import time
def get_score_stings(df, team_names, teams):
    score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
    if len(score) == 3:
        scores = [score[0], score[2]]
    else:
        scores = [f'{score[4]}{score[:3]}', f'{score[6]}{score[-3:]}']
    return scores

def compute_winner(scores):
    if len(scores[0]) == 1:
        if int(scores[0]) > int(scores[1]):
            return [True,False]
        else:
            return [False,True]
    else:
        if int(scores[0][2]) > int(scores[1][2]):
            return [True,False]
        else:
            return [False,True]


def create_playoff_bracket(spoilers=False, initialize=False):
    df = pd.read_csv(f'{data_folder}/match_data.csv')
    df = df[['home_team', 'away_team', 'score']]
    
    team_names = {'USA': 'United States',
                  'Netherlands': 'Netherlands',
                  'England': 'England',
                  'France': 'France',
                  'Spain': 'Spain',
                  'Portugal': 'Portugal',
                  'Switzerland': 'Switzerland',
                  'Poland': 'Poland',
                  'Senegal': 'Senegal',
                  'Morocco': 'Morocco',
                  'Argentina': 'Argentina',
                  'Australia': 'Australia',
                  'Brasil': 'Brazil',
                  'Korea': 'Korea Republic',
                  'Japan': 'Japan',
                  'Croatia': 'Croatia'
                  }
    heatmap_scale = 0.2
    font = "Courier New, monospace"
    left = 0
    right = playoff_right
    top = playoff_top
    bottom = 0
    vertical_distance = 50
    bottom = 0
    box_width = 170
    box_height = 120
    space_between_boxes = 100
    vertical_border_spacing = 100
    line_width = 1
    center_x = (right-left)/2
    center_y = (top-bottom)/2
    text_spacing = 50
    font_size = 15
    start_y_text = -30
    text_left_spacing = 10
    text_right_spacing = 20
    font_color = 'RoyalBlue'
    line_color = 'RoyalBlue'
    eigth_finals = ['Brasil - Korea', 'Japan - Croatia', 'Argentina - Australia', 'Netherlands - USA',
                    'Portugal - Switzerland', 'Morocco - Spain', 'France - Poland', 'England - Senegal']
    quart_finals = ['Croatia - Brasil', 'Netherlands - Argentina', 'Morocco - Portugal', 'England - France']
    semi_finals = ['Argentina - Croatia', 'France - Morocco']
    final = ['Argentina - France']
    third_place = ['Croatia - Morocco']
    fig = go.Figure()
    fig.update_layout(template='plotly_white')

    fig.update_xaxes(
    showticklabels=False,
    showgrid=False,
    zeroline=False)

    fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False)
    fig.update_xaxes(range=[left, right])
    fig.update_yaxes(range=[bottom, top])
    
    start_y = center_y - 2*(box_height + space_between_boxes) + space_between_boxes/2 
    #Create header bar
    fig.add_shape(type="rect",
                    x0=left,
                    y0=top,
                    x1=right,
                    y1=top - 50,
                    line=dict(color=line_color,width=line_width),
                    fillcolor="LightSkyBlue")
    
    #Create 1/8 finals header
    fig.add_annotation(x=left + vertical_border_spacing + box_width/2,
                        y=top - 25,
                        text='Round of 16',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color=font_color
                            ),
                        align='center'
                        )
    fig.add_annotation(x=right - vertical_border_spacing - box_width/2,
                        y=top - 25,
                        text='Round of 16',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color=font_color
                            ),
                        align='center'
                        )
    #Create quarter finals header
    fig.add_annotation(x=left + vertical_border_spacing + box_width + vertical_distance + box_width/2,
                        y=top - 25,
                        text='Quarter Finals',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color=font_color
                            ),
                        align='center'
                        )
    fig.add_annotation(x=right - vertical_border_spacing - box_width - vertical_distance - box_width/2,
                        y=top - 25,
                        text='Quarter Finals',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color=font_color
                            ),
                        align='center'
                        )
    #Create semi finals header
    fig.add_annotation(x=left + vertical_border_spacing + 2*box_width + 2*vertical_distance + box_width/2,
                        y=top - 25,
                        text='Semi Finals',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color=font_color
                            ),
                        align='center'
                        )
    fig.add_annotation(x=right - vertical_border_spacing - 2*box_width - 2*vertical_distance - box_width/2,
                        y=top - 25,
                        text='Semi Finals',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color=font_color
                            ),
                        align='center'
                        )
    
    boxes_x = []
    boxes_y = []
    boxes_text = []
    #The 1/8 finals
    for i in range(4):
        #Create 4 boxes on the left side of the 
        #bracket making the allgined in the middle of the y
        x0 = left+ vertical_border_spacing
        y0 = start_y + i*(box_height + space_between_boxes)
        x1 = left+box_width+ vertical_border_spacing
        y1 = start_y+box_height + i*(box_height + space_between_boxes)
        boxes_x.append([x0,x1])
        boxes_y.append([y0,y1])
        fig.add_shape(type="rect",
                      x0=x0,
                      y0=y0,
                      x1=x1,
                      y1=y1,
                      line=dict(color=line_color,width=line_width),
                      fillcolor="LightSkyBlue")
        teams = eigth_finals[i].split(' - ')
        boxes_text.append([team_names[teams[0]], team_names[teams[1]]])
        scores = get_score_stings(df, team_names, teams)
        winner = compute_winner(scores)
        for j, team in enumerate(teams):
            if spoilers:
                team_string = f'<b>{team}' if winner[j] else team
            else:
                team_string = team
            fig.add_annotation(x=left + vertical_border_spacing + text_left_spacing,
                                y=start_y+box_height/2 + i*(box_height + space_between_boxes)- j*text_spacing - start_y_text,
                                text=team_string,
                                xanchor="left",
                                showarrow=False,
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    )
                                )
            if spoilers:
                
                scores = get_score_stings(df, team_names, teams)
                winner = compute_winner(scores)

                
                fig.add_annotation(x=left + box_width + vertical_border_spacing - 2*text_right_spacing,
                                y=start_y+box_height/2 + i*(box_height + space_between_boxes)- j*text_spacing - start_y_text,
                                text=scores[j],
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    ),
                                align='right'
                                )
        #Create 4 boxes on the right side of the
        #bracket making the allgined in the middle of the y
        x0 = right-box_width - vertical_border_spacing
        y0 = start_y + i*(box_height + space_between_boxes)
        x1 = right - vertical_border_spacing
        y1 = start_y+box_height + i*(box_height + space_between_boxes)
        boxes_x.append([x0,x1])
        boxes_y.append([y0,y1])
        fig.add_shape(type="rect",
                      x0=x0,
                      y0=y0,
                      x1=x1,
                      y1=y1,
                      line=dict(color=line_color,width=line_width),
                      fillcolor="LightSkyBlue")
        teams = eigth_finals[i+4].split(' - ')
        scores = get_score_stings(df, team_names, teams)
        winner = compute_winner(scores)
        boxes_text.append([team_names[teams[0]], team_names[teams[1]]])
        for j, team in enumerate(teams):
            if spoilers:
                team_string = f'<b>{team}' if winner[j] else team
            else:
                team_string = team
            fig.add_annotation(x=right - box_width - vertical_border_spacing + text_left_spacing,
                                y=start_y+box_height/2 + i*(box_height + space_between_boxes)- j*text_spacing - start_y_text,
                                text=team_string,
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    ),
                                align='left'
                                )
            if spoilers:
                
                scores = get_score_stings(df, team_names, teams)
                fig.add_annotation(x=right - vertical_border_spacing - 2*text_right_spacing,
                                y=start_y+box_height/2 + i*(box_height + space_between_boxes)- j*text_spacing - start_y_text,
                                text=scores[j],
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    ),
                                align='left'
                                )

    # Quarter finals
    for i in range(2):
        #Create 2 boxes on vertical_distance pixels to the right of the left side of the bracket
        #
        x0 = left+box_width+vertical_distance+ vertical_border_spacing
        x1 = left+box_width+vertical_distance+box_width + vertical_border_spacing
        y0 = start_y + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2
        y1 = start_y+box_height + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2
        fig.add_shape(type="rect",
                      x0=x0,
                      y0=y0,
                      x1=x1,
                      y1=y1,
                      line=dict(color=line_color,width=line_width),
                      fillcolor="LightSkyBlue")
        # Create 2 boxes on vertical_distance pixels to the left of the right side of the bracket
        #
        boxes_x.append([x0,x1])
        boxes_y.append([y0,y1])
        x0 = right-box_width-vertical_distance-box_width - vertical_border_spacing
        x1 = right-box_width-vertical_distance- vertical_border_spacing
        y0 = start_y + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2
        y1 = start_y+box_height + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2
        boxes_x.append([x0,x1])
        boxes_y.append([y0,y1])
        fig.add_shape(type="rect",
                      x0=x0,
                      y0=y0,
                      x1=x1,
                      y1=y1,
                      line=dict(color=line_color,width=line_width),
                      fillcolor="LightSkyBlue")
        teams = quart_finals[i].split(' - ')
        scores = get_score_stings(df, team_names, teams)
        boxes_text.append([team_names[teams[0]], team_names[teams[1]]])
        winner = compute_winner(scores)
        if spoilers:
            for j, team in enumerate(teams):
                team = f'<b>{team}' if winner[j] else team
                fig.add_annotation(x=left+box_width+vertical_distance+ vertical_border_spacing + text_left_spacing,
                                    y=start_y+box_height/2 + 2*i*(box_height + space_between_boxes)+ (box_height + space_between_boxes)/2-j*text_spacing - start_y_text,
                                    text=team,
                                    showarrow=False,
                                    xanchor="left",
                                    font=dict(
                                        family=font,
                                        size=font_size,
                                        color=font_color
                                        ),
                                    align='left'
                                    )
                
                    
                fig.add_annotation(x=left+box_width+vertical_distance+box_width + vertical_border_spacing - 2*text_right_spacing,
                                y=start_y+box_height/2 + 2*i*(box_height + space_between_boxes)+ (box_height + space_between_boxes)/2-j*text_spacing - start_y_text,
                                text=scores[j],
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    ),
                                align='right'
                                )
                
            teams = quart_finals[i+2].split(' - ')
            boxes_text.append([team_names[teams[0]], team_names[teams[1]]])
            for j, team in enumerate(teams):
                team_string = f'<b>{team}' if winner[j] else team
                fig.add_annotation(x=right-box_width-vertical_distance-box_width - vertical_border_spacing + text_left_spacing,
                                    y=start_y+box_height/2 + 2*i*(box_height + space_between_boxes)+ (box_height + space_between_boxes)/2-j*text_spacing - start_y_text,
                                    text=team_string,
                                    showarrow=False,
                                    xanchor="left",
                                    font=dict(
                                        family=font,
                                        size=font_size,
                                        color=font_color
                                        ),
                                    align='left'
                                    )
                    
                scores = get_score_stings(df, team_names, teams)
                fig.add_annotation(x=right-box_width-vertical_distance - vertical_border_spacing - 2*text_right_spacing,
                                y=start_y+box_height/2 + 2*i*(box_height + space_between_boxes)+ (box_height + space_between_boxes)/2-j*text_spacing - start_y_text,
                                text=scores[j],
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    ),
                                align='right'
                                )
        
    # Adding all the lines between the boxes of the 1/8 finals with the quarter finals
    for i in range(4):
        fig.add_shape(type="line",
                      x0=left+box_width +vertical_border_spacing,
                      y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      x1=left+box_width+vertical_distance/2 + vertical_border_spacing,
                      y1=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      line=dict(color=line_color,width=line_width))
        fig.add_shape(type="line",
                      x0=right-box_width - vertical_border_spacing,
                      y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      x1=right-box_width-vertical_distance/2 - vertical_border_spacing,
                      y1=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      line=dict(color=line_color,width=line_width))
        if i % 2 == 0:
            fig.add_shape(type="line",
                          x0=left+box_width+vertical_distance/2 + vertical_border_spacing,
                          y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                          x1=left+box_width+vertical_distance/2 + vertical_border_spacing,
                          y1=start_y + box_height/2 + (i+1)*(box_height + space_between_boxes),
                          line=dict(color=line_color,width=line_width))
            fig.add_shape(type="line",
                          x0=right-box_width-vertical_distance/2 - vertical_border_spacing,
                          y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                          x1=right-box_width-vertical_distance/2 - vertical_border_spacing,
                          y1=start_y + box_height/2 + (i+1)*(box_height + space_between_boxes),
                          line=dict(color=line_color,width=line_width))
            fig.add_shape(type="line",
                          x0=left+box_width+vertical_distance/2 + vertical_border_spacing,
                          y0=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                          x1=left+box_width+vertical_distance + vertical_border_spacing,
                          y1=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                          line=dict(color=line_color,width=line_width))
            fig.add_shape(type="line",
                            x0=right-box_width-vertical_distance/2 - vertical_border_spacing,
                            y0=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                            x1=right-box_width-vertical_distance - vertical_border_spacing,
                            y1=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                            line=dict(color=line_color,width=line_width))
        
    # Semi finals
    x0 = left+box_width+2*vertical_distance+box_width + vertical_border_spacing
    x1 = left+box_width+2*vertical_distance+2*box_width + vertical_border_spacing
    y0 = center_y + (box_height)/2
    y1 = center_y - (box_height)/2
    boxes_x.append([x0,x1])
    boxes_y.append([y0,y1])
    fig.add_shape(type="rect",
                    x0=x0,
                    y0=y0,
                    x1=x1,
                    y1=y1,
                    line=dict(color=line_color,width=line_width),
                    fillcolor="LightSkyBlue")
    x0 = right-box_width-2*vertical_distance-2*box_width - vertical_border_spacing
    x1 = right-box_width-2*vertical_distance-box_width - vertical_border_spacing
    y0 = y0=center_y + (box_height)/2
    y1 = center_y - (box_height)/2
    boxes_x.append([x0,x1])
    boxes_y.append([y0,y1])
    fig.add_shape(type="rect",
                    x0=x0,
                    y0=y0,
                    x1=x1,
                    y1=y1,
                    line=dict(color=line_color,width=line_width),
                    fillcolor="LightSkyBlue")
    teams = semi_finals[0].split(' - ')
    scores = get_score_stings(df, team_names, teams)
    winners = compute_winner(scores)
    boxes_text.append([team_names[teams[0]], team_names[teams[1]]])
    if spoilers:
        for j, team in enumerate(teams):
            team_string = f'<b>{team}' if winners[j] else team
            fig.add_annotation(x=left+box_width+2*vertical_distance+box_width + vertical_border_spacing + text_left_spacing,
                                y=center_y  - j*text_spacing - start_y_text,
                                text=team_string,
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    ),
                                align='left'
                                )
            fig.add_annotation(x=left+box_width+2*vertical_distance+2*box_width + vertical_border_spacing - 2*text_right_spacing,
                            y=center_y  - j*text_spacing - start_y_text,
                            text=scores[j],
                            showarrow=False,
                            xanchor="left",
                            font=dict(
                                family=font,
                                size=font_size,
                                color=font_color
                                ),
                            align='right'
                            )
        teams = semi_finals[1].split(' - ')
        scores = get_score_stings(df, team_names, teams)
        winners = compute_winner(scores)
        boxes_text.append([team_names[teams[0]], team_names[teams[1]]])
        for j, team in enumerate(teams):
            team_string = f'<b>{team}' if winners[j] else team
            fig.add_annotation(x=right-box_width-2*vertical_distance-2*box_width - vertical_border_spacing + text_left_spacing,
                                y=center_y - j*text_spacing - start_y_text,
                                text=team_string,
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    ),
                                align='left'
                                )
            scores = get_score_stings(df, team_names, teams)
            fig.add_annotation(x=right-box_width-2*vertical_distance-box_width - vertical_border_spacing - 2*text_right_spacing,
                            y=center_y - j*text_spacing - start_y_text,
                            text=scores[j],
                            showarrow=False,
                            xanchor="left",
                            font=dict(
                                family=font,
                                size=font_size,
                                color=font_color
                                ),
                            align='right'
                            )
    
    # adding lines between the quarter finals and the semi finals
    for i in range(2):
        fig.add_shape(type="line",
                    x0=left+box_width+vertical_distance+box_width + vertical_border_spacing,
                    y0=start_y + 2*(i)*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2 + box_height/2,
                    x1=left+box_width+1.5*vertical_distance+box_width + vertical_border_spacing,
                    y1=start_y + 2*(i)*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2 + box_height/2,
                    line=dict(color=line_color,width=line_width))
    
        fig.add_shape(type="line",
                    x0=right-box_width-vertical_distance-box_width - vertical_border_spacing,
                    y0=start_y + 2*(i)*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2 + box_height/2,
                    x1=right-box_width-1.5*vertical_distance-box_width - vertical_border_spacing,
                    y1=start_y + 2*(i)*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2 + box_height/2,
                    line=dict(color=line_color,width=line_width))
        fig.add_shape(type="line",
                        x0=(-1)**((i)%2)*(left+box_width+1.5*vertical_distance+box_width + vertical_border_spacing) + right*(i),
                        y0=start_y + (box_height + space_between_boxes)/2 + box_height/2,
                        x1=(-1)**((i)%2)*(left+box_width+1.5*vertical_distance+box_width + vertical_border_spacing) + right*(i),
                        y1=start_y+box_height + 2*(box_height + space_between_boxes) + space_between_boxes/2,
                        line=dict(color=line_color,width=line_width))
    fig.add_shape(type="line",
                        x0=left+box_width+1.5*vertical_distance+box_width + vertical_border_spacing,
                        y0=center_y,
                        x1=left+box_width+2*vertical_distance+box_width + vertical_border_spacing,
                        y1=center_y,
                        line=dict(color=line_color,width=line_width))
        
    fig.add_shape(type="line",
                          x0=right-box_width-1.5*vertical_distance-box_width - vertical_border_spacing,
                            y0=center_y,
                            x1=right-box_width-2*vertical_distance-box_width - vertical_border_spacing,
                            y1=center_y,
                            line=dict(color=line_color,width=line_width))
    # Third place
    x0 = center_x - box_width/2
    x1 = center_x + box_width/2
    y0 = center_y - 3*box_height
    y1 = center_y - 2*box_height
    boxes_x.append([x0,x1])
    boxes_y.append([y0,y1])
    fig.add_shape(type="rect",
                    x0=x0,
                    y0=y0,
                    x1=x1,
                    y1=y1,
                    line=dict(color=line_color,width=line_width),
                    fillcolor="LightSkyBlue")            
    fig.add_annotation(x=center_x,
                        y=center_y - 1.8*box_height,
                        text='Third Place',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color=font_color
                            ),
                        align='center'
                        )
    if spoilers:
        teams = third_place[0].split(' - ')
        scores = get_score_stings(df, team_names, teams)
        winners = compute_winner(scores)
        boxes_text.append([team_names[teams[0]], team_names[teams[1]]])
        for j, team in enumerate(teams):
            team_string = f'<b>{team}' if winners[j] else team
            fig.add_annotation(x=center_x - box_width/2 + text_left_spacing,
                                y=center_y - j*text_spacing - start_y_text - 2.5*box_height,
                                text=team_string,
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color=font_color
                                    ),
                                align='center'
                                )
            fig.add_annotation(x=center_x + box_width/2 - 2*text_right_spacing,
                            y=center_y - j*text_spacing - start_y_text - 2.5*box_height,
                            text=scores[j],
                            showarrow=False,
                            xanchor="left",
                            font=dict(
                                family=font,
                                size=font_size,
                                color=font_color
                                ),
                            align='right'
                            )
    # Final
    x0 = center_x - box_width/2
    x1 = center_x + box_width/2
    y0 = center_y + (box_height)/2
    y1 = center_y - (box_height)/2
    boxes_x.append([x0,x1])
    boxes_y.append([y0,y1])
    fig.add_shape(type="rect",
                    x0=x0,
                    y0=y0,
                    x1=x1,
                    y1=y1,
                    line=dict(color=line_color,width=line_width),
                    fillcolor="LightSkyBlue")
    fig.add_annotation(x=center_x,
                        y=center_y + 0.7*box_height,
                        text='Final',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color=font_color
                            ),
                        align='center'
                        )
    if spoilers:
            
        teams = final[0].split(' - ')
        scores = get_score_stings(df, team_names, teams)
        winners = compute_winner(scores)
        boxes_text.append([team_names[teams[0]], team_names[teams[1]]])
        for j, team in enumerate(teams):
            team_string = f'<b>{team}' if winners[j] else team
            fig.add_annotation(x=center_x - box_width/2 + text_left_spacing,
                                y=center_y - j*text_spacing - start_y_text,
                                text=f'{team_string}',
                                showarrow=False,
                                xanchor="left",
                                font={'family': font, 'size': font_size,
                                      'color': font_color},
                                align='center'
                                )
                
            fig.add_annotation(x=center_x + box_width/2 - 2*text_right_spacing,
                            y=center_y - j*text_spacing - start_y_text,
                            text=scores[j],
                            showarrow=False,
                            xanchor="left",
                            font=dict(
                                family=font,
                                size=font_size,
                                color=font_color
                                ),
                            align='right'
                            )
    # adding lines between the semi finals and the final
    
    fig.add_shape(type="line",
                    x0=left+box_width+2*vertical_distance+2*box_width + vertical_border_spacing,
                    y0=center_y,
                    x1=center_x - box_width/2,
                    y1=center_y,
                    line=dict(color=line_color,width=line_width))
    fig.add_shape(type="line",
                    x0=right-box_width-2*vertical_distance-2*box_width - vertical_border_spacing,
                    y0=center_y,
                    x1=center_x + box_width/2,
                    y1=center_y,
                    line=dict(color=line_color,width=line_width))
    fig.update_layout(clickmode='event+select')
    
    
    fig.add_trace(go.Heatmap(
        z=[[1 for _ in range(int(right*heatmap_scale))] for _ in range(int(top*heatmap_scale))],
        hoverinfo='none',
        showscale=False,
        x=[x/heatmap_scale for x in range(int(right*heatmap_scale))],
        y=[y/heatmap_scale for y in range(int(top*heatmap_scale))],
        hoverongaps=True,
        name='Heatmap',
        text=[x for x in range(int(right*heatmap_scale*top*heatmap_scale))],
    ))
    for index, box in enumerate(boxes_x):
        box.sort()
        boxes_x[index] = box
        
    for index, box in enumerate(boxes_y):
        box.sort()
        boxes_y[index] = box
        
    boxes_data = {'x': boxes_x, 'y': boxes_y, 'text': boxes_text}
    if initialize:
        return fig, boxes_data
    else:
        return fig
    
@app.callback(
    Output('bracket', 'figure'),
    Input('spoiler-switch', 'on'),
    prevent_initial_call=True)

def show_match_results(spoilers):
    return create_playoff_bracket(spoilers)
        
@app.callback(
    Output('debug', 'children'),
    Input('bracket', 'clickData'),
    State('boxes-store', 'data'),
)
def bracket_click(clickData, storedata):
    x = clickData['points'][0]['x']
    y = clickData['points'][0]['y']
    boxes_x = storedata['x']
    boxes_x = [tuple(x) for x in boxes_x]
    boxes_y = storedata['y']
    boxes_y = [tuple(y) for y in boxes_y]
    boxes_text = [['Brazil', 'Korea Republic'],
                  ['Portugal', 'Switzerland'],
                  ['Japan', 'Croatia'],
                  ['Morocco', 'Spain'],
                  ['Argentina', 'Australia'],
                  ['France', 'Poland'],
                  ['Netherlands', 'United States'],
                  ['England', 'Senegal'],
                  ['Croatia', 'Brazil'],
                  ['Morocco', 'Portugal'],
                  ['Netherlands', 'Argentina'],
                  ['England', 'France'],
                  ['Argentina', 'Croatia'],
                  ['France', 'Morocco'],
                  ['Croatia', 'Morocco'],
                  ['Argentina', 'France']]
    x_range_true = []
    y_range_true = []
    for index_y, (start_x, end_x) in enumerate(boxes_x):
        if start_x <= x <= end_x:
            x_range_true.append(index_y)
    for index_y, (start_y, end_y) in enumerate(boxes_y):
        if start_y <= y <= end_y:
            y_range_true.append(index_y)
    
    both_true = list(set(x_range_true).intersection(y_range_true))

    if both_true:
        df_po = pd.read_csv(f'{data_folder}/match_data.csv')
        id = df_po.loc[(df_po['home_team'] == str(boxes_text[both_true[0]][0])) & (df_po['away_team'] == str(boxes_text[both_true[0]][1])), 'match_id']
        return create_match_dashboard(int(id))
        
    return 'No box selected'


pd.read_csv(f'{data_folder}/match_data.csv')