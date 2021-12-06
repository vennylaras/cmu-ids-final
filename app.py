import streamlit as st

# Custom imports 
from utils.multipage import MultiPage
from pages import home, dataset, analysis, case, references, linear_regression

# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("Home", home.app)
app.add_page("Dataset", dataset.app)
app.add_page("Analysis", analysis.app)
app.add_page("Case Studies", case.app)
app.add_page("Prediction", linear_regression.app)
app.add_page("References", references.app)

# The main app
app.run()
