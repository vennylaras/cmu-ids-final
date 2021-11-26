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

    # Pivoted
    df_pivot = df.pivot_table(index="Country name", columns="year", values="Happiness Score").reset_index()
    df_pivot = df_pivot.rename(columns={2019:'2019'})[['Country name', '2019']]
    df_pivot = df_pivot.rename(columns={'Country name':'Country'})
    df_pivot['Country'] = df_pivot['Country'].str.strip()

    # Gender
    df_gender = pd.read_excel('data/Gender Development Index (GDI).xlsx')

    # Mental Health
    df_mh_adm = pd.read_excel('data/MentalHealthAdmissionsPer100000.xlsx')
    df_mh_fac = pd.read_excel('data/MentalHealthFacilitiesPer100000.xlsx')

    # Suicide
    df_suicide = pd.read_excel ('data/MortalityData.xlsx')
    new_header = df_suicide.iloc[1] # grab the first row for the header
    df_suicide = df_suicide [2:] # take the data less the header row
    df_suicide.columns = new_header
    df_suicide['Period']= df_suicide['Period'].apply(lambda x: int(x))

    # Sunshine
    df_sunshine = pd.read_excel('data/Cities_by_Sunshine_Duration_2019_wikipedia.xlsx')
    df_sunshine = df_sunshine.groupby('Country').mean().reset_index()

    return df, df_pivot, df_country, df_gender, df_mh_adm, df_mh_fac, df_suicide, df_sunshine

def app():
    df, df_pivot, df_country, df_gender, df_mh_adm, df_mh_fac, df_suicide, df_sunshine = load_data()

    st.title('Contributing Factors')

    st.markdown('### Quality of Life')
    st.write('In this section, we explore the correlation between happiness index and several quality of life factors presented in the original report.\
    The first graph below describes yearly change of the selected feature in each continent given in our main happiness dataset, and\
    the second graph shows the correlation between each feature and the happiness score for each year.')

    option = st.selectbox('Feature that explains Happiness Index',\
    ['Social Support', 'Healthy Life Expectancy at Birth', 'Log GDP per Capita',\
    'Generosity','Freedom to Make Life Choices','Perceptions of corruption'])

    ## 1
    # Social Support vs. Year

    if option == 'Social Support':
        # st.markdown('### Social Support')
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)]
        df1 = df1.groupby(['region','year'])[['Social support']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1, x="Year", y="Social support", color = 'region',title='Social Support by Year',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
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
        # st.markdown('### Healthy Life Expectancy at Birth')
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Healthy life expectancy at birth']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Healthy life expectancy at birth", color = 'region',title='Healthy Life Expectancy at Birth by Year',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
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
        # st.markdown('### Gross Domestic Product')
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Log GDP per capita']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Log GDP per capita", color = 'region',title='GDP by Year',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
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
        # st.markdown('### Generosity')
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Generosity']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Generosity", color = 'region',title='Generosity by Year',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
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
        # st.markdown('### Freedom to Make Life Choices')
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Freedom to make life choices']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Freedom to make life choices", color = 'region',title='Freedom to make life choices change by Year',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
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
        # st.markdown('### Perceptions of Corruption')
        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Perceptions of corruption']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Perceptions of corruption", color = 'region',title='Perceptions of corruption change by Year',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        st.write('Except for Asia and Africa, this feature slightly increases in entire continents.')

        fig = px.scatter(df.dropna(), x="Perceptions of corruption", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        st.write('From the scatterplot we can see that there is a negative correlation between happiness index and perceptions of corruption, \
        the lower the corruption score, the higher the happiness index is likely to be. \
        There is also no clear difference for each region.')
    

    st.text("")
    st.markdown('### Gender Disparity')

    st.write("""
        Next, we hypothesize that gender disparity might play a role in the happiness score of a country. \
        Living in an equal society where everyone has the ability to choose the circumstances of their own lives, \
        would likely lead to greater happiness. To test this hypothesis, we explore a dataset that comprises the \
        Gender Development Index (GDI) for countries spanning multiple years.
        GDI is defined as the ratio of female to male HDI values. Countries that have achieved some success in \
        expanding capabilities for both men and women will have higher GDI. A country having a GDI less than 0.5 \
        indicates larger gender disparity.
    """)

    def plot_gender(happiness_df, gender):
        gender_19 = gender.rename(columns={2019.0:'2019'})[['Country', '2019']]
        gender_19['Country'] = gender_19['Country'].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index('country'), on='Country')

        merged = happiness_df_with_continent.merge(gender_19, on='Country', how='inner')
        merged = merged.rename(columns={'2019_x':'Happiness','2019_y':'GDI'})
        
        fig = px.scatter(merged.dropna(), x="GDI", y="Happiness", hover_name='Country', color='region',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})

        return fig
    
    st.plotly_chart(plot_gender(df_pivot, df_gender))


    st.write("""
        We observe that countries having a higher GDI have a higher happiness score. This seems to align with what \
            one would expect; a country having low gender disparity is more inclusive and diverse, and likely to have \
                a higher happiness score.
    """)


    st.text("")
    st.markdown('### Mental Health')
    st.markdown('**Availability and Admissions**')

    st.write("""
        We are also interested in exploring whether a country's mental health services availability has any \
        impact on the happiness score. For this, we explore a dataset published by the World Health Organization, \
        that contains information on mental hospitals, mental health admissions, etc. for countries spanning across \
        multiple years. For the purpose of this analysis, we consider the following two factors: 1. Mental Health \
        Admissions per 100,000 people and 2. Mental Health Facilities per 100,000 people. We consider data for the year 2019.
    """)

    def plot_mental_health(happiness_df, mental_health):
        mental_health = mental_health[['Location','FactValueNumeric', 'ParentLocation']]
        mental_health = mental_health.rename(columns={'Location':'Country', 
                                                    'FactValueNumeric':'MentalHealthAdmissionsPer100000'})
        mental_health['Country'] = mental_health['Country'].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index('country'), on='Country')

        happiness_mental_health_merged = happiness_df_with_continent.merge(mental_health, on='Country', how='inner')
        happiness_mental_health_merged = happiness_mental_health_merged.rename(columns={'2019':'Happiness'})

        fig = px.scatter(happiness_mental_health_merged.dropna(), x="MentalHealthAdmissionsPer100000", y="Happiness", hover_name='Country', color="region",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        return fig
    
    st.plotly_chart(plot_mental_health(df_pivot, df_mh_adm))

    def plot_mental_health_facilities(happiness_df, mental_health_facilities):
        x = mental_health_facilities[mental_health_facilities['IndicatorCode'].str.strip() == 'MH_17'][['Location','FactValueNumeric', 'ParentLocation']]
        x = x.rename(columns={'Location':'Country', 
                            'FactValueNumeric':'MentalHealthFacilitiesPer100000'})
        x['Country'] = x['Country'].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index('country'), on='Country')

        happiness_mental_health_facilities_merged = happiness_df_with_continent.merge(x, on='Country', how='inner')
        happiness_mental_health_facilities_merged = happiness_mental_health_facilities_merged.rename(columns={'2019':'Happiness'})
        fig = px.scatter(happiness_mental_health_facilities_merged.dropna(), x="MentalHealthFacilitiesPer100000", y="Happiness", hover_name='Country', 
                range_x=(0,1), color="region", category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        return fig

    st.plotly_chart(plot_mental_health_facilities(df_pivot, df_mh_fac))

    st.write("""
        For countries having close to 0 mental health admissions per 100,000 people, the happiness score seems to be \
        dependent on other factors and a direct correlation cannot be observed. However, in countries having >100 mental \
        health admissions per 100,000, the happiness score is >5, indicating that perhaps countries that have destigmatized \
        mental health are more likely to have a higher happiness score. The graph could also indicate that there is poor \
        reporting of mental health admissions in various countries.
    """)

    st.text("")
    st.markdown('### Suicide Rates')

    st.write("In this section, we examine the correlation between suicide rate and happiness. \
        We used the suicide rate data per 100,000 people. [Add more .....]")

    def plot_suicide(df, suicide):
        suicide = suicide[suicide['Dim1'] == 'Both sexes']
        suicide = suicide[['Location','FactValueNumeric', 'ParentLocation', 'Period']]
        suicide = suicide.rename(columns={'Location':'Country', 
                                        'FactValueNumeric':'SuicideRatePer100000'})
        suicide['Country'] = suicide['Country'].str.strip()


        happiness_suicide_merged = df.merge(suicide, left_on=['Country name', 'year'], right_on=['Country', 'Period'], how='inner')

        fig = px.scatter(happiness_suicide_merged.dropna(), x="SuicideRatePer100000", y="Happiness Score", hover_name='Country name', 
                color="region", range_x=(0,40), animation_frame='year',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        return fig

    st.plotly_chart(plot_suicide(df, df_suicide))

    st.write("TODO: Add writeup")



    st.text("")
    st.markdown('### Sunshine Hours')

    st.write("In this section, we examine the correlation between sunshine hours and happiness. \
        We consider data for the yearly sunshine hour avergae for the year 2019. [Add more .....]")

    def plot_sunshine(happiness_df, sunshine):
        sunshine = sunshine[['Country','Year']]
        sunshine = sunshine.rename(columns={'Year':'YearlySunshineHours'})
        sunshine['Country'] = sunshine['Country'].str.strip()
        
        happiness_df_with_continent = happiness_df.join(df_country.set_index('country'), on='Country')

        happiness_sunshine_merged = happiness_df_with_continent.merge(sunshine, on='Country', how='inner')
        happiness_sunshine_merged = happiness_sunshine_merged.rename(columns={'2019':'Happiness'})

        fig = px.scatter(happiness_sunshine_merged.dropna(), x="YearlySunshineHours", y="Happiness", hover_name='Country', color="region",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        return fig

    st.plotly_chart(plot_sunshine(df_pivot, df_sunshine))

    st.write("TODO: Add writeup")


