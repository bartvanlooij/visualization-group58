from functions import *
from variables import *
from dash import Dash, html, dcc, Input, Output, State


# Initial layout for 'right-column' with general home page content

# Define the layout of the app with a 50% transparent background
app.layout = html.Div(
    id="app-container",
    children=initial_app_content,
    style={
        "fontFamily": "Arial, sans-serif",
        "width": "100%",
        "min-height": "100vh"
    }
)

if __name__ == '__main__':
    app.run_server(debug=True)