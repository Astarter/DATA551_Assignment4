"""
This file renders all the layouts.
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    html.H1("GDP")
)

if __name__ == '__main__':
    app.run_server(debug=True)
