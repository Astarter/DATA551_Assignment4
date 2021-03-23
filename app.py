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
server = app.server
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
        sticky='top'
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
                dbc.Tab(
                    [
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
                                html.Br(),
                                # Texts:
                                dbc.Jumbotron(
                                    [
                                        html.H2("Real GDP", className="display-4"),
                                        html.H4("Gross domestic product(GDP)"),
                                        html.P(
                                            "The total unduplicated value of the goods and services produced in the "
                                            "economic territory of a country or region during a given period. A "
                                            "valuation expressed in terms of the prices actually paid by the "
                                            "purchaser after all applicable taxes and subsidies. "
                                        ),
                                        html.Hr(className="my-2"),
                                        html.H4("GDP, expenditure-based"),
                                        html.P(
                                            "The sum of expenditure on final consumption plus gross capital formation "
                                            "plus exports less imports. "
                                        ),
                                        html.Hr(className="my-2"),
                                        html.H4("GDP at market prices"),
                                        html.P(
                                            "Gross domestic product at basic prices (traditional value) plus taxes "
                                            "less subsidies on products. "
                                        ),
                                        html.Hr(className="my-2"),
                                        html.H4("Real gross domestic product"),
                                        html.P(
                                            "Gross domestic product at constant prices (chained 2012 dollars)."
                                        ),
                                        html.Hr(className="my-2"),
                                        html.H4("Chained dollars"),
                                        html.P(
                                            "Method of adjusting real dollar amounts for inflation over time, "
                                            "to allow the comparison of figures from different years. It generally "
                                            "reflects dollar figures computed with 2012 as the base year. "
                                        ),
                                    ]
                                )
                            ], width=4
                            )
                        ])
                    ],
                    label="Real GDP",
                ),
                dbc.Tab(
                    [
                        # tab1.5
                        dbc.Row([
                            dbc.Col([
                                dbc.Jumbotron(
                                    [
                                        html.H2("Real GDP - Industry", className="display-4"),
                                        html.H4("GDP by Industry"),
                                        html.P(
                                            "Also referred to as valued-added, equals output by the industry minus "
                                            "the value of intermediate inputs that were purchased from other "
                                            "industries. domestic or foreign. "
                                        )
                                    ]
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Iframe(
                                    id='tab1_5_1',
                                    style={'border-width': '0', 'width': '100%', 'height': '900px'}
                                )
                            ])
                        ])
                    ],
                    label="Real GDP - Industry"),
                dbc.Tab(
                    [
                        # Tab 2:
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
                                html.Br(),
                                # Texts:
                                dbc.Jumbotron(
                                    [
                                        html.H2("Nominal GDP", className="display-4"),
                                        html.H4("Gross domestic product(GDP)"),
                                        html.P(
                                            "The total unduplicated value of the goods and services produced in the "
                                            "economic territory of a country or region during a given period. A "
                                            "valuation expressed in terms of the prices actually paid by the "
                                            "purchaser after all applicable taxes and subsidies. "
                                        ),
                                        html.Hr(className="my-2"),
                                        html.H4("GDP, expenditure-based"),
                                        html.P(
                                            "The sum of expenditure on final consumption plus gross capital formation "
                                            "plus exports less imports. "
                                        ),
                                        html.Hr(className="my-2"),
                                        html.H4("GDP at market prices"),
                                        html.P(
                                            "Gross domestic product at basic prices (traditional value) plus taxes "
                                            "less subsidies on products. "
                                        ),
                                        html.Hr(className="my-2"),
                                        html.H4("Nominal GDP"),
                                        html.P(
                                            "Gross domestic product using current prices, without adjusting for "
                                            "inflation. "
                                        ),
                                        html.Hr(className="my-2"),
                                        html.H4("Chained dollars"),
                                        html.P(
                                            "Method of adjusting real dollar amounts for inflation over time, "
                                            "to allow the comparison of figures from different years. It generally "
                                            "reflects dollar figures computed with 2012 as the base year. "
                                        ),
                                    ]
                                )
                            ], width=4
                            )
                        ])
                    ],
                    label="Nominal GDP"),
                dbc.Tab(
                    [
                        # tab 3:
                        dbc.Row([
                            dbc.Col([
                                dbc.Jumbotron(
                                    [
                                        html.H2("Labour Force", className="display-4"),
                                        html.H4("Unemployment Rate"),
                                        html.P(
                                            "Unemployed people as a percentage of the labour force."
                                        )
                                    ]
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Iframe(
                                    id='tab3_1',
                                    style={'border-width': '0', 'width': '100%', 'height': '600px'}
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Iframe(
                                    id='tab3_2',
                                    style={'border-width': '0', 'width': '100%', 'height': '900px'}
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Jumbotron(
                                    [
                                        html.H4("Earnings"),
                                        html.P(
                                            "Employment and average weekly earnings (including overtime) for all "
                                            "employees. "
                                        )
                                    ]
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Iframe(
                                    id='tab3_3',
                                    style={'border-width': '0', 'width': '100%', 'height': '300px'}
                                )
                            ])
                        ]),
                    ],
                    label="Labour Force"),
                dbc.Tab(
                    [
                        # tab4:
                        dbc.Row([
                            dbc.Col([
                                dbc.Jumbotron(
                                    [
                                        html.H2("Inflation", className="display-4"),
                                        html.H4("Price index"),
                                        html.P("An average of the proportionate changes in the prices of a specified "
                                               "set of goods and services between two periods of time."),
                                        html.Hr(className="my-2"),
                                        html.H4("Consumer Price Index(CPI)"),
                                        html.P("Represents changes in prices as experienced by consumers. It measures "
                                               "price change by comparing, through time, the cost of a fixed basket "
                                               "of goods and services."),
                                    ]
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Iframe(
                                    id='tab4_1',
                                    style={'border-width': '0', 'width': '100%', 'height': '900px'}
                                )
                            ])
                        ])
                    ],
                    label="Inflation"),
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
    Output('tab1_5_1', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t1_visuals.concat_gdp_indus_vis(year, geo)


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


@app.callback(
    Output('tab3_1', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t3_visuals.concat_employment_vis(year, geo)


@app.callback(
    Output('tab3_2', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t3_visuals.concat_earnings_vis(year, geo)


@app.callback(
    Output('tab3_3', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t3_visuals.concat_earnings_rank(year, geo)


@app.callback(
    Output('tab4_1', 'srcDoc'),
    Input('year', 'value'),
    Input("geo", 'value'))
def update_output(year, geo):
    return t4_visuals.concat_cpi_vis(year, geo)


if __name__ == '__main__':
    app.run_server(debug=True)
