YEAR = "Year"
COUNTRY = "Country"
CONTINENT = "Continent"
REGION = "region"
HAPPINESS_SCORE = "Happiness Score"
LOG_GDP = "Log GDP per capita"
GDP = "GDP per capita"
SOCIAL_SUPPORT = "Social support"
LIFE_EXPECTANCY = "Healthy life expectancy at birth"
FREEDOM = "Freedom to make life choices"
GENEROSITY = "Generosity"
CORRUPTION = "Perceptions of corruption"
POSITIVE_AFFECT = "Positive affect"
NEGATIVE_AFFECT = "Negative affect"

GDI = "GDI"
HDI = "HDI"

REGION_LIST = ["Africa", "Americas", "Asia", "Europe", "Oceania"]

column_descriptions = {
    HAPPINESS_SCORE: "The average happiness index as measured by the Cantril Ladder poll", 
    LOG_GDP: "A country's per capita GDP on log-scale. GDP per capita is in terms of Purchasing Power Parity (PPP) adjusted to constant 2011 international dollars, taken from the World Development Indicators (WDI) released by the World Bank on November 14, 2018.", 
    SOCIAL_SUPPORT: "Social support is the national average of the binary responses (either 0 or 1) to the Gallup World Poll (GWP) question “If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?”", 
    LIFE_EXPECTANCY: "The time series of healthy life expectancy at birth are constructed based on data from the World Health Organization (WHO) Global Health Observatory data repository.", 
    FREEDOM: "Freedom to make life choices is the national average of binary responses to the GWP question “Are you satisfied or dissatisfied with your freedom to choose what you do with your life?”", 
    GENEROSITY: "Generosity is the residual of regressing the national average of GWP responses to the question “Have you donated money to a charity in the past month?” on GDP per capita.", 
    CORRUPTION: "It's the average of binary answers to two GWP questions: “Is corruption widespread throughout the government or not?” and “Is corruption widespread within businesses or not?” (Note: Where data for government corruption are missing, the perception of business corruption is used as the overall corruption-perception measure.)", 
    POSITIVE_AFFECT: "It comprises the average frequency of happiness, laughter and enjoyment on the previous day", 
    NEGATIVE_AFFECT: "It comprises the average frequency of worry, sadness and anger on the previous day.", 
}

column_descriptions_short = {
    HAPPINESS_SCORE: "The average happiness index", 
    LOG_GDP: "A country's per capita GDP on log-scale", 
    SOCIAL_SUPPORT: "Average of binary responses to “Do you have relatives or friends you can count on to help you whenever you need them, or not?”", 
    LIFE_EXPECTANCY: "Expected life expectancy based on WHO Global Health Repository data", 
    FREEDOM: "Average of binary responses to “Are you satisfied or dissatisfied with your freedom to choose what you do with your life?”", 
    GENEROSITY: "Generosity is the residual of regressing the national average of GWP responses to the question “Have you donated money to a charity in the past month?” on GDP per capita.", 
    CORRUPTION: "It's the average of binary answers to two GWP questions: “Is corruption widespread throughout the government or not?” and “Is corruption widespread within businesses or not?” (Note: Where data for government corruption are missing, the perception of business corruption is used as the overall corruption-perception measure.)", 
    POSITIVE_AFFECT: "It comprises the average frequency of happiness, laughter and enjoyment on the previous day", 
    NEGATIVE_AFFECT: "It comprises the average frequency of worry, sadness and anger on the previous day", 
}

cite_num = {
    "base":     "[1]", 
    "hdi":      "[2]", 
    "gdi":      "[3]", 
    "suic":     "[4]", 
    "mhadm":    "[5]", 
    "mhfac":    "[6]", 
    "sun":      "[7]", 
    "sad":      "[8]", 
    "geo":      "[9]", 
    "cantril":  "[10]"
}

citation_links = {
    "base":     """https://worldhappiness.report/""", 
    "hdi":      """http://hdr.undp.org/en/indicators/137506""", # HDI
    "gdi":      """http://hdr.undp.org/en/indicators/137906""", # gender development index
    "suic":     """https://www.who.int/data/gho/data/themes/mental-health/suicide-rates""", # suicide
    "mhfac":    """https://www.who.int/data/gho/data/indicators/indicator-details/GHO/mental-health-outpatient-facilities-(per-100-000)""", # mental health facilities
    "mhadm":    """https://www.who.int/data/gho/data/indicators/indicator-details/GHO/mental-hospital-admissions-(per-100-000)""", # mental health admissions
    "sun":      """https://data.world/makeovermonday/2019w44""", # sunshine
    "sad":      """https://www.webmd.com/mental-health/news/20021205/unraveling-suns-role-in-depression""",
    "geo":      """https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme""", # countries and regions
    "cantril":  """https://news.gallup.com/poll/122453/understanding-gallup-uses-cantril-scale.aspx"""
    # TODO add more that we've used
}

def cite(key):
    return f"[{cite_num[key]}]({citation_links[key]})"
