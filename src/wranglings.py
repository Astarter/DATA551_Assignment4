"""
This file renders and cleans the data
"""

import pandas as pd

"""
**1. Gross domestic product, expenditure-based, provincial and territorial, annual (x 1,000,000)**

Statistics Canada. Table 36-10-0222-01  Gross domestic product, expenditure-based, provincial and territorial, 
annual (x 1,000,000) https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=3610022201 
"""
gdp = pd.read_csv("data/raw/GDP.csv", skiprows=[i for i in range(0, 6)])
gdp.drop(gdp.index[0], inplace=True)
gdp['Geography'] = gdp['Geography'].fillna(method='ffill')
gdp = gdp[:-7]
gdp['Geography'] = gdp['Geography'].replace(['Canada 1 (map)', 'Northwest Territories 2 (map)', 'Nunavut 2 (map)'],
                                            ['Canada', 'Northwest Territories', 'Nunavut'])
gdp.rename(columns={'Reference period': 'Year', 'Gross domestic product at market prices': 'Real GDP',
                    'Gross domestic product at market prices.1': 'Nominal GDP'}, inplace=True)
gdp.reset_index(inplace=True)
gdp.drop('index', axis=1, inplace=True)
gdp = gdp.replace(',', '', regex=True)
convert_dict = {'Real GDP': float, 'Nominal GDP': float}
gdp = gdp.astype(convert_dict)
gdp['Geography'] = gdp['Geography'].str.strip()

# print(gdp.head())

"""
**2. Population estimates on July 1st, by age and sex**
Statistics Canada. Table 17-10-0005-01  Population estimates on July 1st, by age and sex\
https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=1710000501
"""

population = pd.read_csv('data/raw/population.csv', skiprows=[i for i in range(0, 4)])
population['Geography'] = population['Geography'].fillna(method='ffill')
population.drop(population.index[0], inplace=True)
population.drop('Age group 3 5', axis='columns', inplace=True)
population.rename(columns={'Reference period': 'Year', 'Both sexes': 'Population'}, inplace=True)
population = population[:-11]
population['Geography'] = population['Geography'].replace(['Northwest Territories 6 (map)', 'Nunavut 6 (map)'],
                                                          ['Northwest Territories', 'Nunavut'])
population.reset_index(inplace=True)
population.drop('index', axis=1, inplace=True)
population = population.replace(',', '', regex=True)
convert_dict = {'Population': float, 'Year': str}
population = population.astype(convert_dict)
population['Year'] = population['Year'].str.split('.').str[0]

"""
**3. Gross domestic product (GDP) at basic prices, by industry, provinces and territories (x 1,000,000)**

Statistics Canada. Table 36-10-0402-01  Gross domestic product (GDP) at basic prices, by industry, provinces and 
territories (x 1,000,000) https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=3610040201 """

industry_gdp = pd.read_csv('data/raw/industryGDP.csv', skiprows=[i for i in range(0, 4)])
industry_gdp.drop(industry_gdp.index[0], inplace=True)
industry_gdp['Geography'] = industry_gdp['Geography'].fillna(method='ffill')
industry_gdp['North American Industry Classification System (NAICS) 7 8'] = industry_gdp['North American Industry ' \
                                                                                         'Classification System (' \
                                                                                         'NAICS) 7 8'].fillna(
    method='ffill')
industry_gdp['North American Industry Classification System (NAICS) 7 8'] = \
    industry_gdp['North American Industry Classification System (NAICS) 7 8'].str.split('[').str[0]
industry_gdp = industry_gdp[:-26]
industry_gdp.rename(
    columns={'Reference period': 'Year', 'North American Industry Classification System (NAICS) 7 8': 'Industry',
             'Chained (2012) dollars 9': 'Industry GDP'}, inplace=True)
industry_gdp.reset_index(inplace=True)
industry_gdp.drop('index', axis=1, inplace=True)
industry_gdp = industry_gdp.replace(',', '', regex=True)
industry_gdp.replace(to_replace="..", value="0", inplace=True)
convert_dict = {'Industry GDP': float, 'Year': str, 'Industry': str}
industry_gdp = industry_gdp.astype(convert_dict)
industry_gdp['Year'] = industry_gdp['Year'].str.split('.').str[0]
industry_gdp['Industry'] = industry_gdp['Industry'].str.strip()
industry_gdp['Geography'] = industry_gdp['Geography'].str.strip()
industry_gdp.to_csv(r'Data/industry.csv', index=False)

# industry_gdp.head()

"""
**4. Labour force characteristics by industry, annual**
Statistics Canada. Table 14-10-0023-01  Labour force characteristics by industry, annual (x 1,000)\
https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=1410002301
"""

labour = pd.read_csv('data/raw/labour.csv', skiprows=[i for i in range(0, 4)])
labour.drop(labour.index[0], inplace=True)
labour.rename(columns={'Reference period': 'Year', 'Geography 2': 'Geography',
                       'North American Industry Classification System (NAICS) 3': 'Industry',
                       'Employment 4': 'Employed', 'Unemployment 5': 'Unemployed'}, inplace=True)
labour['Geography'] = labour['Geography'].fillna(method='ffill')
labour['Industry'] = labour['Industry'].fillna(method='ffill')
labour.drop('Age group', axis='columns', inplace=True)
labour.drop('Sex', axis='columns', inplace=True)
labour = labour[:-15]
labour['Industry'] = labour['Industry'].replace(
    ['Total, all industries 6', 'Goods-producing sector 7', 'Services-producing sector 8', 'Unclassified industries 9'],
    ['All industries', 'Goods-producing sector', 'Services-producing sector', 'Unclassified industries'])
labour = labour.replace(',', '', regex=True)
labour.replace(to_replace="..", value="0", inplace=True)
convert_dict = {'Employed': float, 'Unemployed': float, 'Year': str}
labour = labour.astype(convert_dict)
labour.reset_index(inplace=True)
labour.drop('index', axis=1, inplace=True)
labour['Year'] = labour['Year'].str.split('.').str[0]
labour['Unemployment rate'] = labour['Unemployed'] / labour['Employed']

# labour.head()

"""
**5. Average weekly earnings by industry, annual**

Statistics Canada. Table 14-10-0204-01  Average weekly earnings by industry, annual\
https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=1410020401
"""

earnings = pd.read_csv('data/raw/earnings.csv', skiprows=[i for i in range(0, 4)])
earnings.drop(earnings.index[0], inplace=True)
earnings.rename(
    columns={'Reference period': 'Year', 'Industrial aggregate excluding unclassified businesses 5 6': 'All industries',
             'Goods producing industries 7': 'Goods-producing sector',
             'Service producing industries 8': 'Service-producing sector'}, inplace=True)
earnings.drop('Type of employees', axis='columns', inplace=True)
earnings.drop('Overtime', axis='columns', inplace=True)
earnings['Geography'] = earnings['Geography'].fillna(method='ffill')
earnings = earnings[:-19]
earnings['Geography'] = earnings['Geography'].replace(['Northwest Territories 10 11 (map)', 'Nunavut 10 11 (map)'],
                                                      ['Northwest Territories', 'Nunavut'])
earnings = earnings.replace(',', '', regex=True)
earnings['Goods-producing sector'].replace(to_replace="F", value="1431.82", inplace=True)
convert_dict = {'Year': str, 'Goods-producing sector': float, 'Service-producing sector': float,
                'All industries': float}
earnings = earnings.astype(convert_dict)
earnings.reset_index(inplace=True)
earnings.drop('index', axis=1, inplace=True)
earnings['Year'] = earnings['Year'].str.split('.').str[0]

# earnings.head()

"""
**6. Consumer Price Index, annual average, not seasonally adjusted**

Statistics Canada. Table 18-10-0005-01  Consumer Price Index, annual average, not seasonally adjusted\
https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=1810000501
"""
cpi = pd.read_csv('data/raw/cpi.csv', skiprows=[i for i in range(0, 4)])
cpi.drop(cpi.index[0], inplace=True)
cpi['Geography'] = cpi['Geography'].fillna(method='ffill')
cpi.rename(columns={'Reference period': 'Year'}, inplace=True)
cpi = cpi[:-12]
cpi['Geography'] = cpi['Geography'].replace(
    ['Whitehorse, Yukon 5 (map)', 'Yellowknife, Northwest Territories 5 (map)', 'Iqaluit, Nunavut 6 (map)'],
    ['Yukon', 'Northwest Territories', 'Nunavut'])
cpi.reset_index(inplace=True)
cpi.drop('index', axis=1, inplace=True)
cpi.replace(to_replace="..", value="0", inplace=True)
convert_dict = {'All-items': float, 'Gasoline': float}
cpi = cpi.astype(convert_dict)

# cpi.head()

"""
**7. Economic Measurements**
"""
eco = gdp.merge(population, on=['Geography', 'Year'], how='outer').merge(labour, on=['Geography', 'Year'],
                                                                         how='outer').merge(earnings,
                                                                                            on=['Geography', 'Year'],
                                                                                            how='outer').merge(cpi, on=[
    'Geography', 'Year'], how='outer')
eco = eco[eco.Industry != 'Unclassified industries']
eco['Real GDP per Capita'] = eco['Real GDP'] / eco['Population'] * 1000000
eco['Nominal GDP per Capita'] = eco['Nominal GDP'] / eco['Population'] * 1000000
eco.to_csv(r'data/processed/eco.csv', index=False)

# eco.sample(5)

if __name__ == '__main__':
    # Test the wrangled files:
    print(gdp.head())
    print(population.head())
    print(industry_gdp.head())
    print(labour.head())
    print(earnings.head())
    print(cpi.head())
    print(eco.head())
    print(earnings.head())
