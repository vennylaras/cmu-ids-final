import collections
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from utils.dataloader import load_data, load_mvp_data
from utils.constants import *

# Read File 
def app():
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

    X = np.array(df)
    y = np.array(df_y['Happiness Score'])
    reg = LinearRegression().fit(X, y)
    
    
    st.markdown("# Let's Predict Your Country")
    st.markdown("We created a linear regression model using 6 features. This model predicts the happiness score based on your provided inputs. \
    Feel free to move the sliders below to provide inputs to our model and predict the happiness score of your country! \
    Also, our model additionally guesses your country by finding the one which has the most similar happiness score by applying euclidean distance.")
    
    gdp  = st.number_input('GDP per Capita')

    social_support = st.slider('Social Support', 0, 10, 1)

    healthy_life = st.slider('Healthy life expectancy at birth', 1, 100, 10)

    freedom = st.slider('Freedom to make life choices', 0, 10, 1)

    generosity = st.slider('Generosity', 0, 10, 1)

    corruption = st.slider('Perceptions of Corruption', 0, 10, 1)

    if gdp == 0:
      st.write("Error! Please fill out 'GDP per Capita.' The value should be higher than 0.")
    else:
      add_row = {'Log GDP per capita': np.log(gdp), 'Social support': social_support/10, 'Healthy life expectancy at birth': healthy_life,\
            'Freedom to make life choices':freedom/10,'Generosity':generosity/10,'Perceptions of corruption':corruption/10}

      df = df.append(add_row, ignore_index = True)
      #st.write(df)
      df_centered = (df - np.min(df, axis = 0)) / (np.max(df, axis = 0) - np.min(df, axis = 0))
      predicted_val = reg.predict(np.array(([df.iloc[-1]])))
      predicted_val_round = np.round(predicted_val[0],5)
      st.write('Here is your happiness score:', predicted_val_round)

      predict_country = df_raw[['country','Life Ladder']].reset_index()
      min_val = 1000
      for i in range(len(predict_country['Life Ladder'])):
            val = predict_country['Life Ladder'][i]
            dist = np.sqrt((predicted_val - val)**2)
            if dist < min_val:
                  country = predict_country['country'][i]
                  value = val
                  min_val = dist

      st.write('You might be from ',country, '!')
      st.write('Your happiness score is ',predicted_val_round, ', and', country,"'s happiness score is", round(value,5 ), '!')
