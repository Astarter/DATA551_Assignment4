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
app.layout = html.Div([
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
        brand="Canada 1999-2019 Macroeconomic Analysis",
        brand_href="#",
        color="primary",
        dark=True,
        style={"position": "sticky"}
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
                tooltip={"placement": "topLeft"})
        ], width=6),
        dbc.Col([
            dbc.Label(html.H5("Province:")),
            dcc.Dropdown(
                id="geo",
                options=drop_options,
                value="British Columbia"
            )], width=6
        )
    ], style={
        "margin-left": "3px",
        "margin-right": "3px",
    }),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Tabs([
                dbc.Tab([
                    # Tab 1:
                    dbc.Row([
                        dbc.Col([
                            # Graphs:
                            dbc.Row([
                                dbc.Col([
                                    html.Iframe(
                                        id='tab1_1',
                                        style={'border-width': '0', 'width': '100%', 'height': '900px'}
                                    )
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Iframe(
                                        id='tab1_2',
                                        style={'border-width': '0', 'width': '100%', 'height': '900px'}
                                    )
                                ]),
                            ]),
                        ], width=8
                        ),
                        dbc.Col([
                            # Texts:

                        ], width=4
                        )
                    ])
                ],
                    label="Real GDP",
                ),
                dbc.Tab([
                    # Tab 1:
                    dbc.Row([
                        dbc.Col([
                            # Graphs:
                            dbc.Row([
                                dbc.Col([
                                    html.Iframe(
                                        id='tab2_1',
                                        style={'border-width': '0', 'width': '100%', 'height': '900px'}
                                    )
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Iframe(
                                        id='tab2_2',
                                        style={'border-width': '0', 'width': '100%', 'height': '900px'}
                                    )
                                ]),
                            ]),
                        ], width=8
                        ),
                        dbc.Col([
                            # Texts:

                        ], width=4
                        )
                    ])
                ], label="Nominal GDP"),
                dbc.Tab(label="Labour Force"),
                dbc.Tab(label="Inflation"),
            ])
        )
    ], style={
        "margin-left": "3px",
        "margin-right": "3px",
    })
], style={
    "width": "100%",
}
)


@app.callback(
    Output('tab1_1', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t1_visuals.concat_gpd_vis(year, geo)


@app.callback(
    Output('tab1_2', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t1_visuals.concat_gdpc_vis(year, geo)


@app.callback(
    Output('tab2_1', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t2_visuals.concat_ngdp_vis(year, geo)


@app.callback(
    Output('tab2_2', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t2_visuals.concat_ngdpc_vis(year, geo)


if __name__ == '__main__':
    app.run_server(debug=True)
