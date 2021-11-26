import collections
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import math
import seaborn as sns
from plotly.subplots import make_subplots

# Read File 
df = pd.read_excel('HappinessScores.xls')
years_to_keep = list(range(2010, 2020, 1))
df = df[df["year"].isin(years_to_keep)]
df_country = pd.read_excel('un_geoscheme.xlsx')
df_country.columns = ['country', 'sub-subregion', 'subregion', 'region', 'unsd_m49_codes']
df_country['country'] = df_country['country'].str.strip()


happiness = pd.read_excel (r'HappinessScores.xls')
happiness.dropna() 
 

suicide = pd.read_csv('suicide.csv')
suicide.dropna()

base = pd.read_excel (r'population_world_bank.xlsx')
base.dropna()

new_header = lst = list(base.iloc[0][:4]) + list(base.iloc[0][4:].astype(int)) #grab the first row for the header
base = base[1:] #take the data less the header row
base.columns = new_header #

# add continent info column to happiness tbl 
continent_loca = suicide[['ParentLocation','Location']].rename(columns={'Location':'Country name','ParentLocation':'Continent'})
happiness = happiness.merge(continent_loca, on='Country name', how='left')

# change the continent categories
happiness.loc[(happiness.Continent == 'Eastern Mediterranean'),'Continent']='Asia'
happiness.loc[(happiness.Continent == 'South-East Asia'),'Continent']='Asia'
happiness.loc[(happiness.Continent == 'Western Pacific'),'Continent']='Oceania'

#df_country
df_happy_country = df.join(df_country.set_index('country'), on='Country name')
df_happy_country['GDP per capita'] = df_happy_country['Log GDP per capita'].map(lambda x: math.exp(x))
df_happy_country = df_happy_country.rename(columns= {'Life Ladder':'Happiness Score'})


st.title('Regional Happiness Index')


st.markdown('**Happiness Index by Continent**')
st.write('In this section, we explores the happiness index by continent.\
The first graph below describes yearly change of the selected feature in each continent given in our main happiness dataset, and\
the second graph shows the correlation between each feature and the happiness score for each year.')

option = st.selectbox('Feature that explains Happiness Index',\
['Social Support', 'Healthy Life Expectancy at Birth', 'Log GDP per Capita',\
'Generosity','Freedom to Make Life Choices','Perceptions of corruption'])

## 1
# Social Support vs. Year
if option == 'Social Support':
    df1 = happiness.loc[(happiness.year >= 2010) & (happiness.year <= 2019)]
    df1 = df1.groupby(['Continent','year'])[['Social support']].mean().reset_index().rename(columns = {'year':'Year'})
    fig = px.line(df1, x="Year", y="Social support", color = 'Continent',title='Social Support by Year')
    st.plotly_chart(fig)

    st.write('This graph shows the yearly change in social support that was available in each continent in the past years. \
        There is small change in social support of America, Europe, and Oceania while the social support in Asia and Africa has decreased.\
        Especially around 2014, both Asia and Africa reach the lowest social support.')

    fig1 = px.scatter(df_happy_country.dropna(), x="Social support", y="Happiness Score", animation_frame="year", size='GDP per capita',
            color="region", hover_name="Country name",
            category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
    st.plotly_chart(fig)
    st.write('We can see a positive correlation between happiness index and social support, with Europe leading in the top right quadrant and Africa in the lower quadrant.')
    


## 2
# Health Life Expectancy at Birth vs. Year
elif option == 'Healthy Life Expectancy at Birth':
    df1 = happiness.loc[(happiness.year >= 2010) & (happiness.year <= 2019)].dropna()
    df1 = df1.groupby(['Continent','year'])[['Healthy life expectancy at birth']].mean().reset_index().rename(columns = {'year':'Year'})
    fig = px.line(df1.dropna(), x="Year", y="Healthy life expectancy at birth", color = 'Continent',title='Healthy Life Expectancy at Birth by Year')
    st.plotly_chart(fig)
    st.write('In general, healthy life expectancy at birth increases in all continents. Especially, the value in Africa increases the fastest.')
    
    fig = px.scatter(df_happy_country.dropna(), x="Healthy life expectancy at birth", y="Happiness Score", animation_frame="year", size='GDP per capita',
            color="region", hover_name="Country name",
            category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
    st.plotly_chart(fig)
    st.write('There is a positive correlation between life expectancy and happiness index, with similar region distribution.')

## 3
# Log GDP per Capita vs. Year
elif option == 'Log GDP per Capita':
    df1 = happiness.loc[(happiness.year >= 2010) & (happiness.year <= 2019)].dropna()
    df1 = df1.groupby(['Continent','year'])[['Log GDP per capita']].mean().reset_index().rename(columns = {'year':'Year'})
    fig = px.line(df1.dropna(), x="Year", y="Log GDP per capita", color = 'Continent',title='GDP by Year')
    st.plotly_chart(fig)
    st.write('In general, log GDP per capita slowly increases in all continents.')

    fig = px.scatter(df_happy_country.dropna(), x="Log GDP per capita", y="Happiness Score", animation_frame="year",
            color="region", hover_name="Country name",
            category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
    st.plotly_chart(fig)
    st.write('There is a positive correlation between Happiness Index and GDP,\
     the higher the GDP, the likelier it is to have a high happiness index score.\
      Countries in Europe occupy the top right quadrant and are quite stable throughout the years. \
      African countries, on the other hand, occupy the lower left of the quadrant.')

## 4
# Generosity vs. Year
elif option == 'Generosity':
    df1 = happiness.loc[(happiness.year >= 2010) & (happiness.year <= 2019)].dropna()
    df1 = df1.groupby(['Continent','year'])[['Generosity']].mean().reset_index().rename(columns = {'year':'Year'})
    fig = px.line(df1.dropna(), x="Year", y="Generosity", color = 'Continent',title='Generosity by Year')
    st.plotly_chart(fig)
    st.write('Generosity fluctuates and slowly decreases by 2018; however it slightly increases in all continents after 2018.')

    fig = px.scatter(df_happy_country.dropna(), x="Generosity", y="Happiness Score", animation_frame="year", size='GDP per capita',
            color="region", hover_name="Country name",
            category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
    st.plotly_chart(fig)
    st.write('There is a slight positive correlation between happiness index and generosity.\
     There is also no significant difference between each region.')

## 5
# Freedom to make a life choices vs. Year
elif option == 'Freedom to Make Life Choices':
    df1 = happiness.loc[(happiness.year >= 2010) & (happiness.year <= 2019)].dropna()
    df1 = df1.groupby(['Continent','year'])[['Freedom to make life choices']].mean().reset_index().rename(columns = {'year':'Year'})
    fig = px.line(df1.dropna(), x="Year", y="Freedom to make life choices", color = 'Continent',title='Freedom to make life choices change by Year')
    st.plotly_chart(fig)
    st.write('Freedom to make a life choices increase in all continents; however, in 2012, this feature reaches the lowest point in Asia and Africa')

    fig = px.scatter(df_happy_country.dropna(), x="Freedom to make life choices", y="Happiness Score", animation_frame="year", size='GDP per capita',
            color="region", hover_name="Country name",
            category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
    st.plotly_chart(fig)
    st.write('Throughout the years, the score for freedom to make life choices increased overall, \
    with the trend of all countries moving towards the right side of the graph.\
     There also seems to be a positive correlation between happiness index and freedom to make life choices.\
      However, the difference between regions is not as significant.')

## 6
# Perceptions of corruption vs. Year
else:
    df1 = happiness.loc[(happiness.year >= 2010) & (happiness.year <= 2019)].dropna()
    df1 = df1.groupby(['Continent','year'])[['Perceptions of corruption']].mean().reset_index().rename(columns = {'year':'Year'})
    fig = px.line(df1.dropna(), x="Year", y="Perceptions of corruption", color = 'Continent',title='Perceptions of corruption change by Year')
    st.plotly_chart(fig)
    st.write('Except for Asia and Africa, this feature slightly increases in entire continents.')

    fig = px.scatter(df_happy_country.dropna(), x="Perceptions of corruption", y="Happiness Score", animation_frame="year", size='GDP per capita',
            color="region", hover_name="Country name",
            category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
    st.plotly_chart(fig)
    st.write('From the scatterplot we can see that there is a negative correlation between happiness index and perceptions of corruption, \
    the lower the corruption score, the higher the happiness index is likely to be. \
    There is also no clear difference for each region.')



st.markdown('**Happiness Index by Country**')
st.write('Here, we are going to see the happiness index trend for each country in its respective region. \
To get the region (continent) and sub-region for each country, we joined the happiness index dataset with \
the United Nations (UN) geoscheme data. There are several countries which have inconsistent names so we manually\
 changed them before joining. Furthermore, there are two countries/territories present in the happiness dataset which \
 are not present in the UN dataset, namely Kosovo and Taiwan, so we added them manually to their respective regions.')

# Match country names in happy dataset with country dataset
df_country['country'][df_country['country'] == 'Palestine'] = 'Palestinian Territories'
df_country['country'][df_country['country'] == 'Myanmar\xa0[Burma]'] = 'Myanmar'
df_country['country'][df_country['country'] == 'Timor-Leste\xa0[East Timor]'] = 'Timor Leste'
df_country['country'][df_country['country'] == 'China, Hong Kong Special Administrative Region'] = 'Hong Kong S.A.R. of China'
df_country['country'][df_country['country'] == "Democratic People's Republic of Korea\xa0[North Korea]"] = 'North Korea'
df_country['country'][df_country['country'] == 'Republic of Korea\xa0[South Korea]'] = 'South Korea'
df_country['country'][df_country['country'] == 'France\xa0[French Republic]'] = 'France'
df_country['country'][df_country['country'] == 'Czechia\xa0[Czech Republic]'] = 'Czech Republic'
df_country['country'][df_country['country'] == 'Eswatini\xa0[Swaziland]'] = 'Swaziland'
df_country['country'][df_country['country'] == 'Congo\xa0[Republic of the Congo]'] = 'Congo (Brazzaville)'
df_country['country'][df_country['country'] == 'DR Congo'] = 'Congo (Kinshasa)'

asia_south = df_country[df_country['sub-subregion'] == 'Southern Asia']['country'].tolist()
asia_west = df_country[df_country['sub-subregion'] == 'Western Asia']['country'].tolist()
asia_southeast = df_country[df_country['sub-subregion'] == 'South-eastern Asia']['country'].tolist()
asia_east = df_country[df_country['sub-subregion'] == 'Eastern Asia']['country'].tolist()
asia_east.append('Taiwan Province of China')
asia_central = df_country[df_country['sub-subregion'] == 'Central Asia']['country'].tolist()

europe_east = df_country[df_country['sub-subregion'] == 'Eastern Europe']['country'].tolist()
europe_west = df_country[df_country['sub-subregion'] == 'Western Europe']['country'].tolist()
europe_south = df_country[df_country['sub-subregion'] == 'Southern Europe']['country'].tolist()
europe_south.append('Kosovo')
europe_north = df_country[df_country['sub-subregion'] == 'Northern Europe']['country'].tolist()

america_north = df_country[df_country['sub-subregion'] == 'Northern America']['country'].tolist()
america_south = df_country[df_country['sub-subregion'] == 'South America']['country'].tolist()
america_central = df_country[df_country['sub-subregion'] == 'Central America']['country'].tolist()
caribbean = df_country[df_country['sub-subregion'] == 'Caribbean']['country'].tolist()

australia_nz = df_country[df_country['sub-subregion'] == 'Australia and New Zealand']['country'].tolist()

africa_north = df_country[df_country['sub-subregion'] == 'Northern Africa']['country'].tolist()
africa_east = df_country[df_country['sub-subregion'] == 'Eastern Africa']['country'].tolist()
africa_west = df_country[df_country['sub-subregion'] == 'Western Africa']['country'].tolist()
africa_south = df_country[df_country['sub-subregion'] == 'Southern Africa']['country'].tolist()
africa_middle = df_country[df_country['sub-subregion'] == 'Middle Africa']['country'].tolist()

df_happy_10na = df[['Country name', 'year', 'Life Ladder']].dropna().rename(columns={'Country name' : 'country'})

def plot_line_chart(i, j, region, title): 
    df_happy_10na_reg = df_happy_10na[df_happy_10na['country'].isin(region)]
    df_happy_10na_reg = df_happy_10na_reg.pivot(index='year', columns='country', values='Life Ladder')
    ax[i,j].plot(df_happy_10na_reg)
    ax[i,j].set_title(title)
    ax[i,j].set_ylim([2.0, 8.0])

    box = ax[i,j].get_position()
    ax[i,j].set_position([box.x0, box.y0, box.width * 0.75, box.height])
    ax[i,j].legend(df_happy_10na_reg.columns.tolist(), loc='center left', bbox_to_anchor=(1, 0.5))

option2 = st.selectbox('Select a continent to see the happiness index by countries',\
['Asia & Oceania', 'Europe', 'America',\
'Africa'])

if option2 == 'Asia & Oceania':
 
    fig, ax = plt.subplots(3, 2, figsize=(30, 16))
    plot_line_chart(0, 0, asia_central, "Central Asia")
    plot_line_chart(0, 1, asia_east, "East Asia")
    plot_line_chart(1, 0, asia_southeast, "Southeast Asia")
    plot_line_chart(1, 1, asia_south, "South Asia")
    plot_line_chart(2, 0, asia_west, "West Asia")
    plot_line_chart(2, 1, australia_nz, "Australia & New Zealand")
    
    st.pyplot(fig)
    st.write('Countries in Asia generally do not have significantly high or significantly low happiness index.\
     In its subregion, countries in South Asia have a lower happiness index compared to other subregions in Asia.\
     For Oceania, we only have data from two countries and both of them are in the Australia & New Zealand subregion \
     and both countries have high happiness index.')

elif option2 == 'Europe':

    fig, ax = plt.subplots(2, 2, figsize=(20, 7))

    plot_line_chart(0, 0, europe_east, "East Europe")
    plot_line_chart(0, 1, europe_north, "North Europe")
    plot_line_chart(1, 0, europe_south, "South Europe")
    plot_line_chart(1, 1, europe_west, "West Europe")
    st.pyplot(fig)
    st.write('Countries in Europe have an overall high happiness index score.\
     Countries in the subregion West Europe have highest average happiness index compared to other regions \
     and their happiness index score is pretty stable throughout the years. \
     Countries in Northern Europe also have stable happiness index and several countries with significantly high happiness index,\
      but three of them have a mediocore index.')

elif option2 == 'America':
    fig, ax = plt.subplots(2, 2, figsize=(14, 7))

    plot_line_chart(0, 0, america_north, "North America")
    plot_line_chart(0, 1, america_central, "Central America")
    plot_line_chart(1, 0, america_south, "South America")
    plot_line_chart(1, 1, caribbean, "Caribbean")
    st.pyplot(fig)
    st.write('The subregion North America have a significantly high happiness index while Central and South America have a moderately high happiness index.\
     On the other hand, countries in the Carribean subregion have a moderately low happiness index.')

elif option2 == 'Africa':
    fig, ax = plt.subplots(3, 2, figsize=(21, 16))
    plot_line_chart(0, 0, africa_north, "North Africa")
    plot_line_chart(0, 1, africa_east, "East Africa")
    plot_line_chart(1, 0, africa_middle, "Middle Africa")
    plot_line_chart(1, 1, africa_south, "South Africa")
    plot_line_chart(2, 0, africa_west, "West Africa")
    fig.delaxes(ax[2,1])
    st.pyplot(fig)
    st.write('Generally, we can see that countries in Africa have averagely lower happiness index compared to other continents.\
     The index also seems to fluctuate a lot through out the years.')

