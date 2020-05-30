# -*- coding: utf-8 -*-
"""
Created on Fri May 29 19:15:09 2020

@author: Minu Beena Sisupal
"""

# Import libraries

import pandas as pd
from io import BytesIO
import requests

def data_ingest():
    # COVID 19 GEOGRPAHIC DISTRIBUTION
    full_url ="https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx"
    cases_df = pd.read_excel(full_url,sep=" ")
    country_list = cases_df["countriesAndTerritories"].unique().tolist()
    country_list.sort()
    
    to_cases = cases_df[cases_df["countriesAndTerritories"]== to_country]
    from_cases =  cases_df[cases_df["countriesAndTerritories"]== from_country]
    
    to_code = to_cases.countryterritoryCode.unique()
    from_code = from_cases.countryterritoryCode.unique()
    
    
    # TRAVEL DATA WRT COUNTRY
    r = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vTxATUFm0tR6Vqq-UAOuqQ-BoQDvYYEe-BmJ20s50yBKDHEifGofP2P1LJ4jWFIu0Pb_4kRhQeyhHmn/pub?gid=0&single=true&output=csv')
    data = r.content
    flight_info_Coun = pd.read_csv(BytesIO(data),parse_dates=['published'])
    flight_info_Coun.rename(columns={'adm0_name': 'country'}, inplace=True)
    
    # TRAVEL DATA WRT AIRLINE OF EACH COUNTRY
    r = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vTxATUFm0tR6Vqq-UAOuqQ-BoQDvYYEe-BmJ20s50yBKDHEifGofP2P1LJ4jWFIu0Pb_4kRhQeyhHmn/pub?gid=646351539&single=true&output=csv')
    data = r.content
    flight_info_airline = pd.read_csv(BytesIO(data),parse_dates=['published'])
    flight_info_airline.rename(columns={'adm0_name': 'country'}, inplace=True)
    
    flight_info_airline["country"]= flight_info_airline["country"].str.replace("'"," ")
    flight_info_Coun["country"]= flight_info_Coun["country"].str.replace("'"," ")
    
    return flight_info_airline,flight_info_Coun,to_code,from_code

def getTravelInfo(from_Country, to_Country):
    
    flight_info_airline,flight_info_Coun,to_code,from_code = data_ingest()
    
    to_airline = flight_info_airline[flight_info_airline.iso3.isin(to_code)]
    from_airline =  flight_info_airline[flight_info_airline.iso3.isin(from_code)]
    
    to_countryInfo = flight_info_Coun[flight_info_Coun.iso3.isin(to_code)]
    from_countryInfo = flight_info_Coun[flight_info_Coun.iso3.isin(from_code)]
    
    from_airline = from_airline.fillna("")
    to_airline = to_airline.fillna("")
    
    from_df = airlineInfo(from_airline)
    to_df = airlineInfo(to_airline)
    
    print("FINAL INFORMATION ON TRAVEL")
    print("---------------------------")
    print("\n")
    
    print("INFORMATION ON ORIGIN COUNTRY : ",from_Country)
    from_airlines = getAvailableAirlines(from_df)      
    print("Airlines Available from ",from_Country,": ", from_airlines)
    from_text = getAvailableInfo(from_countryInfo)
    print(from_text)

   
    print("INFORMATION ON DESTINATION COUNTRY : ",to_Country)
    to_airlines = getAvailableAirlines(to_df)
    print("Airlines Available from ",to_Country,": ", to_airlines)
    to_text = getAvailableInfo(to_countryInfo)
    print(to_text)
    
    return None

def airlineInfo(df):
    keywords = ['resume','open']

    info = pd.DataFrame()
    for key in keywords:
        temp_df = pd.DataFrame()
        temp_df = df[df['info'].str.contains(key)]
        info = info.append(temp_df, ignore_index = True)
        
    return info

def getAvailableAirlines(df):
    airline_lst = df.airline.tolist()
    airline_lst = list( dict.fromkeys(airline_lst) )
    airlines = []
    for l in airline_lst:
        l = l.replace('.', '')
        l = l.replace(',', '')
        airlines.append(l)
    return airlines

def getAvailableInfo(df):
    import re
    from gensim.summarization import summarize
    
    text = df['info'].values
    text = str(text)
    text = re.sub(r'\n|\r', ' ', text)
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    text = summarize(text, ratio=0.2, split=False)
    return text
    

    