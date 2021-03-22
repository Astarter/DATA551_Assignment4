import pandas as pd
import altair as alt
import numpy as np
from altair import datum

# from src import wrangling as wr

alt.data_transformers.disable_max_rows()
alt.themes.enable('latimes')

# eco = wr.eco
# labour = wr.labour

def employment_vis(year, geo):
    er_evo = alt.Chart(eco, title="Unemployment rate evolution").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='Year', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Unemployment rate):Q', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=('%')), title=None),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(Unemployment rate):Q', format=('.2%'), title='Unemployment rate')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2000,year])).properties(height=430)

    er_rank = alt.Chart(eco, title="Unemployment rate by province/territory").mark_bar().encode(
        x=alt.X('average(Unemployment rate):Q', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=('%')), title=None), 
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'), alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(Unemployment rate):Q', format=('.2%'), title='Unemployment rate')]).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal= year))

    er_ind_rank= alt.Chart(labour, title="Unemployment rate by industry").mark_bar().encode(
        x=alt.X('Unemployment rate:Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None), 
        y=alt.Y('Industry:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.value('lightblue'),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('Industry'), alt.Tooltip('Unemployment rate:Q', format=('.2%'), title='Unemployment rate')]).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal= year)).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo))
            
    employment_plot = (er_evo | (er_rank & er_ind_rank)).configure_view(strokeOpacity=0).configure_axis(domain=False).configure_title(fontSize=30)
                    
    return employment_plot.to_html()

def earnings_vis(year, geo):
    all_ear_evo = alt.Chart(eco, title="All industries").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='CA$', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(All industries):Q', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=('$,f')), title=None),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(All industries):Q', format=('$,'), title='Earnings')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2002,year]))

    all_ear_gr_evo = alt.Chart(eco_gr, title="Growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(All industries):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(All industries):Q', format=('.2%'), title='Growth rate')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2002,year]))

    goods_ear_evo = alt.Chart(eco, title="Goods-producing sector").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='CA$', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Goods-producing sector):Q', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=('$,f')), title=None),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(Goods-producing sector):Q', format=('$,'), title='Earnings')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2002,year]))

    goods_ear_gr_evo = alt.Chart(eco_gr, title="Growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Goods-producing sector):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(Goods-producing sector):Q', format=('.2%'), title='Growth rate')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2002,year]))

    serv_ear_evo = alt.Chart(eco, title="Service-producing").mark_area(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue')).encode(
        x=alt.X('Year', title='CA$', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Service-producing sector):Q', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=('$,f')), title=None),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(Service-producing sector):Q', format=('$,'), title='Earnings')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2002,year]))

    serv_ear_gr_evo = alt.Chart(eco_gr, title="Growth rates").mark_bar(
        point=alt.OverlayMarkDef(filled=False, fill='darkblue'), size=16).encode(
        x=alt.X('Year', title='Year', axis=alt.Axis(tickCount=5, titleFontSize=20, grid=False, ticks=False, format='Y')),
        y=alt.Y('average(Service-producing sector):Q', axis=alt.Axis(tickCount=3, grid=False, ticks=False, format=('%')), title=None),
        color=alt.condition((alt.datum.Year == year), alt.value('darkblue'), alt.value('lightblue')),
        tooltip = [alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(Service-producing sector):Q', format=('.2%'), title='Growth rate')]).transform_filter(
            alt.FieldEqualPredicate(field='Geography', equal= geo)).transform_filter(
            alt.FieldRangePredicate('Year',[2002,year]))
        
    all_ear = (all_ear_evo | all_ear_gr_evo)
    goods_ear = (goods_ear_evo | goods_ear_gr_evo)
    serv_ear = (serv_ear_evo | serv_ear_gr_evo)
    earnings_plot = ((all_ear & serv_ear) & goods_ear).configure_view(strokeOpacity=0).configure_axis(domain=False).configure_title(fontSize=30)
    
    return earnings_plot.to_html()

def earnings_rank(year, geo):
    ear_rank = alt.Chart(eco, title="Average weekly earnings by province/territory").mark_bar().encode(
        x=alt.X('average(All industries):Q', axis=alt.Axis(tickCount=3, titleFontSize=20, grid=False, ticks=False, format=('$,f')), title=None), 
        y=alt.Y('Geography:O', sort='-x', axis=alt.Axis(labelFontSize=18), title=None),
        color=alt.condition((alt.datum.Geography == geo) | (alt.datum.Geography == 'Canada'), alt.value('darkblue'), alt.value('lightblue')),
        tooltip=[alt.Tooltip('Geography', title='Province/territory'), alt.Tooltip('Year'), alt.Tooltip('average(All industries):Q', format=('$,'), title='Earnings')]).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal= year)).configure_view(strokeOpacity=0).configure_axis(domain=False).configure_title(fontSize=30)
        
    return ear_rank.to_html()


# test
# if __name__ == '__main__':
#    year = 2010
#    Geography = 'Ontario'

#    chart = plt_province_gdp(year)
#    chart.show()
