import pandas as pd
import altair as alt
import numpy as np
from altair import datum

# from src import wrangling as wr

alt.data_transformers.disable_max_rows()
alt.themes.enable('latimes')

# eco = wr.eco
# labour = wr.labour

def cpi_vis(year, geo):
    all_cpi_evo = alt.Chart(eco, title="CPI all-items evolution").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='2002=100', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(All-items):Q', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=(',.0f')), title=None),
            tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(All-items):Q', format=('.0f'), title='CPI')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2000,year]))

    all_cpi_gr = alt.Chart(eco_gr, title="Growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('sum(All-items):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('sum(All-items):Q', format=('.2%'), title='Growth rate')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2000,year]))

    gasoline_cpi_evo = alt.Chart(eco, title="CPI gasoline evolution").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='2002=100', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Gasoline):Q', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=(',.0f')), title=None),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(Gasoline):Q', title='CPI')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2000,year]))

    gasoline_cpi_gr = alt.Chart(eco_gr, title="Growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('sum(Gasoline):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('sum(Gasoline):Q', format=('.2%'), title='Growth rate')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2000,year]))

    cpi_rank = alt.Chart(eco, title="CPI all-items by province/territory").mark_bar().encode(
        x=alt.X('average(All-items):Q', title='2002=100', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=(',.0f'))), 
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'), alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(All-items):Q', title='CPI')]).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal= year))

    cpi_gr_rank = alt.Chart(eco_gr, title="Growth rate by province/territory").mark_bar().encode(
        x=alt.X('average(All-items):Q', title=None, axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, format=('%'))), 
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'), alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(All-items):Q', format=('.2%'), title='CPI')]).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal= year))
        
    all_cpi = (all_cpi_evo | all_cpi_gr)
    gasoline_cpi = (gasoline_cpi_evo | gasoline_cpi_gr)
    rank_cpi = (cpi_rank | cpi_gr_rank)
    cpi_plot = ((all_cpi & gasoline_cpi) & rank_cpi).configure_view(strokeOpacity=0).configure_axis(domain=False).configure_title(fontSize=30)

# test
# if __name__ == '__main__':
#    year = 2010
#    Geography = 'Ontario'

#    chart = plt_province_gdp(year)
#    chart.show()
