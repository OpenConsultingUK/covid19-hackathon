# Covid19 Risk & Recovery Index App for air travel,HR and retail industry.
# Covid19 Analysis for Recovery Phase Prediction.

Source Datasets:

1. Our World in Data COVID-19 Testing dataset https://ourworldindata.org/coronavirus-testing
1. Google Covid19 Community Mobility Reports https://www.google.com/covid19/mobility/

Methdology:

1. Aggregate source data at daily country level and consolidate as master data
1. Calculate risk index based on rate of infection and total number of infections
1. Train machine learning model to translate relationship between risk drivers (mobility and/or restriction) and risk index

Prediction Scenario:
1. To prevent second spike in recovery phase, one would be able to predict on the risk index given the assumed risk drivers therefore to adjust government policies and country wide communications

Risk Index Formula: 

1. rate of infection: the increase/decrease rate of current total cases against total cases from 14 days ago (normal virus incubation period)
1. number of infection: current total cases per million

Formula refers to uk government risk index guidance: 
https://www.spectator.co.uk/article/how-number-10-should-illustrate-its-covid-alert-formula

Prediction Model Build: 

Make use of a classification model to capture relationship between risk drivers (mobility and/or restriction) and risk index to future prediction that aids recovery phase planning

Travel Information during Covid:

The outcome of this analysis will provide current travel information on the countries enquired by the end user. This includes
1. Which airlines are currently operating from the input countries
2. What are the current restrictions or travel information available for the countries selected.

The data is divided in two datasets: 
- COVID-19 restrictions by country: This dataset shows current travel restrictions. 
- COVID-19 airline restrictions information: This dataset shows restrictions taken by individual airlines or country. 

Information is collected from various sources: IATA, media, national sources, WFP internal and public sources.

Question and Answering on Covid19 Information:
