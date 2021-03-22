"""
This file draws all of the graphs
"""

import altair as alt
import pandas as pd

alt.data_transformers.disable_max_rows()
alt.themes.enable('latimes')

# load in the datasets:

eco = pd.read_csv('Data/eco.csv')
my_cols = eco[eco.columns[2:16]].columns
eco.set_index(['Geography', 'Year', 'Industry'], inplace=True)

eco_gr = eco.pct_change().reset_index()
eco_gr.loc[eco_gr.Year == 1999, my_cols] = 0
eco_gr_cum = eco.pct_change().cumsum().reset_index()
eco_gr_cum.loc[eco_gr_cum.Year == 1999, my_cols] = 0
eco = eco.reset_index()

industry_gdp = pd.read_csv('Data/industry.csv')
industry_gdp.set_index(['Geography', 'Year', 'Industry'], inplace=True)

industry_gdp_gr = industry_gdp.pct_change().reset_index()
industry_gdp_gr.loc[industry_gdp_gr.Year == 1999, 'Industry GDP'] = 0
industry_gdp_gr_cum = industry_gdp.pct_change().cumsum().reset_index()
industry_gdp_gr_cum.loc[industry_gdp_gr_cum.Year == 1999, 'Industry GDP'] = 0
industry_gdp = industry_gdp.reset_index()

labour = eco.groupby(['Geography', 'Year', 'Industry'])[
    'Unemployment rate', 'Employed', 'Unemployed'].sum().reset_index()

# visualization functions:
year = 2019
geo = 'British Columbia'

