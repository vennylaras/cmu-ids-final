import collections
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression

# Read File 
raw = pd.read_excel('HappinessScores.xls')
df_raw = raw[['Country name','Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices', 'Generosity',
       'Perceptions of corruption','Life Ladder']].rename(columns={'Country name':'country'})
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



df_y = df_raw[['Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices', 'Generosity',
       'Perceptions of corruption','Life Ladder']].dropna()
df = df_raw[['Log GDP per capita','Social support','Healthy life expectancy at birth','Freedom to make life choices', 'Generosity',
       'Perceptions of corruption']]
df_centered = (df - np.min(df, axis = 0)) / (np.max(df, axis = 0) - np.min(df, axis = 0))

X = np.array(df)
y = np.array(df_y['Life Ladder'])
reg = LinearRegression().fit(X, y)

gdp  = st.number_input('GDP per Capita')

social_support = st.slider('Social Support', 0, 10, 1)

healthy_life = st.slider('Healthy life expectancy at birth', 1, 100, 10)

freedom = st.slider('Freedom to make life choices', 0, 10, 1)

generosity = st.slider('Generosity', 0, 10, 1)

corruption = st.slider('Perceptions of Corruption', 0, 10, 1)

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

st.write('Then, you might be from ',country, '!')
st.write('Your happiness score is ',predicted_val_round, ', and', country,"'s happiness score is", round(value,5 ), '!')
