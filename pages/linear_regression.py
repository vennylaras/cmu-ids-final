import collections
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from utils.dataloader import load_data, load_mvp_data, load_country_data
from utils.constants import *

# Read File 
def app():
    raw,_ = load_mvp_data()
    df_raw = raw[[COUNTRY,LOG_GDP,SOCIAL_SUPPORT,LIFE_EXPECTANCY,FREEDOM, GENEROSITY,
          CORRUPTION,HAPPINESS_SCORE]]
    df_raw = df_raw.dropna()

    df_country = load_country_data()
    df_country = df_country[[COUNTRY, REGION]]

    merged = df_raw.merge(df_country, on=COUNTRY, how='left')


    df_y = df_raw[[LOG_GDP,SOCIAL_SUPPORT,LIFE_EXPECTANCY,FREEDOM, GENEROSITY,
          CORRUPTION,HAPPINESS_SCORE]].dropna()
    df = df_raw[[LOG_GDP,SOCIAL_SUPPORT,LIFE_EXPECTANCY,FREEDOM, GENEROSITY,
          CORRUPTION]]
    df_centered = (df - np.min(df, axis = 0)) / (np.max(df, axis = 0) - np.min(df, axis = 0))

    X = np.array(df)
    y = np.array(df_y[HAPPINESS_SCORE])
    reg = LinearRegression().fit(X, y)
    
    
    st.markdown("# Let's Predict Your Country")
    st.markdown("We created a linear regression model using 6 features. This model predicts the happiness score based on your provided inputs. \
    Feel free to move the sliders below to provide inputs to our model and predict the happiness score of your country! \
    Also, our model additionally guesses your country by finding the one which has the most similar happiness score by applying euclidean distance.")

    col1, col2 = st.columns([1, 1])
    with col1:    
        gdp = st.slider(GDP, int(np.exp(np.min(np.array(df_y[LOG_GDP])))), int(np.exp(np.max(np.array(df_y[LOG_GDP])))), int(np.exp(np.median(np.array(df_y[LOG_GDP])))))
        social_support = st.slider(SOCIAL_SUPPORT, 0, 10, 8)
        healthy_life = st.slider(LIFE_EXPECTANCY, 1, 100, 60)

    with col2: 
        freedom = st.slider(FREEDOM, 0, 10, 7)
        generosity = st.slider(GENEROSITY, 0, 10, 1)
        corruption = st.slider(CORRUPTION, 0, 10, 8)

    if gdp == 0:
      st.write("Error! Please fill out 'GDP per Capita.' The value should be higher than 0.")
    else:
      add_row = {LOG_GDP: np.log(gdp), SOCIAL_SUPPORT: social_support/10, LIFE_EXPECTANCY: healthy_life,\
            FREEDOM:freedom/10,GENEROSITY:generosity/10,CORRUPTION:corruption/10}

      df = df.append(add_row, ignore_index = True)
      #st.write(df)
      df_centered = (df - np.min(df, axis = 0)) / (np.max(df, axis = 0) - np.min(df, axis = 0))
      predicted_val = reg.predict(np.array(([df.iloc[-1]])))
      predicted_val_round = np.round(predicted_val[0],4)

      predict_country = df_raw[[COUNTRY, HAPPINESS_SCORE]].reset_index()
      min_val = 1000
      for i in range(len(predict_country[HAPPINESS_SCORE])):
            val = predict_country[HAPPINESS_SCORE][i]
            dist = np.sqrt((predicted_val - val)**2)
            if dist < min_val:
                  country = predict_country[COUNTRY][i]
                  value = val
                  min_val = dist

      col1, col2 = st.columns([1, 1])
      st.markdown("""
        ---
      """)
      st.write(f'You might be from {country.strip()}!')
      with col1:
        st.metric(f'Predicted happiness score:', predicted_val_round) 
      with col2: 
        st.metric(f"{country}'s happiness score:", round(value, 4)) 
