import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import home, exploration

# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("Home", home.app)
app.add_page("Data Exploration", exploration.app)

# The main app
app.run()