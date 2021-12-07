import numpy as np
import streamlit as st
import plotly.express as px

from utils.dataloader import load_data
from utils.constants import *

def world_map(df):
    df_sort_year = df.sort_values(by=[YEAR])
    fig = px.choropleth(
        data_frame=df_sort_year, 
        locations=COUNTRY, 
        locationmode="country names",
        # hover_name=HAPPINESS_SCORE, 
        hover_data={
            YEAR: True, 
            COUNTRY: True, 
            HAPPINESS_SCORE: ":.2f"
        },
        color=HAPPINESS_SCORE,
        animation_frame=YEAR,
        color_continuous_scale="RdYlGn",
        range_color=(2.5, 7.5)
    )
    # fig.update_layout(geo=dict(bgcolor='rgba(100,100,100,0)'))
    fig.update_layout(
    # title_text='2014 Global GDP',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular', 
            fitbounds="locations"
        ),
    )
    return fig

@st.cache()
def filter_df_by_continent(df, df_pivot, region): 
    return df[df[REGION] == region], df_pivot[df_pivot[REGION] == region]

def app():
    df, _, df_country, df_pivot, df_hdi, df_gender, df_mh_adm, df_mh_fac, df_suicide, df_sunshine = load_data()

    continent = st.sidebar.radio('Continent', ["Whole World"] + REGION_LIST)
    if continent != "Whole World":
        df, df_pivot = filter_df_by_continent(df, df_pivot, continent)

    st.markdown('# Analysis')
    if continent == "Whole World":
        st.markdown("""### Worldwide Happiness""")
    else: 
        st.markdown(f"""### Happiness in {continent}""")

    col1, col2 = st.columns([3, 5])

    most19_country = df_pivot.set_index(COUNTRY).select_dtypes(np.number).idxmax()[2019]
    most19_score = df_pivot[df_pivot[COUNTRY] == most19_country][2019].values[0]
    most19_text = "<div style='color:grey;'>The Happiest Country in 2019</div>\
        <div style='font-size: 36px; color:green; font-weight:bold;'>%s</div>\
        <div style='font-size: 20px;'>Index: %0.2f</div>" % (most19_country, most19_score)
    col1.markdown(most19_text, unsafe_allow_html=True)

    least19_country = df_pivot.set_index(COUNTRY).select_dtypes(np.number).idxmin()[2019]
    least19_score = df_pivot[df_pivot[COUNTRY] == least19_country][2019].values[0]
    least19_text = "<div style='color:grey;'>The Least Happy Country in 2019</div>\
        <div style='font-size: 36px; color:firebrick; font-weight:bold;'>%s</div>\
        <div style='font-size: 20px;'>Index: %0.2f</div>" % (least19_country, least19_score)
    col2.markdown(least19_text, unsafe_allow_html=True)

    col1.write('\n')
    col2.write('\n')

    most_avg_country = df_pivot.set_index(COUNTRY).mean(axis=1).idxmax()
    most_avg_score = df_pivot.set_index(COUNTRY).mean(axis=1).max()
    most_avg_text = "<div style='color:grey;'>The Happiest Country in 2010-2019</div>\
        <div style='font-size: 36px; color:green; font-weight:bold;'>%s</div>\
        <div style='font-size: 20px;'>Average Index: %0.2f</div>" % (most_avg_country, most_avg_score)
    col1.markdown(most_avg_text, unsafe_allow_html=True)

    least_avg_country = df_pivot.set_index(COUNTRY).mean(axis=1).idxmin()
    least_avg_score = df_pivot.set_index(COUNTRY).mean(axis=1).min()
    least_avg_text = "<div style='color:grey;'>The Least Happy Country in 2010-2019</div>\
        <div style='font-size: 36px; color:firebrick; font-weight:bold;'>%s</div>\
        <div style='font-size: 20px;'>Average Index: %0.2f</div>" % (least_avg_country, least_avg_score)
    col2.markdown(least_avg_text, unsafe_allow_html=True)

    st.write('\n')

    writeups_map = {
        "Whole World" : """The map below shows the happiness index for each country throughout the year 2010 until 2019. 
            From the map we can see that countries in Europe, America, and Australia generally have higher happiness index 
            than countries in Asia and Africa.""",
        "Africa" : """The map below shows the happiness index for each country throughout the year 2010 until 2019. 
            From the map we can see that countries in Africa generally have low happiness index. In Eastern Africa,
            Zimbabwe's happiness index score gradually decreased until it became the least happiest country in Africa
            in the year 2019.""",
        "Americas" : """The map below shows the happiness index for each country throughout the year 2010 until 2019. 
            From the map we can see that countries in Americas generally have high happiness index, with Canada
            consistently having particularly high happiness index throughout the decade.""",
        "Asia" : """The map below shows the happiness index for each country throughout the year 2010 until 2019. 
            From the map we can see that countries in East and Central Asia generally have moderately high happiness index.
            Countries in Southeast Asia also have moderately high score except for Cambodia and Myanmar. In West Asia,
            Saudi Arabia, United Arab Emirates, and Israel consistently have high happines index. In South Asia,
            we can see Afghanistan and India have gradually decreasing score in the past few years.""",
        "Europe" : """The map below shows the happiness index for each country throughout the year 2010 until 2019. 
            From the map we can see that countries in Northern Europe generally have higher happiness index,
            followed by Western Europe.""",
        "Oceania" : """The map below shows the happiness index for each country throughout the year 2010 until 2019. 
            The only available data for the region Oceania is Australia and New Zealand, we can see that noth countries 
            have high happiness index."""
    }
    st.markdown(writeups_map[continent])

    st.plotly_chart(world_map(df))
    st.markdown("""
        ---
        ### Happiness Index by Region
    """)   


    st.markdown(f"""
        Below are the happiness index trend for each region. 
        To get the region (continent) and sub-region for each country, we joined the happiness index dataset with 
        the United Nations (UN) geoscheme data {cite("geo")}. There are several countries which have inconsistent names so we manually 
        changed them before joining. Furthermore, there are five countries/territories present in the happiness dataset which 
        are not present in the UN dataset, so we added them manually to their respective regions.
    """)

    def plot_line_chart(region): 
        df_reg = df[df['sub-subregion'] == region]
        df_reg = df_reg.pivot(index=YEAR, columns=COUNTRY, values=HAPPINESS_SCORE)
        fig = px.line(df_reg, range_y=(2.5,8), width=340, height=280)
        fig.update_layout(
            showlegend=False,
            margin=dict(l=5, r=5, t=30, b=20),
            title={
                'text': region,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis_title=None,
            yaxis_title=None
        )

        return fig


    if continent == "Whole World":
        st.write("""
            Overall, we observed that countries in Europe, Americas, and Oceania have a relatively higher happiness score
            compared to countries in Asia and Africa. The happiness index for those 3 regions throughout the years are also more
            stable than Asia and Africa.
        """)
        # option2 = st.selectbox('Select a continent to see the happiness index by countries', REGION_LIST)
    # else:
    #     option2 = continent
    
    df_subregion = df.groupby(by=[YEAR, REGION, 'sub-subregion']).mean().reset_index()

    def plot_bar_chart(df) :
        fig = px.bar(df_subregion, x="sub-subregion", y=HAPPINESS_SCORE, color=REGION, 
            animation_frame=YEAR, range_y=(2,8), category_orders={REGION: REGION_LIST})

        fig.update_layout(
            xaxis_title=None
        )

        fig['layout']['updatemenus'][0]['pad'] = dict(r=10, t=110)
        fig['layout']['sliders'][0]['pad'] = dict(r=10, t=110)

        return fig


    st.plotly_chart(plot_bar_chart(df))

    # if option2 == 'Asia':
    # # with st.expander("Asia"):
    #     st.write('Countries in Asia generally do not have significantly high or significantly low happiness index.\
    #     In its subregion, countries in South Asia have a lower happiness index compared to other subregions in Asia.')

    #     col1, col2 = st.columns(2)
    #     col1.plotly_chart(plot_line_chart("Central Asia"))
    #     col1.plotly_chart(plot_line_chart("Eastern Asia"))
    #     col1.plotly_chart(plot_line_chart("South-eastern Asia"))
    #     col2.plotly_chart(plot_line_chart("Southern Asia"))
    #     col2.plotly_chart(plot_line_chart("Western Asia"))

    
    # if option2 == 'Oceania':
    # # with st.expander("Oceania"):
    #     st.write('For Oceania, we only have data from two countries and both of them are in the Australia & New Zealand subregion \
    #     and both countries have high happiness index.')

    #     st.plotly_chart(plot_line_chart("Australia and New Zealand"))
        

    # elif option2 == 'Europe':
    # # with st.expander("Europe"):
    #     st.write('Countries in Europe have an overall high happiness index score.\
    #     Countries in the subregion West Europe have highest average happiness index compared to other regions with all countries having \
    #     happiness index score greater than 6 throughout the years. \
    #     Countries in Northern Europe also have stable happiness index ranging from 5 to 8. \
    #     A country from this subregion, Finland has the highest happiness index out of all countries in the world for the year 2016-2019.')

    #     col1, col2 = st.columns(2)
    #     col1.plotly_chart(plot_line_chart("Eastern Europe"))

    #     fig = plot_line_chart("Northern Europe")
    #     # score = df[(df[COUNTRY] == 'Finland') & (df[YEAR] == 2018)].values[0]
    #     # fig.add_annotation(x=2018, y=score, text='Finland', showarrow=True)
    #     col1.plotly_chart(fig)

    #     col2.plotly_chart(plot_line_chart("Southern Europe"))
    #     col2.plotly_chart(plot_line_chart("Western Europe"))

    # elif option2 == 'Americas':
    # # with st.expander("America"):
    #     st.write('The subregion North America have a significantly high happiness index while Central and South America have a moderately high happiness index.\
    #     On the other hand, countries in the Carribean subregion have a moderately low happiness index.')

    #     col1, col2 = st.columns(2)
    #     col1.plotly_chart(plot_line_chart("Northern America"))
    #     col1.plotly_chart(plot_line_chart("Central America"))
    #     col2.plotly_chart(plot_line_chart("South America"))
    #     col2.plotly_chart(plot_line_chart("Caribbean"))
        

    # elif option2 == 'Africa':
    # # with st.expander("Africa"):
    #     st.write('Generally, we can see that countries in Africa have averagely lower happiness index compared to other continents, \
    #     with almost all countries throughout the years having happiness score less than 6.\
    #     The index also seems to fluctuate a lot through out the years.')

    #     col1, col2 = st.columns(2)
    #     col1.plotly_chart(plot_line_chart("Northern Africa"))
    #     col1.plotly_chart(plot_line_chart("Eastern Africa"))
    #     col1.plotly_chart(plot_line_chart("Middle Africa"))
    #     col2.plotly_chart(plot_line_chart("Southern Africa"))
    #     col2.plotly_chart(plot_line_chart("Western Africa"))
        
    st.markdown("---")
    st.markdown('### What Metrics Correlate with Happiness?')

    writeups_corr_most = {
        'Whole World': 'GDP, Life Expectancy, and Social Support',
        'Africa': 'GDP, Life Expectancy, and Social Support',
        'Americas' : 'GDP, Life Expectancy, and Social Support',
        'Asia' : 'GDP, Life Expectancy, and Social Support',
        'Europe' : 'GDP and Freedom to make life choices',
        'Oceania' : 'Freedom to make life choices, Generosity, and Social Support'
    }

    st.markdown(f"""Looking at the pairwise correlations of all metrics with each other for all countries for the decade 2010-2019,
        we find that {writeups_corr_most[continent]} are **on average most heavily correlated with the Happiness Score.**""")

    fig = px.imshow(df.corr().iloc[1:-1,1:-1], color_continuous_scale="RdBu")
    st.plotly_chart(fig)

    st.markdown(f"""
        **However, we hypothesize that these correlations might vary significantly with the standard of living in different 
        countries and the general ability of people to fight for survival versus being able to take a safe and healthy 
        environment as a given.**

        To test this hypothesis, we turn to looking at **Human Development Index** as a way to categorize countries.

        The Human Development Index (HDI) is compiled by the United Nations Development Programme (UNDP) for 189 countries on 
        an annual basis {cite("hdi")}. The index considers the health, education and income in a given country to provide a measure of 
        human development which is comparable between countries and over time. 
    """)

    st.markdown(f"""
        HDI is divided into four tiers {cite("hdiimf")}: very high human development (above or equal to 0.8), high human development
        (0.7 to 0.79), medium human development (0.55 to 0.7), and low human development (below 0.55).
        The International Monetary Fund (IMF) categorizes "developed countries" have an HDI score of 0.8 or above 
        (in the very high human development tier). These countries have stable governments, widespread education, 
        healthcare, high life expectancies, and growing, powerful economies.
    """)

    # hdi_option = st.radio('Select HDI category', ['Developed Countries', 'Developing Countries'])
    writeups_developed = {
        "Whole World" : """
            For developed countries with high Human Development Indices, happiness is positively correlated to many factors like 
            social support, freedom to make life choices, generosity, etc. Further, perceptions of corruption is highly negatively 
            correlated with happiness index, showing that people care about politics, who the country's leaders are, and are aware 
            enough to know what might be affecting their access to peace and standard of living on a daily basis.

            This shows that when basic needs like economy (as measured by GDP) and health (as measured by life expectancy) are in good shape, 
            people start caring about a well-rounded life and factors like generosity, social support systems, political influences, and 
            other nuanced factors to happiness.
        """,
        "Africa" : """
            In Africa, only one country fell into the category of Developed country when the threshold is equal to 0.8, Mauritius. 
            In this country, happiness is positively correlated to many factors such as GDP, social support, helathy life expectancy at birth, 
            and freedom to make life choices. It correlates most strongly with both GDP and healthy life expectancy. Further, generosity and 
            perceptions of corruption is negatively correlated with happiness score.
        """,
        "Americas" : """
            For developed countries with high Human Development Indices in Americas, happiness is slightly positively correlated to many factors like 
            social support, freedom to make life choices, generosity, etc. Further, perceptions of corruption is highly negatively 
            correlated with happiness index, showing that people care about politics, who the country's leaders are, and are aware 
            enough to know what might be affecting their access to peace and standard of living on a daily basis.
        """,
        "Asia" : """
            For developed countries with high Human Development Indices in Asia, happiness is positively correlated to many features with the strongest
            correlation being GDP, social support, and generosity. Meanwhile, healthy life expectancy at birth and freedom to make lide choices were only
            slightly positively correlated.  Further, perceptions of corruption is slightly negatively correlated with happiness index.
        """,
        "Europe" : """
            For developed countries with high Human Development Indices in Europe, happiness is strongly positively correlated to many features with 
            the strongest correlation being GDP and freedom to make life choices. Further, perceptions of corruption is strongly negatively correlated 
            with happiness score, showing that people care about politics, who the country's leaders are, and are aware  enough to know what might 
            be affecting their access to peace and standard of living on a daily basis.
        """,
        "Oceania" : """
            All countries is Oceania in the available data is categorized as developed country so the heatmap below is identical to the heatmap above.
        """
    }

    writeups_developing = {
        "Whole World" : """
            Through the below heatmap, we see that as we move towards developing countries with lower Human Development Indices, 
            happiness is positively only correlated to per capita GDP and Life Expectancy at birth, i.e., the economy and health 
            systems play the most significant roles as people's happiness depends on their ability to get by and make a living 
            and work towards a respectable standard of living.

            Things like generosity, or freedom to make life choices are effectively first world problems that don't really factor 
            into general happiness for most people.
        """,
        "Africa" : """
            Through the below heatmap, we see that as we move towards developing countries in Africa with lower Human Development Indices, 
            happiness is only slightly positively correlated with GDP and social support. 
        """,
        "Americas" : """
            Through the below heatmap,  we see that as we move towards developing countries with lower Human Development Indices in Americas,
            the factors that were positively correlated with happiness index for developed countries are also positively correlated 
            in developing countries, more significantly. Further, we can see that generosity is strongly  negatively correlated 
            and in perceptions of corruption is only slightly negatively correlated.
        """,
        "Asia" : """
            Through the below heatmap,  we see that as we move towards developing countries with lower Human Development Indices in Asia,
            in contrast to the developed countries, the factors that is the most positively correlated with happiness score are healthy life 
            expectancy at birth, followed by social support. Also contrary to developed countries, generosity seem to have a negative correlation
            with happiness index and the negative correlation to perceptions of corruption is stronger.
        """,
        "Europe" : """
            Through the below heatmap,  we see that as we move towards developing countries with lower Human Development Indices in Europe,
            contrary to the developed countries, there are no attributes with strong positive correlation.
        """,
        "Oceania" : """"N/A"""
    }

    threshold = st.slider('HDI Score Threshold', 0.5, 0.8, 0.8)

    developed_countries = list(df_hdi[df_hdi["hdi2019"] >= threshold][COUNTRY])
    developing_countries = list(df_hdi[df_hdi["hdi2019"] < threshold][COUNTRY])
    developed_region_df = df[df[COUNTRY].isin(developed_countries)]
    developing_region_df = df[df[COUNTRY].isin(developing_countries)]
    
    col1, col2 = st.columns([1, 1])
    with col1: 
        if not developed_region_df.empty:
            with st.expander("List of Developed Countries"):
                st.write(", ".join(developed_region_df[COUNTRY].unique().tolist()))
        else: 
            st.markdown(f"""No developed countries found for HDI threshold {threshold} in {continent}.""")
    
    with col2: 
        if not developing_region_df.empty:
            with st.expander("List of Developing Countries"):
                st.write(", ".join(developing_region_df[COUNTRY].unique().tolist()))
        else: 
            st.markdown(f"""No developing countries found for HDI threshold {threshold} in {continent}.""")  
    
    if not developed_region_df.empty:
        st.markdown("""**Developed Countries**""")
        st.markdown(writeups_developed[continent])
        fig = px.imshow(developed_region_df.corr().iloc[1:-1,1:-1], color_continuous_scale="RdBu", width=680)
        st.plotly_chart(fig)
  
    if not developing_region_df.empty:
        st.markdown("""**Developing Countries**""")
        st.markdown(writeups_developing[continent])
        fig = px.imshow(developing_region_df.corr().iloc[1:-1,1:-1], color_continuous_scale="RdBu", width=680)
        st.plotly_chart(fig)
        
    st.markdown("---")
    st.markdown('### Quality of Life Factors')
    st.write('In this section, we explore the correlation between happiness index and several quality of life factors presented in the original report.\
    The first graph below describes yearly change of the selected feature in each continent given in our main happiness dataset, and\
    the second graph shows the correlation between each feature and the happiness score for each year.')

    option = st.selectbox('Quality of Life Factors', [LOG_GDP, SOCIAL_SUPPORT, LIFE_EXPECTANCY, FREEDOM, GENEROSITY, CORRUPTION])

    writeups_vs_year_1 = {
        SOCIAL_SUPPORT: """This graph shows the yearly change in social support that was available in each continent in the past years. 
            There is small change in social support of America, Europe, and Oceania while the social support in Asia and Africa has decreased.
            Especially around 2014, both Asia and Africa reach the lowest social support.""", 
        LIFE_EXPECTANCY: """In general, healthy life expectancy at birth increases in all continents. Especially, the value in Africa increases the fastest.""", 
        LOG_GDP: """In general, log GDP per capita slowly increases in all continents.""", 
        GENEROSITY: """Generosity fluctuates and slowly decreases by 2018, however it slightly increases in all continents after 2018.""", 
        FREEDOM: """Freedom to make a life choices increase in all continents; however, in 2012, this feature reaches the lowest point in Asia and Africa""", 
        CORRUPTION: """Except for Asia and Africa, this feature slightly increases in entire continents.
            We can also observe that the region Oceania have a significantly lower perceptions of corruption compared to other regions."""
    }

    writeups_vs_year_2 = {
        SOCIAL_SUPPORT: """We can see a positive correlation between happiness index and social support, 
            with Europe, Americas, and Oceania leading in the top right quadrant, Asia spread out in the middle,
            and Africa in the lower quadrant.""", 
        LIFE_EXPECTANCY: """There is a positive correlation between healthy life expectancy and happiness index. 
            All four continents beside Africa occupy the top right quadrant while Africa in the lower left,
            which suggested that the lower health life expectancy rate in Africa is one of the contributing factors
            of why happiness index scores are generally low in African countries.""", 
        LOG_GDP: """There is a positive correlation between Happiness Index and GDP,
            the higher the GDP, the likelier it is to have a high happiness index score.
            Countries in Europe occupy the top right quadrant and are quite stable throughout the years. 
            African countries, on the other hand, occupy the lower left of the quadrant.
            For example, in 2019 the country with the highest GDP, Luxembourg, has a relatively high happiness index at 7.4,
            while the country with lowest GDP, Malawi, has a relatively low happiness index at approximately 3.9.
            Just like the happiness score, we can see that countries in Europe, Americas, and Ocenia 
            have less fluctuative GDP per capita throughout the years compared to countries in Africa and Asia.
            This might be because most countries in those three regions are developed countries while countries in
            Asia and Africa are developing countries.""", 
        GENEROSITY: """Overall, it seems like there is no correlation between happiness index and generosity.
            Focusing on the region Europe, we can see a slightly positive correlation between happiness index and generosity.
            However, when we look at other regions, there seem to be no correlation. 
            Especially if we look at Asia, which seem pretty scattered thouhout the plot.
            Throughout the decade, Asian countries are always the top country in terms of genersity score,
            but those countries do not have a high happiness index.""", 
        FREEDOM: """Throughout the years, the score for freedom to make life choices increased overall,
            with the trend of all countries moving towards the right side of the graph.
            There also seems to be a positive correlation between happiness index and freedom to make life choices.
            However, the difference between regions is not significant, with countries from all regions scattered throughout the plot.""", 
        CORRUPTION: """From the scatterplot we can see that there is a negative correlation between happiness index and perceptions of corruption,
            the lower the corruption score, the higher the happiness index is likely to be.
            There no clear difference for each region with all countries in each region scattered throughout the plot."""
    }    

    st.write(writeups_vs_year_1[option])
    df1 = df.dropna()
    df1 = df1.groupby([REGION, YEAR])[[option]].mean().reset_index()
    fig = px.line(df1, x=YEAR, y=option, color=REGION,
            category_orders={REGION: REGION_LIST})
    st.plotly_chart(fig)
    st.write(writeups_vs_year_2[option])

    # if option == LOG_GDP: 
    #     fig = px.scatter(df_pop_merged.dropna(), x=LOG_GDP, y=HAPPINESS_SCORE, animation_frame=YEAR, size='Log Population', size_max=10,
    #             color=REGION, hover_name=COUNTRY,
    #             category_orders={REGION: REGION_LIST})
    # else: 
    fig = px.scatter(df.dropna(), x=option, y=HAPPINESS_SCORE, animation_frame=YEAR, 
            color=REGION, hover_name=COUNTRY,
            category_orders={REGION: REGION_LIST})
    st.plotly_chart(fig)
    

    st.markdown("---")
    st.markdown("""
        ### Other Factors
        We now look at other factors outside of the quality life factors from the original World Happiness Report. 
        We analyzed several additional datasets to see if there is a correlation between these factors with happiness index.
    """)

    st.markdown(f"""
        ### Gender Disparity
        Next, we hypothesize that gender disparity might play a role in the happiness score of a country.
        Living in an equal society where everyone has the ability to choose the circumstances of their own lives,
        would likely lead to greater happiness. To test this hypothesis, we explore a dataset that comprises the
        Gender Development Index (GDI) for countries spanning multiple years {cite("gdi")}.
        GDI is defined as the ratio of female to male HDI values. Countries that have achieved some success in
        expanding capabilities for both men and women will have higher GDI. A country having a GDI less than 0.5
        indicates larger gender disparity.
    """)

    def plot_gender(happiness_df, gender):
        gender_19 = gender.rename(columns={2019.0:'2019'})[[COUNTRY, '2019']]
        gender_19[COUNTRY] = gender_19[COUNTRY].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index(COUNTRY), on=COUNTRY)

        merged = happiness_df_with_continent.merge(gender_19, on=COUNTRY, how='inner')
        merged = merged.rename(columns={'2019_x':HAPPINESS_SCORE,'2019_y':'GDI'})
        
        fig = px.scatter(merged.dropna(), x="GDI", y=HAPPINESS_SCORE, hover_name=COUNTRY, color=REGION,
                category_orders={REGION: REGION_LIST})

        return fig
    
    df_pivot19 = df_pivot.rename(columns={2019:'2019'})[[COUNTRY, '2019']]
    df_pivot19 = df_pivot19.rename(columns={COUNTRY:COUNTRY})
    df_pivot19[COUNTRY] = df_pivot19[COUNTRY].str.strip()

    st.plotly_chart(plot_gender(df_pivot19, df_gender))


    st.write("""
        We observe that countries having a higher GDI have a higher happiness score. This seems to align with what
        one would expect; a country having low gender disparity is more inclusive and diverse, and likely to have
        a higher happiness score.
    """)


    st.markdown('---') 
    st.markdown('### Mental Health')
    st.markdown('**Availability and Admissions**')

    st.markdown(f"""
        We are also interested in exploring whether a country's mental health services availability has any
        impact on the happiness score. For this, we explore a dataset published by the World Health Organization,
        that contains information on mental hospitals, mental health admissions, etc. for countries spanning across
        multiple years. For the purpose of this analysis, we consider the following two factors: Mental Health
        Admissions per 100,000 people {cite("mhadm")} and Mental Health Facilities per 100,000 people {cite("mhfac")}. 
        We consider data for the year 2019.
    """)

    def plot_mental_health(happiness_df, mental_health):
        mental_health = mental_health[['Location','FactValueNumeric', 'ParentLocation']]
        mental_health = mental_health.rename(columns={'Location': COUNTRY, 
                                                    'FactValueNumeric':'MentalHealthAdmissionsPer100000'})
        mental_health[COUNTRY] = mental_health[COUNTRY].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index(COUNTRY), on=COUNTRY)

        happiness_mental_health_merged = happiness_df_with_continent.merge(mental_health, on=COUNTRY, how='inner')
        happiness_mental_health_merged = happiness_mental_health_merged.rename(columns={'2019': HAPPINESS_SCORE})

        fig = px.scatter(happiness_mental_health_merged.dropna(), x="MentalHealthAdmissionsPer100000", y=HAPPINESS_SCORE, 
                hover_name=COUNTRY, color="region", labels={"MentalHealthAdmissionsPer100000": "Mental Health Admissions (per 100,000)"}, 
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        return fig
    
    st.plotly_chart(plot_mental_health(df_pivot19, df_mh_adm))

    st.write("""
        For countries having close to 0 mental health admissions per 100,000 people, the happiness score seems to be \
        dependent on other factors and a direct correlation cannot be observed. However, in countries having more than 100 mental \
        health admissions per 100,000, the happiness score is greater than 5, indicating that perhaps countries that have destigmatized \
        mental health are more likely to have a higher happiness score. The graph could also indicate that there is poor \
        reporting of mental health admissions in various countries.
    """)

    def plot_mental_health_facilities(happiness_df, mental_health_facilities):
        x = mental_health_facilities[mental_health_facilities['IndicatorCode'].str.strip() == 'MH_17'][['Location','FactValueNumeric', 'ParentLocation']]
        x = x.rename(columns={'Location':COUNTRY, 
                            'FactValueNumeric':'MentalHealthFacilitiesPer100000'})
        x[COUNTRY] = x[COUNTRY].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index(COUNTRY), on=COUNTRY)

        happiness_mental_health_facilities_merged = happiness_df_with_continent.merge(x, on=COUNTRY, how='inner')
        happiness_mental_health_facilities_merged = happiness_mental_health_facilities_merged.rename(columns={'2019':HAPPINESS_SCORE})
        fig = px.scatter(happiness_mental_health_facilities_merged.dropna(), x="MentalHealthFacilitiesPer100000", y=HAPPINESS_SCORE, 
                hover_name=COUNTRY, labels={"MentalHealthFacilitiesPer100000": "Mental Health Facilities (per 100,000)"}, 
                range_x=(0,1), color="region", category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        return fig

    st.plotly_chart(plot_mental_health_facilities(df_pivot19, df_mh_fac))

    st.markdown("""
        --- 
        ### Suicide Rates
    """)

    st.markdown(f"""In this section, we examine the correlation between suicide rate and happiness.
        We hypothesized that a less happy country would have a higher suicide rate.
        We used the suicide rate data per 100,000 people obtained from World Health Organization {cite("suic")}. 
        """)
    
    st.write("""We plotted happiness score as a line sorted from highest to lowest throughout the year.
        Another line representing the suicide rate was added to see the correlation.
        As we can see, the suicide rate fluctuates a lot irrespective of happiness score.
        Contrary to intuition, there seem to be no significant correlation between happiness index and suicide rate.
        """)

    def plot_suicide(df, suicide):
        suicide = suicide[suicide['Dim1'] == 'Both sexes']
        suicide = suicide[['Location','FactValueNumeric', 'ParentLocation', 'Period']]
        suicide = suicide.rename(columns={'Location':COUNTRY, 
                                        'FactValueNumeric':'SuicideRatePer100000'})
        suicide[COUNTRY] = suicide[COUNTRY].str.strip()

        happiness_suicide_merged = df.merge(suicide, left_on=[COUNTRY, YEAR], right_on=[COUNTRY, 'Period'], how='inner')
        happiness_suicide_merged = happiness_suicide_merged[[COUNTRY, YEAR, HAPPINESS_SCORE, 'SuicideRatePer100000']].dropna()
        happiness_suicide_merged = happiness_suicide_merged.astype({HAPPINESS_SCORE: 'float64', 'SuicideRatePer100000': 'float64'})

        df_hs = happiness_suicide_merged.sort_values(by=[YEAR,HAPPINESS_SCORE], ascending=[True, False])
        
        fig = px.line(data_frame=df_hs, x=COUNTRY, y=[HAPPINESS_SCORE, "SuicideRatePer100000"], 
                    hover_name=COUNTRY, animation_frame=YEAR)
        
        for t in fig.data:
            if t.name=="SuicideRatePer100000": t.update(yaxis="y2")
        for f in fig.frames:
            for t in f.data:
                if t.name=="SuicideRatePer100000": t.update(yaxis="y2")
        
        fig.update_layout(
            yaxis2={"overlaying":"y", "side":"right", "title": "Suicide Rates Per 100,000", "range":(0,50)},
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            legend_title="",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.1,
                xanchor="right",
                x=1
            ),
            xaxis={'visible': True, 'showticklabels': False}
        )
        
        fig.update_yaxes(title_text=HAPPINESS_SCORE, secondary_y=False, range=(3,8))
        
        fig['layout']['updatemenus'][0]['pad'] = dict(r=10, t=20)
        fig['layout']['sliders'][0]['pad'] = dict(r=10, t=20,)
        
        return fig


    st.plotly_chart(plot_suicide(df, df_suicide))

    st.markdown("""
        --- 
        ### Sunshine Hours
    """)

    st.markdown(f"""In this section, we examine the correlation between sunshine hours and happiness.
        We consider data for the yearly sunshine hour average for the year 2019 {cite("sun")}.""")

    def plot_sunshine(happiness_df, sunshine):
        sunshine = sunshine[[COUNTRY,YEAR]]
        sunshine = sunshine.rename(columns={YEAR:'YearlySunshineHours'})
        sunshine[COUNTRY] = sunshine[COUNTRY].str.strip()
        
        happiness_df_with_continent = happiness_df.join(df_country.set_index(COUNTRY), on=COUNTRY)

        happiness_sunshine_merged = happiness_df_with_continent.merge(sunshine, on=COUNTRY, how='inner')
        happiness_sunshine_merged = happiness_sunshine_merged.rename(columns={'2019':HAPPINESS_SCORE})

        fig = px.scatter(happiness_sunshine_merged.dropna(), x="YearlySunshineHours", y=HAPPINESS_SCORE, hover_name=COUNTRY, color="region",
                category_orders={REGION: REGION_LIST})

        # Add annotations for a high happiness low sunshine country, and a low happiness, high sunshine country 
        # to corroborate the inconclusivity of the correlation in the writeup
        country = "Finland"
        if country in list(happiness_sunshine_merged[COUNTRY]):
            low_sunshine = happiness_sunshine_merged[happiness_sunshine_merged[COUNTRY] == country]["YearlySunshineHours"].values[0]
            high_happiness = happiness_sunshine_merged[happiness_sunshine_merged[COUNTRY] == country][HAPPINESS_SCORE].values[0]
            fig.add_annotation(x=low_sunshine, y=high_happiness, text=country, showarrow=True, arrowhead=1)

        country = "Egypt"
        if country in list(happiness_sunshine_merged[COUNTRY]):
            high_sunshine = happiness_sunshine_merged[happiness_sunshine_merged[COUNTRY] == country]["YearlySunshineHours"].values[0]
            low_happiness = happiness_sunshine_merged[happiness_sunshine_merged[COUNTRY] == country][HAPPINESS_SCORE].values[0]
            fig.add_annotation(x=high_sunshine, y=low_happiness, text=country, showarrow=True, arrowhead=1)

        return fig

    st.plotly_chart(plot_sunshine(df_pivot19, df_sunshine))

    st.markdown(f"""
        **Well, not everything has a correlation!**

        Though research suggests that lack of sunshine is a leading cause of depression and anxiety {cite("sad")}, 
        we don't find any marginal correlation between happiness and sunshine, since other factors like GDP and health systems play a more important role.

        For example, consider Finland and Egypt (highlighted in the above chart for convenience). Finland is the happiest country in the world even as 
        its residents fight cold and long for a healthy dose of sunshine for the most part of the year, while Egypt, a country that receives the 
        highest sunshine in the world on average, ranks pretty low on the happiness scale.

        This highlights how difficult it is to study happiness based on individual factors. It is a nuanced mixture of many factors!
    """)


