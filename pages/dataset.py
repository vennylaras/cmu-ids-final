import streamlit as st
import plotly.express as px
import missingno

from utils.dataloader import load_mvp_data
from utils.constants import *

def app():
    df_filtered, df_unfiltered = load_mvp_data()

    

    st.markdown('# Dataset')

    st.markdown('### Data Source')

    st.markdown('##### World Happiness Report')
    st.write("""
        The World Happiness Report is a publication of the United Nations Sustainable Development Solutions Network. 
        This report contains a national happiness index for each country every year, and other key metrics noted below, based on respondent ratings of their own lives.
        Note that the happiness score, is also a result of a poll question in the Gallup World Poll survey, and is NOT computed using the other key metrics collected using the survey.""")
    # st.dataframe(df_unfiltered)
    st.markdown(f"""
        Here is a brief description of  these columns collected from the Gallup World Poll (GWP): 
        - **{HAPPINESS_SCORE}:** {column_descriptions[HAPPINESS_SCORE]}
        - **{LOG_GDP}:** {column_descriptions[LOG_GDP]}
        - **{SOCIAL_SUPPORT}:** {column_descriptions[SOCIAL_SUPPORT]}
        - **{LIFE_EXPECTANCY}:** {column_descriptions[LIFE_EXPECTANCY]}
        - **{FREEDOM}:** {column_descriptions[FREEDOM]}
        - **{GENEROSITY}:** {column_descriptions[GENEROSITY]}
        - **{CORRUPTION}:** {column_descriptions[CORRUPTION]}
        - **{POSITIVE_AFFECT}:** {column_descriptions[POSITIVE_AFFECT]}
        - **{NEGATIVE_AFFECT}:** {column_descriptions[NEGATIVE_AFFECT]}
        The affect measures lie between 0 and 1.
        """)

    st.markdown('##### Secondary Datasets')
    # TODO Explain secondary datasets
    st.write('TODO')

    # TODO Add 4C: Completeness, Coherence, Correctness, aCcountability
    st.markdown('###  Data Quality')
    st.write('TODO: 4C')

    st.markdown('###  Initial Exploration')
    st.markdown('##### Analysis of Missing Data')
    st.write('We first look at our whole table to check if there is any jarring nullity that warrants dropping some columns.')

    def preview_nulls(df):
        # generate preview of entries with null values
        if df.isnull().any(axis=None):
            fig = missingno.matrix(df).figure
            return fig

    st.pyplot(preview_nulls(df_unfiltered))

    st.write("""
        While the overall data seems reliably populated from the above chart, we note that surveys might not be 
        conducted or complete in some countries in some years.
    """)

    st.write("""As such, since the main metric we want to study is the happiness index, given by the Happiness Score score, 
        we further check the nullity over years of the happiness index for each country, by pivoting our data appropriately 
        to have countries as rows, years as columns, and values as the happiness index
    """)

    happiness_df = df_unfiltered.pivot_table(index=COUNTRY, columns=YEAR, values=HAPPINESS_SCORE).reset_index()
    happiness_df_years_filtered = df_filtered.pivot_table(index=COUNTRY, columns=YEAR, values=HAPPINESS_SCORE).reset_index()
    st.pyplot(preview_nulls(happiness_df))

    st.write("""
        We find that the happiness report survey data is **extremely sparse for 2005 - 2009, and 2020**. Therefore, we make a 
        conscious decision of removing these years from all our analysis and **restrict to a decade worth** of more reliable 
        data found in the 2010 to 2019 survey results.

        Considering that a country might consistently score low or high on the happiness scale, this also drives a decision 
        to make sure we only present aggregate metrics over years for a **subset of countries that have data for all years**, 
        as comparing 2019 overall averages with 2020 averages given 2020 doesn't have a subset of low scoring countries 
        would be fallacious. 

        Therefore, all **global averages mentioned in the report automatically refer to this subset**. However, when looking at individual 
        countries in multiples of line plots, the disconnections between the lines in the plots signify the unavailability of data 
        instead.
    """)

    col1, col2 = st.columns([3, 3])
    with col1:
        st.metric("Total Countries (2005-2020)", len(happiness_df))
    with col2: 
        st.metric("Total Countries (2010-2019)", len(happiness_df_years_filtered))
    col1, col2 = st.columns([3, 3])
    with col1:
        st.metric("Good* Countries (2005-2020)", len(happiness_df.dropna()))
    with col2: 
        st.metric("Good* Countries (2010-2019)", len(happiness_df_years_filtered.dropna()))

    st.write("*Good countries refer to the subset of countries that have data for ALL the years mentioned, i.e., no nulls.")
    st.markdown("""
        --- 
        #### Statistical Analysis of Numerical Metrics
    """)
    st.write("""
        From a quick statistical analysis of the base dataset (see below), we do not find any funky outliers that would warrant removing. 
        Therefore, the only filtering we do on our base dataset is removing years with high nulls, as noted above.
    """)

    # def stats(df): 
    #     df = df.describe().drop(columns=[YEAR])
    #     return df

    # st.dataframe(stats(df_unfiltered))

    columns = df_unfiltered.columns.tolist()
    columns.remove(YEAR)
    columns.remove(COUNTRY)
    column = st.selectbox('Attribute', columns)

    fig = px.box(df_unfiltered, x=YEAR, y=column, hover_data=[COUNTRY], points="all")
    st.plotly_chart(fig)
    

