import streamlit as st
import plotly.express as px
import missingno

from utils.dataloader import load_mvp_data

def app():
    _, df_happy = load_mvp_data()

    st.title('Dataset')

    st.markdown('### Data Source')

    st.markdown('##### World Happiness Report')
    st.write("""
        The World Happiness Report is a publication of the United Nations Sustainable Development Solutions Network. 
        This report contains articles and rankings of national happiness, based on respondent ratings of their own lives,
        which the report also correlates with various quality of life factors.""")
    # st.dataframe(df_happy)
    st.markdown("""
        Here is a brief description of  these columns collected from the Gallup World Poll (GWP): 
        - **Life Ladder:** The average happiness index
        - **Log GDP Per Capita:** A country's per capita GDP on log-scale
        - **Social Support:** Social support is the national average of the binary responses (either 0 or 1) to the Gallup World Poll (GWP) question “If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?”
        - **Healthy Life Expectancy at Birth:** The expected life expectancy of an average human-being at birth
        - **Generosity:** Generosity is the residual of regressing the national average of GWP responses to the question “Have you donated money to a charity in the past month?” on GDP per capita.
        - **Perceptions of Corruption:** It's the average of binary answers to two GWP questions: “Is corruption widespread throughout the government or not?” and “Is corruption widespread within businesses or not?” (Note: Where data for government corruption are missing, the perception of business corruption is used as the overall corruption-perception measure.)
        - **Positive affect:** It comprises the average frequency of happiness, laughter and enjoyment on the previous day
        - **Negative affect:** It comprises the average frequency of worry, sadness and anger on the previous day. 
        The affect measures lie between 0 and 1.
        """)

    st.markdown('##### Secondary Datasets')
    # TODO Explain secondary datasets
    st.write('TODO')


    st.markdown("[1] https://worldhappiness.report/")
    st.markdown("[2] http://hdr.undp.org/en/indicators/137506") # HDI
    st.markdown("[3] https://worldpopulationreview.com/country-rankings/hdi-by-country") # also HDI, which one are we using??
    st.markdown("[4] http://hdr.undp.org/en/indicators/137906") # gender development index
    st.markdown("[4] https://www.who.int/data/gho/data/themes/mental-health/suicide-rates") # suicide
    st.markdown("[6] https://www.who.int/data/gho/data/indicators/indicator-details/GHO/mental-health-outpatient-facilities-(per-100-000)") # mental health facilities
    st.markdown("[7] https://www.who.int/data/gho/data/indicators/indicator-details/GHO/mental-hospital-admissions-(per-100-000)") # mental health admissions
    st.markdown("[8] https://data.world/makeovermonday/2019w44") # sunshine
    st.markdown("[9] https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme") # countries and regions
    # TODO add more that we've used



    # TODO Add 4C: Completeness, Coherence, Correctness, aCcountability
    st.text("")
    st.markdown('###  Data Quality')
    st.write('TODO: 4C')



    
    st.text("")
    st.markdown('###  Initial Exploration')
    st.markdown('##### Analysis of Missing Data')
    st.write('We first look at our whole table to check if there is any jarring nullity that warrants dropping some columns.')

    def preview_nulls(df):
        # generate preview of entries with null values
        if df.isnull().any(axis=None):
            fig = missingno.matrix(df).figure
            return fig

    st.pyplot(preview_nulls(df_happy))

    st.write("""
        While the overall data seems reliably populated from the above chart, we note that surveys might not be 
        conducted or complete in some countries in some years.
    """)

    st.write("""As such, since the main metric we want to study is the happiness index, given by the Life Ladder score, 
        we further check the nullity over years of the happiness index for each country, by pivoting our data appropriately 
        to have countries as rows, years as columns, and values as the happiness index
    """)

    happiness_df = df_happy.pivot_table(index="Country name", columns="year", values="Life Ladder").reset_index()
    st.pyplot(preview_nulls(happiness_df))

    st.write("""
        We find that the happiness report survey data is extremely sparse for 2005 - 2009, and 2020. Therefore, we make a 
        conscious decision of removing these years from all our analysis and restrict to a decade worth of more reliable 
        data found in the 2010 to 2019 survey results.

        Considering that a country might consistently score low or high on the happiness scale, this also drives a decision 
        to make sure we only present aggregate metrics over years for a subset of countries that have data for all years, 
        as comparing 2019 overall averages with 2020 averages given 2020 doesn't have a subset of low scoring countries 
        would be fallacious. 

        Therefore, all global averages mentioned in the report automatically refer to a subset. When looking at individual 
        countries in multiples of line plots, the disconnections between the lines will signify the unavailability of data 
        instead.
    """)

    st.text("")
    st.markdown('##### Statistical Analysis of Numerical Metrics')
    st.write("""
        Next, we look at a quick statistical analysis of our numerical columns to see if anything stands out as an 
        outlier and might be worth removing.
    """)

    def stats(df): 
        df = df.describe().drop(columns=["year"])
        return df

    st.dataframe(stats(df_happy))


    columns = df_happy.columns.tolist()
    columns.remove('year')
    columns.remove('Country name')
    column = st.selectbox('Attribute', columns)

    fig = px.box(df_happy, x="year", y=column, hover_data=["Country name"], points="all")
    st.plotly_chart(fig)
    

