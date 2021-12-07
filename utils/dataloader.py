import streamlit as st
import pandas as pd
import math

from utils.constants import *

@st.cache()
def load_mvp_data():
    # Happiness data
    df = pd.read_excel('data/HappinessScores.xls')
    df = df.rename(columns= {'Life Ladder':HAPPINESS_SCORE, 'year': YEAR, 'Country name': COUNTRY})
    df_unfiltered = df.copy()
    years_to_keep = list(range(2010, 2020, 1))
    df = df[df[YEAR].isin(years_to_keep)]
    return df, df_unfiltered

@st.cache()  
def load_country_data(): 
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

    df_country = df_country.rename(columns={"country": COUNTRY})
    return df_country

@st.cache(show_spinner=False, suppress_st_warning=True)
def load_data():
    df, df_unfiltered = load_mvp_data()
    df_country = load_country_data()

    # Country joined with happiness
    df = df.join(df_country.set_index(COUNTRY), on=COUNTRY)
    df[GDP] = df[LOG_GDP].map(lambda x: math.exp(x))

    # HDI
    df_hdi = pd.read_csv('data/hdi19.csv')
    df_hdi = df_hdi.rename(columns={"country": COUNTRY})
    df_hdi[COUNTRY][df_hdi[COUNTRY] == 'Palestine'] = 'Palestinian Territories'
    df_hdi[COUNTRY][df_hdi[COUNTRY] == 'Republic of the Congo'] = 'Congo (Brazzaville)'
    df_hdi[COUNTRY][df_hdi[COUNTRY] == 'DR Congo'] = 'Congo (Kinshasa)'

    # Pivoted
    df_pivot = df.pivot_table(index=COUNTRY, columns=YEAR, values=HAPPINESS_SCORE).reset_index()
    df_pivot = df_pivot.join(df_country.set_index(COUNTRY), on=COUNTRY)

    # Gender
    df_gender = pd.read_excel('data/Gender Development Index (GDI).xlsx')
    df_gender[COUNTRY] = df_gender[COUNTRY].str.strip()
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Bolivia (Plurinational State of)'] = 'Bolivia'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Congo'] = 'Congo (Brazzaville)'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Congo (Democratic Republic of the)'] = 'Congo (Kinshasa)'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Czechia'] = 'Czech Republic'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Hong Kong, China (SAR)'] = 'Hong Kong S.A.R. of China'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Iran (Islamic Republic of)'] = 'Iran'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Lao People\'s Democratic Republic'] = 'Laos'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Moldova (Republic of)'] = 'Moldova'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Palestine, State of'] = 'Palestinian Territories'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Russian Federation'] = 'Russia'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Korea (Republic of)'] = 'South Korea'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Tanzania (United Republic of)'] = 'Tanzania'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Venezuela (Bolivarian Republic of)'] = 'Venezuela'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Viet Nam'] = 'Vietnam'
    df_gender[COUNTRY][df_gender[COUNTRY] == 'Syrian Arab Republic'] = 'Syria'

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
    df_sunshine = df_sunshine.groupby(COUNTRY).mean().reset_index()

    # Population
    df_pop = pd.read_excel('data/population_world_bank.xlsx')
    df_pop = df_pop.fillna(0)

    i = 0
    for col in df_pop.columns:
        if i > 3:
            df_pop[col] = df_pop[col].astype(int)
        i += 1

    new_header = df_pop.iloc[0] # grab the first row for the header
    df_pop = df_pop[1:] # take the data less the header row
    df_pop.columns = new_header
    df_pop = df_pop.rename(columns={'Country Name': COUNTRY})

    i = 0
    for col in df_pop.columns:
        if i > 3:
            if int(col) < 2010 or int(col) > 2019:
                df_pop = df_pop.drop(col, axis=1)
        i += 1
    
    # df_pop = df_pop.melt(id_vars=[COUNTRY], value_vars=[y for y in range(2010,2020)],
    #        var_name=YEAR, value_name=POPULATION)
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Congo, Rep.'] = 'Congo (Brazzaville)'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Congo, Dem. Rep.'] = 'Congo (Kinshasa)'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Egypt, Arab Rep.'] = 'Egypt'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Gambia, The'] = 'Gambia'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Hong Kong SAR, China'] = 'Hong Kong S.A.R. of China'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Iran, Islamic Rep.'] = 'Iran'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Kyrgyz Republic'] = 'Kyrgyzstan'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Lao PDR'] = 'Laos'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Russian Federation'] = 'Russia'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Slovak Republic'] = 'Slovakia'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Korea, Rep.'] = 'South Korea'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Syrian Arab Republic'] = 'Syria'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Venezuela, RB'] = 'Venezuela'
    # df_pop[COUNTRY][df_pop[COUNTRY] == 'Yemen, Rep.'] = 'Yemen'

    # df_pop['Log Population'] = df_pop[POPULATION].map(lambda x: math.log(x+2))
    
    # df_pop_merged = df.merge(df_pop, on=[COUNTRY, YEAR])

    return df, df_unfiltered, df_country, df_pivot, df_hdi, df_gender, df_mh_adm, df_mh_fac, df_suicide, df_sunshine