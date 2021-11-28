import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

@st.cache
def load_data():
	# Happiness data
	df = pd.read_excel('data/HappinessScores.xls')
	years_to_keep = list(range(2010, 2020, 1))
	df = df[df["year"].isin(years_to_keep)]
	df_happy = df
	return df_happy

def app():
	df = load_data()
	

	st.title('Case Studies')
	st.write("Apart from the attributes we explored in the dataset and factors discussed in further analysis, we believe that other, \
		less measurable factors can also play a significant role in the happiness scores of a country.")

	yem_df = df[df['Country name'] == 'Yemen']
	#st.write(yem_df)
	fig, ax = plt.subplots(figsize=(8, 4))
	ax = plt.plot(yem_df['year'], yem_df['Life Ladder'])
	plt.xlabel('Year')
	plt.ylabel('Happiness score')
	plt.title('Happiness score trends: Yemen')
	st.pyplot(fig)

	st.write("Going back to the happiness score by \
		country charts, we observe sharp dips in the happiness score trends for some countries. Yemen shows a steep decline in the happiness \
		score starting from 2014, with the lowest score around 2015 and again in 2018. \
		These years correspond to periods of major disruption in the political stability of Yemen. The Yemeni civil war began in September 2014 \
		with the takeover of the government.")
	st.write("The civil war induced a massive food crisis in Yemen. By 2017, a quarter of the country's population was nearing a \
		state of population and the United Nations warned that Yemen could face the worst famine the world has seen for many decades. \
		These events coincide with the declines in the happiness score of Yemen.")

	ven_df = df[df['Country name'] == 'Venezuela']
	#st.write(yem_df)
	fig, ax = plt.subplots(figsize=(8, 4))
	ax = plt.plot(yem_df['year'], yem_df['Life Ladder'])
	plt.xlabel('Year')
	plt.ylabel('Happiness score')
	plt.title('Happiness score trends: Venezuela')
	st.pyplot(fig)

	st.write("Another example that suggests that socioeconomic and political factors might reflect in the happiness score trends of a country \
		is the case of Venezuela. The happiness score chart shows a steady decline in the happiness scores from 2012, and the chart shows a sharper \
		decline after 2015, hitting the lowest point near 2016.")
	st.write("If we look back to the political climate in Venezuela in 2012, the presidential elections marked the beginning of the crisis in Venezuela. \
		This has been described as the worst economic crisis in Venezuala's history; more severe than that of the United States during the Great Depression. \
		The life of the average Venezuelan was affected on all levels. 75% of the population had lost an average of 8 kgs/19 lbs in weight and majority of the \
		people were not able to meet their basic food needs. Another side-effect of this was a sharp increase in the homicide rate from 39 per 100,000 in 2013 \
		to 90 per 100,000 in 2015. Once again, we can see how all of these factors might have contributed to the overall happiness of the country's population.")
	