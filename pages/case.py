import streamlit as st
import plotly.express as px

from utils.dataloader import load_mvp_data
from utils.constants import *

def app():
    df, _ = load_mvp_data()
    
    st.title('Case Studies')
    st.write("Apart from the attributes we explored in the dataset and factors discussed in further analysis, we believe that other, \
        less measurable factors can also play a significant role in the happiness scores of a country.")

    with st.expander("Yemen"):
        st.write("Going back to the happiness score by \
            country charts, we observe sharp dips in the happiness score trends for some countries. Yemen shows a steep decline in the happiness \
            score starting from 2014, with the lowest score around 2015 and again in 2018. \
            These years correspond to periods of major disruption in the political stability of Yemen. The Yemeni civil war began in September 2014 \
            with the takeover of the government.")

        col1, _ = st.columns([9, 1])
        with col1:
            yem_df = df[df[COUNTRY] == 'Yemen']
            fig = px.line(yem_df, x=YEAR, y=HAPPINESS_SCORE)
            score = lambda year: yem_df[yem_df[YEAR]==year][HAPPINESS_SCORE].values[0]
            fig.add_annotation(x=2014, y=score(2014), text="Onset of Yemeni Civil War", showarrow=True, arrowhead=1)
            st.plotly_chart(fig)

        col1, _spacing, col2, _ = st.columns([5, 1, 4, 1])
        with col1:    
            st.write("The civil war induced a massive food crisis in Yemen. By 2017, a quarter of the country's population was nearing a \
                state of population and the United Nations warned that Yemen could face the worst famine the world has seen for many decades. \
                These events coincide with the declines in the happiness score of Yemen.")

        with col2:
            st.image('imgs/veronique-de-viguerie-yemen-civil-war-2.jpg', width=300)
            st.write('Image Source: https://time.com/yemen-saudi-arabia-war-human-toll/')

    with st.expander("Venezuela"):
        st.write("Another example that suggests that socioeconomic and political factors might reflect in the happiness score trends of a country \
            is the case of Venezuela. The happiness score chart shows a steady decline in the happiness scores from 2012, and the chart shows a sharper \
            decline after 2015, hitting the lowest point near 2016.")

        ven_df = df[df[COUNTRY] == 'Venezuela']
        fig = px.line(ven_df, x=YEAR, y=HAPPINESS_SCORE)
        score = lambda year: ven_df[ven_df[YEAR]==year][HAPPINESS_SCORE].values[0]
        fig.add_annotation(x=2012, y=score(2012), text="Venezuela's crisis onset", showarrow=True, arrowhead=1)
        fig.add_annotation(x=2013, y=score(2013), text="Basic food needs impacted", showarrow=True, arrowhead=1)
        fig.add_annotation(x=2015, y=score(2015), text="Sharp increase in homicide rates", showarrow=True, arrowhead=1)
        st.plotly_chart(fig)

        col1, _spacing, col2 = st.columns([5,1,4])
        with col1:    
            st.write("If we look back to the political climate in Venezuela in 2012, the presidential elections marked the beginning of the crisis in Venezuela. \
                This has been described as the worst economic crisis in Venezuela's history; more severe than that of the United States during the Great Depression. \
                The life of the average Venezuelan was affected on all levels. 75% of the population had lost an average of 8 kgs/19 lbs in weight and majority of the \
                people were not able to meet their basic food needs. Another side-effect of this was a sharp increase in the homicide rate from 39 per 100,000 in 2013 \
                to 90 per 100,000 in 2015. Once again, we can see how all of these factors might have contributed to the overall happiness of the country's population.")

        with col2:
            st.image('imgs/venez_gettyimages-1093004142.jpg', width=350)
            st.write('Image Source: https://www.bbc.com/news/world-latin-america-36319877')

    with st.expander("India"):
        st.write("Looking at the trend in India, we observe a gradual decline in the happiness score till about 2013-2014 and then a sharper decline post 2014.")
            

        ind_df = df[df[COUNTRY] == 'India']
        x = df.loc[(df[COUNTRY] == 'India') | (df[COUNTRY] == 'Pakistan') | (df[COUNTRY] == 'Afghanistan') | (df[COUNTRY] == 'Bangladesh') | (df[COUNTRY] == 'Bhutan') | (df[COUNTRY] == 'Nepal') | (df[COUNTRY] == 'Sri Lanka')]
        
        fig = px.line(ind_df, x=YEAR, y=HAPPINESS_SCORE)
        score = lambda year: ind_df[ind_df[YEAR]==year][HAPPINESS_SCORE].values[0]
        fig.add_annotation(x=2014, y=score(2014), text="Prime Ministerial Elections", showarrow=True, arrowhead=1)
        fig.add_annotation(x=2016, y=score(2016), text="Demonetization", showarrow=True, arrowhead=1)
        fig.add_annotation(x=2019, y=score(2019), text="Prime Ministerial Elections", showarrow=True, arrowhead=1)
        st.plotly_chart(fig)
        
        st.markdown("""
            It might be worth noting that the 2014 Indian general elections marked the landslide victory of the Bharatiya Janta Party in India, a right-wing party, 
            with Narendra Modi becoming the Prime Minister. This could imply that the political mood of a country can impact the overall happiness score.

            Another implication of this could be pointing toward a **potential bias in the selection of the participants of the survey.** 
            Are Gallup World Poll survey takers in India usually progressives (left-inclined)? If so, is it possible the happiness levels in the country have not actually declined for the majority, but only for the left-inclined subset? 

            ---
            **Comparison with SAARC Nations**
            
            Since India is still a developing country, it would make more sense to compare the happiness score trends with other such countries. 
            To do this, we choose the [SAARC](https://en.wikipedia.org/wiki/South_Asian_Association_for_Regional_Cooperation) group of nations as the comparison group. 
            Since 2015, India fared poorer on the happiness index than all other SAARC nations except Afghanistan.
        """)
        
        fig2 = px.line(x, x=YEAR, y=HAPPINESS_SCORE, color=COUNTRY)
        st.plotly_chart(fig2)
    