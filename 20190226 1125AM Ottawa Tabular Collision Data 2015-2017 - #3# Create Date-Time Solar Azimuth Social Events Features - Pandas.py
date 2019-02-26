
# coding: utf-8

# # Ottawa Tabular Collision Data 2015-2017 #3# Create Date/Time and Event Features

# In[1]:


import sys
print(sys.executable)
import os
import pandas as pd
import numpy as np
import math 

import datetime
import time

from pysolar.solar import *
from pytz import timezone

# Format of ACCIDENT_DATE m/dd/yyyy

ottawa_fury_soccer = [ 
    # Arena: TD Place
    "4/18/2015" , "4/22/2015", "4/25/2015",
    "5/9/2015" , "5/23/2015", "5/29/2015",
    "7/5/2015" , "7/19/2015" , "7/22/2015" , "7/26/2015" ,
    "8/15/2015" , "8/26/2015", "8/29/2015" ,
    "9/12/2015" ,
    "10/4/2015" , "18/4/2015",
    "11/8/2015",
                 
    "5/18/2016",
    "6/1/2016", "6/11/2016",
    "7/10/2016", "7/27/2016", "7/30/2016",
    "8/13/2016", "8/24/2016", "8/28/2016",
    "9/2/2016", "9/24/2016",
    "10/2/2016", "10/9/2016", "10/29/2016",
                  
    "4/22/2017",
    "5/6/2017", "5/13/2017", "5/27/2017",
    "6/10/2017","6/20/2017", "6/24/2017",
    "7/15/2017", "7/29/2017",
    "8/5/2017", "8/12/2017", "8/27/2017",
    "9/3/2017", "9/24/2017",
    "10/1/2017", "10/8/2017"
]

ottawa_senators_hockey = [
    # Arena: Canadian Tire Centre
    "1/4/2015" , "1/15/2015", "1/17/2015","1/21/2015" , "1/29/2015", "1/31/2015",
    "2/5/2015" , "2/7/2015", "2/12/2015","2/14/2015" , "2/16/2015", "2/18/2015", "2/21/2015",
    "3/6/2015" , "3/8/2015", "3/10/2015","3/15/2015" , "3/19/2015", "3/21/2015", "3/23/2015","3/26/2015","3/29/2015",
    "4/2/2015","4/4/2015","4/7/2015","4/19/2015","4/22/2015","4/26/2015",
    "9/21/2015","9/26/2015",
    "10/3/2015","10/11/2015","10/17/2015","10/22/2015","10/24/2015","10/28/2015","10/31/2015",
    "11/5/2015","11/12/2015","11/14/2015","11/16/2015","11/19/2015","11/21/2015",
    "12/1/2015","12/3/2015","12/5/2015","12/14/2015","12/18/2015","12/27/2015","12/30/2015",
    
    "1/7/2016" , "1/9/2016", "1/22/2016","1/24/2016" , "1/26/2016", 
    "2/4/2016" , "2/6/2016", "2/8/2016","2/11/2016" , "2/16/2016", "2/18/2016", "2/20/2016",
    "3/1/2016" , "3/3/2016", "3/6/2016","3/12/2016" , "3/15/2016", "3/19/2016", "3/22/2016","3/26/2016",
    "4/5/2016","4/7/2016",
    "10/1/2016","10/4/2016","10/7/2016","10/12/2016","10/15/2016","10/18/2016","10/22/2016",
    "11/1/2016","11/3/2016","11/5/2016","11/11/2016","11/13/2016","11/17/2016","11/19/2016","11/24/2016","11/26/2016","11/29/2016",
    "12/1/2016","12/3/2016","12/14/2016","12/17/2016","12/22/2016","12/29/2016",
    
    "1/7/2017" , "1/8/2017", "1/12/2017","1/14/2017" , "1/22/2017", "1/24/2017", "1/26/2017",
    "2/7/2017" , "2/9/2017", "2/11/2017","2/14/2017" , "2/19/2017", 
    "3/2/2017" , "3/4/2017", "3/6/2017","3/14/2017" , "3/16/2017", "3/18/2017", "3/23/2017",
    "4/4/2017","4/8/2017","4/12/2017","4/15/2017","4/21/2017","4/27/2017","4/29/2017",
    "5/6/2017","5/17/2017", "5/19/2017","5/23/2017",
    "9/18/2017","9/23/2017","9/25/2017",
    "10/5/2017","10/7/2017","10/17/2017","10/19/2017","10/21/2017","10/24/2017","10/26/2017","10/30/2017",
    "11/2/2017","11/4/2017","11/11/2017","11/16/2017","11/18/2017","11/25/2017",
    "12/13/2017","12/16/2017","12/19/2017","12/29/2017","12/30/2017"
]

ottawa_67s_hockey = [
    # Arena: TD Place
    
    # 2014 - 2015 Regular Season
    "1/6/2015", "1/9/2015", "1/11/2015", "1/16/2015", "1/18/2015","1/23/2015", "1/27/2015", "1/30/2015",
    "2/1/2015", "2/6/2015", "2/8/2015", "2/13/2015", "2/15/2015", "2/20/2015", "2/21/2015",
    "3/6/2015", "3/13/2015","3/20/2015","3/22/2015",
    # 2015 Playoffs
    "3/26/2015", "3/28/2015", "4/3/2015",
    
    # 2015 Pre-season
    "9/4/2015", "9/17/2015",
    # 2015 - 2016 Regular Season
    "9/27/2015",
    "10/2/2015","10/9/2015", "10/21/2015","10/23/2015","10/25/2015",
    "11/4/2015","11/6/2015","11/27/2015","11/28/2015",
    "12/9/2015","12/11/2015","12/13/2015","12/18/2015","12/19/2015",
    "1/8/2016", "1/9/2016", "1/15/2016", "1/17/2016", "1/22/2016","1/24/2016", "1/29/2016", "1/30/2016",
    "2/5/2016", "2/9/2016", "2/12/2016", "2/14/2016", "2/15/2016", "2/19/2016", "2/22/2016","2/26/2016","2/27/2016",
    "3/16/2016", "3/18/2016",
    # 2016 Playoffs
    "3/28/2016", "3/30/2016",
    
    # 2016 Pre-season
    "9/4/2016", "9/11/2016",
    # 2016 - 2017 Regular Season
    "9/25/2016",
    "10/6/2016","10/8/2016", "10/15/2016","10/16/2016","10/29/2016","10/30/2016",
    "11/5/2016","11/16/2016","11/25/2016","11/26/2016",
    "12/3/2016","12/4/2016","12/10/2016","12/11/2016","12/30/2016",
    "1/7/2017", "1/8/2017", "1/24/2017", "1/25/2017", "1/28/2017",
    "2/4/2017", "2/8/2017", "2/11/2017", "2/12/2017", "2/20/2017", "2/24/2017", "2/25/2017","2/26/2017",
    "3/4/2017", "3/5/2017","3/15/2017", "3/18/2017","3/19/2017",
    # 2017 Playoffs
    "3/28/2017", "3/30/2017",
    "4/2/2017",
    
    # 2017 Pre-season
    "9/15/2017",
    # 2017 - 2018 Regular Season
    "9/24/2017",
    "10/8/2017","10/20/2017", "10/28/2017",
    "11/1/2017","11/3/2017","11/5/2017","11/10/2017","11/18/2017",
    "12/2/2017","12/3/2017","12/9/2017","12/10/2017","12/17/2017","12/29/2017"
    
]

ottawa_redblacks_football = [
    # Arena: TD Place
    
    "6/8/2015","6/25/2015",
    "7/9/2015",
    "8/15/2015","8/23/2015",
    "9/13/2015","9/19/2015",
    "10/6/2015","10/24/2015",
    "11/1/2015","11/29/2015",
    
    "6/17/2016","6/25/2016","6/30/2016",
    "7/13/2016","7/22/2016",
    "9/1/2016","9/17/2016",
    "10/1/2016","10/14/2016","10/29/2016",
    
    "6/15/2017","6/29/2017",
    "7/14/2017","7/24/2017",
    "8/18/2017","8/31/2017",
    "9/17/2017","9/22/2017",
    "10/7/2017","10/13/2017"
]

carleton_ravens_football = [
    # Arena: MNP Park, TD Place (Panda)
    "9/6/2015",
    "9/19/2015",
    "10/9/2015",
    "10/24/2015",
    
    "9/4/2016",
    "9/17/2016",
    "10/1/2016",
    "10/7/2016",
    
    "9/3/2017",
    "9/16/2017",
    "9/30/2017",
    "10/14/2017",
    "10/21/2017"
]

ottawa_gee_gees_football = [
    # Arena: Minto Sport Complex
    
    "9/6/2015",
    "9/19/2015",
    "10/3/2015",
    "10/24/2015",
    
    "9/10/2016",
    "9/17/2016",
    "10/7/2016",
    "10/15/2016",
    
    "9/4/2017",
    "9/23/2017",
    "9/30/2017",
    "10/14/2017"
]

ottawa_champions_bbc = [
    # Arena: RCGT Park
    
    # 2015 Regular
    "5/22/2015", "5/23/2015", "5/24/2015",
    "6/2/2015","6/3/2015","6/4/2015","6/5/2015","6/6/2015","6/7/2015","6/11/2015","6/12/2015","6/13/2015",
    "6/15/2015","6/16/2015","6/17/2015","6/25/2015","6/26/2015","6/27/2015","6/28/2015","6/29/2015","6/30/2015",
    "7/14/2015","7/15/2015","7/18/2015","7/19/2015","7/20/2015","7/21/2015","7/29/2015","7/30/2015","7/31/2015",
    "8/1/2015","8/2/2015","8/3/2015","8/4/2015","8/5/2015","8/6/2015","8/7/2015","8/12/2015","8/13/2015",
    "8/17/2015","8/18/2015","8/19/2015","8/21/2015","8/22/2015","8/23/2015","8/28/2015","8/29/2015","8/30/2015",
    "9/5/2015","9/6/2015","9/7/2015",
    
    # 2016 Regular
    "5/15/2016","5/19/2016","5/20/2016","5/21/2016","5/22/2016","5/23/2016","5/30/2016","5/31/2016",
    "6/1/2016","6/2/2016","6/3/2016","6/4/2016","6/5/2016","6/14/2016","6/15/2016","6/16/2016","6/17/2016",
    "6/18/2016","6/19/2016","6/21/2016","6/22/2016","6/23/2016","6/28/2016","6/29/2016","6/30/2016",
    "7/1/2016","7/2/2016","7/3/2016","7/12/2016","7/13/2016","7/14/2016","7/15/2016","7/16/2016","7/17/2016",
    "7/25/2016","7/26/2016","7/27/2016",
    "8/5/2016","8/6/2016","8/7/2016","8/8/2016","8/9/2016","8/10/2016","8/11/2016","8/19/2016","8/20/2016",
    "8/21/2016","8/22/2016","8/23/2016","8/24/2016",
    "9/2/2016","9/3/2016","9/4/2016","9/5/2016",
    # 2016 Playoffs
    "9/7/2016","9/8/2016","9/13/2016","9/14/2016",
    
    # 2017 Regular
    "5/18/2017","5/19/2017","5/20/2017","5/21/2017","5/22/2017","5/23/2017","5/24/2017","5/25/2017",
    "6/2/2017","6/3/2017","6/4/2017","6/5/2017","6/6/2017","6/7/2017","6/16/2017","6/17/2017","6/19/2017",
    "6/20/2017","6/21/2017","6/27/2017","6/28/2017","6/29/2017","6/30/2017",
    "7/1/2017","7/2/2017","7/11/2017","7/12/2017","7/13/2017","7/14/2017","7/15/2017","7/16/2017","7/27/2017",
    "7/28/2017","7/29/2017","7/30/2017",
    "8/7/2017","8/8/2017","8/9/2017","8/10/2017","8/11/2017","8/12/2017","8/13/2017","8/22/2017","8/23/2017",
    "8/24/2017","8/25/2017","8/26/2017","8/27/2017",
    "9/1/2017","9/2/2017","9/3/2017","9/4/2017"
]


ottawa_statutory_holidays = [
    "1/1/2015", #New Years Day
    "2/16/2015", #Family Day
    "4/3/2015", #Good Friday
    "5/18/2015", #Victoria Day
    "7/1/2015", #Canada Day
    "9/7/2015", #Labour Day
    "10/12/2015", #Thanksgiving
    "12/25/2015", #Christmas Day
    "12/26/2015", #Boxing Day
    
    "1/1/2016", #New Years Day
    "2/15/2016", #Family Day
    "3/25/2016", #Good Friday
    "5/23/2016", #Victoria Day
    "7/1/2016", #Canada Day
    "9/5/2016", #Labour Day
    "10/10/2016", #Thanksgiving
    "12/25/2016", #Christmas Day
    "12/26/2016", #Boxing Day
    
    "1/1/2017", #New Years Day
    "2/20/2017", #Family Day
    "4/14/2017", #Good Friday
    "5/22/2017", #Victoria Day
    "7/3/2017", #Canada Day
    "9/4/2017", #Labour Day
    "10/9/2017", #Thanksgiving
    "12/25/2017", #Christmas Day
    "12/26/2017" #Boxing Day 
]

carleton_calendar_winter2015 = {
    'START_DATE' : "1/5/2015",
    'END_DATE'   : "4/8/2015",
    'HOLIDAYS'   : ["2/16/2015", 
                    "2/17/2015", "2/18/2015", "2/19/2015", "2/20/2015",
                    "4/3/2015"]
}

carleton_calendar_summer2015 = {
    'START_DATE' : "5/4/2015",
    'END_DATE'   : "8/14/2015",
    'HOLIDAYS'   : ["5/18/2015", 
                    "7/1/2015",
                    "8/3/2015"]
}

carleton_calendar_fall2015 = {
    'START_DATE' : "9/2/2015",
    'END_DATE'   : "12/7/2015",
    'HOLIDAYS'   : ["9/7/2015",
                    "10/12/2015",
                    "10/26/2015", "10/27/2015", "10/28/2015", "10/29/2015","10/30/2015"
                   ]
}


carleton_calendar_winter2016 = {
    'START_DATE' : "1/6/2016",
    'END_DATE'   : "4/8/2016",
    'HOLIDAYS'   : ["2/15/2016", 
                    "2/16/2016", "2/17/2016", "2/18/2016", "2/19/2016",
                    "4/25/2016"]
}

carleton_calendar_summer2016 = {
    'START_DATE' : "5/2/2016",
    'END_DATE'   : "8/16/2016",
    'HOLIDAYS'   : ["5/23/2016", 
                    "7/1/2016",
                    "8/1/2016"]
}

carleton_calendar_fall2016 = {
    'START_DATE' : "9/7/2016",
    'END_DATE'   : "12/9/2016",
    'HOLIDAYS'   : ["9/5/2016",
                    "10/10/2016",
                    "10/24/2016", "10/25/2016", "10/26/2016", "10/27/2016","10/28/2016"
                   ]
}

carleton_calendar_winter2017 = {
    'START_DATE' : "1/5/2017",
    'END_DATE'   : "4/7/2017",
    'HOLIDAYS'   : ["2/20/2017", 
                    "2/21/2017", "2/22/2017", "2/23/2017", "2/24/2017",
                    "4/14/2017"]
}

carleton_calendar_summer2017 = {
    'START_DATE' : "5/1/2017",
    'END_DATE'   : "8/16/2017",
    'HOLIDAYS'   : ["5/22/2017", 
                    "7/3/2017",
                    "8/7/2017"]
}

carleton_calendar_fall2017 = {
    'START_DATE' : "9/6/2017",
    'END_DATE'   : "12/8/2017",
    'HOLIDAYS'   : ["9/4/2017",
                    "10/9/2017",
                    "10/23/2017", "10/24/2017", "10/25/2017", "10/26/2017","10/27/2017"
                   ]
}


carleton_calendar_winter = [ carleton_calendar_winter2015, carleton_calendar_winter2016, carleton_calendar_winter2017]
carleton_calendar_summer = [ carleton_calendar_summer2015, carleton_calendar_summer2016, carleton_calendar_summer2017]
carleton_calendar_fall = [ carleton_calendar_fall2015, carleton_calendar_fall2016, carleton_calendar_fall2017]


print("Changing Directory")

basedir = 'C:\\Users\\Enrique\\PycharmProjects\\TestGeopandas'
os.chdir(basedir)

data_file = basedir + '\\Tabular Data 2015-2017 datafiles\\Ottawa Tabular Collision Data 2015-2017 FINAL DATA with Sampling.csv'


# # Load the Collision Dataset

# In[ ]:


df = pd.read_csv(data_file, dtype = str, na_values = "", keep_default_na = False)

df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'], infer_datetime_format=True)
df['ACCIDENT_DATE_TIME'] = pd.to_datetime(df['ACCIDENT_DATE_TIME'])

df.info()
df.head()


# # 1. Adding Time / Date Features

# In[ ]:


def create_time_date_features(df):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    total = len(df)
    print("Number of Items to Handle:" + str(total))
    one_per = int(round(total / 100))
    
    df['ACCIDENT_DATE_daym'] = 0
    df['ACCIDENT_DATE_dayw'] = 0
    df['ACCIDENT_DATE_dayy'] = 0
    df['ACCIDENT_DATE_month'] = 0
    df['ACCIDENT_DATE_weekm'] = 0
    df['ACCIDENT_DATE_weeky'] = 0
    df['ACCIDENT_DATE_hour'] = 0
    df['ACCIDENT_DATE_year'] = 0
    
    ACCIDENT_DATE_TIME = df.columns.get_loc('ACCIDENT_DATE_TIME')
    
    ACCIDENT_DATE_daym = df.columns.get_loc('ACCIDENT_DATE_daym')
    ACCIDENT_DATE_dayw = df.columns.get_loc('ACCIDENT_DATE_dayw')
    ACCIDENT_DATE_dayy = df.columns.get_loc('ACCIDENT_DATE_dayy')
    ACCIDENT_DATE_month = df.columns.get_loc('ACCIDENT_DATE_month')
    ACCIDENT_DATE_weekm = df.columns.get_loc('ACCIDENT_DATE_weekm')
    ACCIDENT_DATE_weeky = df.columns.get_loc('ACCIDENT_DATE_weeky')
    ACCIDENT_DATE_hour = df.columns.get_loc('ACCIDENT_DATE_hour')
    ACCIDENT_DATE_year = df.columns.get_loc('ACCIDENT_DATE_year')
    
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    j = 0
    
    for index, row in df.iterrows():
        
        if j == one_per:
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
        
        temp = pd.Timestamp(df.iat[index,ACCIDENT_DATE_TIME])

        df.iat[index,ACCIDENT_DATE_daym] = temp.day
        df.iat[index,ACCIDENT_DATE_dayw] = temp.dayofweek
        df.iat[index,ACCIDENT_DATE_dayy] = temp.dayofyear
        df.iat[index,ACCIDENT_DATE_month] = temp.month
        df.iat[index,ACCIDENT_DATE_weekm] = temp.week
        df.iat[index,ACCIDENT_DATE_weeky] = temp.weekofyear
        df.iat[index,ACCIDENT_DATE_hour] = temp.hour
        df.iat[index,ACCIDENT_DATE_year] = temp.year
        
        j = j + 1                     
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(df)


# In[ ]:


df = create_time_date_features(df)
df.head()


# # 2. Adding Ottawa Fury Soccer Feature

# In[ ]:


def create_social_event_feature(event_data,df,column_name):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    total = len(event_data)
    print("Number of Events Dates to Handle:" + str(total))
    one_per = int(round(total / 100))
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    
    df[column_name] = 0
    
    ACCIDENT_DATE = df.columns.get_loc('ACCIDENT_DATE')
    EVENT = df.columns.get_loc(column_name)
    
    for x in event_data:
        
        temp = df[df['ACCIDENT_DATE'] == x]
        
        for index, row in temp.iterrows():
            df.iat[index,EVENT] = 1
                                
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(df)


# In[ ]:


df = create_social_event_feature(ottawa_fury_soccer,df, "OTTAWA_FURY_SOCCER")
df[df['OTTAWA_FURY_SOCCER'] == 1].head()


# # 3. Adding Ottawa Senators Hockey Feature

# In[ ]:


df = create_social_event_feature(ottawa_senators_hockey,df, "OTTAWA_SENATORS_HOCKEY")
df[df['OTTAWA_SENATORS_HOCKEY'] == 1].head()


# # 4. Adding Ottawa 67s Hockey Feature

# In[ ]:


df = create_social_event_feature(ottawa_67s_hockey,df, "OTTAWA_67S_HOCKEY")
df[df['OTTAWA_67S_HOCKEY'] == 1].head()


# # 5. Adding Ottawa Redblacks Football Feature

# In[ ]:


df = create_social_event_feature(ottawa_redblacks_football,df, "OTTAWA_REDBLACKS_FOOTBALL")
df[df['OTTAWA_REDBLACKS_FOOTBALL'] == 1].head()


# # 6. Adding Carleton Ravens Football Feature

# In[ ]:


df = create_social_event_feature(carleton_ravens_football,df, "OTTAWA_RAVENS_FOOTBALL")
df[df['OTTAWA_RAVENS_FOOTBALL'] == 1].head()


# # 7. Adding uOttawa Gee-Gees Football Feature

# In[ ]:


df = create_social_event_feature(ottawa_gee_gees_football,df, "OTTAWA_GEEGEES_FOOTBALL")
df[df['OTTAWA_GEEGEES_FOOTBALL'] == 1].head()


# # 8. Adding Ottawa Statutory Holiday Feature

# In[ ]:


df = create_social_event_feature(ottawa_statutory_holidays,df, "OTTAWA_STATUTORY_HOLIDAYS")
df[df['OTTAWA_STATUTORY_HOLIDAYS'] == 1].head()


# # 9. Adding Ottawa Champions Baseball  Feature

# In[ ]:


df = create_social_event_feature(ottawa_champions_bbc,df, "OTTAWA_CHAMPIONS_BBC")
df[df['OTTAWA_CHAMPIONS_BBC'] == 1].head()


# # 10. Adding Solar Azimuth / Elevation Feature

# In[ ]:


def create_solar_features(df):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    total = len(df)
    print("Number of Items to Handle:" + str(total))
    one_per = int(round(total / 100))
    
    df['SOLAR_AZIMUTH'] = 0.0
    df['SOLAR_ELEVATION'] = 0.0
    
    ACCIDENT_DATE_TIME = df.columns.get_loc('ACCIDENT_DATE_TIME')
    LONGITUDE = df.columns.get_loc('LONGITUDE')
    LATITUDE = df.columns.get_loc('LATITUDE')
    SOLAR_AZIMUTH = df.columns.get_loc('SOLAR_AZIMUTH')
    SOLAR_ELEVATION = df.columns.get_loc('SOLAR_ELEVATION')
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    j = 0
    
    for index, row in df.iterrows():
        
        if j == one_per:
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
        
        date_temp = pd.Timestamp(df.iat[index,ACCIDENT_DATE_TIME])
        
        datetime_temp = datetime.datetime(
            date_temp.year, 
            date_temp.month, 
            date_temp.day, 
            date_temp.hour, 
            date_temp.minute, 
            date_temp.second, 
            tzinfo=datetime.timezone.utc)
        
        datetime_temp = datetime_temp.replace(tzinfo=timezone('Canada/Eastern'))
        
        df.iat[index,SOLAR_AZIMUTH] = round(get_azimuth(float(df.iat[index,LATITUDE]),
                                                        float(df.iat[index,LONGITUDE]),
                                                        datetime_temp),2)
        
        
        df.iat[index,SOLAR_ELEVATION] = round(get_altitude(float(df.iat[index,LATITUDE]),
                                                           float(df.iat[index,LONGITUDE]),
                                                           datetime_temp),2)
            
        j = j + 1                     
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(df)


# In[ ]:


df = create_solar_features(df)
df.head()


# In[ ]:


#date = datetime.datetime.now()
#print(get_altitude(42.206, -71.382, date))
date = datetime.datetime(2007, 2, 18, 15, 13, 1, tzinfo=datetime.timezone.utc)
x = get_altitude(42.206, 42.206, date)
print(round(x,2))
print(get_altitude(42.206, 42.206, date))


# In[ ]:


date = datetime.datetime(2019, 2, 23, 15, 0, 0, tzinfo=datetime.timezone.utc)
get_azimuth(45.42, -75.7, date)


# # 11. Adding Carleton University Calendar Feature

# In[ ]:


def create_carleton_calendar_features(calendar_data,df,column_name):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    total = len(calendar_data)
    print("Number of Events Dates to Handle:" + str(total))
    one_per = int(round(total / 100))
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    
    df[column_name] = 0
    
    ACCIDENT_DATE = df.columns.get_loc('ACCIDENT_DATE')
    ACCIDENT_DATE_dayw = df.columns.get_loc('ACCIDENT_DATE_dayw')
    ACCIDENT_DATE_daym = df.columns.get_loc('ACCIDENT_DATE_daym')
    ACCIDENT_DATE_month = df.columns.get_loc('ACCIDENT_DATE_month')
    ACCIDENT_DATE_year = df.columns.get_loc('ACCIDENT_DATE_year')
    
    EVENT = df.columns.get_loc(column_name)
    
    for x in calendar_data:
         
        start_date_temp = pd.to_datetime(x['START_DATE'],infer_datetime_format=True)
        end_date_temp = pd.to_datetime(x['END_DATE'],infer_datetime_format=True)
            
        temp = df[ (df['ACCIDENT_DATE'] >= start_date_temp) &
                   (df['ACCIDENT_DATE'] <= end_date_temp) ]
        
        for index, row in temp.iterrows():
            
            if (df.iat[index,ACCIDENT_DATE_dayw] < 5):
                # Is not Saturday or Sunday
                df.iat[index,EVENT] = 1
        
        
        HOLIDAYS = x['HOLIDAYS']
        
        for y in HOLIDAYS:
            
            y_date_temp = pd.to_datetime(y,infer_datetime_format=True)
                
            temp = df[df['ACCIDENT_DATE'] == y_date_temp]
        
            for index, row in temp.iterrows():
                df.iat[index,EVENT] = 0
                                
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(df)


# In[ ]:


df = create_carleton_calendar_features(carleton_calendar_winter,df,'CARLETON_CALENDAR_WINTER')
df = create_carleton_calendar_features(carleton_calendar_summer,df,'CARLETON_CALENDAR_SUMMER')
df = create_carleton_calendar_features(carleton_calendar_fall,df,'CARLETON_CALENDAR_FALL')

df[df['CARLETON_CALENDAR_FALL'] == 1]


# # 12. Adding Collision Feature 

# In[ ]:


def create_collision_feature(df,column_name):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    total = len(df)
    print("Number of Events Dates to Handle:" + str(total))
    one_per = int(round(total / 100))
    
    df[column_name] = 0
    CLASSIFICATION_OF_ACCIDENT = df.columns.get_loc('CLASSIFICATION_OF_ACCIDENT')
    COLLISION = df.columns.get_loc(column_name)
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    j = 0
    
    for index, row in df.iterrows():
        
        if j == one_per:
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
        
        
        if (df.iat[index,CLASSIFICATION_OF_ACCIDENT] == "00 - No accident"):
            df.iat[index,COLLISION] = 0
        else:
            df.iat[index,COLLISION] = 1
        j = j + 1
        
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(df)
    


# In[ ]:


df = create_collision_feature(df,"COLLISION")
df.head()


# # 13. Adding Log(x) Feature for Long Features

# In[ ]:


df['ROAD_SINUOSITY_LOG'] = np.log(abs(df['ROAD_SINUOSITY'].astype(float)))
df['ROAD_LEN_LOG'] = np.log(abs(df['ROAD_LEN'].astype(float)))

df['SOLAR_AZIMUTH_LOG'] = np.log(abs(df['SOLAR_AZIMUTH'].astype(float)))
df['SOLAR_ELEVATION_LOG'] = np.log(abs(df['SOLAR_ELEVATION'].astype(float)))

df.head()


# # 14. Adding Number of Collision per Road Segment / Intersection Feature

# In[ ]:


def number_of_collision_feature(df):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    total = len(df)
    print("Number of Points to Handle:" + str(total))
    one_per = int(round(total / 100))
    
    df['NUMBER_OF_COLLISIONS'] = 0
    COLLISION = df.columns.get_loc('COLLISION')
    ROAD_SEGMENT = df.columns.get_loc('ROAD_SEGMENT')
    NUMBER_COLLISIONS = df.columns.get_loc('NUMBER_OF_COLLISIONS')
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    j = 0
    
    for index, row in df.iterrows():
        
        if j == one_per:
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
        
        if (df.iat[index,ROAD_SEGMENT] != "") & (df.iat[index,NUMBER_COLLISIONS] == 0):
            # Needs to be filled
            
            df_temp = df[(df['ROAD_SEGMENT'] == df.iat[index,ROAD_SEGMENT]) &
                         (df['COLLISION'] == 1)]
            
            number_of_collisions = len(df_temp)
            
            for index2, row2 in df_temp.iterrows():
                df.iat[index2,NUMBER_COLLISIONS] = number_of_collisions
                
        j = j + 1
        
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(df)


# In[ ]:


df = number_of_collision_feature(df)
df.head()


# # 15. Write csv File

# In[ ]:


df['ACCIDENT_DATE'] = df['ACCIDENT_DATE'].apply(pd.Timestamp.date)
df.to_csv("Ottawa Tabular Collision Data 2015-2017 FINAL DATA with Sampling and Events.csv", 
          index = None)

