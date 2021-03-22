"""
This file renders all the layouts.
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# prepare the slider and drop down menu items:
import pandas as pd
from src import wranglings as wr

years = pd.unique(wr.eco["Year"])
minyear = int(min(years))
maxyear = int(max(years))

drop_options = []
provinces = pd.unique(wr.eco["Geography"])
for i in provinces:
    temp = {"label": i, "value": i}
    drop_options.append(temp)

# Import pre-made visualizations:
from src import t1_visuals, t2_visuals, t3_visuals, t4_visuals

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("GDP", href="https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid"
                                                     "=3610022201"),
                    dbc.DropdownMenuItem("Population", href="https://www150.statcan.gc.ca/t1/tbl1/en/cv.action"
                                                            "?pid=1710000501"),
                    dbc.DropdownMenuItem("GDP by industry, provinces and territories", href="https://www150"
                                                                                            ".statcan.gc.ca/t1"
                                                                                            "/tbl1/en/cv.action"
                                                                                            "?pid=3610040201"),
                    dbc.DropdownMenuItem("Labour force", href="https://www150.statcan.gc.ca/t1/tbl1/en/cv.action"
                                                              "?pid=1410002301"),
                    dbc.DropdownMenuItem("Weekly Earnings by industry", href="https://www150.statcan.gc.ca/t1"
                                                                             "/tbl1/en/cv.action?pid=1410020401"),
                    dbc.DropdownMenuItem("Consumer price index", href="https://www150.statcan.gc.ca/t1/tbl1/en/cv"
                                                                      ".action?pid=1810000501"),
                ],
                nav=True,
                in_navbar=True,
                label="References",
            ),
        ],
        brand="Canada 21st Century Macroeconomic Analysis",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Label(html.H5("Year:")),
            dcc.Slider(
                id="year",
                min=minyear,
                max=maxyear,
                value=2009,
                marks={minyear: str(minyear), 2009: "2009", maxyear: str(maxyear)},
                tooltip={"placement":"topLeft"})
        ], width=6),
        dbc.Col([
            dbc.Label(html.H5("Province:")),
            dcc.Dropdown(
                id="geo",
                options=drop_options,
                value="British Columbia"
            )], width=6
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Tabs([
                dbc.Tab(label="Real GDP"),
                dbc.Tab(label="Nominal GDP"),
                dbc.Tab(label="Labour Force"),
                dbc.Tab(label="Inflation"),
            ])
        )
    ]),
    dbc.Row([
        dbc.Col(
            width=6
        ),
        dbc.Col(
            width=6
        )
    ])
], style={"width": "85%"}
)

if __name__ == '__main__':
    app.run_server(debug=True)
