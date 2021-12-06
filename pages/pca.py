import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from utils.dataloader import load_data, load_mvp_data
from utils.constants import *

def app():

    # Read File 
    raw,_ = load_mvp_data()
    df_raw = raw[['Country','Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices', 'Generosity',
           'Perceptions of corruption','Happiness Score']]
    df_raw = df_raw.dropna()
    df_country = load_country_data()
    df_country = df_country[['Country', 'region']]

    merged = df_raw.merge(df_country, on='Country', how='left')
    df_y = df_raw[['Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices', 'Generosity',
           'Perceptions of corruption','Happiness Score']].dropna()
    df = df_raw[['Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices', 'Generosity',
           'Perceptions of corruption']]
    df_centered = (df - np.min(df, axis = 0)) / (np.max(df, axis = 0) - np.min(df, axis = 0))
    m = np.cov(df_centered, rowvar = False)
    eigenvalues, eigenvectors = np.linalg.eigh(m) 
    # sort the eigenvalues from highest to lowest
    sorted_idx = np.argsort(eigenvalues)[::-1]
    # sort the eigenvectors according to the new order of the eigenvalues
    eigenvectors_sorted = eigenvectors[:, sorted_idx]
    # sort the eigenvalues
    eigenvalues_sorted = eigenvalues[sorted_idx]

    v = eigenvalues_sorted / np.sum(eigenvalues_sorted)
    v_cumulative = np.cumsum(v)
    print(v_cumulative)


    pc = eigenvectors_sorted[:, :3]
    # now, let's transform the data
    data_transform = np.dot(df_centered, pc)

    data = pd.DataFrame(data_transform)
    data['Continent'] = merged['region']

    fig = px.scatter(x = data[0], y = data[1], color = data['Continent'])
    st.plotly_chart(fig)
    
    ## 3d plot
    fig = px.scatter_3d(
        data, x=0, y=1, z=2, color=data['Continent'],
        title=f'Total Explained Variance:{v_cumulative[2]*100:.2f}%',
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
    )

    st.plotly_chart(fig)
    
