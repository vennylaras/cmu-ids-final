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
    df_happy = df

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

    return df, df_happy, df_country

def app():
    df, df_happy, df_country = load_data()

    st.title('Dataset')

    st.markdown('## Data Source')

    st.markdown('### World Happiness Report')
    st.markdown("[1] https://worldhappiness.report/")
    st.write("""
        The World Happiness Report is a publication of the United Nations Sustainable Development Solutions Network. 
        This report contains articles and rankings of national happiness, based on respondent ratings of their own lives,
        which the report also correlates with various quality of life factors.""")
    st.dataframe(df_happy)
    st.markdown("""
        Here is a brief description of  these columns collected from the Gallup World Poll (GWP): 
        - **Life Ladder:** The average happiness index
        - **Log GDP Per Capita:** A country's per capita GDP on log-scale
        - **Social Support:** Social support is the national average of the binary responses (either 0 or 1) to the Gallup World Poll (GWP) question “If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?”
        - **Healthy Life Expectancy at Birth:** The expected life expectancy of an average human-being at birth
        - **Generosity:** Generosity is the residual of regressing the national average of GWP responses to the question “Have you donated money to a charity in the past month?” on GDP per capita.
        - **Perceptions of Corruption:** It's the average of binary answers to two GWP questions: “Is corruption widespread throughout the government or not?” and “Is corruption widespread within businesses or not?” (Note: Where data for government corruption are missing, the perception of business corruption is used as the overall corruption-perception measure.)
        - **Positive affect:** It comprises the average frequency of happiness, laughter and enjoyment on the previous day
        - **Negative affect:** It comprises the average frequency of worry, sadness and anger on the previous day. 
        The affect measures lie between 0 and 1.
        """)

    st.markdown('### Secondary Datasets')
    # TODO Explain secondary datasets
    st.markdown("[2] http://hdr.undp.org/en/indicators/137906")
    st.markdown("[3] http://hdr.undp.org/en/indicators/137506")
    st.markdown("[4] https://www.who.int/data/gho/data/themes/mental-health/suicide-rates")

    # TODO Add 4C

    # TODO Add analysis of missing data, duplicates, etc

    st.markdown('## Happiness Index by Country')
    st.write('Here, we are going to see the happiness index trend for each country in its respective region. \
    To get the region (continent) and sub-region for each country, we joined the happiness index dataset with \
    the United Nations (UN) geoscheme data. There are several countries which have inconsistent names so we manually \
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

