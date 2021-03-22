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
    children=[
        dbc.NavbarSimple(
            children=[
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Page 2", href="#"),
                        dbc.DropdownMenuItem("Page 2", href="#"),
                        dbc.DropdownMenuItem("Page 2", href="#"),
                        dbc.DropdownMenuItem("Page 2", href="#"),
                        dbc.DropdownMenuItem("Page 2", href="#"),
                        dbc.DropdownMenuItem("Page 2", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="References",
                ),
            ],
            brand="NavbarSimple",
            brand_href="#",
            color="primary",
            dark=True,
        ),
    ], style={"width": "85%"})

if __name__ == '__main__':
    app.run_server(debug=True)
