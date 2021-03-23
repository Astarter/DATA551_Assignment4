import altair as alt
import pandas as pd

alt.data_transformers.disable_max_rows()
alt.themes.enable('latimes')

# load in the datasets:

eco = pd.read_csv('data/processed/eco.csv')
my_cols = eco[eco.columns[2:16]].columns
eco.set_index(['Geography', 'Year', 'Industry'], inplace=True)

eco_gr = eco.pct_change().reset_index()
eco_gr.loc[eco_gr.Year == 1999, my_cols] = 0
eco_gr_cum = eco.pct_change().cumsum().reset_index()
eco_gr_cum.loc[eco_gr_cum.Year == 1999, my_cols] = 0
eco = eco.reset_index()

industry_gdp = pd.read_csv('data/processed/industry.csv')
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


def concat_cpi_vis(year, geo):
    all_cpi_evo = alt.Chart(eco, title="CPI all-items evolution").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='2002=100',
                axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(All-items):Q',
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=(',.0f')), title=None),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('average(All-items):Q', format=('.0f'), title='CPI')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldRangePredicate('Year', [2000, year]))

    all_cpi_gr = alt.Chart(eco_gr, title="Growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year',
                axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('sum(All-items):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('sum(All-items):Q', format=('.2%'), title='Growth rate')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldRangePredicate('Year', [2000, year]))

    gasoline_cpi_evo = alt.Chart(eco, title="CPI gasoline evolution").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='2002=100',
                axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Gasoline):Q',
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=(',.0f')), title=None),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('average(Gasoline):Q', title='CPI')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldRangePredicate('Year', [2000, year]))

    gasoline_cpi_gr = alt.Chart(eco_gr, title="Growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year',
                axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('sum(Gasoline):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('sum(Gasoline):Q', format=('.2%'), title='Growth rate')]).transform_filter(
        alt.FieldEqualPredicate(field='Geography', equal=geo)).transform_filter(
        alt.FieldRangePredicate('Year', [2000, year]))

    cpi_rank = alt.Chart(eco, title="CPI all-items by province/territory").mark_bar().encode(
        x=alt.X('average(All-items):Q', title='2002=100',
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=(',.0f'))),
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'),
                            alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('average(All-items):Q', title='CPI')]).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year))

    cpi_gr_rank = alt.Chart(eco_gr, title="Growth rate by province/territory").mark_bar().encode(
        x=alt.X('average(All-items):Q', title=None,
                axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=('%'))),
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'),
                            alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'),
                 alt.Tooltip('average(All-items):Q', format=('.2%'), title='CPI')]).transform_filter(
        alt.FieldEqualPredicate(field='Year', equal=year))

    w = 300
    h = 200

    all_cpi_evo = all_cpi_evo.properties(
        width=w,
        height=h
    )

    all_cpi_gr = all_cpi_gr.properties(
        width=w,
        height=h
    )
    gasoline_cpi_evo = gasoline_cpi_evo.properties(
        width=w,
        height=h
    )

    gasoline_cpi_gr = gasoline_cpi_gr.properties(
        width=w,
        height=h
    )

    cpi_rank = cpi_rank.properties(
        width=w,
        height=h
    )

    cpi_gr_rank = cpi_gr_rank.properties(
        width=w,
        height=h
    )

    all_cpi = (all_cpi_evo | all_cpi_gr)
    gasoline_cpi = (gasoline_cpi_evo | gasoline_cpi_gr)
    rank_cpi = (cpi_rank | cpi_gr_rank)
    cpi_plot = ((all_cpi & gasoline_cpi) & rank_cpi).configure_view(strokeOpacity=0).configure_axis(
        domain=False).configure_title(fontSize=30)

    return cpi_plot.to_html()

# test
# if __name__ == '__main__':
#    year = 2010
#    Geography = 'Ontario'

#    chart = plt_province_gdp(year)
#    chart.show()
