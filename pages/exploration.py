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
@st.cache
def load_data():
    # Happiness data
    df = pd.read_excel('data/HappinessScores.xls')
    years_to_keep = list(range(2010, 2020, 1))
    df = df[df["year"].isin(years_to_keep)]

    # Country data
    df_country = pd.read_excel('data/un_geoscheme.xlsx')
    df_country.columns = ['country', 'sub-subregion', 'subregion', 'region', 'unsd_m49_codes']
    df_country['country'] = df_country['country'].str.strip()

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

    # Add countries not in UN list
    df_country = df_country.append({'country': 'Ivory Coast', 'sub-subregion': 'Western Africa', 'subregion': 'Sub-Saharan Africa', 'region': 'Africa'}, ignore_index=True)
    df_country = df_country.append({'country': 'Kosovo', 'sub-subregion': 'Southern Europe', 'subregion': 'Southern Europe', 'region': 'Europe'}, ignore_index=True)
    df_country = df_country.append({'country': 'North Cyprus', 'sub-subregion': 'Western Asia', 'subregion': 'Western Asia', 'region': 'Asia'}, ignore_index=True)
    df_country = df_country.append({'country': 'Somaliland region', 'sub-subregion': 'Eastern Africa', 'subregion': 'Sub-Saharan Africa', 'region': 'Africa'}, ignore_index=True)
    df_country = df_country.append({'country': 'Taiwan Province of China', 'sub-subregion': 'Eastern Asia', 'subregion': 'Eastern Asia', 'region': 'Asia'}, ignore_index=True)

    # Country joined with happiness
    df = df.join(df_country.set_index('country'), on='Country name')
    df['GDP per capita'] = df['Log GDP per capita'].map(lambda x: math.exp(x))
    df = df.rename(columns= {'Life Ladder':'Happiness Score'})

    return df

def app():
    df = load_data()

    st.title('Regional Happiness Index')


    st.markdown('### Happiness Index by Continent')
    st.write('In this section, we explores the happiness index by continent.\
    The first graph below describes yearly change of the selected feature in each continent given in our main happiness dataset, and\
    the second graph shows the correlation between each feature and the happiness score for each year.')

    option = st.selectbox('Feature that explains Happiness Index',\
    ['Social Support', 'Healthy Life Expectancy at Birth', 'Log GDP per Capita',\
    'Generosity','Freedom to Make Life Choices','Perceptions of corruption'])

    ## 1
    # Social Support vs. Year
    if option == 'Social Support':
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)]
        df1 = df1.groupby(['region','year'])[['Social support']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1, x="Year", y="Social support", color = 'region',title='Social Support by Year')
        st.plotly_chart(fig)

        st.write('This graph shows the yearly change in social support that was available in each continent in the past years. \
            There is small change in social support of America, Europe, and Oceania while the social support in Asia and Africa has decreased.\
            Especially around 2014, both Asia and Africa reach the lowest social support.')

        fig = px.scatter(df.dropna(), x="Social support", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        st.write('We can see a positive correlation between happiness index and social support, with Europe leading in the top right quadrant and Africa in the lower quadrant.')
        


    ## 2
    # Health Life Expectancy at Birth vs. Year
    elif option == 'Healthy Life Expectancy at Birth':
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Healthy life expectancy at birth']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Healthy life expectancy at birth", color = 'region',title='Healthy Life Expectancy at Birth by Year')
        st.plotly_chart(fig)
        st.write('In general, healthy life expectancy at birth increases in all continents. Especially, the value in Africa increases the fastest.')
        
        fig = px.scatter(df.dropna(), x="Healthy life expectancy at birth", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        st.write('There is a positive correlation between life expectancy and happiness index, with similar region distribution.')

    ## 3
    # Log GDP per Capita vs. Year
    elif option == 'Log GDP per Capita':
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Log GDP per capita']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Log GDP per capita", color = 'region',title='GDP by Year')
        st.plotly_chart(fig)
        st.write('In general, log GDP per capita slowly increases in all continents.')

        fig = px.scatter(df.dropna(), x="Log GDP per capita", y="Happiness Score", animation_frame="year",
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
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Generosity']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Generosity", color = 'region',title='Generosity by Year')
        st.plotly_chart(fig)
        st.write('Generosity fluctuates and slowly decreases by 2018; however it slightly increases in all continents after 2018.')

        fig = px.scatter(df.dropna(), x="Generosity", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        st.write('There is a slight positive correlation between happiness index and generosity.\
        There is also no significant difference between each region.')

    ## 5
    # Freedom to make a life choices vs. Year
    elif option == 'Freedom to Make Life Choices':
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Freedom to make life choices']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Freedom to make life choices", color = 'region',title='Freedom to make life choices change by Year')
        st.plotly_chart(fig)
        st.write('Freedom to make a life choices increase in all continents; however, in 2012, this feature reaches the lowest point in Asia and Africa')

        fig = px.scatter(df.dropna(), x="Freedom to make life choices", y="Happiness Score", animation_frame="year", size='GDP per capita',
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
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Perceptions of corruption']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Perceptions of corruption", color = 'region',title='Perceptions of corruption change by Year')
        st.plotly_chart(fig)
        st.write('Except for Asia and Africa, this feature slightly increases in entire continents.')

        fig = px.scatter(df.dropna(), x="Perceptions of corruption", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        st.write('From the scatterplot we can see that there is a negative correlation between happiness index and perceptions of corruption, \
        the lower the corruption score, the higher the happiness index is likely to be. \
        There is also no clear difference for each region.')


    st.markdown('### Happiness Index by Country')
    st.write('Here, we are going to see the happiness index trend for each country in its respective region. \
    To get the region (continent) and sub-region for each country, we joined the happiness index dataset with \
    the United Nations (UN) geoscheme data. There are several countries which have inconsistent names so we manually\
    changed them before joining. Furthermore, there are two countries/territories present in the happiness dataset which \
    are not present in the UN dataset, namely Kosovo and Taiwan, so we added them manually to their respective regions.')

    def plot_line_chart(i, j, region): 
        df_reg = df[df['sub-subregion'] == region]
        df_reg = df_reg.pivot(index='year', columns='Country name', values='Happiness Score')
        ax[i,j].plot(df_reg)
        ax[i,j].set_title(region)
        ax[i,j].set_ylim([2.0, 8.0])

        box = ax[i,j].get_position()
        ax[i,j].set_position([box.x0, box.y0, box.width * 0.75, box.height])
        ax[i,j].legend(df_reg.columns.tolist(), loc='center left', bbox_to_anchor=(1, 0.5))


    option2 = st.selectbox('Select a continent to see the happiness index by countries',\
    ['Asia & Oceania', 'Europe', 'America', 'Africa'])

    if option2 == 'Asia & Oceania':
    
        fig, ax = plt.subplots(3, 2, figsize=(30, 16))
        plot_line_chart(0, 0, "Central Asia")
        plot_line_chart(0, 1, "Eastern Asia")
        plot_line_chart(1, 0, "South-eastern Asia")
        plot_line_chart(1, 1, "Southern Asia")
        plot_line_chart(2, 0, "Western Asia")
        plot_line_chart(2, 1, "Australia and New Zealand")
        
        st.pyplot(fig)
        st.write('Countries in Asia generally do not have significantly high or significantly low happiness index.\
        In its subregion, countries in South Asia have a lower happiness index compared to other subregions in Asia.\
        For Oceania, we only have data from two countries and both of them are in the Australia & New Zealand subregion \
        and both countries have high happiness index.')

    elif option2 == 'Europe':

        fig, ax = plt.subplots(2, 2, figsize=(20, 7))

        plot_line_chart(0, 0, "Eastern Europe")
        plot_line_chart(0, 1, "Northern Europe")
        plot_line_chart(1, 0, "Southern Europe")
        plot_line_chart(1, 1, "Western Europe")
        st.pyplot(fig)
        st.write('Countries in Europe have an overall high happiness index score.\
        Countries in the subregion West Europe have highest average happiness index compared to other regions \
        and their happiness index score is pretty stable throughout the years. \
        Countries in Northern Europe also have stable happiness index and several countries with significantly high happiness index,\
        but three of them have a mediocore index.')

    elif option2 == 'America':
        fig, ax = plt.subplots(2, 2, figsize=(14, 7))

        plot_line_chart(0, 0, "Northern America")
        plot_line_chart(0, 1, "Central America")
        plot_line_chart(1, 0, "South America")
        plot_line_chart(1, 1, "Caribbean")
        st.pyplot(fig)
        st.write('The subregion North America have a significantly high happiness index while Central and South America have a moderately high happiness index.\
        On the other hand, countries in the Carribean subregion have a moderately low happiness index.')

    elif option2 == 'Africa':
        fig, ax = plt.subplots(3, 2, figsize=(21, 16))
        plot_line_chart(0, 0, "Northern Africa")
        plot_line_chart(0, 1, "Eastern Africa")
        plot_line_chart(1, 0, "Middle Africa")
        plot_line_chart(1, 1, "Southern Africa")
        plot_line_chart(2, 0, "Western Africa")
        fig.delaxes(ax[2,1])
        st.pyplot(fig)
        st.write('Generally, we can see that countries in Africa have averagely lower happiness index compared to other continents.\
        The index also seems to fluctuate a lot through out the years.')

