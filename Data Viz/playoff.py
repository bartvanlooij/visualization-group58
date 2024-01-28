

from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq
from initial_content import app
import pandas as pd
from variables import data_folder, playoff_right, playoff_top

def create_playoff_bracket(spoilers=False):
    if spoilers:
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
    text_spacing = 20
    font_size = 15
    start_y_text = 20
    text_left_spacing = 20
    eigth_finals = ['Brasil - Korea', 'Japan - Croatia', 'Argentina - Australia', 'Netherlands - USA',
                    'Portugal - Switzerland', 'Morocco - Spain', 'France - Poland', 'England - Senegal']
    quart_finals = ['Croatia - Brasil', 'Netherlands - Argentina', 'Morocco - Portugal', 'England - France']
    semi_finals = ['Argentina - Croatia', 'France - Morocco']
    final = ['Argentina - France']
    third_place = ['Croatia - Morocco']
    fig = go.Figure()
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
    
    #The 1/8 finals
    for i in range(4):
        #Create 4 boxes on the left side of the 
        #bracket making the allgined in the middle of the y
        fig.add_shape(type="rect",
                      x0=left+ vertical_border_spacing,
                      y0=start_y + i*(box_height + space_between_boxes),
                      x1=left+box_width+ vertical_border_spacing,
                      y1=start_y+box_height + i*(box_height + space_between_boxes),
                      line=dict(color="RoyalBlue",width=line_width),
                      fillcolor="LightSkyBlue")
        teams = eigth_finals[i].split(' - ')
        for j, team in enumerate(teams):
            fig.add_annotation(x=left + vertical_border_spacing + text_left_spacing,
                                y=start_y+box_height/2 + i*(box_height + space_between_boxes)- j*text_spacing - start_y_text,
                                text=team,
                                xanchor="left",
                                showarrow=False,
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color="RoyalBlue"
                                    )
                                )
            if spoilers:
                
                score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
                if len(score) == 3:
                    scores = [score[0], score[2]]
                else:
                    scores = [score[4], score[6]]
                fig.add_annotation(x=left + box_width + vertical_border_spacing - text_left_spacing,
                                y=start_y+box_height/2 + i*(box_height + space_between_boxes)- j*text_spacing - start_y_text,
                                text=scores[j],
                                showarrow=False,
                                xanchor="right",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color="RoyalBlue"
                                    ),
                                align='right'
                                )
        #Create 4 boxes on the right side of the
        #bracket making the allgined in the middle of the y
        fig.add_shape(type="rect",
                      x0=right-box_width - vertical_border_spacing,
                      y0=start_y + i*(box_height + space_between_boxes),
                      x1=right - vertical_border_spacing,
                      y1=start_y+box_height + i*(box_height + space_between_boxes),
                      line=dict(color="RoyalBlue",width=line_width),
                      fillcolor="LightSkyBlue")
        teams = eigth_finals[i+4].split(' - ')
        for j, team in enumerate(teams):
            fig.add_annotation(x=right - box_width - vertical_border_spacing + text_left_spacing,
                                y=start_y+box_height/2 + i*(box_height + space_between_boxes)- j*text_spacing - start_y_text,
                                text=team,
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color="RoyalBlue"
                                    ),
                                align='left'
                                )
            if spoilers:
                
                score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
                if len(score) == 3:
                    scores = [score[0], score[2]]
                else:
                    scores = [score[4], score[6]]
                fig.add_annotation(x=right - vertical_border_spacing - text_left_spacing,
                                y=start_y+box_height/2 + i*(box_height + space_between_boxes)- j*text_spacing - start_y_text,
                                text=scores[j],
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color="RoyalBlue"
                                    ),
                                align='left'
                                )

    # Quarter finals
    for i in range(2):
        #Create 2 boxes on vertical_distance pixels to the right of the left side of the bracket
        #
        fig.add_shape(type="rect",
                      x0=left+box_width+vertical_distance+ vertical_border_spacing,
                      y0=start_y + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2,
                      x1=left+box_width+vertical_distance+box_width + vertical_border_spacing,
                      y1=start_y+box_height + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2,
                      line=dict(color="RoyalBlue",width=line_width),
                      fillcolor="LightSkyBlue")
        # Create 2 boxes on vertical_distance pixels to the left of the right side of the bracket
        #
        fig.add_shape(type="rect",
                      x0=right-box_width-vertical_distance-box_width - vertical_border_spacing,
                      y0=start_y + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2,
                      x1=right-box_width-vertical_distance- vertical_border_spacing,
                      y1=start_y+box_height + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2,
                      line=dict(color="RoyalBlue",width=line_width),
                      fillcolor="LightSkyBlue")
        teams = quart_finals[i].split(' - ')
        for j, team in enumerate(teams):
            
            fig.add_annotation(x=left+box_width+vertical_distance+ vertical_border_spacing + text_left_spacing,
                                y=start_y+box_height/2 + 2*i*(box_height + space_between_boxes)+ (box_height + space_between_boxes)/2-j*text_spacing - start_y_text,
                                text=team,
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color="RoyalBlue"
                                    ),
                                align='left'
                                )
            
            if spoilers:
                
                score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
                if len(score) == 3:
                    scores = [score[0], score[2]]
                else:
                    scores = [score[4], score[6]]
                fig.add_annotation(x=left+box_width+vertical_distance+box_width + vertical_border_spacing - text_left_spacing,
                                y=start_y+box_height/2 + 2*i*(box_height + space_between_boxes)+ (box_height + space_between_boxes)/2-j*text_spacing - start_y_text,
                                text=scores[j],
                                showarrow=False,
                                xanchor="right",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color="RoyalBlue"
                                    ),
                                align='right'
                                )
            
        teams = quart_finals[i+2].split(' - ')
        for j, team in enumerate(teams):
            fig.add_annotation(x=right-box_width-vertical_distance-box_width - vertical_border_spacing + text_left_spacing,
                                y=start_y+box_height/2 + 2*i*(box_height + space_between_boxes)+ (box_height + space_between_boxes)/2-j*text_spacing - start_y_text,
                                text=team,
                                showarrow=False,
                                xanchor="left",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color="RoyalBlue"
                                    ),
                                align='left'
                                )
            if spoilers:
                
                score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
                if len(score) == 3:
                    scores = [score[0], score[2]]
                else:
                    scores = [score[4], score[6]]
                fig.add_annotation(x=right-box_width-vertical_distance - vertical_border_spacing - text_left_spacing,
                                y=start_y+box_height/2 + 2*i*(box_height + space_between_boxes)+ (box_height + space_between_boxes)/2-j*text_spacing - start_y_text,
                                text=scores[j],
                                showarrow=False,
                                xanchor="right",
                                font=dict(
                                    family=font,
                                    size=font_size,
                                    color="RoyalBlue"
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
                      line=dict(color="RoyalBlue",width=line_width))
        fig.add_shape(type="line",
                      x0=right-box_width - vertical_border_spacing,
                      y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      x1=right-box_width-vertical_distance/2 - vertical_border_spacing,
                      y1=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      line=dict(color="RoyalBlue",width=line_width))
        if i % 2 == 0:
            fig.add_shape(type="line",
                          x0=left+box_width+vertical_distance/2 + vertical_border_spacing,
                          y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                          x1=left+box_width+vertical_distance/2 + vertical_border_spacing,
                          y1=start_y + box_height/2 + (i+1)*(box_height + space_between_boxes),
                          line=dict(color="RoyalBlue",width=line_width))
            fig.add_shape(type="line",
                          x0=right-box_width-vertical_distance/2 - vertical_border_spacing,
                          y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                          x1=right-box_width-vertical_distance/2 - vertical_border_spacing,
                          y1=start_y + box_height/2 + (i+1)*(box_height + space_between_boxes),
                          line=dict(color="RoyalBlue",width=line_width))
            fig.add_shape(type="line",
                          x0=left+box_width+vertical_distance/2 + vertical_border_spacing,
                          y0=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                          x1=left+box_width+vertical_distance + vertical_border_spacing,
                          y1=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                          line=dict(color="RoyalBlue",width=line_width))
            fig.add_shape(type="line",
                            x0=right-box_width-vertical_distance/2 - vertical_border_spacing,
                            y0=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                            x1=right-box_width-vertical_distance - vertical_border_spacing,
                            y1=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                            line=dict(color="RoyalBlue",width=line_width))
        
    # Semi finals
    fig.add_shape(type="rect",
                    x0=left+box_width+2*vertical_distance+box_width + vertical_border_spacing,
                    y0=center_y + (box_height)/2,
                    x1=left+box_width+2*vertical_distance+2*box_width + vertical_border_spacing,
                    y1=center_y - (box_height)/2,
                    line=dict(color="RoyalBlue",width=line_width),
                    fillcolor="LightSkyBlue")
    fig.add_shape(type="rect",
                    x0=right-box_width-2*vertical_distance-2*box_width - vertical_border_spacing,
                    y0=center_y + (box_height)/2,
                    x1=right-box_width-2*vertical_distance-box_width - vertical_border_spacing,
                    y1=center_y - (box_height)/2,
                    line=dict(color="RoyalBlue",width=line_width),
                    fillcolor="LightSkyBlue")
    teams = semi_finals[0].split(' - ')
    for j, team in enumerate(teams):
        
        fig.add_annotation(x=left+box_width+2*vertical_distance+box_width + vertical_border_spacing + text_left_spacing,
                            y=center_y  - j*text_spacing - start_y_text,
                            text=team,
                            showarrow=False,
                            xanchor="left",
                            font=dict(
                                family=font,
                                size=font_size,
                                color="RoyalBlue"
                                ),
                            align='left'
                            )
        if spoilers:
            score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
            if len(score) == 3:
                scores = [score[0], score[2]]
            else:
                scores = [score[4], score[6]]
            fig.add_annotation(x=left+box_width+2*vertical_distance+2*box_width + vertical_border_spacing - text_left_spacing,
                            y=center_y  - j*text_spacing - start_y_text,
                            text=scores[j],
                            showarrow=False,
                            xanchor="right",
                            font=dict(
                                family=font,
                                size=font_size,
                                color="RoyalBlue"
                                ),
                            align='right'
                            )
    teams = semi_finals[1].split(' - ')
    for j, team in enumerate(teams):
        
        fig.add_annotation(x=right-box_width-2*vertical_distance-2*box_width - vertical_border_spacing + text_left_spacing,
                            y=center_y - j*text_spacing - start_y_text,
                            text=team,
                            showarrow=False,
                            xanchor="left",
                            font=dict(
                                family=font,
                                size=font_size,
                                color="RoyalBlue"
                                ),
                            align='left'
                            )
        if spoilers:
            score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
            if len(score) == 3:
                scores = [score[0], score[2]]
            else:
                scores = [score[4], score[6]]
            fig.add_annotation(x=right-box_width-2*vertical_distance-box_width - vertical_border_spacing - text_left_spacing,
                            y=center_y - j*text_spacing - start_y_text,
                            text=scores[j],
                            showarrow=False,
                            xanchor="right",
                            font=dict(
                                family=font,
                                size=font_size,
                                color="RoyalBlue"
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
                    line=dict(color="RoyalBlue",width=line_width))
    
        fig.add_shape(type="line",
                    x0=right-box_width-vertical_distance-box_width - vertical_border_spacing,
                    y0=start_y + 2*(i)*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2 + box_height/2,
                    x1=right-box_width-1.5*vertical_distance-box_width - vertical_border_spacing,
                    y1=start_y + 2*(i)*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2 + box_height/2,
                    line=dict(color="RoyalBlue",width=line_width))
        fig.add_shape(type="line",
                        x0=(-1)**((i)%2)*(left+box_width+1.5*vertical_distance+box_width + vertical_border_spacing) + right*(i),
                        y0=start_y + (box_height + space_between_boxes)/2 + box_height/2,
                        x1=(-1)**((i)%2)*(left+box_width+1.5*vertical_distance+box_width + vertical_border_spacing) + right*(i),
                        y1=start_y+box_height + 2*(box_height + space_between_boxes) + space_between_boxes/2,
                        line=dict(color="RoyalBlue",width=line_width))
    fig.add_shape(type="line",
                        x0=left+box_width+1.5*vertical_distance+box_width + vertical_border_spacing,
                        y0=center_y,
                        x1=left+box_width+2*vertical_distance+box_width + vertical_border_spacing,
                        y1=center_y,
                        line=dict(color="RoyalBlue",width=line_width))
        
    fig.add_shape(type="line",
                          x0=right-box_width-1.5*vertical_distance-box_width - vertical_border_spacing,
                            y0=center_y,
                            x1=right-box_width-2*vertical_distance-box_width - vertical_border_spacing,
                            y1=center_y,
                            line=dict(color="RoyalBlue",width=line_width))
    # Third place
    fig.add_shape(type="rect",
                    x0=center_x - box_width/2,
                    y0=center_y - 3*box_height,
                    x1=center_x + box_width/2,
                    y1=center_y - 2*box_height,
                    line=dict(color="RoyalBlue",width=line_width),
                    fillcolor="LightSkyBlue")            
    fig.add_annotation(x=center_x,
                        y=center_y - 1.8*box_height,
                        text='Third Place',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color="RoyalBlue"
                            ),
                        align='center'
                        )
    teams = third_place[0].split(' - ')
    for j, team in enumerate(teams):
        fig.add_annotation(x=center_x - box_width/2 + text_left_spacing,
                            y=center_y - j*text_spacing - start_y_text - 2.5*box_height,
                            text=team,
                            showarrow=False,
                            xanchor="left",
                            font=dict(
                                family=font,
                                size=font_size,
                                color="RoyalBlue"
                                ),
                            align='center'
                            )
        if spoilers:
            
            score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
            if len(score) == 3:
                scores = [score[0], score[2]]
            else:
                scores = [score[4], score[6]]
            fig.add_annotation(x=center_x + box_width/2 - text_left_spacing,
                            y=center_y - j*text_spacing - start_y_text - 2.5*box_height,
                            text=scores[j],
                            showarrow=False,
                            xanchor="right",
                            font=dict(
                                family=font,
                                size=font_size,
                                color="RoyalBlue"
                                ),
                            align='right'
                            )
    # Final
    fig.add_shape(type="rect",
                    x0=center_x - box_width/2,
                    y0=center_y + (box_height)/2,
                    x1=center_x + box_width/2,
                    y1=center_y - (box_height)/2,
                    line=dict(color="RoyalBlue",width=line_width),
                    fillcolor="LightSkyBlue")
    fig.add_annotation(x=center_x,
                        y=center_y + 0.7*box_height,
                        text='Final',
                        showarrow=False,
                        xanchor="center",
                        font=dict(
                            family=font,
                            size=font_size,
                            color="RoyalBlue"
                            ),
                        align='center'
                        )
        
    teams = final[0].split(' - ')
    for j, team in enumerate(teams):
        fig.add_annotation(x=center_x - box_width/2 + text_left_spacing,
                            y=center_y - j*text_spacing - start_y_text,
                            text=team,
                            showarrow=False,
                            xanchor="left",
                            font=dict(
                                family=font,
                                size=font_size,
                                color="RoyalBlue"
                                ),
                            align='center'
                            )
        if spoilers:
            
            score = df[(df['home_team'] == team_names[teams[0]]) & (df['away_team'] == team_names[teams[1]])]['score'].values[0]
            if len(score) == 3:
                scores = [score[0], score[2]]
            else:
                scores = [score[4], score[6]]
            fig.add_annotation(x=center_x + box_width/2 - text_left_spacing,
                            y=center_y - j*text_spacing - start_y_text,
                            text=scores[j],
                            showarrow=False,
                            xanchor="right",
                            font=dict(
                                family=font,
                                size=font_size,
                                color="RoyalBlue"
                                ),
                            align='right'
                            )
    # adding lines between the semi finals and the final
    
    fig.add_shape(type="line",
                    x0=left+box_width+2*vertical_distance+2*box_width + vertical_border_spacing,
                    y0=center_y,
                    x1=center_x - box_width/2,
                    y1=center_y,
                    line=dict(color="RoyalBlue",width=line_width))
    fig.add_shape(type="line",
                    x0=right-box_width-2*vertical_distance-2*box_width - vertical_border_spacing,
                    y0=center_y,
                    x1=center_x + box_width/2,
                    y1=center_y,
                    line=dict(color="RoyalBlue",width=line_width))
    return fig
    
@app.callback(
    Output('bracket', 'figure'),
    Input('spoiler-switch', 'on'),
    prevent_initial_call=True)
def show_match_results(spoilers):
    return create_playoff_bracket(spoilers)
    
