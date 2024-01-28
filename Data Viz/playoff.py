from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_playoff_bracket():
    left = 0
    right = 1000
    top = 1000
    bottom = 0
    center_x = (right-left)/2
    center_y = (top-bottom)/2
    vertical_distance = 50
    bottom = 0
    box_width = 100
    box_height = 100
    space_between_boxes = 40
    
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
                      x0=left,
                      y0=start_y + i*(box_height + space_between_boxes),
                      x1=left+box_width,
                      y1=start_y+box_height + i*(box_height + space_between_boxes),
                      line=dict(color="RoyalBlue",width=2),
                      fillcolor="LightSkyBlue",)
        #Create 4 boxes on the right side of the
        #bracket making the allgined in the middle of the y
        fig.add_shape(type="rect",
                      x0=right-box_width,
                      y0=start_y + i*(box_height + space_between_boxes),
                      x1=right,
                      y1=start_y+box_height + i*(box_height + space_between_boxes),
                      line=dict(color="RoyalBlue",width=2),
                      fillcolor="LightSkyBlue")
        
    # Quarter finals
    for i in range(2):
        #Create 2 boxes on vertical_distance pixels to the right of the left side of the bracket
        #
        fig.add_shape(type="rect",
                      x0=left+box_width+vertical_distance,
                      y0=start_y + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2,
                      x1=left+box_width+vertical_distance+box_width,
                      y1=start_y+box_height + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2,
                      line=dict(color="RoyalBlue",width=2),
                      fillcolor="LightSkyBlue")
        # Create 2 boxes on vertical_distance pixels to the left of the right side of the bracket
        #
        fig.add_shape(type="rect",
                      x0=right-box_width-vertical_distance-box_width,
                      y0=start_y + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2,
                      x1=right-box_width-vertical_distance,
                      y1=start_y+box_height + 2*i*(box_height + space_between_boxes) + (box_height + space_between_boxes)/2,
                      line=dict(color="RoyalBlue",width=2),
                      fillcolor="LightSkyBlue")
        
    # Adding all the lines between the boxes of the 1/8 finals with the quarter finals
    for i in range(4):
        fig.add_shape(type="line",
                      x0=left+box_width,
                      y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      x1=left+box_width+vertical_distance/2,
                      y1=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      line=dict(color="RoyalBlue",width=2))
        fig.add_shape(type="line",
                      x0=right-box_width,
                      y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      x1=right-box_width-vertical_distance/2,
                      y1=start_y + box_height/2 + i*(box_height + space_between_boxes),
                      line=dict(color="RoyalBlue",width=2))
        if i % 2 == 0:
            fig.add_shape(type="line",
                          x0=left+box_width+vertical_distance/2,
                          y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                          x1=left+box_width+vertical_distance/2,
                          y1=start_y + box_height/2 + (i+1)*(box_height + space_between_boxes),
                          line=dict(color="RoyalBlue",width=2))
            fig.add_shape(type="line",
                          x0=right-box_width-vertical_distance/2,
                          y0=start_y + box_height/2 + i*(box_height + space_between_boxes),
                          x1=right-box_width-vertical_distance/2,
                          y1=start_y + box_height/2 + (i+1)*(box_height + space_between_boxes),
                          line=dict(color="RoyalBlue",width=2))
            fig.add_shape(type="line",
                          x0=left+box_width+vertical_distance/2,
                          y0=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                          x1=left+box_width+vertical_distance,
                          y1=start_y - space_between_boxes/2+ (i+1)*(box_height + space_between_boxes),
                          line=dict(color="RoyalBlue",width=2))
        
    # Semi finals
    fig.add_shape(type="rect",
                    x0=left+box_width+2*vertical_distance+box_width,
                    y0=center_y + (box_height)/2,
                    x1=left+box_width+2*vertical_distance+2*box_width,
                    y1=center_y - (box_height)/2,
                    line=dict(color="RoyalBlue",width=2),
                    fillcolor="LightSkyBlue")
    fig.add_shape(type="rect",
                    x0=right-box_width-2*vertical_distance-2*box_width,
                    y0=center_y + (box_height)/2,
                    x1=right-box_width-2*vertical_distance-box_width,
                    y1=center_y - (box_height)/2,
                    line=dict(color="RoyalBlue",width=2),
                    fillcolor="LightSkyBlue")
    
    
    # Final
    fig.add_shape(type="rect",
                    x0=center_x - box_width/2,
                    y0=center_y + (box_height)/2,
                    x1=center_x + box_width/2,
                    y1=center_y - (box_height)/2,
                    line=dict(color="RoyalBlue",width=2),
                    fillcolor="LightSkyBlue")
    return dcc.Graph(id='bracket', figure=fig, 
                     style={'width': right, 'height': top})