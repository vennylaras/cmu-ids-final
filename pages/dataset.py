import collections
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import math
import missingno
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

    # HDI
    df_hdi = pd.read_csv('data/hdi19.csv')

    return df, df_happy, df_country, df_hdi

def app():
    df, df_happy, df_country, df_hdi = load_data()

    st.title('Dataset')

    st.markdown('### Data Source')

    st.markdown('##### World Happiness Report')
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

    st.markdown('##### Secondary Datasets')
    # TODO Explain secondary datasets
    st.write('TODO')


    st.markdown("[1] https://worldhappiness.report/")
    st.markdown("[2] http://hdr.undp.org/en/indicators/137906")
    st.markdown("[3] http://hdr.undp.org/en/indicators/137506")
    st.markdown("[4] https://www.who.int/data/gho/data/themes/mental-health/suicide-rates")
    st.markdown("[5] https://worldpopulationreview.com/country-rankings/hdi-by-country")
    st.markdown("[6] https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme")
    # TODO add more that we've used



    # TODO Add 4C: Completeness, Coherence, Correctness, aCcountability
    st.text("")
    st.markdown('###  Data Quality')
    st.write('TODO: 4C')



    # TODO Add analysis of missing data, duplicates, etc
    st.text("")
    st.markdown('###  Initial Exploration')
    st.markdown('##### Analysis of Missing Data')
    st.write('We first look at our whole table to check if there is any jarring nullity that warrants dropping some columns.')

    def preview_nulls(df):
        # generate preview of entries with null values
        if df.isnull().any(axis=None):
            print("\nPreview of data with null values:")
            fig = missingno.matrix(df).figure
            return fig

    st.pyplot(preview_nulls(df_happy))

    st.write('While the overall data seems reliably populated from the above chart, we note that surveys might not be \
        conducted or complete in some countries in some years.')

    st.write('As such, since the main metric we want to study is the happiness index, given by the Life Ladder score, \
        we further check the nullity over years of the happiness index for each country, by pivoting our data appropriately \
            to have countries as rows, years as columns, and values as the happiness index')

    happiness_df = df_happy.pivot_table(index="Country name", columns="year", values="Life Ladder").reset_index()
    st.pyplot(preview_nulls(happiness_df))

    st.write("""
        We find that the happiness report survey data is extremely sparse for 2005 - 2009, and 2020. Therefore, we make a \
            conscious decision of removing these years from all our analysis and restrict to a decade worth of more reliable \
                data found in the 2010 to 2019 survey results.

        Considering that a country might consistently score low or high on the happiness scale, this also drives a decision \
            to make sure we only present aggregate metrics over years for a subset of countries that have data for all years, \
                as comparing 2019 overall averages with 2020 averages given 2020 doesn't have a subset of low scoring countries \
                    would be fallacious. 

        Therefore, all global averages mentioned in the report automatically refer to a subset. When looking at individual \
            countries in multiples of line plots, the disconnections between the lines will signify the unavailability of data \
                instead.
    """)

    st.text("")
    st.markdown('##### Statistical Analysis of Numerical Metrics')
    st.write('Next, we look at a quick statistical analysis of our numerical columns to see if anything stands out as an \
        outlier and might be worth removing.')

    def stats(df): 
        df = df.describe().drop(columns=["year"])
        return df

    st.dataframe(stats(df_happy))

    # TODO: Maybe add a dropdown for each attribute so that it won't be too long?
    columns = df_happy.columns.tolist()
    columns.remove('year')
    columns.remove('Country name')
    column = st.selectbox('Attribute', columns)

    fig = px.box(df_happy, x="year", y=column, hover_data=["Country name"], points="all")
    st.plotly_chart(fig)
    

    st.text("")
    st.markdown('##### Pairwise Correlations of Numerical Metrics')
    st.markdown('Looking at the pairwise correlations of all metrics with each other for all countries for the decade 2010-2020, \
        we find that GDP, Life Expectancy, and Social Support are **on average most heavily correlated with the Life Ladder \
        happiness index.**')

    fig = plt.figure()
    sns.heatmap(df_happy.corr(), cmap="coolwarm_r")
    st.pyplot(fig)

    st.markdown("""
        **However, we hypothesize that these correlations might vary significantly with the standard of living in different \
            countries and the general ability of people to fight for survival versus being able to take a safe and healthy \
                environment as a given.**

        To test this hypothesis, we turn to looking at **Human Development Index** as a way to categorize countries.

        The Human Development Index (HDI) is compiled by the United Nations Development Programme (UNDP) for 189 countries on \
            an annual basis. The index considers the health, education and income in a given country to provide a measure of \
                human development which is comparable between countries and over time. 
    """)

    st.markdown("""
        The International Monetary Fund (IMF) categorizes "developed countries" have an HDI score of 0.8 or above [5] \
            (in the very high human development tier). These countries have stable governments, widespread education, \
                healthcare, high life expectancies, and growing, powerful economies.
    """)

    st.markdown("""
    **Developed Countries**

    For developed countries with high Human Development Indices, happiness is positively correlated to many factors like \
        social support, freedom to make life choices, generosity, etc. Further, perceptions of corruption is highly negatively \
            correlated with happiness index, showing that people care about politics, who the country's leaders are, and are aware \
                enough to know what might be affecting their access to peace and standard of living on a daily basis.

    This shows that when basic needs like economy (as measured by GDP) and health (as measured by life expectancy) are in good shape, \
        people start caring about a well-rounded life and factors like generosity, social support systems, polotiical influences, and \
            other nuanced factors to happiness.
    """)

    developed_countries = list(df_hdi[df_hdi["hdi2019"] >= 0.8]["country"])
    region_df = df_happy[df_happy["Country name"].isin(developed_countries)]
    fig = plt.figure()
    sns.heatmap(region_df.corr(), cmap="coolwarm_r")
    st.pyplot(fig)

    st.markdown("""
    **Developing Countries**

    Through the below heatmap, we see that as we move towards developing countries with lower Human Development Indices, \
        happiness is positively only correlated to per capita GDP and Life Expectancy at birth, i.e., the economy and health \
            systems play the most significant roles as people's happiness depends on their ability to get by and make a living \
                and work towards a respectable standard of living.

    Things like generosity, or social support are effectively first world problems that don't really factor into general happiness \
        for most people.
    """)

    developing_countries = list(df_hdi[df_hdi["hdi2019"] < 0.7]["country"])
    region_df = df[df["Country name"].isin(developing_countries)]
    fig = plt.figure()
    sns.heatmap(region_df.corr(), cmap="coolwarm_r")
    st.pyplot(fig)


    st.text("")
    st.markdown('##### Happiness Score Trend by Country')
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
    
        fig, ax = plt.subplots(3, 2, figsize=(18, 14))
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

        fig, ax = plt.subplots(2, 2, figsize=(16, 8))

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
        fig, ax = plt.subplots(2, 2, figsize=(14, 8))

        plot_line_chart(0, 0, "Northern America")
        plot_line_chart(0, 1, "Central America")
        plot_line_chart(1, 0, "South America")
        plot_line_chart(1, 1, "Caribbean")
        st.pyplot(fig)
        st.write('The subregion North America have a significantly high happiness index while Central and South America have a moderately high happiness index.\
        On the other hand, countries in the Carribean subregion have a moderately low happiness index.')

    elif option2 == 'Africa':
        fig, ax = plt.subplots(3, 2, figsize=(18, 14))
        plot_line_chart(0, 0, "Northern Africa")
        plot_line_chart(0, 1, "Eastern Africa")
        plot_line_chart(1, 0, "Middle Africa")
        plot_line_chart(1, 1, "Southern Africa")
        plot_line_chart(2, 0, "Western Africa")
        fig.delaxes(ax[2,1])
        st.pyplot(fig)
        st.write('Generally, we can see that countries in Africa have averagely lower happiness index compared to other continents.\
        The index also seems to fluctuate a lot through out the years.')

