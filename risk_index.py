# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import math
from datetime import timedelta
from itertools import chain
import country_converter as coco
from functools import lru_cache


@lru_cache(maxsize=250)
def get_risk_index(countryname,selectiondate):
    #load master dataset
    ref = pd.read_csv("master_dataset_with_risk_index.csv")
    d = max(pd.to_datetime(ref['date']))-timedelta(days=15)
    print ('max date is', max(pd.to_datetime(ref['date'])))

    #load coviddata dataset
    #url="https://covid.ourworldindata.org/data/owid-covid-data.csv"
    #coviddata=pd.read_csv(url)
    coviddata=pd.read_csv("owid-covid-data.csv")
    coviddata = coviddata[coviddata['date']>str(d)]

    #load mobility dataset
    #url="https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=6d352e35dcffafce"
    #mobility=pd.read_csv(url)
    mobility=pd.read_csv("Global_Mobility_Report.csv", low_memory=False)
    mobility = mobility[mobility['date']>str(d)]

    if max(pd.to_datetime(mobility['date']))==max(pd.to_datetime(ref['date'])):
        print("dataset is up to date")
    else:
        #change data types and column names
        coviddata = coviddata[coviddata['iso_code']!='OWID_WRL']
        coviddata['date'] = pd.to_datetime(coviddata['date'])
        coviddata.rename(columns={'iso_code':'iso3_code'}, inplace=True)

        iso2_code = coco.convert(names=coviddata['iso3_code'].to_list(), to='ISO2', not_found=None)

        coviddata['iso2_code'] = iso2_code
        coviddata = coviddata[coviddata['iso2_code']!='None']

        #change data type
        mobility['date']= pd.to_datetime(mobility['date'])

        #aggregate values by date and country
        mobility_agg = mobility.groupby(['date','country_region','country_region_code']).agg(
        {'retail_and_recreation_percent_change_from_baseline':'sum',
        'grocery_and_pharmacy_percent_change_from_baseline':'sum',
        'parks_percent_change_from_baseline':'sum',
        'transit_stations_percent_change_from_baseline':'sum',
        'workplaces_percent_change_from_baseline':'sum',
        'residential_percent_change_from_baseline':'sum'}).reset_index()

        #join three dataset by country code

        #version1 : use datasets (kaggle covid19, population and mobility)
        #before_master = covid19_agg.merge(mobility_agg, left_on=['ObservationDate','CountryCode'], right_on=['date','country_region_code'], how='left')
        #master = before_master.merge(population, left_on='country_region_code', right_on='Code', how='left')
        #master = master.drop(['ObservationDate', 'Country/Region','CountryCode', 'Index', 'Country', 'Country code', 'Code'], axis=1)
        #master = master.dropna(, inplace=True)

        #version2： use datasets (owid world coviddata with population included and mobility)
        master = coviddata.merge(mobility_agg, left_on=['date','iso2_code'], right_on=['date','country_region_code'], how='left')
        master = master.dropna(subset=['country_region_code']) 
        master = master.drop(['iso3_code', 'iso2_code'], axis=1)

        #align data with total cases minus 14 days

        #version1: total manual weightage assignment
        #master['risk_index'] = (master['Confirmed']/master['Year_2020'])*0.2+(master['Deaths']/master['Year_2020'])*0.6-(master['Recovered']/master['Year_2020'])*0.2

        #version2: combined use of spead rate r and number of accumulative infections i
        master['country_level_index'] = master.groupby(['country_region_code']).cumcount()+1
        
        back_track = []
        total_cases_minus14 = []
        for country in master['country_region_code'].unique():
            for index in range(0,max(master[master['country_region_code']==country]['country_level_index'])):
                try:
                    back_track.append(master.loc[(master['country_region_code']==country) & (master['country_level_index']==(index-14)),'total_cases'].values)
                except KeyError:
                    back_track.append(float("nan"))
                
        out = []
        for i in range(0,len(back_track)):
            if len(back_track[i])==0:
                out.append(np.array([0]))
            else:
                out.append(back_track[i])
        
        total_cases_minus14 = list(chain(*out))

        master['total_cases_minus14'] = total_cases_minus14

        #calcualte the two factors that contribute to risk index
        master['rate_of_infection'] = (master['total_cases']-master['total_cases_minus14'])/master['total_cases_minus14']
        master['number_of_infection'] = master['total_cases_per_million']

        #calcualte risk index 
        risk_index = []

        for i in range(0,len(master)):
            if math.isinf(master.iloc[i]['rate_of_infection']) or (master.iloc[i]['rate_of_infection']<20 and master.iloc[i]['number_of_infection']<1000):
                risk_index.append(1)
            elif master.iloc[i]['rate_of_infection']<40 and master.iloc[i]['number_of_infection']<2000:
                risk_index.append(2)
            elif master.iloc[i]['rate_of_infection']<60 and master.iloc[i]['number_of_infection']<3000:
                risk_index.append(3)
            elif master.iloc[i]['rate_of_infection']<80 and master.iloc[i]['number_of_infection']<4000:
                risk_index.append(4)
            else:
                risk_index.append(5)

        master['risk_index'] = risk_index
        master = master[master['date']>max(pd.to_datetime(ref['date']))]
        master.to_csv('master_dataset_with_risk_index.csv', mode='a', index=False, header=False)

    ref_updated = pd.read_csv("master_dataset_with_risk_index.csv")
    output = ref_updated.loc[(ref_updated['location']==countryname) & (ref_updated['date']==selectiondate),'risk_index'].values
    print('the risk index is',output[0])
    return output[0]

    #test code:
    #python3 -c "import risk_index; risk_index.get_risk_index('United Kingdom','2020-05-25')"
