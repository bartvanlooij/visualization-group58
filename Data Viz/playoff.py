from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_playoff_bracket():
    left = 0
    right = 1000
    top = 1000
    bottom = 0
    vertical_distance = 50
    bottom = 0
    box_width = 100
    box_height = 100
    space_between_boxes = 40
    vertical_border_spacing = 20
    line_width = 1
    center_x = (right-left)/2
    center_y = (top-bottom)/2
    eigth_finals = ['Brasil - Korea', 'Japan - Croatia', 'Argentina - Australia', 'Netherlands - USA',
                      'Portugal - Switzerland', 'Marocco - Spain', 'France - Poland', 'England - Senegal']
    quart_finals = ['Brasil - Croatia', 'Netherlands - Argentina', 'Marocco - Portugal', 'England - France']
    semi_finals = ['Argentina - Croatia', 'France - Marocco']
    final = ['Argentina - France']
    third_place = ['Croatia - Marocco']
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
                      fillcolor="LightSkyBlue",)
        #Create 4 boxes on the right side of the
        #bracket making the allgined in the middle of the y
        fig.add_shape(type="rect",
                      x0=right-box_width - vertical_border_spacing,
                      y0=start_y + i*(box_height + space_between_boxes),
                      x1=right - vertical_border_spacing,
                      y1=start_y+box_height + i*(box_height + space_between_boxes),
                      line=dict(color="RoyalBlue",width=line_width),
                      fillcolor="LightSkyBlue")
        
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
    
    # Final
    fig.add_shape(type="rect",
                    x0=center_x - box_width/2,
                    y0=center_y + (box_height)/2,
                    x1=center_x + box_width/2,
                    y1=center_y - (box_height)/2,
                    line=dict(color="RoyalBlue",width=line_width),
                    fillcolor="LightSkyBlue")
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
    return dcc.Graph(id='bracket', figure=fig, 
                     style={'width': right, 'height': top})