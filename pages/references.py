import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from utils.dataloader import load_data, load_mvp_data
from utils.constants import *

def app():
    st.markdown("## References:")
    for key, link in citation_links.items(): 
        st.markdown(f"""{cite_num[key]} {link}""")