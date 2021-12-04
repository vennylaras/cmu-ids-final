import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from utils.dataloader import load_data, load_mvp_data
from utils.constants import *

def app():
    # Load a small bare minimum dataset on app load for faster load times
    df, _ = load_mvp_data()

    st.markdown("# Happiness, Around the World")
    st.write("""Happiness is one of the key factors that relates to success, satisfaction, 
        and a sense of well-being for human beings. Even after a person achieves great things in life, 
        like money, fame, or success in the field they're in, a real sense of achievement in life is not 
        complete unless people are happy with their lives, which often comes from a sense of community support, 
        having a purpose to live, and so on.""")

    col1, col2 = st.columns([5, 5])
    with col1: 
        st.markdown(f"""
            ### But, is it measurable?
            Recognizing the fact that happiness is subjective, 
            the World Happiness Report {cite("base")} is a 
            landmark survey that focuses on how happy individuals **perceive** themselves to be. 
            Every year, to measure the state of global happiness, it ranks 156 countries by whether 
            its citizens think they're living a good life.
        """)
    col2.image("imgs/socialsupport.jpg")
    
    st.markdown(f"""    
        ### Key Questions
        Individual measurable and tangible factors like a country's GDP, life expectancy, suicide rates, etc. 
        might contribute toward explaining this perceived happiness, but given the subjective nature of happiness, 
        might be too limited or narrow to be able to explain how satisfied people are with their lives.
    
        In this project, we aim to answer the following questions:
        - What are the the general long-term factors that affect happiness?
        - How has the happiness index changed for various regions of the world over the last decade? 
        - Do short-term events like major political events in a country affect its happiness levels? 
        
        We explore and discuss these questions through various sections (access the navigation pane on the left sidebar).

        ### Our Contributions
        We analyse the World Happiness Report dataset*, which contains the Gallup World Poll's 
        survey results of perceived happiness over the years in the form of the Cantril Ladder score, 
        and also contains several other key metrics like GDP, social support, and so on, 
        that might go towards explaining this perceived happiness, or part of it.
        
        We further add additional datasets on Human Development Index {cite("hdi")}, 
        Gender Inequality {cite("gdi")}, Suicide Rates {cite("suic")}, Mental Health {cite("mhadm")}, 
        and Sunshine Hours {cite("sun")}, and do correlation studies that can help us identify what factors 
        explain self-reported happiness the best, why some countries always rank higher than others on 
        the happiness scale, and so on. 

        ---
        *The dataset is published by the Sustainable Development Solutions Network, and powered by data from 
        the Gallup World Poll and Lloyd’s Register Foundation.
    """)

    

     # Load all data used on other pages and cache it for improved performance on navigating to these other pages
    load_data()
