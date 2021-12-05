import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from utils.dataloader import load_data, load_mvp_data
from utils.constants import *

def app():


    # Read File 
    raw = pd.read_excel('HappinessScores.xls')
    df_raw = raw[['Country name','Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices', 'Generosity',
           'Perceptions of corruption']].rename(columns={'Country name':'country'})
    df_raw = df_raw.dropna()
    df_country = pd.read_excel('un_geoscheme.xlsx')
    df_country.columns = ['country', 'sub-subregion', 'subregion', 'region', 'unsd_m49_codes']
    df_country = df_country[['country', 'region']]
    df_country['country'] = df_country['country'].str.strip()

    merged = df_raw.merge(df_country, on='country', how='left')
    merged.loc[(merged.country == 'Congo (Brazzaville)'),'region'] = 'Africa'
    merged.loc[(merged.country == 'Congo (Kinshasa)'),'region'] = 'Africa'
    merged.loc[(merged.country == 'Czech Republic'),'region'] = 'Europe'
    merged.loc[(merged.country == 'France'),'region'] = 'Europe'
    merged.loc[(merged.country == 'Ivory Coast'),'region'] = 'Africa'
    merged.loc[(merged.country == 'Myanmar'),'region'] = 'Asia'
    merged.loc[(merged.country == 'Palestinian Territories'),'region'] = 'Asia'
    merged.loc[(merged.country == 'South Korea'),'region'] = 'Asia'
    merged.loc[(merged.country == 'Swaziland'),'region'] = 'Africa'
    merged.loc[(merged.country == 'Taiwan Province of China'),'region'] = 'Asia'



    df = df_raw[['Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices', 'Generosity',
           'Perceptions of corruption']].dropna()
    df_centered = (df - np.min(df, axis = 0)) / (np.max(df, axis = 0) - np.min(df, axis = 0))
    m = np.cov(df_centered, rowvar = False)
    eigenvalues, eigenvectors = np.linalg.eigh(m) 
    # sort the eigenvalues from highest to lowest
    sorted_idx = np.argsort(eigenvalues)[::-1]
    # sort the eigenvectors according to the new order of the eigenvalues
    eigenvectors_sorted = eigenvectors[:, sorted_idx]
    # sort the eigenvalues
    eigenvalues_sorted = eigenvalues[sorted_idx]
    #print(eigenvalues_sorted)
    #print(eigenvectors_sorted)
    v = eigenvalues_sorted / np.sum(eigenvalues_sorted)
    v_cumulative = np.cumsum(v)
    print(v_cumulative)

    pc = eigenvectors_sorted[:, :2]
    # now, let's transform the data
    data_transform = np.dot(df_centered, pc)

    data = pd.DataFrame(data_transform)
    data['Continent'] = merged['region']

    fig = px.scatter(x = data[0], y = data[1], color = data['Continent'])
    st.plotly_chart(fig)
