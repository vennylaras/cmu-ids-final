import streamlit as st
import plotly.express as px
import missingno

from utils.dataloader import load_mvp_data
from utils.constants import *

def app():
    df_filtered, df_unfiltered = load_mvp_data()

    st.markdown('# Dataset')
    st.markdown('## Data Sources')

    st.markdown('#### World Happiness Report')
    st.markdown(f"""
        The World Happiness Report {cite("base")} is a publication of the United Nations Sustainable Development Solutions Network. 
        This report contains a national happiness index for each country every year, and other key metrics noted below, based on respondent ratings of their own lives.
        Note that the happiness score, is also a result of a poll question in the Gallup World Poll survey, and is NOT computed using the other key metrics collected using the survey.""")
    # st.dataframe(df_unfiltered)
    with st.expander("Description of primary dataset columns"):
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

    st.markdown('#### Secondary Datasets')
    # TODO Explain secondary datasets
    st.markdown(f"""
        - **Human Development Index** {cite("hdi")}: Human development index (HDI) is a composite index measuring average achievement in three basic dimensions of human development
            which are long and healthly life, knowledge, and decent standard of living. This data is obtained from the United Nations Development Programme (UNDP) Human Development Report.
        - **Gender Development Index** {cite("gdi")}: Gender Development Index (GDI) is the ratio of female versus male HDI values, also obtained from UNDP Human Development Report.
        - **Mental Health Admissions** {cite("mhadm")}: The number of mental hospital admissions per 100,000 population per country, obtained from WHO.
        - **Mental Health Facilities** {cite("mhfac")}: The number of mental health outpatients facilities per 100,000 population per country, obtained from World Health Organization (WHO).
        - **Suicide Rates** {cite("suic")}: Suicide rate per 100,000 population per country, obtained from WHO.
        - **Sunshine Hours** {cite("sun")}: Monthly average sunshine hours per country in the year of 2019, obtained from Wikipedia.
        - **UN Geoscheme** {cite("geo")}: The United Nations (UN) geoscheme is a system which divides countries and territories into regions and subregions.
        """)

    # TODO Add 4C: Completeness, Coherence, Correctness, aCcountability
    st.markdown("""
        ---
        ##  Data Quality
        Here we analyze our datasets through the lens of the 4Cs of data quality. 

        #### Completeness: 
        The base dataset containing both countries and years as columns on initial exploration has deceptively low NULL values, 
        however, on pivoting the dataset by country, a lot of NULLs are seen concentrated for the initial years in which the Gallup World Poll started.
        This is likely because they slowly expanded their operations to cover the globe as they went on. As such, we remove the few years that have sparse data and choose to work with the decade 2010-2019, 
        as these years have densely populated and largely complete data for about 150 of the total 195 countries of the world.

        Please see the _Analysis of Missing Data_ section below for more details.

        #### Correctness:
        Happiness is a subjective topic. The World Gallup Poll is the largest operation across the globe that tries to objectively survey its participants based on binary poll questions and averages them through the responses obtained from a country. 
        Furthermore, all our secondary datasets with the exception of sunshine hours are obtained from the official websites of the World Health Organization or the United Nations, which are the best sources of this information to the best of our knowledge.
        That said, there might be unintentional biases in the selection of the people who take the surveys as we see in the case study for India, but there isn't a good way to verify that without another survey of similar scale. 
          
        #### Coherence:     
        From the various correlations presented in the Analysis and Case Studies tab, the data tells us a consistent and intuitive story. 
        For instance, the data supports intuition that people in developed countries care more about softer factors like social support, generosity, and so on, while in developing countries, 
        these might be first world problems as people try to make ends meet, and their happiness correlates more to their basic needs like money and health being fulfilled.

        #### aCcountability: 
        All datasets used are from official and well-known sources. 
        For instance, as noted in the _Statistical Analysis of Numerical Metrics_ section below, we notice that statistical metrics over the years have remained fairly stable over the past decade. 
        Links to all datasets are available in on the references page. 
    """)

    st.markdown("""
        ---
        ## Data Exploration
        #### Analysis of Missing Data
        We first look at our whole table to check if there is any jarring nullity that warrants dropping some columns.
    """)

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

        Most notably, the min, max, mean, standard deviation of the Happiness Index scores have remained 
        fairly stable across the globe in the past decade, which instills confindence in the accountability and systematic consistency of GWP surveys over the year.

        Therefore, the only filtering we do on our base dataset is removing years with high nulls, as noted above.
    """)

    # def stats(df): 
    #     df = df.describe().drop(columns=[YEAR])
    #     return df

    # st.dataframe(stats(df_unfiltered))

    columns = df_filtered.columns.tolist()
    columns.remove(YEAR)
    columns.remove(COUNTRY)
    column = st.selectbox('Attribute', columns)

    fig = px.box(df_filtered, x=YEAR, y=column, hover_data=[COUNTRY], points="all")
    st.plotly_chart(fig)
    

