# CMU: Interactive Data Science (05-839) Final Project
* **Streamlit URL**: [Happiness, Around the World](https://share.streamlit.io/vennylaras/cmu-ids-final/main/app.py)
* **Video URL**: [YouTube](https://www.youtube.com/watch?v=It_cIs9a2l4)
* **Team members**:
  * apsharma@andrew.cmu.edu
  * pvarshne@andrew.cmu.edu
  * vayudian@andrew.cmu.edu
  * yerinh@andrew.cmu.edu


## Abstract
The World Happiness Report is a publication of the Sustainable Development Solutions Network. It contains data from the Gallup World Poll, based on answers given by survey respondents. The survey asks respondents to think of a ladder, with the best possible life for them being a 10, and the worst possible life being a 0. They are then asked to rate their current lives on that scale. 6 factors are estimated to contribute to making life evaluations higher in any country compared to "Dystopia" - a hypothetical country that has values equal to the world's lowest national averages for each of the factors. The factors are:
* GDP
* Life expectancy
* Generosity
* Social support
* Freedom
* Corruption

## Overview
The Streamlit application contains the following tabs:
* Home - a high-level description of the project and the key questions we are trying to answer
* Dataset - insights into the data sources and an initial statistical analysis of the data
* Analysis - exploratory data analysis with interactive visualizations to analyze correlations between different factors. We also look at secondary datasets to draw more inferences about correlations between various factors
* Case studies - deep dive into other factors that could contribute to trends in happiness scores, specifically with respect to 3 countries, Yemen, Venezuela, and India 
* Prediction - using linear regression to predict the happiness score given the 6 factors, and the country most similar to that score
* References

## Contributions
- Implemented and deployed a Streamlit application with interactive components, incorporating data preprocessing, initial statistical analysis and exploratory data analysis
- Performed correlation analysis for various factors in the primary dataset, as well as joined with other datasets like Mental Health, Suicide Rates, etc. along with visualizations and controls for users to interactively filter and view data as they like
- Explored 3 countries and their happiness score trends over the years, and proposed hypotheses relating their geopolitical mood with the happiness scores during tumultous periods
- Developed a machine learning model that can predict the happiness score based on relevant factors and further predict the country that is nearest to the predicted score based on euclidean distance
