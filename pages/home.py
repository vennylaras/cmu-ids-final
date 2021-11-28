import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from utils.dataloader import load_data

def app():
    # Load a small bare minimum dataset on app load for faster load times
    df = load_mvp_data()

    st.markdown("# Happiness Around the World")

    st.markdown("### Is it measurable?")
    st.write("Happiness is one of the key factors that relates to success, satisfaction, \
        and a sense of well-being for human beings. Even after a person achieves great things in life, \
        like money, fame, or success in the field they're in, a real sense of achievement in life is not \
        complete unless people are happy with their lives, which often comes from a sense of community support, \
        having a purpose to live, and so on.")
    st.write("In this report, we analyse the World Happiness Report [1] dataset as our base dataset, \
        which is a global survey being conducted for over 10 years across the globe in 140+ countries, \
        and is published by the Sustainable Development Solutions Network, powered by data from \
        the Gallup World Poll and Lloyd’s Register Foundation.")
    st.write("We do exploratory data analysis to look for completeness, duplicates, outliers, \
        and pairwise correlations for all of the different metrics they report.")
    st.write("We further add additional datasets on gender inequality [2], human development index [3], \
        and suicide rates [4] obtained from United Nations' and World Health Organization's websites, \
        and do correlation studies to build preliminary hypotheses that can help us identify what factors \
        explain self-reported happiness the best, why some countries always rank higher than others on \
        the happiness scale, and so on. ")
    
    st.markdown("### Worldwide Happiness Index")
    st.write("The map below shows the happiness index for each country throughout the year 2010 untul 2019. \
        From the map we can see that countries in Europe, America, and Australia generally have higher happiness index \
        than countries in Asia and Africa.")

    st.plotly_chart(world_map(df))

    st.write("What are the the contributing factors affecting happiness? \
     How did the happiness index change over the years? \
     Does a contry's happiness index correlate with major political events in that country? \
     In the following sections we are going to explore and discuss these questions." )

     # Load all data used on other pages and cache it for improved performance on navigating to these other pages
    load_data()

@st.cache
def load_mvp_data():
    df = pd.read_excel('data/HappinessScores.xls')
    years_to_keep = list(range(2010, 2020, 1))
    df = df[df["year"].isin(years_to_keep)]
    return df
    
def world_map(df):
    df_happy_sort_year = df.sort_values(by=['year'])
    fig = px.choropleth(locations=df_happy_sort_year['Country name'], 
              locationmode="country names",
              color=df_happy_sort_year['Life Ladder'],
              animation_frame=df_happy_sort_year['year'],
              color_continuous_scale="Bluyl",
              range_color=(2.5, 7.5))
    fig.update_geos(projection_type="natural earth")
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
    return fig
