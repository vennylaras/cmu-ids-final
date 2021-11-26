import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import home, dataset, analysis

# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("Home", home.app)
app.add_page("Dataset", dataset.app)
app.add_page("Analysis", analysis.app)

# The main app
app.run()