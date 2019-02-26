
# coding: utf-8

# # Ottawa Tabular Collision Data 2015-2017 - #2# Create Non-Collision Samples

# In[1]:


import sys
print(sys.executable)
import os
import pandas as pd
#import geopandas as gpd
#from shapely.geometry import Point, Polygon, LineString
#from shapely.strtree import STRtree
#import shapely.speedups
import numpy as np

#import fiona
#import matplotlib.cm as cm
#import matplotlib.colors as colors
import math 

import datetime
import time
#import osmnx as ox

print("Changing Directory")

basedir = 'C:\\Users\\Enrique\\PycharmProjects\\TestGeopandas'
os.chdir(basedir)

data_file = basedir + '\\Tabular Data 2015-2017 datafiles\\Ottawa Tabular Collision Data 2015-2017 - ALL FEATURES.csv'


# In[2]:


df = pd.read_csv(data_file, dtype = str, na_values = "", keep_default_na = False)
df.info()
df.head()


# In[3]:


def create_new_observations(df, n):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    total = n
    print("Number of Observations to Create:" + str(total))
    one_per = int(round(n / 100))
    
    init_size = len(df)
    df_original = df.copy()
    
    cols = df.columns
    
    j = 0
    index_items = 0
 
    start_per = datetime.datetime.now().replace(microsecond=0)
    
    LOCATION = df.columns.get_loc('LOCATION')
    LOCATION_A = df.columns.get_loc('LOCATION_A')
    LOCATION_B = df.columns.get_loc('LOCATION_B')
    XCOORD = df.columns.get_loc('XCOORD')
    YCOORD = df.columns.get_loc('YCOORD')
    LATITUDE = df.columns.get_loc('LATITUDE')
    LONGITUDE = df.columns.get_loc('LONGITUDE')
    ACCIDENT_DATE = df.columns.get_loc('ACCIDENT_DATE')
    ACCIDENT_TIME = df.columns.get_loc('ACCIDENT_TIME')
    ACCIDENT_DATE_TIME = df.columns.get_loc('ACCIDENT_DATE_TIME')
    ACCIDENT_LOCATION = df.columns.get_loc('ACCIDENT_LOCATION')
    
    TRAFFIC_CONTROL = df.columns.get_loc('TRAFFIC_CONTROL')
    #TRAFFIC_CONTROL_CONDITION = df.columns.get_loc('TRAFFIC_CONTROL_CONDITION')
    
    #ROAD_CONDITION = df.columns.get_loc('ROAD_CONDITION')
    ROAD_SURFACE_CONDITION = df.columns.get_loc('ROAD_SURFACE_CONDITION')
    #ROAD_ALIGNMENT = df.columns.get_loc('ROAD_ALIGNMENT')
    #ROAD_PAVEMENT_MARKINGS = df.columns.get_loc('ROAD_PAVEMENT_MARKINGS')
    ENVIRONMENT_CONDITION = df.columns.get_loc('ENVIRONMENT_CONDITION')
    LIGHT = df.columns.get_loc('LIGHT')
    ROAD_SUBTYPE = df.columns.get_loc('ROAD_SUBTYPE')
    ROAD_SUBCLASS = df.columns.get_loc('ROAD_SUBCLASS')
    ROAD_SEGMENT = df.columns.get_loc('ROAD_SEGMENT')
    ROAD_DIRECTION = df.columns.get_loc('ROAD_DIRECTION')
    ROAD_NAME = df.columns.get_loc('ROAD_NAME')
    ROAD_LEN = df.columns.get_loc('ROAD_LEN')
    ROAD_SINUOSITY = df.columns.get_loc('ROAD_SINUOSITY')
    ONS_ID = df.columns.get_loc('ONS_ID')
    ONS_NAME = df.columns.get_loc('ONS_NAME')
    
    TILE_ID = df.columns.get_loc('TILE_ID')
    #SOLAR_AZIMUTH = df.columns.get_loc('SOLAR_AZIMUTH')
    #SOLAR_ELEVATION = df.columns.get_loc('SOLAR_ELEVATION')
    CLASSIFICATION_OF_ACCIDENT = df.columns.get_loc('CLASSIFICATION_OF_ACCIDENT')
    
        

    while (len(df) < init_size + n):
        
        if (j == one_per): 
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index_items)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
    
        item1 = df_original.sample(n=1)
        
        
        item1_TILE_ID = item1.iat[0,TILE_ID]
        item1_ROAD_SEGMENT = item1.iat[0,ROAD_SEGMENT]
    
        action = np.random.randint(1,3,size = 1)
        #action = 1
        
        if (action == 1):
            # Change Road Segment:
            #       Assuming the same ENVIRONEMNT conditions at the same DATE/TIME inside the same TILE_ID
            # 1. Pickup randomly an observation in the same TILE_ID in a different road (different ROAD_SEGMENT
            # 2. Build the new observation with:
            #           ENV/DATE/TIME == ORIGINAL
            #           ROAD/LOCATION/TRAFFIC CONTROL == SELECTED ITEM
            #
            # 3. If not exists that observation in the original dataset include it as:
            #           CLASSIFICATION_OF_ACCIDENT == 05 - Non collision
            
            
            
            temp_data = df_original.loc[(df_original['TILE_ID'] == item1.iat[0,TILE_ID]) & 
                               (df_original['ROAD_SEGMENT'] != item1.iat[0,ROAD_SEGMENT]) ]
            
            if (len(temp_data) > 0):
            
                #item2 = temp_data.sample(n=1, random_state=2019)
                item2 = temp_data.sample(n=1)
                new_observation = ""
                #ENV/DATE/TIME/SOLAR
                new_observation_ACCIDENT_DATE = item1.iat[0,ACCIDENT_DATE]
                new_observation_ACCIDENT_TIME = item1.iat[0,ACCIDENT_TIME]    
                new_observation_ACCIDENT_DATE_TIME = item1.iat[0,ACCIDENT_DATE_TIME]
                new_observation_ROAD_SURFACE_CONDITION = item1.iat[0,ROAD_SURFACE_CONDITION]
                new_observation_ENVIRONMENT_CONDITION = item1.iat[0,ENVIRONMENT_CONDITION]
                new_observation_LIGHT = item1.iat[0,LIGHT]
                #new_observation_SOLAR_AZIMUTH = item1.iat[0,SOLAR_AZIMUTH]
                #new_observation_SOLAR_ELEVATION = item1.iat[0,SOLAR_ELEVATION]
        
        
                # Add values from the selected item (item2)
                new_observation_LOCATION = item2.iat[0,LOCATION]
                new_observation_LOCATION_A = item2.iat[0,LOCATION_A]
                new_observation_LOCATION_B = item2.iat[0,LOCATION_B]
                new_observation_XCOORD = item2.iat[0,XCOORD]
                new_observation_YCOORD = item2.iat[0,YCOORD]
                new_observation_LATITUDE = item2.iat[0,LATITUDE]
                new_observation_LONGITUDE = item2.iat[0,LONGITUDE]
                new_observation_ACCIDENT_LOCATION = item2.iat[0,ACCIDENT_LOCATION]
                new_observation_TRAFFIC_CONTROL = item2.iat[0,TRAFFIC_CONTROL]
                #new_observation_TRAFFIC_CONTROL_CONDITION = item2.iat[0,TRAFFIC_CONTROL_CONDITION]
                #new_observation_ROAD_CONDITION = item2.iat[0,ROAD_CONDITION]
                #new_observation_ROAD_ALIGNMENT = item2.iat[0,ROAD_ALIGNMENT]
                #new_observation_ROAD_PAVEMENT_MARKINGS = item2.iat[0,ROAD_PAVEMENT_MARKINGS]
                new_observation_ROAD_SUBTYPE  = item2.iat[0,ROAD_SUBTYPE]
                new_observation_ROAD_SUBCLASS = item2.iat[0,ROAD_SUBCLASS]
                new_observation_ROAD_SEGMENT = item2.iat[0,ROAD_SEGMENT]
                new_observation_ROAD_NAME = item2.iat[0,ROAD_NAME]
                new_observation_ROAD_LEN = item2.iat[0,ROAD_LEN]
                new_observation_ROAD_SINUOSITY = item2.iat[0,ROAD_SINUOSITY]
                new_observation_ROAD_DIRECTION = item2.iat[0,ROAD_DIRECTION]
                new_observation_ONS_ID = item2.iat[0,ONS_ID]
                new_observation_ONS_NAME = item2.iat[0,ONS_NAME]
                new_observation_TILE_ID = item2.iat[0,TILE_ID]
                #new_observation_INITIAL_DIRECTION_OF_TRAVEL = item2.iat[0,INITIAL_DIRECTION_OF_TRAVEL]
        
                new_observation_CLASSIFICATION_OF_ACCIDENT = "00 - No accident"
            
                check_observation = df.loc[ 
                    (df['XCOORD'] == item2.iat[0,XCOORD]) &                           
                    (df['YCOORD'] == item2.iat[0,YCOORD]) &                           
                    (df['ACCIDENT_DATE_TIME'] == item1.iat[0,ACCIDENT_DATE_TIME]) &
                    (df['ROAD_SEGMENT'] == item2.iat[0,ROAD_SEGMENT]) &
                    (df['ACCIDENT_LOCATION'] == item2.iat[0,ACCIDENT_LOCATION]) &
                    (df['ENVIRONMENT_CONDITION'] == item1.iat[0,ENVIRONMENT_CONDITION])]
            
        
                if (len(check_observation) == 0):
                    # The observation does not exists, add to the dataset
                    #print("adding observation")
                    df_new = pd.DataFrame.from_records([{ 
                        'LOCATION' : new_observation_LOCATION,
                        'LOCATION_A' : new_observation_LOCATION_A,
                        'LOCATION_B' : new_observation_LOCATION_B,
                        
                        'XCOORD' : new_observation_XCOORD,
                        'YCOORD' : new_observation_YCOORD,
                        'LATITUDE' : new_observation_LATITUDE,
                        'LONGITUDE' : new_observation_LONGITUDE,
                        
                        'ACCIDENT_LOCATION' : new_observation_ACCIDENT_LOCATION,
                        
                        
                        'ACCIDENT_DATE' : new_observation_ACCIDENT_DATE,
                        'ACCIDENT_TIME' : new_observation_ACCIDENT_TIME,
                        'ACCIDENT_DATE_TIME' : new_observation_ACCIDENT_DATE_TIME,
                        
                        'TRAFFIC_CONTROL' : new_observation_TRAFFIC_CONTROL,
                        #'TRAFFIC_CONTROL_CONDITION' : new_observation_TRAFFIC_CONTROL_CONDITION,
                        
                        #'ROAD_CONDITION' : new_observation_ROAD_CONDITION,
                        'ROAD_SURFACE_CONDITION' : new_observation_ROAD_SURFACE_CONDITION,
                        #'ROAD_ALIGNMENT' : new_observation_ROAD_ALIGNMENT,
                        #'ROAD_PAVEMENT_MARKINGS' : new_observation_ROAD_PAVEMENT_MARKINGS,
                        
                        'ENVIRONMENT_CONDITION' : new_observation_ENVIRONMENT_CONDITION,
                        'LIGHT' : new_observation_LIGHT,
                        
                        'ROAD_SUBTYPE' : new_observation_ROAD_SUBTYPE,
                        'ROAD_SUBCLASS' : new_observation_ROAD_SUBCLASS,
                        'ROAD_SEGMENT' : new_observation_ROAD_SEGMENT,
                        'ROAD_NAME' : new_observation_ROAD_NAME,
                        'ROAD_LEN' : new_observation_ROAD_LEN,
                        'ROAD_SINUOSITY' : new_observation_ROAD_SINUOSITY,
                        'ROAD_DIRECTION' : new_observation_ROAD_DIRECTION,
                        
                        'ONS_ID' : new_observation_ONS_ID,
                        'ONS_NAME' : new_observation_ONS_NAME,
                        'TILE_ID' : new_observation_TILE_ID,
                        
                        #'SOLAR_AZIMUTH' : new_observation_SOLAR_AZIMUTH,
                        #'SOLAR_ELEVATION' : new_observation_SOLAR_ELEVATION,
                    
                        
                        'CLASSIFICATION_OF_ACCIDENT' : new_observation_CLASSIFICATION_OF_ACCIDENT}])
                        
                        
                    #df_new = df_new.reindex(cols, axis=1)
                    #df = df.reindex(cols, axis=1)
                    df = df.append(df_new)
                    #df = df.reindex(cols, axis=1)
                    j = j + 1
                    index_items = index_items + 1
                    
          
        if (action == 2):
            # Change Hour:
            #       Assuming the same ENVIRONEMNT conditions at the same DATE/TIME inside the same TILE_ID
            # 1. Pickup randomly an observation in the same TILE_ID in a different hour (different ACCIDENT_TIME)
            # 2. Build the new observation with:
            #           ENV/DATE/TIME == SELECTED ITEM
            #           ROAD/LOCATION/TRAFFIC CONTROL == ORIGINAL
            #
            # 3. If not exists that observation in the original dataset include it as:
            #           CLASSIFICATION_OF_ACCIDENT == 05 - Non collision
            
            
            
            temp_data = df_original.loc[(df_original['TILE_ID'] == item1.iat[0,TILE_ID]) & 
                               (df_original['ACCIDENT_TIME'] != item1.iat[0,ACCIDENT_TIME]) ]
            
            if (len(temp_data) > 0):
            
                #item2 = temp_data.sample(n=1, random_state=2019)
                item2 = temp_data.sample(n=1)
                new_observation = ""
                #ENV/DATE/TIME/SOLAR
                new_observation_ACCIDENT_DATE = item2.iat[0,ACCIDENT_DATE]
                new_observation_ACCIDENT_TIME = item2.iat[0,ACCIDENT_TIME]    
                new_observation_ACCIDENT_DATE_TIME = item2.iat[0,ACCIDENT_DATE_TIME]
                new_observation_ROAD_SURFACE_CONDITION = item2.iat[0,ROAD_SURFACE_CONDITION]
                new_observation_ENVIRONMENT_CONDITION = item2.iat[0,ENVIRONMENT_CONDITION]
                new_observation_LIGHT = item2.iat[0,LIGHT]
                #new_observation_SOLAR_AZIMUTH = item2.iat[0,SOLAR_AZIMUTH]
                #new_observation_SOLAR_ELEVATION = item2.iat[0,SOLAR_ELEVATION]
        
        
                # Add values from the selected item (item1)
                new_observation_LOCATION = item2.iat[0,LOCATION]
                new_observation_LOCATION_A = item2.iat[0,LOCATION_A]
                new_observation_LOCATION_B = item2.iat[0,LOCATION_B]
                new_observation_XCOORD = item1.iat[0,XCOORD]
                new_observation_YCOORD = item1.iat[0,YCOORD]
                new_observation_LATITUDE = item1.iat[0,LATITUDE]
                new_observation_LONGITUDE = item1.iat[0,LONGITUDE]
                new_observation_ACCIDENT_LOCATION = item1.iat[0,ACCIDENT_LOCATION]
                new_observation_TRAFFIC_CONTROL = item1.iat[0,TRAFFIC_CONTROL]
                #new_observation_TRAFFIC_CONTROL_CONDITION = item1.iat[0,TRAFFIC_CONTROL_CONDITION]
                #new_observation_ROAD_CONDITION = item1.iat[0,ROAD_CONDITION]
                #new_observation_ROAD_ALIGNMENT = item1.iat[0,ROAD_ALIGNMENT]
                #new_observation_ROAD_PAVEMENT_MARKINGS = item1.iat[0,ROAD_PAVEMENT_MARKINGS]
                new_observation_ROAD_SUBTYPE  = item1.iat[0,ROAD_SUBTYPE]
                new_observation_ROAD_SUBCLASS = item1.iat[0,ROAD_SUBCLASS]
                new_observation_ROAD_SEGMENT = item1.iat[0,ROAD_SEGMENT]
                new_observation_ROAD_NAME = item1.iat[0,ROAD_NAME]
                new_observation_ROAD_LEN = item1.iat[0,ROAD_LEN]
                new_observation_ROAD_SINUOSITY = item1.iat[0,ROAD_SINUOSITY]
                new_observation_ROAD_DIRECTION = item1.iat[0,ROAD_DIRECTION]
                new_observation_ONS_ID = item1.iat[0,ONS_ID]
                new_observation_ONS_NAME = item1.iat[0,ONS_NAME]
                new_observation_TILE_ID = item1.iat[0,TILE_ID]
                #new_observation_INITIAL_DIRECTION_OF_TRAVEL = item1.iat[0,INITIAL_DIRECTION_OF_TRAVEL]
        
                new_observation_CLASSIFICATION_OF_ACCIDENT = "00 - No accident"
            
                check_observation = df.loc[ 
                    (df['XCOORD'] == item2.iat[0,XCOORD]) &                           
                    (df['YCOORD'] == item2.iat[0,YCOORD]) &                           
                    (df['ACCIDENT_DATE_TIME'] == item1.iat[0,ACCIDENT_DATE_TIME]) &
                    (df['ROAD_SEGMENT'] == item2.iat[0,ROAD_SEGMENT]) &
                    (df['ACCIDENT_LOCATION'] == item2.iat[0,ACCIDENT_LOCATION]) &
                    (df['ENVIRONMENT_CONDITION'] == item1.iat[0,ENVIRONMENT_CONDITION])]
            
        
                if (len(check_observation) == 0):
                    # The observation does not exists, add to the dataset
                    #print("adding observation")
                    df_new = pd.DataFrame.from_records([{ 
                        'ACCIDENT_DATE' : new_observation_ACCIDENT_DATE,
                        'ACCIDENT_TIME' : new_observation_ACCIDENT_TIME,
                        'ACCIDENT_DATE_TIME' : new_observation_ACCIDENT_DATE_TIME,
                        'ROAD_SURFACE_CONDITION' : new_observation_ROAD_SURFACE_CONDITION,
                        'ENVIRONMENT_CONDITION' : new_observation_ENVIRONMENT_CONDITION,
                        'LIGHT' : new_observation_LIGHT,
                        #'SOLAR_AZIMUTH' : new_observation_SOLAR_AZIMUTH,
                        #'SOLAR_ELEVATION' : new_observation_SOLAR_ELEVATION,
                    
                        'LOCATION' : new_observation_LOCATION,
                        'LOCATION_A' : new_observation_LOCATION_A,
                        'LOCATION_B' : new_observation_LOCATION_B,
                    
                        'XCOORD' : new_observation_XCOORD,
                        'YCOORD' : new_observation_YCOORD,
                        'LATITUDE' : new_observation_LATITUDE,
                        'LONGITUDE' : new_observation_LONGITUDE,
                    
                        'ACCIDENT_LOCATION' : new_observation_ACCIDENT_LOCATION,
                        'TRAFFIC_CONTROL' : new_observation_TRAFFIC_CONTROL,
                        #'TRAFFIC_CONTROL_CONDITION' : new_observation_TRAFFIC_CONTROL_CONDITION,
                    
                        #'ROAD_CONDITION' : new_observation_ROAD_CONDITION,
                        #'ROAD_ALIGNMENT' : new_observation_ROAD_ALIGNMENT,
                        #'ROAD_PAVEMENT_MARKINGS' : new_observation_ROAD_PAVEMENT_MARKINGS,
                    
                        'ROAD_SUBTYPE' : new_observation_ROAD_SUBTYPE,
                        'ROAD_SUBCLASS' : new_observation_ROAD_SUBCLASS,
                        'ROAD_SEGMENT' : new_observation_ROAD_SEGMENT,
                        'ROAD_NAME' : new_observation_ROAD_NAME,
                        'ROAD_LEN' : new_observation_ROAD_LEN,
                        'ROAD_SINUOSITY' : new_observation_ROAD_SINUOSITY,
                        'ROAD_DIRECTION' : new_observation_ROAD_DIRECTION,
                    
                        'ONS_ID' : new_observation_ONS_ID,
                        'ONS_NAME' : new_observation_ONS_NAME,
                        'TILE_ID' : new_observation_TILE_ID,
                    
                        
                        'CLASSIFICATION_OF_ACCIDENT' : new_observation_CLASSIFICATION_OF_ACCIDENT}])
                    #df_new = df_new.reindex(cols, axis=1)
                    #df = df.reindex(cols, axis=1)
                    df = df.append(df_new)
                    
                    j = j + 1
                    index_items = index_items + 1          
            
         
        
        if (action == 3):
            # Change Date:
            #       Assuming the same ENVIRONEMNT conditions at the same DATE/TIME inside the same TILE_ID
            # 1. Pickup randomly an observation in the same TILE_ID in a different date (different ACCIDENT_DATE)
            # 2. Build the new observation with:
            #           ENV/DATE/TIME == SELECTED ITEM
            #           ROAD/LOCATION/TRAFFIC CONTROL == ORIGINAL
            #
            # 3. If not exists that observation in the original dataset include it as:
            #           CLASSIFICATION_OF_ACCIDENT == 05 - Non collision
            
            #print("Action is 1")
            
            temp_data = df_original.loc[(df_original['TILE_ID'] == item1.iat[0,TILE_ID]) & 
                               (df_original['ACCIDENT_DATE'] != item1.iat[0,ACCIDENT_DATE]) ]
            
            if (len(temp_data) > 0):
            
                #item2 = temp_data.sample(n=1, random_state=2019)
                item2 = temp_data.sample(n=1)
                new_observation = ""
                #ENV/DATE/TIME/SOLAR
                new_observation_ACCIDENT_DATE = item2.iat[0,ACCIDENT_DATE]
                new_observation_ACCIDENT_TIME = item2.iat[0,ACCIDENT_TIME]    
                new_observation_ACCIDENT_DATE_TIME = item2.iat[0,ACCIDENT_DATE_TIME]
                new_observation_ROAD_SURFACE_CONDITION = item2.iat[0,ROAD_SURFACE_CONDITION]
                new_observation_ENVIRONMENT_CONDITION = item2.iat[0,ENVIRONMENT_CONDITION]
                new_observation_LIGHT = item2.iat[0,LIGHT]
                #new_observation_SOLAR_AZIMUTH = item2.iat[0,SOLAR_AZIMUTH]
                #new_observation_SOLAR_ELEVATION = item2.iat[0,SOLAR_ELEVATION]
        
        
                # Add values from the selected item (item1)
                new_observation_LOCATION = item2.iat[0,LOCATION]
                new_observation_LOCATION_A = item2.iat[0,LOCATION_A]
                new_observation_LOCATION_B = item2.iat[0,LOCATION_B]
                new_observation_XCOORD = item1.iat[0,XCOORD]
                new_observation_YCOORD = item1.iat[0,YCOORD]
                new_observation_LATITUDE = item1.iat[0,LATITUDE]
                new_observation_LONGITUDE = item1.iat[0,LONGITUDE]
                new_observation_ACCIDENT_LOCATION = item1.iat[0,ACCIDENT_LOCATION]
                new_observation_TRAFFIC_CONTROL = item1.iat[0,TRAFFIC_CONTROL]
                new_observation_TRAFFIC_CONTROL_CONDITION = item1.iat[0,TRAFFIC_CONTROL_CONDITION]
                new_observation_ROAD_CONDITION = item1.iat[0,ROAD_CONDITION]
                new_observation_ROAD_ALIGNMENT = item1.iat[0,ROAD_ALIGNMENT]
                new_observation_ROAD_PAVEMENT_MARKINGS = item1.iat[0,ROAD_PAVEMENT_MARKINGS]
                new_observation_ROAD_SUBTYPE  = item1.iat[0,ROAD_SUBTYPE]
                new_observation_ROAD_SUBCLASS = item1.iat[0,ROAD_SUBCLASS]
                new_observation_ROAD_SEGMENT = item1.iat[0,ROAD_SEGMENT]
                new_observation_ROAD_NAME = item1.iat[0,ROAD_NAME]
                new_observation_ROAD_LEN = item1.iat[0,ROAD_LEN]
                new_observation_ROAD_SINUOSITY = item1.iat[0,ROAD_SINUOSITY]
                new_observation_ROAD_DIRECTION = item1.iat[0,ROAD_DIRECTION]
                new_observation_ONS_ID = item1.iat[0,ONS_ID]
                new_observation_ONS_NAME = item1.iat[0,ONS_NAME]
                new_observation_TILE_ID = item1.iat[0,TILE_ID]
                #new_observation_INITIAL_DIRECTION_OF_TRAVEL = item1.iat[0,INITIAL_DIRECTION_OF_TRAVEL]
        
                new_observation_CLASSIFICATION_OF_ACCIDENT = "00 - No accident"
            
                check_observation = df.loc[ 
                    (df['XCOORD'] == item2.iat[0,XCOORD]) &                           
                    (df['YCOORD'] == item2.iat[0,YCOORD]) &                           
                    (df['ACCIDENT_DATE_TIME'] == item1.iat[0,ACCIDENT_DATE_TIME]) &
                    (df['ROAD_SEGMENT'] == item2.iat[0,ROAD_SEGMENT]) &
                    (df['ACCIDENT_LOCATION'] == item2.iat[0,ACCIDENT_LOCATION]) &
                    (df['ENVIRONMENT_CONDITION'] == item1.iat[0,ENVIRONMENT_CONDITION])]
            
        
                if (len(check_observation) == 0):
                    # The observation does not exists, add to the dataset
                    #print("adding observation")
                    df_new = pd.DataFrame.from_records([{ 
                        'LOCATION' : new_observation_LOCATION,
                        'LOCATION_A' : new_observation_LOCATION_A,
                        'LOCATION_B' : new_observation_LOCATION_B,
                        
                        'XCOORD' : new_observation_XCOORD,
                        'YCOORD' : new_observation_YCOORD,
                        'LATITUDE' : new_observation_LATITUDE,
                        'LONGITUDE' : new_observation_LONGITUDE,
                        
                        'ACCIDENT_LOCATION' : new_observation_ACCIDENT_LOCATION,
                        
                        
                        'ACCIDENT_DATE' : new_observation_ACCIDENT_DATE,
                        'ACCIDENT_TIME' : new_observation_ACCIDENT_TIME,
                        'ACCIDENT_DATE_TIME' : new_observation_ACCIDENT_DATE_TIME,
                        
                        'TRAFFIC_CONTROL' : new_observation_TRAFFIC_CONTROL,
                        #'TRAFFIC_CONTROL_CONDITION' : new_observation_TRAFFIC_CONTROL_CONDITION,
                        
                        #'ROAD_CONDITION' : new_observation_ROAD_CONDITION,
                        'ROAD_SURFACE_CONDITION' : new_observation_ROAD_SURFACE_CONDITION,
                        #'ROAD_ALIGNMENT' : new_observation_ROAD_ALIGNMENT,
                        #'ROAD_PAVEMENT_MARKINGS' : new_observation_ROAD_PAVEMENT_MARKINGS,
                        
                        'ENVIRONMENT_CONDITION' : new_observation_ENVIRONMENT_CONDITION,
                        'LIGHT' : new_observation_LIGHT,
                        
                        'ROAD_SUBTYPE' : new_observation_ROAD_SUBTYPE,
                        'ROAD_SUBCLASS' : new_observation_ROAD_SUBCLASS,
                        'ROAD_SEGMENT' : new_observation_ROAD_SEGMENT,
                        'ROAD_NAME' : new_observation_ROAD_NAME,
                        'ROAD_LEN' : new_observation_ROAD_LEN,
                        'ROAD_SINUOSITY' : new_observation_ROAD_SINUOSITY,
                        'ROAD_DIRECTION' : new_observation_ROAD_DIRECTION,
                        
                        'ONS_ID' : new_observation_ONS_ID,
                        'ONS_NAME' : new_observation_ONS_NAME,
                        'TILE_ID' : new_observation_TILE_ID,
                        
                        #'SOLAR_AZIMUTH' : new_observation_SOLAR_AZIMUTH,
                        #'SOLAR_ELEVATION' : new_observation_SOLAR_ELEVATION,
                    
                        
                        'CLASSIFICATION_OF_ACCIDENT' : new_observation_CLASSIFICATION_OF_ACCIDENT}])
                        
                        
           
                    #df_new = df_new.reindex(cols, axis=1)
                    #df = df.reindex(cols, axis=1)
                    df = df.append(df_new)
                    
                    j = j + 1
                    index_items = index_items + 1 
        
        
            
        end_iter = datetime.datetime.now().replace(microsecond=0)
    
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(df)


# In[4]:


def create_new_observationsv2(df, n):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    #total = len(df)
    total = n
    print("Number of items to Assign:" + str(total))
    #one_per = int(round(total / 100))
    one_per = int(round(n / 100))
    
    init_size = len(df)
    cols = df.columns
    
    j = 0
    index_items = 0
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    
    STREET1 = df.columns.get_loc('STREET1')
    STREET2 = df.columns.get_loc('STREET2')
    STREET3 = df.columns.get_loc('STREET3')
    XCOORD = df.columns.get_loc('XCOORD')
    YCOORD = df.columns.get_loc('YCOORD')
    LATITUDE = df.columns.get_loc('LATITUDE')
    LONGITUDE = df.columns.get_loc('LONGITUDE')
    ACCIDENT_DATE = df.columns.get_loc('ACCIDENT_DATE')
    ACCIDENT_TIME = df.columns.get_loc('ACCIDENT_TIME')
    ACCIDENT_DATE_TIME = df.columns.get_loc('ACCIDENT_DATE_TIME')
    ACCIDENT_LOCATION = df.columns.get_loc('ACCIDENT_LOCATION')
    
    TRAFFIC_CONTROL = df.columns.get_loc('TRAFFIC_CONTROL')
    TRAFFIC_CONTROL_CONDITION = df.columns.get_loc('TRAFFIC_CONTROL_CONDITION')
    
    ROAD_CONDITION = df.columns.get_loc('ROAD_CONDITION')
    ROAD_SURFACE_CONDITION = df.columns.get_loc('ROAD_SURFACE_CONDITION')
    ROAD_ALIGNMENT = df.columns.get_loc('ROAD_ALIGNMENT')
    ROAD_PAVEMENT_MARKINGS = df.columns.get_loc('ROAD_PAVEMENT_MARKINGS')
    ENVIRONMENT_CONDITION = df.columns.get_loc('ENVIRONMENT_CONDITION')
    LIGHT = df.columns.get_loc('LIGHT')
    ROAD_SUBTYPE = df.columns.get_loc('ROAD_SUBTYPE')
    ROAD_SUBCLASS = df.columns.get_loc('ROAD_SUBCLASS')
    ROAD_SEGMENT = df.columns.get_loc('ROAD_SEGMENT')
    ROAD_DIRECTION = df.columns.get_loc('ROAD_DIRECTION')
    ROAD_NAME = df.columns.get_loc('ROAD_NAME')
    ROAD_LEN = df.columns.get_loc('ROAD_LEN')
    ROAD_SINUOSITY = df.columns.get_loc('ROAD_SINUOSITY')
    ONS_ID = df.columns.get_loc('ONS_ID')
    ONS_NAME = df.columns.get_loc('ONS_NAME')
    
    TILE_ID = df.columns.get_loc('TILE_ID')
    SOLAR_AZIMUTH = df.columns.get_loc('SOLAR_AZIMUTH')
    SOLAR_ELEVATION = df.columns.get_loc('SOLAR_ELEVATION')
    CLASSIFICATION_OF_ACCIDENT = df.columns.get_loc('CLASSIFICATION_OF_ACCIDENT')
    #INITIAL_DIRECTION_OF_TRAVEL = df.columns.get_loc('INITIAL_DIRECTION_OF_TRAVEL')
        

    while (len(df) < init_size + n):
        
        if (j == one_per): 
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index_items)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
    
        #item1 = df.sample(n=1, random_state=2019)
        item1 = df.sample(n=1)
        
        #while (str(item1.iat[0,ROAD_SEGMENT]) == "nan"):
        #    item1 = df.sample(n=1)
        
    
        #action = np.random.randint(1,3,size = 1)
        action = 1
        
        if (action == 1):
            # Change Road Segment:
            #       Assuming the same ENVIRONEMNT conditions at the same DATE/TIME inside the same TILE_ID
            # 1. Pickup randomly an observation in the same TILE_ID in a different road (different ROAD_SEGMENT
            # 2. Build the new observation with:
            #           ENV/DATE/TIME == ORIGINAL
            #           ROAD/LOCATION/TRAFFIC CONTROL == SELECTED ITEM
            #
            # 3. If not exists that observation in the original dataset include it as:
            #           CLASSIFICATION_OF_ACCIDENT == 05 - Non collision
            
            #print("Action is 1")
            
            query_str = 'TILE_ID==' + str(item1.iat[0,TILE_ID]) + ' and ' + 'ROAD_SEGMENT!="'+str(item1.iat[0,ROAD_SEGMENT]) + '"'
            #print("QUERY:" + query_str)
            #temp_data = df.loc[(df['TILE_ID'] == item1.iat[0,TILE_ID]) & 
            #                   (df['ROAD_SEGMENT'] != item1.iat[0,ROAD_SEGMENT]) ]
            temp_data = df.query(query_str)
            
            
            if (len(temp_data) > 0):
            
                #item2 = temp_data.sample(n=1, random_state=2019)
                item2 = temp_data.sample(n=1)
                
                new_observation = ""
                #ENV/DATE/TIME/SOLAR
                new_observation_ACCIDENT_DATE = item1.iat[0,ACCIDENT_DATE]
                new_observation_ACCIDENT_TIME = item1.iat[0,ACCIDENT_TIME]    
                new_observation_ACCIDENT_DATE_TIME = item1.iat[0,ACCIDENT_DATE_TIME]
                new_observation_ROAD_SURFACE_CONDITION = item1.iat[0,ROAD_SURFACE_CONDITION]
                new_observation_ENVIRONMENT_CONDITION = item1.iat[0,ENVIRONMENT_CONDITION]
                new_observation_LIGHT = item1.iat[0,LIGHT]
                new_observation_SOLAR_AZIMUTH = item1.iat[0,SOLAR_AZIMUTH]
                new_observation_SOLAR_ELEVATION = item1.iat[0,SOLAR_ELEVATION]
        
        
                # Add values from the selected item (item2)
                new_observation_STREET1 = item2.iat[0,STREET1]
                new_observation_STREET2 = item2.iat[0,STREET2]
                new_observation_STREET3 = item2.iat[0,STREET3]
                new_observation_XCOORD = item2.iat[0,XCOORD]
                new_observation_YCOORD = item2.iat[0,YCOORD]
                new_observation_LATITUDE = item2.iat[0,LATITUDE]
                new_observation_LONGITUDE = item2.iat[0,LONGITUDE]
                new_observation_ACCIDENT_LOCATION = item2.iat[0,ACCIDENT_LOCATION]
                new_observation_TRAFFIC_CONTROL = item2.iat[0,TRAFFIC_CONTROL]
                new_observation_TRAFFIC_CONTROL_CONDITION = item2.iat[0,TRAFFIC_CONTROL_CONDITION]
                new_observation_ROAD_CONDITION = item2.iat[0,ROAD_CONDITION]
                new_observation_ROAD_ALIGNMENT = item2.iat[0,ROAD_ALIGNMENT]
                new_observation_ROAD_PAVEMENT_MARKINGS = item2.iat[0,ROAD_PAVEMENT_MARKINGS]
                new_observation_ROAD_SUBTYPE  = item2.iat[0,ROAD_SUBTYPE]
                new_observation_ROAD_SUBCLASS = item2.iat[0,ROAD_SUBCLASS]
                new_observation_ROAD_SEGMENT = item2.iat[0,ROAD_SEGMENT]
                new_observation_ROAD_NAME = item2.iat[0,ROAD_NAME]
                new_observation_ROAD_LEN = item2.iat[0,ROAD_LEN]
                new_observation_ROAD_SINUOSITY = item2.iat[0,ROAD_SINUOSITY]
                new_observation_ROAD_DIRECTION = item2.iat[0,ROAD_DIRECTION]
                new_observation_ONS_ID = item2.iat[0,ONS_ID]
                new_observation_ONS_NAME = item2.iat[0,ONS_NAME]
                new_observation_TILE_ID = item2.iat[0,TILE_ID]
                #new_observation_INITIAL_DIRECTION_OF_TRAVEL = item2.iat[0,INITIAL_DIRECTION_OF_TRAVEL]
        
                new_observation_CLASSIFICATION_OF_ACCIDENT = "00 - No accident"
            
                check_observation = df.loc[ 
                    (df['XCOORD'] == item2.iat[0,XCOORD]) &                           
                    (df['YCOORD'] == item2.iat[0,YCOORD]) &                           
                    (df['ACCIDENT_DATE_TIME'] == item1.iat[0,ACCIDENT_DATE_TIME]) &
                    (df['ROAD_SEGMENT'] == item2.iat[0,ROAD_SEGMENT]) &
                    (df['ACCIDENT_LOCATION'] == item2.iat[0,ACCIDENT_LOCATION]) &
                    (df['ENVIRONMENT_CONDITION'] == item1.iat[0,ENVIRONMENT_CONDITION])]
            
        
                if (len(check_observation) == 0):
                    # The observation does not exists, add to the dataset
                    #print("adding observation")
                    df_new = pd.DataFrame.from_records([{ 
                        'ACCIDENT_DATE' : new_observation_ACCIDENT_DATE,
                        'ACCIDENT_TIME' : new_observation_ACCIDENT_TIME,
                        'ACCIDENT_DATE_TIME' : new_observation_ACCIDENT_DATE_TIME,
                        'ROAD_SURFACE_CONDITION' : new_observation_ROAD_SURFACE_CONDITION,
                        'ENVIRONMENT_CONDITION' : new_observation_ENVIRONMENT_CONDITION,
                        'LIGHT' : new_observation_LIGHT,
                        'SOLAR_AZIMUTH' : new_observation_SOLAR_AZIMUTH,
                        'SOLAR_ELEVATION' : new_observation_SOLAR_ELEVATION,
                    
                        'STREET1' : new_observation_STREET1,
                        'STREET2' : new_observation_STREET2,
                        'STREET3' : new_observation_STREET3,
                    
                        'XCOORD' : new_observation_XCOORD,
                        'YCOORD' : new_observation_YCOORD,
                        'LATITUDE' : new_observation_LATITUDE,
                        'LONGITUDE' : new_observation_LONGITUDE,
                    
                        'ACCIDENT_LOCATION' : new_observation_ACCIDENT_LOCATION,
                        'TRAFFIC_CONTROL' : new_observation_TRAFFIC_CONTROL,
                        'TRAFFIC_CONTROL_CONDITION' : new_observation_TRAFFIC_CONTROL_CONDITION,
                    
                        'ROAD_CONDITION' : new_observation_ROAD_CONDITION,
                        'ROAD_ALIGNMENT' : new_observation_ROAD_ALIGNMENT,
                        'ROAD_PAVEMENT_MARKINGS' : new_observation_ROAD_PAVEMENT_MARKINGS,
                    
                        'ROAD_SUBTYPE' : new_observation_ROAD_SUBTYPE,
                        'ROAD_SUBCLASS' : new_observation_ROAD_SUBCLASS,
                        'ROAD_SEGMENT' : new_observation_ROAD_SEGMENT,
                        'ROAD_NAME' : new_observation_ROAD_NAME,
                        'ROAD_LEN' : new_observation_ROAD_LEN,
                        'ROAD_SINUOSITY' : new_observation_ROAD_SINUOSITY,
                        'ROAD_DIRECTION' : new_observation_ROAD_DIRECTION,
                    
                        'ONS_ID' : new_observation_ONS_ID,
                        'ONS_NAME' : new_observation_ONS_NAME,
                        'TILE_ID' : new_observation_TILE_ID,
                    
                        #'INITIAL_DIRECTION_OF_TRAVEL' : new_observation_INITIAL_DIRECTION_OF_TRAVEL,
                        'CLASSIFICATION_OF_ACCIDENT' : new_observation_CLASSIFICATION_OF_ACCIDENT}])
           
                
                    df = df.append(df_new)
                    df = df.reindex(cols, axis=1)
                    j = j + 1
                    index_items = index_items + 1
            
            
        end_iter = datetime.datetime.now().replace(microsecond=0)
    
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(df)


# In[ ]:


df2 = create_new_observations(df, len(df))


# In[ ]:


df2.to_csv("Ottawa Tabular Collision Data 2015-2017 FINAL DATA with Sampling.csv", index = None)
non_accident = df2[df2['CLASSIFICATION_OF_ACCIDENT'] == "00 - No accident"]
print(len(non_accident))
non_accident.head()


# In[ ]:


df2.tail()

