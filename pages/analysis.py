import numpy as np
import streamlit as st
import plotly.express as px

from utils.dataloader import load_data

def app():
    df, df_happy, df_country, df_pivot, df_hdi, df_gender, df_mh_adm, df_mh_fac, df_suicide, df_sunshine = load_data()

    st.title('Analysis')

    st.text("")
    st.markdown('### Happiness Index by Country')   

    col1, col2 = st.columns(2)

    most19_country = df_pivot.set_index('Country name').select_dtypes(np.number).idxmax()[2019]
    most19_score = df_pivot[df_pivot['Country name'] == most19_country][2019].values[0]
    most19_text = "<div style='color:grey;'>The Happiest Country in 2019</div>\
        <div style='font-size: 36px; color:green; font-weight:bold;'>%s</div>\
        <div style='font-size: 20px;'>Index: %0.2f</div>" % (most19_country, most19_score)
    col1.markdown(most19_text, unsafe_allow_html=True)

    least19_country = df_pivot.set_index('Country name').select_dtypes(np.number).idxmin()[2019]
    least19_score = df_pivot[df_pivot['Country name'] == least19_country][2019].values[0]
    least19_text = "<div style='color:grey;'>The Least Happy Country in 2019</div>\
        <div style='font-size: 36px; color:red; font-weight:bold;'>%s</div>\
        <div style='font-size: 20px;'>Index: %0.2f</div>" % (least19_country, least19_score)
    col2.markdown(least19_text, unsafe_allow_html=True)

    col1.write('\n')
    col2.write('\n')

    most_avg_country = df_pivot.set_index('Country name').mean(axis=1).idxmax()
    most_avg_score = df_pivot.set_index('Country name').mean(axis=1).max()
    most_avg_text = "<div style='color:grey;'>The Happiest Country in 2010-2019</div>\
        <div style='font-size: 36px; color:green; font-weight:bold;'>%s</div>\
        <div style='font-size: 20px;'>Average Index: %0.2f</div>" % (most_avg_country, most_avg_score)
    col1.markdown(most_avg_text, unsafe_allow_html=True)

    least_avg_country = df_pivot.set_index('Country name').mean(axis=1).idxmin()
    least_avg_score = df_pivot.set_index('Country name').mean(axis=1).min()
    least_avg_text = "<div style='color:grey;'>The Least Happy Country in 2010-2019</div>\
        <div style='font-size: 36px; color:red; font-weight:bold;'>%s</div>\
        <div style='font-size: 20px;'>Average Index: %0.2f</div>" % (least_avg_country, least_avg_score)
    col2.markdown(least_avg_text, unsafe_allow_html=True)

    st.text("")
    st.write("""
        Below are the happiness index trend for each country in its respective region. 
        To get the region (continent) and sub-region for each country, we joined the happiness index dataset with 
        the United Nations (UN) geoscheme data. There are several countries which have inconsistent names so we manually 
        changed them before joining. Furthermore, there are five countries/territories present in the happiness dataset which 
        are not present in the UN dataset, so we added them manually to their respective regions.
    """)

    st.write("""
        Overall, we observed that countries in Europe, Americas, and Oceania have a relatively higher happiness score
        compared to countries in Asia and Africa. The happiness index for those 3 regions throughout the years are also more
        stable than Asia and Africa.
    """)

    def plot_line_chart(region): 
        df_reg = df[df['sub-subregion'] == region]
        df_reg = df_reg.pivot(index='year', columns='Country name', values='Happiness Score')
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


    option2 = st.selectbox('Select a continent to see the happiness index by countries',\
    ["Africa", "Europe", "Asia", "Oceania", "Americas"])

    if option2 == 'Asia':
    # with st.expander("Asia"):
        st.write('Countries in Asia generally do not have significantly high or significantly low happiness index.\
        In its subregion, countries in South Asia have a lower happiness index compared to other subregions in Asia.')

        col1, col2 = st.columns(2)
        col1.plotly_chart(plot_line_chart("Central Asia"))
        col1.plotly_chart(plot_line_chart("Eastern Asia"))
        col1.plotly_chart(plot_line_chart("South-eastern Asia"))
        col2.plotly_chart(plot_line_chart("Southern Asia"))
        col2.plotly_chart(plot_line_chart("Western Asia"))

    
    if option2 == 'Oceania':
    # with st.expander("Oceania"):
        st.write('For Oceania, we only have data from two countries and both of them are in the Australia & New Zealand subregion \
        and both countries have high happiness index.')

        st.plotly_chart(plot_line_chart("Australia and New Zealand"))
        

    elif option2 == 'Europe':
    # with st.expander("Europe"):
        st.write('Countries in Europe have an overall high happiness index score.\
        Countries in the subregion West Europe have highest average happiness index compared to other regions with all countries having \
        happiness index score greater than 6 throughout the years. \
        Countries in Northern Europe also have stable happiness index ranging from 5 to 8. \
        A country from this subregion, Finland has the highest happiness index out of all countries in the world for the year 2016-2019.')

        col1, col2 = st.columns(2)
        col1.plotly_chart(plot_line_chart("Eastern Europe"))

        fig = plot_line_chart("Northern Europe")
        # score = df[(df['Country name'] == 'Finland') & (df['year'] == 2018)].values[0]
        # fig.add_annotation(x=2018, y=score, text='Finland', showarrow=True)
        col1.plotly_chart(fig)

        col2.plotly_chart(plot_line_chart("Southern Europe"))
        col2.plotly_chart(plot_line_chart("Western Europe"))

    elif option2 == 'Americas':
    # with st.expander("America"):
        st.write('The subregion North America have a significantly high happiness index while Central and South America have a moderately high happiness index.\
        On the other hand, countries in the Carribean subregion have a moderately low happiness index.')

        col1, col2 = st.columns(2)
        col1.plotly_chart(plot_line_chart("Northern America"))
        col1.plotly_chart(plot_line_chart("Central America"))
        col2.plotly_chart(plot_line_chart("South America"))
        col2.plotly_chart(plot_line_chart("Caribbean"))
        

    elif option2 == 'Africa':
    # with st.expander("Africa"):
        st.write('Generally, we can see that countries in Africa have averagely lower happiness index compared to other continents, \
        with almost all countried throughout the years having happiness score less than 6.\
        The index also seems to fluctuate a lot through out the years.')

        col1, col2 = st.columns(2)
        col1.plotly_chart(plot_line_chart("Northern Africa"))
        col1.plotly_chart(plot_line_chart("Eastern Africa"))
        col1.plotly_chart(plot_line_chart("Middle Africa"))
        col2.plotly_chart(plot_line_chart("Southern Africa"))
        col2.plotly_chart(plot_line_chart("Western Africa"))
        

    st.text("")
    st.markdown('### What Metrics Correlate with Happiness?')
    st.markdown('Looking at the pairwise correlations of all metrics with each other for all countries for the decade 2010-2020, \
        we find that GDP, Life Expectancy, and Social Support are **on average most heavily correlated with the Life Ladder \
        happiness index.**')

    fig = px.imshow(df_happy.corr(), color_continuous_scale="RdBu")
    st.plotly_chart(fig)

    st.markdown("""
        **However, we hypothesize that these correlations might vary significantly with the standard of living in different \
            countries and the general ability of people to fight for survival versus being able to take a safe and healthy \
                environment as a given.**

        To test this hypothesis, we turn to looking at **Human Development Index** as a way to categorize countries.

        The Human Development Index (HDI) is compiled by the United Nations Development Programme (UNDP) for 189 countries on \
            an annual basis. The index considers the health, education and income in a given country to provide a measure of \
                human development which is comparable between countries and over time. 
    """)

    st.markdown("""
        The International Monetary Fund (IMF) categorizes "developed countries" have an HDI score of 0.8 or above\
            (in the very high human development tier). These countries have stable governments, widespread education, \
                healthcare, high life expectancies, and growing, powerful economies.
    """)

    hdi_option = st.selectbox('Select HDI category',\
    ['Developed Countries', 'Developing Countries'])
    
    if hdi_option == 'Developed Countries':
    # with st.expander("Developed Countries"):
        st.markdown("""
            **Developed Countries**

            For developed countries with high Human Development Indices, happiness is positively correlated to many factors like 
            social support, freedom to make life choices, generosity, etc. Further, perceptions of corruption is highly negatively 
            correlated with happiness index, showing that people care about politics, who the country's leaders are, and are aware 
            enough to know what might be affecting their access to peace and standard of living on a daily basis.

            This shows that when basic needs like economy (as measured by GDP) and health (as measured by life expectancy) are in good shape, 
            people start caring about a well-rounded life and factors like generosity, social support systems, political influences, and 
            other nuanced factors to happiness.
        """)

        developed_countries = list(df_hdi[df_hdi["hdi2019"] >= 0.8]["country"])
        region_df = df_happy[df_happy["Country name"].isin(developed_countries)]
        fig = px.imshow(region_df.corr(), color_continuous_scale="RdBu", width=680)
        st.plotly_chart(fig)

    else:
    # with st.expander("Developing Countries"):
        st.markdown("""
            **Developing Countries**

            Through the below heatmap, we see that as we move towards developing countries with lower Human Development Indices, 
            happiness is positively only correlated to per capita GDP and Life Expectancy at birth, i.e., the economy and health 
            systems play the most significant roles as people's happiness depends on their ability to get by and make a living 
            and work towards a respectable standard of living.

            Things like generosity, or freedom to make life choices are effectively first world problems that don't really factor 
            into general happiness for most people.
        """)

        developing_countries = list(df_hdi[df_hdi["hdi2019"] < 0.7]["country"])
        region_df = df_happy[df_happy["Country name"].isin(developing_countries)]
        fig = px.imshow(region_df.corr(), color_continuous_scale="RdBu", width=680)
        st.plotly_chart(fig)


    st.text("")
    st.markdown('### Quality of Life Factors')
    st.write('In this section, we explore the correlation between happiness index and several quality of life factors presented in the original report.\
    The first graph below describes yearly change of the selected feature in each continent given in our main happiness dataset, and\
    the second graph shows the correlation between each feature and the happiness score for each year.')

    option = st.selectbox('Quality of Life Factors',\
    ['Log GDP per Capita', 'Social Support', 'Healthy Life Expectancy at Birth',\
    'Freedom to Make Life Choices', 'Generosity','Perceptions of corruption'])

    ## 2
    # Social Support vs. Year

    if option == 'Social Support':
        # st.markdown('### Social Support')

        st.write('This graph shows the yearly change in social support that was available in each continent in the past years. \
            There is small change in social support of America, Europe, and Oceania while the social support in Asia and Africa has decreased.\
            Especially around 2014, both Asia and Africa reach the lowest social support.')

        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)]
        df1 = df1.groupby(['region','year'])[['Social support']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1, x="Year", y="Social support", color = 'region',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)

        
        st.write("""We can see a positive correlation between happiness index and social support, 
        with Europe, Americas, and Oceania leading in the top right quadrant, Asia spread out in the middle,
        and Africa in the lower quadrant.""")

        fig = px.scatter(df.dropna(), x="Social support", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)


    ## 3
    # Health Life Expectancy at Birth vs. Year
    elif option == 'Healthy Life Expectancy at Birth':
        # st.markdown('### Healthy Life Expectancy at Birth')
        st.write('In general, healthy life expectancy at birth increases in all continents. Especially, the value in Africa increases the fastest.')

        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Healthy life expectancy at birth']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Healthy life expectancy at birth", color = 'region',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)

        st.write("""There is a positive correlation between healthy life expectancy and happiness index. 
        All four continents beside Africa occupy the top right quadrant while Africa in the lower left,
        which suggested that the lower health life expectancy rate in Africa is one of the contributing factors
        of why happiness index scores are generally low in African countries.""")
        
        fig = px.scatter(df.dropna(), x="Healthy life expectancy at birth", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        

    ## 1
    # Log GDP per Capita vs. Year
    elif option == 'Log GDP per Capita':
        # st.markdown('### Gross Domestic Product')
        st.write('In general, log GDP per capita slowly increases in all continents.')

        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Log GDP per capita']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Log GDP per capita", color = 'region',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)

        st.write("""There is a positive correlation between Happiness Index and GDP,
        the higher the GDP, the likelier it is to have a high happiness index score.
        Countries in Europe occupy the top right quadrant and are quite stable throughout the years. 
        African countries, on the other hand, occupy the lower left of the quadrant.
        For example, in 2019 the country with the highest GDP, Luxembourg, has a relatively high happiness index at 7.4,
        while the country with lowest GDP, Malawi, has a relatively low happiness index at approximately 3.9.""")

        st.write("""Just like the happiness score, we can see that countries in Europe, Americas, and Ocenia 
        have less fluctuative GDP per capita throughout the years compared to countries in Africa and Asia.
        This might be because most countries in those three regions are developed countries while countries in
        Asia and Africa are developing countries.""")

        fig = px.scatter(df.dropna(), x="Log GDP per capita", y="Happiness Score", animation_frame="year",
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)

    ## 5
    # Generosity
    elif option == 'Generosity':
        # st.markdown('### Generosity')
        st.write('Generosity fluctuates and slowly decreases by 2018, however it slightly increases in all continents after 2018.')

        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Generosity']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Generosity", color = 'region',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        
        st.write("""Overall, it seems like there is no correlation between happiness index and generosity.
        Focusing on the region Europe, we can see a slightly positive correlation between happiness index and generosity.
        However, when we look at other regions, there seem to be no correlation. 
        Especially if we look at Asia, which seem pretty scattered thouhout the plot.
        Throughout the decade, Asian countries are always the top country in terms of genersity score,
        but those countries do not have a high happiness index.""")

        fig = px.scatter(df.dropna(), x="Generosity", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)

    ## 4
    # Freedom to make a life choices vs. Year
    elif option == 'Freedom to Make Life Choices':
        # st.markdown('### Freedom to Make Life Choices')

        st.write('Freedom to make a life choices increase in all continents; however, in 2012, this feature reaches the lowest point in Asia and Africa')

        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Freedom to make life choices']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Freedom to make life choices", color = 'region',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
        
        st.write("""Throughout the years, the score for freedom to make life choices increased overall,
        with the trend of all countries moving towards the right side of the graph.
        There also seems to be a positive correlation between happiness index and freedom to make life choices.
        However, the difference between regions is not significant, with countries from all regions scattered throughout the plot.""")

        fig = px.scatter(df.dropna(), x="Freedom to make life choices", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)

    ## 6
    # Perceptions of corruption vs. Year
    else:
        # st.markdown('### Perceptions of Corruption')

        st.write("""Except for Asia and Africa, this feature slightly increases in entire continents.
        We can also observe that the region Oceania have a significantly lower perceptions of corruption compared to other regions.""")

        df1 = df.loc[(df.year >= 2010) & (df.year <= 2019)].dropna()
        df1 = df1.groupby(['region','year'])[['Perceptions of corruption']].mean().reset_index().rename(columns = {'year':'Year'})
        fig = px.line(df1.dropna(), x="Year", y="Perceptions of corruption", color = 'region',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)

        st.write("""
        From the scatterplot we can see that there is a negative correlation between happiness index and perceptions of corruption,
        the lower the corruption score, the higher the happiness index is likely to be.
        There no clear difference for each region with all countries in each region scattered throughout the plot.""")

        fig = px.scatter(df.dropna(), x="Perceptions of corruption", y="Happiness Score", animation_frame="year", size='GDP per capita',
                color="region", hover_name="Country name",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        st.plotly_chart(fig)
    

    st.text("")
    st.markdown('### Other Factors')
    st.write("Now we are going to look at other factors outside of the quality life factors from the original World Happiness Report. \
        We analyzed several additional datasets to see if there is a correlation between these factors with happiness index.")

    st.markdown('##### Gender Disparity')

    st.write("""
        Next, we hypothesize that gender disparity might play a role in the happiness score of a country. \
        Living in an equal society where everyone has the ability to choose the circumstances of their own lives, \
        would likely lead to greater happiness. To test this hypothesis, we explore a dataset that comprises the \
        Gender Development Index (GDI) for countries spanning multiple years.
        GDI is defined as the ratio of female to male HDI values. Countries that have achieved some success in \
        expanding capabilities for both men and women will have higher GDI. A country having a GDI less than 0.5 \
        indicates larger gender disparity.
    """)

    def plot_gender(happiness_df, gender):
        gender_19 = gender.rename(columns={2019.0:'2019'})[['Country', '2019']]
        gender_19['Country'] = gender_19['Country'].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index('country'), on='Country')

        merged = happiness_df_with_continent.merge(gender_19, on='Country', how='inner')
        merged = merged.rename(columns={'2019_x':'Happiness Score','2019_y':'GDI'})
        
        fig = px.scatter(merged.dropna(), x="GDI", y="Happiness Score", hover_name='Country', color='region',
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})

        return fig
    
    df_pivot19 = df_pivot.rename(columns={2019:'2019'})[['Country name', '2019']]
    df_pivot19 = df_pivot19.rename(columns={'Country name':'Country'})
    df_pivot19['Country'] = df_pivot19['Country'].str.strip()

    st.plotly_chart(plot_gender(df_pivot19, df_gender))


    st.write("""
        We observe that countries having a higher GDI have a higher happiness score. This seems to align with what
        one would expect; a country having low gender disparity is more inclusive and diverse, and likely to have
        a higher happiness score.
    """)


    st.text("")
    st.markdown('##### Mental Health')
    st.markdown('**Availability and Admissions**')

    st.write("""
        We are also interested in exploring whether a country's mental health services availability has any \
        impact on the happiness score. For this, we explore a dataset published by the World Health Organization, \
        that contains information on mental hospitals, mental health admissions, etc. for countries spanning across \
        multiple years. For the purpose of this analysis, we consider the following two factors: 1. Mental Health \
        Admissions per 100,000 people and 2. Mental Health Facilities per 100,000 people. We consider data for the year 2019.
    """)

    def plot_mental_health(happiness_df, mental_health):
        mental_health = mental_health[['Location','FactValueNumeric', 'ParentLocation']]
        mental_health = mental_health.rename(columns={'Location':'Country', 
                                                    'FactValueNumeric':'MentalHealthAdmissionsPer100000'})
        mental_health['Country'] = mental_health['Country'].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index('country'), on='Country')

        happiness_mental_health_merged = happiness_df_with_continent.merge(mental_health, on='Country', how='inner')
        happiness_mental_health_merged = happiness_mental_health_merged.rename(columns={'2019':'Happiness Score'})

        fig = px.scatter(happiness_mental_health_merged.dropna(), x="MentalHealthAdmissionsPer100000", y="Happiness Score", hover_name='Country', color="region",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        return fig
    
    st.plotly_chart(plot_mental_health(df_pivot19, df_mh_adm))

    st.write("""
        For countries having close to 0 mental health admissions per 100,000 people, the happiness score seems to be \
        dependent on other factors and a direct correlation cannot be observed. However, in countries having more than 100 mental \
        health admissions per 100,000, the happiness score is less than 5, indicating that perhaps countries that have destigmatized \
        mental health are more likely to have a higher happiness score. The graph could also indicate that there is poor \
        reporting of mental health admissions in various countries.
    """)

    def plot_mental_health_facilities(happiness_df, mental_health_facilities):
        x = mental_health_facilities[mental_health_facilities['IndicatorCode'].str.strip() == 'MH_17'][['Location','FactValueNumeric', 'ParentLocation']]
        x = x.rename(columns={'Location':'Country', 
                            'FactValueNumeric':'MentalHealthFacilitiesPer100000'})
        x['Country'] = x['Country'].str.strip()

        happiness_df_with_continent = happiness_df.join(df_country.set_index('country'), on='Country')

        happiness_mental_health_facilities_merged = happiness_df_with_continent.merge(x, on='Country', how='inner')
        happiness_mental_health_facilities_merged = happiness_mental_health_facilities_merged.rename(columns={'2019':'Happiness Score'})
        fig = px.scatter(happiness_mental_health_facilities_merged.dropna(), x="MentalHealthFacilitiesPer100000", y="Happiness Score", hover_name='Country', 
                range_x=(0,1), color="region", category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})
        return fig

    st.plotly_chart(plot_mental_health_facilities(df_pivot19, df_mh_fac))

    

    st.text("")
    st.markdown('##### Suicide Rates')

    st.write("In this section, we examine the correlation between suicide rate and happiness. \
        We used the suicide rate data per 100,000 people. [Add more .....]")

    def plot_suicide(df, suicide):
        suicide = suicide[suicide['Dim1'] == 'Both sexes']
        suicide = suicide[['Location','FactValueNumeric', 'ParentLocation', 'Period']]
        suicide = suicide.rename(columns={'Location':'Country', 
                                        'FactValueNumeric':'SuicideRatePer100000'})
        suicide['Country'] = suicide['Country'].str.strip()

        happiness_suicide_merged = df.merge(suicide, left_on=['Country name', 'year'], right_on=['Country', 'Period'], how='inner')
        happiness_suicide_merged = happiness_suicide_merged[['Country name', 'year', 'Happiness Score', 'SuicideRatePer100000']].dropna()
        happiness_suicide_merged = happiness_suicide_merged.astype({'Happiness Score': 'float64', 'SuicideRatePer100000': 'float64'})

        df_hs = happiness_suicide_merged.sort_values(by=['year','Happiness Score'], ascending=[True, False])
        
        fig = px.line(data_frame=df_hs, x="Country name", y=["Happiness Score", "SuicideRatePer100000"], 
                    hover_name='Country name', animation_frame="year")
        
        for t in fig.data:
            if t.name=="SuicideRatePer100000": t.update(yaxis="y2")
        for f in fig.frames:
            for t in f.data:
                if t.name=="SuicideRatePer100000": t.update(yaxis="y2")
        
        fig.update_layout(
            yaxis2={"overlaying":"y", "side":"right", "title": "Suicide Rate Per 100000"},
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
            xaxis={'visible': False, 'showticklabels': False}
        )
        
        fig.update_yaxes(title_text="Happiness Score", secondary_y=False)
        
        fig['layout']['updatemenus'][0]['pad'] = dict(r=10, t=20)
        fig['layout']['sliders'][0]['pad'] = dict(r=10, t=20,)
        
        return fig


    st.plotly_chart(plot_suicide(df, df_suicide))

    st.text("")
    st.markdown('##### Sunshine Hours')

    st.write("In this section, we examine the correlation between sunshine hours and happiness. \
        We consider data for the yearly sunshine hour average for the year 2019.")

    def plot_sunshine(happiness_df, sunshine):
        sunshine = sunshine[['Country','Year']]
        sunshine = sunshine.rename(columns={'Year':'YearlySunshineHours'})
        sunshine['Country'] = sunshine['Country'].str.strip()
        
        happiness_df_with_continent = happiness_df.join(df_country.set_index('country'), on='Country')

        happiness_sunshine_merged = happiness_df_with_continent.merge(sunshine, on='Country', how='inner')
        happiness_sunshine_merged = happiness_sunshine_merged.rename(columns={'2019':'Happiness Score'})

        fig = px.scatter(happiness_sunshine_merged.dropna(), x="YearlySunshineHours", y="Happiness Score", hover_name='Country', color="region",
                category_orders={"region": ["Africa", "Europe", "Asia", "Oceania", "Americas"]})

        # Add annotations for a high happiness low sunshine country, and a low happiness, high sunshine country 
        # to corroborate the inconclusivity of the correlation in the writeup
        country = "Finland"
        low_sunshine = happiness_sunshine_merged[happiness_sunshine_merged["Country"] == country]["YearlySunshineHours"].values[0]
        high_happiness = happiness_sunshine_merged[happiness_sunshine_merged["Country"] == country]["Happiness Score"].values[0]
        fig.add_annotation(x=low_sunshine, y=high_happiness, text=country, showarrow=True, arrowhead=1)

        country = "Egypt"
        high_sunshine = happiness_sunshine_merged[happiness_sunshine_merged["Country"] == country]["YearlySunshineHours"].values[0]
        low_happiness = happiness_sunshine_merged[happiness_sunshine_merged["Country"] == country]["Happiness Score"].values[0]
        fig.add_annotation(x=high_sunshine, y=low_happiness, text=country, showarrow=True, arrowhead=1)

        return fig

    st.plotly_chart(plot_sunshine(df_pivot19, df_sunshine))

    st.markdown("""
        **Well, not everything has a correlation!**

        Though research suggests that lack of sunshine is a leading cause of depression and anxiety [TODO: Add citations], 
        we don't find any marginal correlation between happiness and sunshine, since other factors like GDP and health systems play a more important role.

        For example, consider Finland and Egypt (highlighed in the above chart for convenience). Finland is the happiest country in the world even as 
        its residents fight cold and long for a healthy dose of sunshine for the most part of the year, while Egypt, a country that receives the 
        highest sunshine in the world on average, ranks pretty low on the happiness scale.

        This highlights how difficult it is to study happiness based on individual factors. It is a nuanced mixture of many factors!
    """)


