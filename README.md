# Covid19 Analysis for Recovery Phase Prediction

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

1. rate of infection: the increase/decrease rate of current total cases against total cases from 14 days ago (normal virus probation period)
1. number of infection: current total cases per million

Formula refers to uk government risk index guidance: 
https://www.spectator.co.uk/article/how-number-10-should-illustrate-its-covid-alert-formula

Prediction Model Build: 

Make use of a classification model to capture relationship between risk drivers (mobility and/or restriction) and risk index to future prediction that aids recovery phase planning
