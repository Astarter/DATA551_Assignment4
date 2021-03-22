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


def concat_gpd_vis(year, geo):
    real_gdp = alt.Chart(eco, title="Total GDP").mark_bar().transform_aggregate(
        groupby=['Geography', 'Year'], GDP='sum(Real GDP)').encode(
        x=alt.X('sum(GDP):Q', title='CA$ (MM)', axis=alt.Axis(titleFontSize=20, grid=False, ticks=False, labels=False)),
        y=alt.Y('Geography:O', sort='-x', title=None, axis=alt.Axis(labelFontSize=20, ticks=False, grid=False)),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year)).properties(
        height=200, width=400).mark_text(
        dx=-175, color='darkblue', size=40).encode(
        text=alt.Text('sum(GDP):Q', format=('$,')))

    real_gdp_gr = alt.Chart(eco_gr, title="Growth rate").mark_bar().transform_aggregate(
        groupby=['Geography', 'Year'], GDP='sum(Real GDP)').encode(
        x=alt.X('sum(GDP):Q', title='Yearly %', axis=alt.Axis(titleFontSize=20, grid=False, ticks=False, labels=False)),
        y=alt.Y('Geography:O', sort='-x', title=None, axis=alt.Axis(grid=False, ticks=False, labels=False)),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year)).properties(
        height=200, width=400).mark_text(
        dx=-175, color='darkblue', size=40).encode(
        text=alt.Text('sum(GDP):Q', format=('.2%')))

    real_gdp_evo = alt.Chart(eco, title="GDP evolution").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='Year',
                axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('sum(Real GDP):Q',
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=('$,f')), title=None),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('sum(Real GDP):Q', format=('$,'), title='GDP')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldRangePredicate('Year', [2000, year]))

    real_gdp_rank = alt.Chart(eco, title="Contribution by province/territory").mark_bar().encode(
        x=alt.X('sum(Real GDP):Q', title='CA$ (MM)',
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=('$,f'))),
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'),
                            alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('sum(Real GDP):Q', format=('$,'), title='GDP')]).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year))

    real_gdp_gr_evo = alt.Chart(eco_gr, title="GDP growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year',
                axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('sum(Real GDP):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('sum(Real GDP):Q', format=('.2%'), title='Growth rate')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldRangePredicate('Year', [2000, year]))

    real_gdp_gr_rank = alt.Chart(eco_gr, title="By province/territory").mark_bar().encode(
        x=alt.X('sum(Real GDP):Q', title=None, axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=('%'))),
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'),
                            alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('sum(Real GDP):Q', format=('.2%'), title='Growth rate')]).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year))

    real_gdp_ind_rank = alt.Chart(industry_gdp, title="GDP contribution by industry").mark_bar().encode(
        y=alt.Y('sum(Industry GDP):Q', title='CA$ (MM)',
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=('$,f'))),
        x=alt.X('Industry:O', sort='-y', axis=alt.Axis(labelAngle=-90), title=None),
        color=alt.Color('sum(Industry GDP)', title='GDP', scale=alt.Scale(scheme='blues'),
                        legend=alt.Legend(format=('$,f'))),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('Industry'),
                 alt.Tooltip('sum(Industry GDP):Q', format=('$,.0f'), title='GDP')]).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year)).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).configure_view(strokeOpacity=0).configure_axis(
        domain=False, ticks=False).configure_title(fontSize=30)

    real_gdp_ind_gr_rank = alt.Chart(industry_gdp_gr, title="GDP growth rate by industry").mark_bar().encode(
        y=alt.Y('sum(Industry GDP):Q', title=None, axis=alt.Axis(tickCount=3, grid=False, format=('%'))),
        x=alt.X('Industry:O', sort='-y', title=None, axis=alt.Axis(labelLimit=90, labelAngle=-90)),
        color=alt.Color('sum(Industry GDP)', title='GDP growth rate', scale=alt.Scale(scheme='redblue'),
                        legend=alt.Legend(format=('%'))),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('Industry'),
                 alt.Tooltip('sum(Industry GDP):Q', format=('.2%'), title='Growth rate')]).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year)).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).configure_view(strokeOpacity=0).configure_axis(
        domain=False, ticks=False).configure_title(fontSize=30)

    w = 300
    h = 200

    real_gdp = real_gdp.properties(
        width=w,
        height=h
    )

    real_gdp_gr = real_gdp_gr.properties(
        width=w,
        height=h
    )

    real_gdp_evo = real_gdp_evo.properties(
        width=w,
        height=h
    )

    real_gdp_rank = real_gdp_rank.properties(
        width=w,
        height=h
    )

    real_gdp_gr_evo = real_gdp_gr_evo.properties(
        width=w,
        height=h
    )

    real_gdp_gr_rank = real_gdp_gr_rank.properties(
        width=w,
        height=h
    )

    gdp_summary = (real_gdp | real_gdp_gr)
    gdp_total = (real_gdp_evo | real_gdp_rank)
    gdp_gr = (real_gdp_gr_evo | real_gdp_gr_rank)
    gdp_vis = ((gdp_summary & gdp_total) & gdp_gr).configure_view(strokeOpacity=0).configure_axis(
        domain=False).configure_title(fontSize=20)

    return gdp_vis.to_html()

# gdpc_summary =(real_gdpca | real_gdpc_gr)
# gdpc_total = (real_gdpc_evo | real_gdpc_rank)
# gdpc_gr = (real_gdpc_gr_evo | real_gdpc_gr_rank)
# gdpc_vis = ((gdpc_summary & gdpc_total) & gdpc_gr).configure_view(strokeOpacity=0).configure_axis(domain=False).configure_title(fontSize=30)

# print(concat_gpd_vis(year, geo))

def concat_gdpc_vis(year, geo):
    real_gdpca = alt.Chart(eco, title="GDP per Capita").mark_bar().transform_aggregate(
        groupby=['Geography', 'Year'], GDP='average(Real GDP per Capita)').encode(
        x=alt.X('sum(GDP):Q', title='CA$', axis=alt.Axis(titleFontSize=20, grid=False, ticks=False, labels=False)),
        y=alt.Y('Geography:O', sort='-x', title=None, axis=alt.Axis(labelFontSize=20, ticks=False, grid=False)),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year)).properties(
        height=200, width=400).mark_text(
        dx=-175, color='darkblue', size=40).encode(
        text=alt.Text('sum(GDP):Q', format=('$,.0f')))

    real_gdpc_gr = alt.Chart(eco_gr, title="Growth rate").mark_bar().transform_aggregate(
        groupby=['Geography', 'Year'], GDP='average(Real GDP per Capita)').encode(
        x=alt.X('sum(GDP):Q', title='Yearly %', axis=alt.Axis(titleFontSize=20, grid=False, ticks=False, labels=False)),
        y=alt.Y('Geography:O', sort='-x', title=None, axis=alt.Axis(grid=False, ticks=False, labels=False)),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year)).properties(
        height=200, width=400).mark_text(
        dx=-175, color='darkblue', size=40).encode(
        text=alt.Text('sum(GDP):Q', format=('.2%')))

    real_gdpc_evo = alt.Chart(eco, title="GDP per Capita evolution").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='Year',
                axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Real GDP per Capita):Q',
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=('$,f')), title=None),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('average(Real GDP per Capita):Q', format=('$,.0f'),
                             title='GDP per Capita')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldRangePredicate('Year', [2000, year]))

    real_gdpc_rank = alt.Chart(eco, title="By province/territory").mark_bar().encode(
        x=alt.X('average(Real GDP per Capita):Q', title='CA$',
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=('$,f'))),
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'),
                            alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('average(Real GDP per Capita):Q', format=('$,.0f'),
                             title='GDP per Capita')]).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year))

    real_gdpc_gr_evo = alt.Chart(eco_gr, title="GDP per Capita growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year',
                axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Real GDP per Capita):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')),
                title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('average(Real GDP per Capita):Q', format=('.2%'), title='Growth rate')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldRangePredicate('Year', [2000, year]))

    real_gdpc_gr_rank = alt.Chart(eco_gr, title="By province/territory").mark_bar().encode(
        x=alt.X('average(Real GDP per Capita):Q', title=None,
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=('%'))),
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'),
                            alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('average(Real GDP per Capita):Q', format=('.2%'), title='Growth rate')]).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year))

    w = 300
    h = 200

    real_gdpca = real_gdpca.properties(
        width=w,
        height=h
    )

    real_gdpc_gr = real_gdpc_gr.properties(
        width=w,
        height=h
    )

    real_gdpc_evo = real_gdpc_evo.properties(
        width=w,
        height=h
    )

    real_gdpc_rank = real_gdpc_rank.properties(
        width=w,
        height=h
    )

    real_gdpc_gr_evo = real_gdpc_gr_evo.properties(
        width=w,
        height=h
    )

    real_gdpc_gr_rank = real_gdpc_gr_rank.properties(
        width=w,
        height=h
    )

    gdpc_summary = (real_gdpca | real_gdpc_gr)
    gdpc_total = (real_gdpc_evo | real_gdpc_rank)
    gdpc_gr = (real_gdpc_gr_evo | real_gdpc_gr_rank)
    gdpc_vis = ((gdpc_summary & gdpc_total) & gdpc_gr).configure_view(strokeOpacity=0).configure_axis(
        domain=False).configure_title(fontSize=30)

    return gdpc_vis.to_html()
