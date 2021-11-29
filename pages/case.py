import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from utils.dataloader import load_mvp_data

def app():
    df = load_mvp_data()
	
    st.title('Case Studies')
    st.write("Apart from the attributes we explored in the dataset and factors discussed in further analysis, we believe that other, \
		less measurable factors can also play a significant role in the happiness scores of a country.")

    st.markdown("## Yemen")
    yem_df = df[df['Country name'] == 'Yemen']
    fig = px.line(yem_df, x='year', y='Life Ladder', labels={"year": "Year", "Life Ladder": "Happiness Score"})
    st.plotly_chart(fig)

    st.write("Going back to the happiness score by \
		country charts, we observe sharp dips in the happiness score trends for some countries. Yemen shows a steep decline in the happiness \
		score starting from 2014, with the lowest score around 2015 and again in 2018. \
		These years correspond to periods of major disruption in the political stability of Yemen. The Yemeni civil war began in September 2014 \
		with the takeover of the government.")
    st.write("The civil war induced a massive food crisis in Yemen. By 2017, a quarter of the country's population was nearing a \
		state of population and the United Nations warned that Yemen could face the worst famine the world has seen for many decades. \
		These events coincide with the declines in the happiness score of Yemen.")

    st.markdown("## Venezuela")
    ven_df = df[df['Country name'] == 'Venezuela']
    fig = px.line(ven_df, x='year', y='Life Ladder', labels={"year": "Year", "Life Ladder": "Happiness Score"})
    st.plotly_chart(fig)

    st.write("Another example that suggests that socioeconomic and political factors might reflect in the happiness score trends of a country \
		is the case of Venezuela. The happiness score chart shows a steady decline in the happiness scores from 2012, and the chart shows a sharper \
		decline after 2015, hitting the lowest point near 2016.")
    st.write("If we look back to the political climate in Venezuela in 2012, the presidential elections marked the beginning of the crisis in Venezuela. \
		This has been described as the worst economic crisis in Venezuala's history; more severe than that of the United States during the Great Depression. \
		The life of the average Venezuelan was affected on all levels. 75% of the population had lost an average of 8 kgs/19 lbs in weight and majority of the \
		people were not able to meet their basic food needs. Another side-effect of this was a sharp increase in the homicide rate from 39 per 100,000 in 2013 \
		to 90 per 100,000 in 2015. Once again, we can see how all of these factors might have contributed to the overall happiness of the country's population.")
