import streamlit as st
import pandas as pd
import math

@st.cache
def load_mvp_data():
    df = pd.read_excel('data/HappinessScores.xls')
    df_happy = df
    years_to_keep = list(range(2010, 2020, 1))
    df = df[df["year"].isin(years_to_keep)]
    return df, df_happy
    
# Read File 
@st.cache(show_spinner=False, suppress_st_warning=True)
def load_data():
    # Happiness data
    df = pd.read_excel('data/HappinessScores.xls')
    df_happy = df

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

    # HDI
    df_hdi = pd.read_csv('data/hdi19.csv')

    # Pivoted
    df_pivot = df.pivot_table(index="Country name", columns="year", values="Happiness Score").reset_index()

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

    return df, df_happy, df_country, df_pivot, df_hdi, df_gender, df_mh_adm, df_mh_fac, df_suicide, df_sunshine