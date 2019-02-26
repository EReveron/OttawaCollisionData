
# coding: utf-8

# # Ottawa Tabular Collision Data 2015-2017 - #1# Create Geospatial Features - GeoPandas

# # 1. Load Libraries and Define File Names

# In[1]:


import sys
print(sys.executable)
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString
from shapely.strtree import STRtree
import shapely.speedups
import numpy as np

import fiona
import matplotlib.cm as cm
import matplotlib.colors as colors
import math 

import datetime
import time


basedir = 'C:\\Users\\Enrique\\PycharmProjects\\TestGeopandas'
os.chdir(basedir)

roads_file = basedir + '\\Tabular Data 2015-2015 shapefiles\\Ottawa Road Segments Opendata.shp'
boundaries_file = basedir + '\\Tabular Data 2015-2015 shapefiles\\Ottawa ONS Boundaries.shp'
boundaries_file_noz = basedir + '\\Tabular Data 2015-2015 shapefiles\\Ottawa ONS Boundaries no Z coordinates.shp'
collision_data_intersections_file = basedir + '\\Tabular Data 2015-2015 shapefiles\\Ottawa Intersection Tabular Collision Data 2015-2017 .shp'
collision_data_file = basedir + '\\Tabular Data 2015-2015 shapefiles\\Ottawa Tabular Collision Data 2015-2017.shp'
collision_data_nonintersections_file = basedir + '\\Tabular Data 2015-2015 shapefiles\\Ottawa Non-intersection Tabular Collision Data 2015-2017 .shp'
city_limits_tiles = basedir + '\\Tabular Data 2015-2015 shapefiles\\Ottawa City Limits Tiles.shp'


# # 2. Load Ottawa Boundaries Shapefile

# In[2]:


boundaries = gpd.read_file(boundaries_file_noz, index = 'ROW_NUMBER')

boundaries.info()
boundaries


# ## 2.1 Plot the Map

# In[3]:


print("\n=== CRS:" + str(boundaries.crs))
#boundaries.plot(cmap='tab20b', figsize =(15.0,15.0), column = 'Name', legend = True)
boundaries.plot(cmap='tab20b', figsize =(15.0,15.0), column = 'Name')


# ## 2.2 Plot the Map of Carleton University Area

# In[4]:


carleton = boundaries[boundaries['Name'] == 'Carleton University']
carleton.reset_index(drop=True, inplace=True)
carleton.head()


# In[5]:


carleton.plot(cmap='tab20b', figsize =(15.0,15.0), color = 'red')


# ## 2.3 Plot the Map of Carleton University over Ottawa Map

# In[6]:


base = boundaries.plot(color='white', edgecolor='black',figsize =(15.0,15.0),linewidth=0.2)
carleton.plot(ax = base,figsize =(15.0,15.0), color = 'red')


# # 3. Load Roads Segments Shapefile

# In[7]:


roads = gpd.read_file(roads_file)

roads.info()
roads.head()


# In[8]:


roads.crs


# ## 3.1 Plot the Roads Layer

# In[9]:


roads.plot(figsize =(15.0,15.0))
#road_colors = ['black', 'grey', 'grey', 'black', 'grey', 'grey' ]
#line_widths = [1, .5, .5, 1, .5,.5]


# ## 3.2 Plot the Highway 417

# In[10]:


highway_417 = roads[roads['ROAD_NAME'] == 'HIGHWAY 417']
highway_417


# In[11]:


base = boundaries.plot(color='white', edgecolor='black',figsize =(15.0,15.0),linewidth=0.2)
highway_417.plot(ax = base,figsize =(15.0,15.0), color = 'red')


# ## 3.3 Plot Colonel By Dr

# In[12]:


roads_colonel_by_dr = roads[roads['ROAD_NAME'] == 'COLONEL BY DR']
base = boundaries.plot(color='white', edgecolor='black',figsize =(15.0,15.0), linewidth=0.2)
roads_colonel_by_dr.plot(ax = base, figsize =(15.0,15.0), color = 'red', linewidth = 3)


# ## 3.4 Colonel By and Carleton Area

# In[13]:


base = carleton.plot(color='yellow', edgecolor='black',figsize =(15.0,15.0),linewidth=0.2)
roads_colonel_by_dr.plot(ax = base,figsize =(15.0,15.0), color = 'red')


# # 4. Create a new Layer with only Road Centroids to be Used for Classify Roads by Location

# In[14]:


# Create Roads Centroids to be used for Plotting in a Area
roads_centroids = roads.copy()
roads_centroids['geometry'] = roads.centroid 
roads_centroids.to_file('01 - Ottawa Road Centroids Opendata.shp', driver='ESRI Shapefile')
#roads_centroids.to_file('01 - Ottawa Road Centroids Opendata.geojson', driver='GeoJSON')
roads_centroids


# In[15]:


roads_centroids.plot(figsize =(15.0,15.0))


# ## 4.1 Plot Colonel By Dr Roads Centroids

# In[16]:


roads_colonel = roads_centroids[roads_centroids['ROAD_NAME'] == 'COLONEL BY DR']

base = carleton.plot(color='white', edgecolor='black',figsize =(15.0,15.0))
roads_colonel_by_dr.plot(ax = base,cmap='tab20b', figsize =(15.0,15.0))
roads_colonel.plot(ax = base,cmap='tab20b', figsize =(15.0,15.0))


# ## 4.2  Matching Roads Segments using Spatial Index (RTREE) an Roads Centroids in Carleton Area

# In[17]:


spatial_index = roads.sindex
x = carleton.bounds

print(type(x))
print(x['minx'][0])
print(carleton.bounds)

possible_matches_index = list(spatial_index.intersection([x['minx'][0], x['miny'][0], x['maxx'][0], x['maxy'][0]]))
possible_matches = roads.iloc[possible_matches_index]

# Possible matches roads segments around Carleton Area using Spatial Index
base = carleton.plot(color='white', edgecolor='black',figsize =(15.0,15.0))
possible_matches.centroid.plot(ax = base)
possible_matches.plot(ax = base)


# In[ ]:


roads_mask = possible_matches.within(carleton.loc[0,'geometry'])

carleton_roads2 = possible_matches.loc[roads_mask]
print("Number of Roads in Carleton Area:" + str(len(carleton_roads2)))

# Filtered roads in Carleton Area
base = carleton.plot(color='white', edgecolor='black',figsize =(15.0,15.0))
carleton_roads2.plot(ax = base)


# ## 4.3 Matching Roads Segments in Carleton Area Using "Whithin" with Complete Roads Geometry

# In[18]:


roads_mask = roads.within(carleton.loc[0,'geometry'])
carleton_roads = roads.loc[roads_mask]
print("Number of Roads in Carleton Area:" + str(len(carleton_roads)))
carleton_roads


# In[19]:


base = carleton.plot(color='white', edgecolor='black',figsize =(15.0,15.0))
carleton_roads.plot(ax = base, color = 'red', figsize =(15.0,15.0) )


# ## 4.4 Matching Roads Segments in Carleton Area Using "Whithin" with Roads Centroids Geometry

# In[20]:


roads_mask_centroids = roads_centroids.within(carleton.loc[0,'geometry'])
carleton_roads_centroids = roads_centroids.loc[roads_mask]
print("Number of Roads in Carleton Area Using Centroids:" + str(len(carleton_roads_centroids)))
carleton_roads_centroids


# In[21]:


roads_to_plot = carleton_roads_centroids.index
roads_to_plot = list(roads_to_plot)
carleton_roads_original = roads.iloc[roads_to_plot,:]
carleton_roads_original

base = carleton.plot(color='white', edgecolor='black',figsize =(15.0,15.0))
carleton_roads_original.plot(ax = base, color = 'blue')
carleton_roads_centroids.plot(ax = base, color = 'red', figsize =(15.0,15.0))


# # 5. Matching a Road Segment to a Neighborhood

# In[22]:


roads['ONS_ID'] = ""
roads['ONS_NAME'] = ""
roads.head()


# In[23]:


def assing_nearest_area_by_whithin(items, areas):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    ons_id = items.columns.get_loc('ONS_ID')
    ons_name = items.columns.get_loc('ONS_NAME')

    total = len(items)
    print("Number of items to Assign:" + str(total))
 
    start_iter = datetime.datetime.now().replace(microsecond=0)

    for index, row in areas.iterrows():
 
        if (index != 0):
            print("Iteration Time:" + str(end_iter - start_iter))
            start_iter = datetime.datetime.now().replace(microsecond=0)
            
        print("Checking Roads for Area:" + str(row['Name']))
        items_temp = items[items['ONS_ID'] == ""]
        total_now = len(items_temp)
        
        per_no_assigned = (1 - (total - total_now) / total) * 100
        per_assigned = (100 - per_no_assigned)
        
        print("  Number of Roads No Assigned (Empty ONS_ID):" + str(total_now) + " %:" + str(per_no_assigned))
        
        if row.geometry != None:
            mask = items_temp.within(row['geometry'])
        
            items_in = items_temp[mask]
            print("  Number of Roads to be Assigned (Match Current Area):"+ str(len(items_in)))
        
            for index2, row2 in items_in.iterrows():
                items.iat[index2,ons_id] = row['ONS_ID']
                items.iat[index2,ons_name] = row['Name']
        
        end_iter = datetime.datetime.now().replace(microsecond=0)
    
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(items)


# ## 5.1 Using Complete Roads 

# In[24]:


roads['ONS_ID'] = ""
roads['ONS_NAME'] = ""
res1 = assing_nearest_area_by_whithin(roads,boundaries)
res1.head()


# In[25]:


res1_blank = res1[res1['ONS_ID'] == ""]
print("Number of Roads whithout Neighborhood Assigned:"+str(len(res1_blank)))


# In[26]:


base = boundaries.plot(color='white', edgecolor='black',figsize =(15.0,15.0), linewidth=0.2)
res1_blank.plot(ax = base, color = 'red', linewidth = 3)


# ## 5.2 Using Roads Centroids

# In[27]:


roads_centroids['ONS_ID'] = ""
roads_centroids['ONS_NAME'] = ""
res2 = assing_nearest_area_by_whithin(roads_centroids,boundaries)
res2.head()


# In[28]:


res2_blank = res2[res2['ONS_ID'] == ""]
print("Number of Roads whithout Neighborhood Assigned:"+str(len(res2)))
res2_blank


# In[29]:


roads_to_plot = res2_blank.index
roads_to_plot = list(roads_to_plot)
roads_original = roads.iloc[roads_to_plot,:]

base = boundaries.plot(color='white', edgecolor='black',figsize =(15.0,15.0), linewidth=0.2)
roads_original.plot(ax = base,color = 'red', linewidth=3)


# ## 5.3 Matching Roads Segments to Neighborhoods by Road Centroids and the Missing ones by Distance

# In[30]:


def assign_nearest_area_by_mindistance(items, areas):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    ons_id = items.columns.get_loc('ONS_ID')
    ons_name = items.columns.get_loc('ONS_NAME')

    items_temp = items[items['ONS_ID'] == ""]
    total = len(items_temp)
    print("Number of items to Assign:" + str(total))
    one_per = int(round(total / 100))
    j = 0
    start_per = datetime.datetime.now().replace(microsecond=0)
    for index,row in items_temp.iterrows():
    
        if (j == index): 
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
    
        if row.geometry != None:
            d = areas.distance(row.geometry)
            d_min = d.min()
            bound_id = d[d==d_min].index[0]
            closest_area = areas.iloc[bound_id]    
            items.iat[index,ons_id] = closest_area['ONS_ID']
            items.iat[index,ons_name] = closest_area['Name']
            
        j = j + 1
    print("  Percentage done: 100%")
    end = datetime.datetime.now().replace(microsecond=0)    
    print("Total Execution Time:" + str(end - start))
    return(items)


# In[31]:


roads_centroids['ONS_ID'] = ""
roads_centroids['ONS_NAME'] = ""
roads_centroids = assing_nearest_area_by_whithin(roads_centroids,boundaries)
roads.head()


# In[32]:


roads_centroids_blank = roads_centroids[roads_centroids['ONS_ID'] == ""]
print("Number of Roads whithout Neighborhood Assigned:"+str(len(roads_centroids_blank)))
roads_centroids_blank


# In[33]:


roads_centroids = assign_nearest_area_by_mindistance(roads_centroids,boundaries)

roads_centroids['ONS_ID'] = roads_centroids['ONS_ID'].astype(str)
roads_centroids['ONS_NAME'] = roads_centroids['ONS_NAME'].astype(str)

roads_centroids.to_file('02 - Ottawa Road Centroids Opendata with Neighborhoods.shp', driver='ESRI Shapefile')
#roads_centroids.to_file('02 - Ottawa Road Centroids Opendata with Neighborhoods.geojson', driver='GeoJSON')
roads_centroids[roads_centroids['ONS_ID']==""]


# In[34]:


roads['ONS_ID'] = roads_centroids['ONS_ID'].astype(str)
roads['ONS_NAME'] = roads_centroids['ONS_NAME'].astype(str)

roads.info()

roads.to_file('03 - Ottawa Road Segments Opendata with Neighborhoods.shp', driver='ESRI Shapefile')
#roads.to_file('03 - Ottawa Road Segments Opendata with Neighborhoods.geojson', driver='GeoJSON')


# # 6 Create Road Intersections

# ## 6.1 Create Init, End Road Points and Road Direction

# In[35]:


def create_init_end_points(items):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    items['FIRST_POINT'] = ""
    items['LAST_POINT'] = ""
    items['DIRECTION'] = ""
    items['FIRST_POINT_COORD'] = ""
    items['SINUOSITY'] = ""
    
    first_point = items.columns.get_loc('FIRST_POINT')
    last_point = items.columns.get_loc('LAST_POINT')
    direction = items.columns.get_loc('DIRECTION')
    first_point_coord = items.columns.get_loc('FIRST_POINT_COORD')
    sinuosity = items.columns.get_loc('SINUOSITY')
    shape_length = items.columns.get_loc('SHAPE_Leng')
    
    total = len(items)
    one_per = int(round(total / 100))
    print("Total number of Items to Handle:" + str(total))
    j = 0
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    for index, row in items.iterrows():
        
        if (j == one_per): 
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
        
        
        if row.geometry != None:
        
            segment_coords = list(row['geometry'].coords)
            c0 = segment_coords[0]
            cn = segment_coords[-1]
            
            x0 = c0[0]
            y0 = c0[1]
            
            x1 = cn[0]
            y1 = cn[1]
        
        
            items.iat[index,first_point_coord] = c0
            

            p0 = Point(x0,y0)
            pn = Point(x1,y1)
            
            items.iat[index,first_point] = p0
            items.iat[index,last_point] = pn
        
            if (abs(y1 - y0) > abs(x1 - x0)):
                items.iat[index,direction] = "NS"
            else:
                items.iat[index,direction] = "EW"
        
            # AQUI ROAD SINUOSITY
            
            euclid_dis = math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
            
            length = items.iat[index,shape_length]
            
            if (euclid_dis > 0):
                items.iat[index,sinuosity] = length/euclid_dis
            else:
                items.iat[index,sinuosity] = 1.0
        
           
        j = j + 1
        
    print("  Percentage done: 100%")
    end = datetime.datetime.now().replace(microsecond=0)    
    print("Total Execution Time:" + str(end - start))
    return(items)


# In[36]:


roads = create_init_end_points(roads)
roads.head()


# In[37]:


roads_temp_NS = roads[roads['DIRECTION'] == 'NS']
roads_temp_NS.plot(figsize =(15.0,15.0))


# In[38]:


roads_temp_EW = roads[roads['DIRECTION'] != 'NS']
roads_temp_EW.plot(figsize =(15.0,15.0), color = 'red')


# In[39]:


base = roads_temp_NS.plot(figsize =(15.0,15.0), color = 'blue')
roads_temp_EW.plot(ax = base, color = 'red')


# In[40]:


# Byward Market Area
byward = boundaries[boundaries['Name'] == 'Byward Market']
base = byward.plot(figsize =(15.0,15.0), edgecolor = 'black', color = 'white', linewidth = 0.2)
roads_temp_NS = roads_temp_NS[roads_temp_NS['ONS_NAME'] == 'Byward Market']

roads_temp_NS.plot(ax = base,figsize =(15.0,15.0), color = 'red')
roads_temp_EW = roads_temp_EW[roads_temp_EW['ONS_NAME'] == 'Byward Market']
roads_temp_EW.plot(ax = base, figsize =(15.0,15.0), color = 'blue')


# ## 6.2 Create Intersections

# In[41]:


def create_intersections(items):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    spatial_index = items.sindex
    
    df = pd.DataFrame(columns=['SUBTYPE','SUBCLASS','ROW_NUMBER', 'INTER_NAME', 
                               'INTER_RD_SEGMENT','geometry', 'ONS_ID', 'ONS_NAME'])        
    i = 0
    
    points_coords = pd.unique(items['FIRST_POINT_COORD']).tolist()
    
    total = len(items)
    one_per = int(round(total / 100))
    j = 0
    
    print(" Number of Roads to Validate:" + str(total))
    start_per = datetime.datetime.now().replace(microsecond=0)
    
    for index_items, row_items in items.iterrows():
        
        if (j == one_per): 
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done = round((1 - (total - index_items)/total)*100)
            print(" Percentage done: " + str(per_done) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
            
        
        if row_items.geometry != None:
        
            if row_items['FIRST_POINT_COORD'] in points_coords:
                intersection_name = ""
                road_name = row_items['ROAD_NAME']
                road_segment = row_items['RD_SEGMENT']
                road_row_number = row_items['ROW_NUMBER']
                road_subtype = row_items['SUBTYPE']
                road_subclass = row_items['SUBCLASS'] 
                #road_ons_id = row_items['ONS_ID']
                #road_ons_name = row_items['ONS_NAME'] 
            
                p0 = row_items['FIRST_POINT']
                
            
                buffer_point = p0.buffer(1.0)
            
                buffer_point_bounds = buffer_point.bounds
             
                mask = list(spatial_index.intersection(buffer_point_bounds)) 
            
                items_intersec = items.iloc[mask]
                
                #mask = items.intersects(p0)
                #items_intersec = items[mask]
            
                items_intersec = items_intersec[items_intersec['ROW_NUMBER']!= road_row_number]
                items_intersec = items_intersec[items_intersec['RD_SEGMENT']!= road_segment]
                items_intersec.reset_index(drop=True, inplace=True)
            
                if (len(items_intersec) > 0):
                
                    #print("\nRoad Segment Name= " + str(road_name) + " / " + str(road_segment))
                    #print("    Number of Intersections:"+ str(len(items_intersec)))
                
                    names = pd.unique(items_intersec['ROAD_NAME']).tolist()
                    
                    #m = len(names)
                    #print("     Number of Unique names" + str(m))
                    #print("     Unique names" + str(names))
                
                    if (len(names) == 1):
                        intersection_name = road_name + ' @ ' + names[0]
                        intersection_rd_segment = road_segment + ' @ ' + items_intersec.loc[0,'RD_SEGMENT']
                    else:
                        if names.count(road_name) == 1:
                            names.remove(road_name) 
                            items_intersec = items_intersec[items_intersec['ROAD_NAME']!= road_name]
                            items_intersec.reset_index(drop=True, inplace=True)
                        
                            
                        intersection_name = road_name
                        intersection_rd_segment = road_segment
                
                        names.sort()
                        for x in names:
                            intersection_name = intersection_name + ' @ ' + str(x) 
                            
                            items_temp = items_intersec[items_intersec['ROAD_NAME'] == x]
                            items_temp.reset_index(drop=True, inplace=True)
                            
                            intersection_rd_segment = intersection_rd_segment + ' @ ' + items_temp.loc[0,'RD_SEGMENT']
                
                    #print("Intersection name:" + str(intersection_name))
        
                    df = df.append({'ROW_NUMBER': i, 
                                'SUBTYPE' : road_subtype,
                                'SUBCLASS' : "INTER-" + road_subclass,
                                'INTER_NAME' : intersection_name,
                                'INTER_RD_SEGMENT' : intersection_rd_segment,
                                'geometry' : p0}, ignore_index=True)
                    i = i + 1
            
                points_coords.remove(row_items['FIRST_POINT_COORD'])
        j = j + 1
    print("  Percentage done: 100%")    
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs={'init':'epsg:32189'})
    end = datetime.datetime.now().replace(microsecond=0)    
    print("Total Execution Time:" + str(end - start))
    return(gdf)


# In[42]:


intersections = create_intersections(roads)
intersections.head()


# In[43]:


base = boundaries.plot(figsize =(15.0,15.0), edgecolor = 'black', color = 'white', linewidth = 0.2)
intersections.plot(ax = base,figsize =(15.0,15.0), color = 'red')


# In[44]:


intersections.to_file('04 - Ottawa Intersections Opendata.shp', driver='ESRI Shapefile')
#intersections.to_file('04 - Ottawa Intersections Opendata.geojson', driver='GeoJSON')


# ## 6.3 Match Neighborhoods

# In[45]:


intersections['ONS_ID'] = ""
intersections['ONS_NAME'] = ""

intersections = assing_nearest_area_by_whithin(intersections,boundaries)
intersections.head()


# In[46]:


intersections = assign_nearest_area_by_mindistance(intersections,boundaries)

intersections['ONS_ID'] = intersections['ONS_ID'].astype(str)
intersections['ONS_NAME'] = intersections['ONS_NAME'].astype(str)

intersections.to_file('05 - Ottawa Intersections with Neighborhoods Opendata.shp', driver='ESRI Shapefile')
#intersections.to_file('05 - Ottawa Intersections with Neighborhoods Opendata.geojson', driver='GeoJSON')
intersections[intersections['ONS_ID']==""]


# # 7. Tabular Collision Data (2015-2017)

# ## 7.1 Load Shapefile

# In[47]:


collision_data = gpd.read_file(collision_data_file, index = 'Record')
collision_data.info()
collision_data.head()


# In[48]:


base = boundaries.plot(figsize =(15.0,15.0), edgecolor = 'black', color = 'white', linewidth = 0.2)
collision_data.plot(ax = base,figsize =(15.0,15.0), color = 'red')


# ## 7.2 Collisions Related with Intersections

# In[49]:


#collision_data_inter = gpd.read_file(collision_data_intersections_file, index = 'ROW_NUMBER')
collision_data_inter = collision_data[ (collision_data['Collision_'] == '02 - Intersection related') | 
                                      (collision_data['Collision_'] == '03 - At intersection')]
collision_data_inter.reset_index(drop=True, inplace=True)
collision_data_inter.info()
collision_data_inter.head()


# In[50]:


base = boundaries.plot(color='white', edgecolor='black',figsize =(15.0,15.0),linewidth=0.2)
collision_data_inter.plot(ax = base, color = 'red')


# ## 7.3 Collisions Non-Related with Intersections

# In[51]:


#collision_data_noninter = gpd.read_file(collision_data_nonintersections_file, index = 'ROW_NUMBER')
collision_data_noninter = collision_data[ (collision_data['Collision_'] != '02 - Intersection related') & 
                                      (collision_data['Collision_'] != '03 - At intersection')]
collision_data_noninter.reset_index(drop=True, inplace=True)
collision_data_noninter.info()
collision_data_noninter.head()


# In[52]:


base = boundaries.plot(color='white', edgecolor='black',figsize =(15.0,15.0),linewidth=0.2)
collision_data_noninter.plot(ax = base, color = 'blue')


# ## 7.4 Plot Collision Colored by Type

# In[92]:


base = boundaries.plot(color='white', edgecolor='black',figsize =(15.0,15.0),linewidth=0.2)
collision_data_noninter.plot(ax = base, color = 'blue')
collision_data_inter.plot(ax = base, color = 'red')


# ## 7.5 Match Collisions to Neighborhoods

# ### 7.5.1 Collisions (Intersections)

# In[54]:


collision_data_inter['ONS_ID'] = ""
collision_data_inter['ONS_NAME'] = ""
collision_data_inter = assing_nearest_area_by_whithin(collision_data_inter,boundaries)
collision_data_inter.head()


# In[55]:


collision_data_inter = assign_nearest_area_by_mindistance(collision_data_inter,boundaries)

collision_data_inter['ONS_ID'] = collision_data_inter['ONS_ID'].astype(str)
collision_data_inter['ONS_NAME'] = collision_data_inter['ONS_NAME'].astype(str)

collision_data_inter.to_file('06 - Ottawa Tabular Collision Data Intersections with Neighborhoods Opendata.shp', driver='ESRI Shapefile')
#collision_data_inter.to_file('06 - Ottawa Collision Data Intersections with Neighborhoods Opendata.geojson', driver='GeoJSON')
collision_data_inter[collision_data_inter['ONS_ID']==""]


# ### 7.5.2 Collisions (Non-Intersections)

# In[56]:


collision_data_noninter['ONS_ID'] = ""
collision_data_noninter['ONS_NAME'] = ""
collision_data_noninter = assing_nearest_area_by_whithin(collision_data_noninter,boundaries)
collision_data_noninter.head()


# In[57]:


collision_data_noninter = assign_nearest_area_by_mindistance(collision_data_noninter,boundaries)

collision_data_noninter['ONS_ID'] = collision_data_noninter['ONS_ID'].astype(str)
collision_data_noninter['ONS_NAME'] = collision_data_noninter['ONS_NAME'].astype(str)

collision_data_noninter.to_file('07 - Ottawa Tabular Collision Data Nonintersections with Neighborhoods Opendata.shp', driver='ESRI Shapefile')
#collision_data_noninter.to_file('07 - Ottawa Tabular Collision Data Nonintersections with Neighborhoods Opendata.geojson', driver='GeoJSON')
collision_data_noninter[collision_data_noninter['ONS_ID']==""]


# ### 7.5.3 Collision by Type in Carleton Area

# In[58]:


collision_data_noninter_carleton = collision_data_noninter[collision_data_noninter['ONS_NAME'] == 'Carleton University']
collision_data_inter_carleton = collision_data_inter[collision_data_inter['ONS_NAME'] == 'Carleton University']
roads_carleton = roads[roads['ONS_NAME'] == 'Carleton University']

base = carleton.plot(color='white', edgecolor='black',figsize =(15.0,15.0),linewidth=0.2)
collision_data_noninter_carleton.plot(ax = base, color = 'blue')
collision_data_inter_carleton.plot(ax = base, color = 'red')
roads_carleton.plot(ax = base, color = 'black')


# ## 7.6 Match Collisions (Non-Intersections) to Road Segments using Spatial Index (RTREE)

# In[61]:


def assign_nearest_road_segment_by_mindistance(points, roads):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
        
    spatial_index = roads.sindex

    
    points['ROAD_SUBTYPE'] =""
    points['ROAD_SUBCLASS'] =""
    points['ROAD_SEGMENT'] =""
    points['ROAD_NAME'] =""
    points['ROAD_ROW_NUMBER'] = ""
    
    points['ROAD_SINUOSITY'] = ""
    points['ROAD_LEN'] = ""
    points['ROAD_DIRECTION'] = ""
    
    road_subtype = points.columns.get_loc('ROAD_SUBTYPE')
    road_subclass = points.columns.get_loc('ROAD_SUBCLASS')
    road_segment = points.columns.get_loc('ROAD_SEGMENT')
    road_name = points.columns.get_loc('ROAD_NAME')
    road_row_n = points.columns.get_loc('ROAD_ROW_NUMBER')
    
    road_sinuosity = points.columns.get_loc('ROAD_SINUOSITY')
    road_len = points.columns.get_loc('ROAD_LEN')
    road_direction = points.columns.get_loc('ROAD_DIRECTION')

    total_point = len(points)
    one_per_point = int(round(total_point / 100))
    #print(" One per cent is "+ str(one_per_point))
    print("Total number of Points to Handle:" + str(total_point))
    j = 0
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    
    for index_point, row_point in points.iterrows():
        
        if (j == one_per_point): 
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done_point = round((1 - (total_point - index_point)/total_point)*100)
            print(" Percentage done: " + str(per_done_point) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
        
        
        if row_point.geometry != None:
        
            buffer_point = row_point['geometry'].buffer(100.0)
            
            buffer_point_bounds = buffer_point.bounds
             
            mask_roads_around= list(spatial_index.intersection(buffer_point_bounds)) 
            
            roads_around = roads.iloc[mask_roads_around]
                
            #mask_roads_around = roads['geometry'].intersects(buffer_point)
        
            #roads_around = roads[mask_roads_around]
        
            if (len(roads_around) > 0):
                d = roads_around.distance(row_point.geometry)
                d_min = d.min()
            
                road_id = d[d==d_min].index[0]
        
                closest_road = roads.iloc[road_id]
        
                #print("Name of the Closes Road:" + str(closest_road['ROAD_NAME']) + str(closest_road['RD_SEGMENT']))
        
                points.iat[index_point,road_subtype] = closest_road['SUBTYPE']
                points.iat[index_point,road_subclass] = closest_road['SUBCLASS']
            
                points.iat[index_point,road_segment] = closest_road['RD_SEGMENT']
                points.iat[index_point,road_name] = closest_road['ROAD_NAME']
                points.iat[index_point,road_row_n] = closest_road['ROW_NUMBER']
                
                points.iat[index_point,road_sinuosity] = closest_road['SINUOSITY']
                points.iat[index_point,road_len] = closest_road['SHAPE_Leng']
                points.iat[index_point,road_direction] = closest_road['DIRECTION']
                
        j= j+1

    print("  Percentage done: 100%")
    end = datetime.datetime.now().replace(microsecond=0)    
    print("Total Execution Time:" + str(end - start))
    
    return(points)


# In[62]:


collision_data_noninter = assign_nearest_road_segment_by_mindistance(collision_data_noninter, roads)
collision_data_noninter.head()


# In[63]:


collision_data_noninter[collision_data_noninter['ROAD_NAME'] == ""]


# In[64]:


collision_data_noninter['ROAD_SUBTYPE'] = collision_data_noninter['ROAD_SUBTYPE'].astype(str)
collision_data_noninter['ROAD_SUBCLASS'] = collision_data_noninter['ROAD_SUBCLASS'].astype(str)
collision_data_noninter['ROAD_SEGMENT'] = collision_data_noninter['ROAD_SEGMENT'].astype(str)
collision_data_noninter['ROAD_NAME'] = collision_data_noninter['ROAD_NAME'].astype(str)
collision_data_noninter['ROAD_ROW_NUMBER'] = collision_data_noninter['ROAD_ROW_NUMBER'].astype(str)

collision_data_noninter.to_file('08 - Ottawa Tabular Collision Data Nonintersections with Neighborhoods and Road Segments Opendata.shp', driver='ESRI Shapefile')
#collision_data_noninter.to_file('08 - Ottawa Tabular Collision Data Nonintersections with Neighborhoods and Road Segments Opendata.geojson', driver='GeoJSON')


# ## 7.7 Match Collisions (Intersections) to Roads Intersections

# In[ ]:


def assign_nearest_intersection_segment_by_mindistance(points, roads):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    spatial_index = roads.sindex
    
    points['ROAD_SUBTYPE'] =""
    points['ROAD_SUBCLASS'] =""
    points['ROAD_SEGMENT'] =""
    points['ROAD_NAME'] =""
    points['ROAD_ROW_NUMBER'] = ""
    
    points['ROAD_SINUOSITY'] = 1.0
    points['ROAD_LEN'] = 1.0
    points['ROAD_DIRECTION'] = "NA"
    
    road_subtype = points.columns.get_loc('ROAD_SUBTYPE')
    road_subclass = points.columns.get_loc('ROAD_SUBCLASS')
    road_segment = points.columns.get_loc('ROAD_SEGMENT')
    road_name = points.columns.get_loc('ROAD_NAME')
    road_row_n = points.columns.get_loc('ROAD_ROW_NUMBER')
    
    total_point = len(points)
    one_per_point = int(round(total_point / 100))
    #print(" One per cent is "+ str(one_per_point))
    print("Total number of Points to Handle:" + str(total_point))
    j = 0
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    
    for index_point, row_point in points.iterrows():
        
        #print("Punto ID" + str(row_point['ROW_ID']))
        
        if (j == one_per_point): 
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done_point = round((1 - (total_point - index_point)/total_point)*100)
            print(" Percentage done:" + str(per_done_point) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
        
        
        if row_point.geometry != None:
            
            
            buffer_point = row_point['geometry'].buffer(100.0)
            
            buffer_point_bounds = buffer_point.bounds
            
            mask_roads_around= list(spatial_index.intersection(buffer_point_bounds)) 
            
            roads_around = roads.iloc[mask_roads_around]
            
            if (len(roads_around) > 0):
        
                d = roads_around.distance(row_point.geometry)
                d_min = d.min()
            
                road_id = d[d==d_min].index[0]
        
                closest_road = roads.iloc[road_id]
        
                #print("Name of the Closes Road:" + str(closest_road['ROAD_NAME']) + str(closest_road['RD_SEGMENT']))
        
                points.iat[index_point,road_subtype] = closest_road['SUBTYPE']
                points.iat[index_point,road_subclass] = closest_road['SUBCLASS']
            
                points.iat[index_point,road_segment] = closest_road['INTER_RD_SEGMENT']
                points.iat[index_point,road_name] = closest_road['INTER_NAME']
                points.iat[index_point,road_row_n] = closest_road['ROW_NUMBER']
                
                #points.iat[index_point,road_sinuosity] = closest_road['SINUOSITY']
                #points.iat[index_point,road_len] = closest_road['SHAPE_Leng']
                #points.iat[index_point,road_direction] = closest_road['DIRECTION']
        j= j+1
        
        
    print("  Percentage done: 100")
    end = datetime.datetime.now().replace(microsecond=0)    
    print("Total Execution Time:" + str(end - start))
    return(points)


# In[65]:


collision_data_inter = assign_nearest_intersection_segment_by_mindistance(collision_data_inter, intersections)
collision_data_inter.head()


# In[66]:


collision_data_inter[collision_data_inter['ROAD_NAME'] == ""]


# In[67]:


collision_data_inter['ROAD_SUBTYPE'] = collision_data_inter['ROAD_SUBTYPE'].astype(str)
collision_data_inter['ROAD_SUBCLASS'] = collision_data_inter['ROAD_SUBCLASS'].astype(str)
collision_data_inter['ROAD_SEGMENT'] = collision_data_inter['ROAD_SEGMENT'].astype(str)
collision_data_inter['ROAD_NAME'] = collision_data_inter['ROAD_NAME'].astype(str)
collision_data_inter['ROAD_ROW_NUMBER'] = collision_data_inter['ROAD_ROW_NUMBER'].astype(str)

collision_data_inter.to_file('09 - Ottawa Tabular Collision Data Intersections with Neighborhoods and Intersections Segments Opendata.shp', driver='ESRI Shapefile')
#collision_data_inter.to_file('09 - Ottawa Tabular Collision Data Intersections with Neighborhoods and Intersections Segments Opendata.geojson', driver='GeoJSON')


# # 8. Ottawa City Limits Tiles

# In[68]:


city_limits_tiles = gpd.read_file(city_limits_tiles, index = 'TILE_ID')

city_limits_tiles.info()
city_limits_tiles.head()


# In[69]:


city_limits_tiles.plot(color='white', edgecolor='black',figsize =(15.0,15.0),linewidth=0.4)


# ## 8.1 Match Collisions with a Tile 

# In[70]:


def assing_nearest_tile_by_whithin(items, tiles):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
    
    #spatial_index = tiles.sindex
    
    tile_id = items.columns.get_loc('TILE_ID')

    total = len(items)
    print("Number of items to Assign:" + str(total))
 
    start_iter = datetime.datetime.now().replace(microsecond=0)

    for index, row in tiles.iterrows():
 
        if (index != 0):
            print("Iteration Time:" + str(end_iter - start_iter))
            start_iter = datetime.datetime.now().replace(microsecond=0)
            
        print("Checking Items for Tile Area:" + str(row['TILE_ID']))
        items_temp = items[items['TILE_ID'] == ""]
        total_now = len(items_temp)
        
        per_no_assigned = (1 - (total - total_now) / total) * 100
        per_assigned = (100 - per_no_assigned)
        
        print("  Number of Items No Assigned (Empty TILE_ID):" + str(total_now) + " %:" + str(per_no_assigned))
        
        if row.geometry != None:
            
            mask = items_temp.within(row['geometry'])
        
            items_in = items_temp[mask]
            
            print("  Number of Items to be Assigned (Match Current Tile):"+ str(len(items_in)))
        
            for index2, row2 in items_in.iterrows():
                items.iat[index2,tile_id] = row['TILE_ID']
        
        end_iter = datetime.datetime.now().replace(microsecond=0)
    
    end = datetime.datetime.now().replace(microsecond=0)
    
    print("Total Execution Time:" + str(end - start))
            
    return(items)


# ## 8.2 Match Collisions (Non-Intersections) to a Tile

# In[71]:


collision_data_noninter['TILE_ID'] = ""
collision_data_noninter = assing_nearest_tile_by_whithin(collision_data_noninter,city_limits_tiles)
collision_data_noninter.head()


# In[72]:


def assign_nearest_tile_by_mindistance(points, tiles):
    
    start = datetime.datetime.now().replace(microsecond=0)
    print("Start Time:"+str(start))
        
    spatial_index = tiles.sindex
    
    item_tile_id = points.columns.get_loc('TILE_ID')

        
    total_point = len(points)
    one_per_point = int(round(total_point / 100))
    #print(" One per cent is "+ str(one_per_point))
    print("Total number of Points to Handle:" + str(total_point))
    j = 0
    
    start_per = datetime.datetime.now().replace(microsecond=0)
    
    points_temp = points[points['TILE_ID'] == ""]
    
    for index_point, row_point in points_temp.iterrows():
        
        if (j == one_per_point): 
            end_per = datetime.datetime.now().replace(microsecond=0)
            per_done_point = round((1 - (total_point - index_point)/total_point)*100)
            print(" Percentage done: " + str(per_done_point) + str("% in ") + str(end_per - start_per))
            j = 0
            start_per = datetime.datetime.now().replace(microsecond=0)
        
        
        if row_point.geometry != None:
        
            buffer_point = row_point['geometry'].buffer(100.0)
            
            buffer_point_bounds = buffer_point.bounds
             
            mask_tiles_around= list(spatial_index.intersection(buffer_point_bounds)) 
            
            tiles_around = roads.iloc[mask_tiles_around]
                
        
            if (len(tiles_around) > 0):
                d = tiles_around.distance(row_point.geometry)
                d_min = d.min()
            
                tile_id = d[d==d_min].index[0]
        
                closest_tile = tiles.iloc[tile_id]
        
                points.iat[index_point,item_tile_id] = closest_tile['TILE_ID']
            
                
        j= j+1

    print("  Percentage done: 100%")
    end = datetime.datetime.now().replace(microsecond=0)    
    print("Total Execution Time:" + str(end - start))
    
    return(points)


# In[73]:


collision_data_noninter = assign_nearest_tile_by_mindistance(collision_data_noninter,city_limits_tiles)
collision_data_noninter.head()


# In[74]:


collision_data_noninter[collision_data_noninter['TILE_ID'] == ""].head()


# In[75]:


collision_data_noninter.to_file('10 - Ottawa Tabular Collision Data Nonintersections with Neighborhoods - Road Segments and Tiles Opendata.shp', driver='ESRI Shapefile')


# ## 8.3 Match Collisions (Intersections) to a Tile 

# In[76]:


collision_data_inter['TILE_ID'] = ""
collision_data_inter = assing_nearest_tile_by_whithin(collision_data_inter,city_limits_tiles)
collision_data_inter.head()


# In[77]:


collision_data_inter = assign_nearest_tile_by_mindistance(collision_data_inter,city_limits_tiles)
collision_data_inter.head()


# In[78]:


collision_data_inter[collision_data_inter['TILE_ID'] == ""].head()


# In[79]:


collision_data_inter.to_file('11 - Ottawa Tabular Collision Data Intersections with Neighborhoods - Intersections Segments and Tiles Opendata.shp', driver='ESRI Shapefile')


# # 8.4 Save Collision GeoDataFrame (Intersection and Non-intersections) to cvs

# In[110]:


df1 = pd.DataFrame(collision_data_inter.drop('geometry', axis=1), copy=True)
df2 = pd.DataFrame(collision_data_noninter.drop('geometry', axis=1), copy=True)

df = df1.append(df2)


df.rename(inplace=True, 
          columns={"Record": "ROW_ID", 
                   "Location": "LOCATION",
                   "LocationA": "LOCATION_A",
                   "LocationB": "LOCATION_B",
                   "X": "XCOORD",
                   "Y": "YCOORD",
                   "Date": "ACCIDENT_DATE",
                   "Time": "ACCIDENT_TIME",
                   "Environmen": "ENVIRONMENT_CONDITION",
                   "Road_Surfa": "ROAD_SURFACE_CONDITION",
                   "Traffic_Co": "TRAFFIC_CONTROL",
                   "Collision_" : "ACCIDENT_LOCATION",
                   "Light" : "LIGHT",
                   "Collisio_1": "CLASSIFICATION_OF_ACCIDENT",
                   "Impact_typ" : "IMPACT_TYPE",
                   "Longitude" : "LONGITUDE",
                   "Latitude" : "LATITUDE",
                   "Date_Time": "ACCIDENT_DATE_TIME"
            })
df.info()
df.to_csv("Ottawa Tabular Collision Data 2015-2017 - ALL FEATURES.csv", index = False)


# In[111]:


df.head()


# ## TEST

# In[94]:


point = collision_data_noninter[collision_data_noninter['Record'] == 38017]
point.reset_index(drop=True, inplace=True)

line = roads[roads['ROW_NUMBER'] == 16625]
line.reset_index(drop=True, inplace=True)

print("Number of Lines:" + str(len(line)))
print("Number de Points:" + str(len(point)))

point_buffer = point.buffer(10.0)

x = line.intersects(point_buffer)

print(x)

base = point.plot(figsize =(15.0,15.0),color = 'blue')
point_buffer.plot(ax = base)
line.plot(ax = base, color = 'red')


# In[81]:


highway = roads[roads['SUBCLASS'] == 'HIGHWAY']
base = highway.plot(figsize =(15.0,15.0),color = 'red')

ramp = roads[roads['SUBCLASS'] == 'RAMP']
ramp.plot(ax = base, figsize =(15.0,15.0),color = 'blue')

intersections = gpd.sjoin(highway, highway, how = 'inner' , op = 'intersects')
intersections.plot(figsize =(15.0,15.0))


# ## Tiles Neighborhood

# In[82]:


city_limits_tiles_centroid = city_limits_tiles.copy()
city_limits_tiles_centroid.geometry = city_limits_tiles.centroid

city_limits_tiles_centroid['ONS_ID'] = ""
city_limits_tiles_centroid['ONS_NAME'] = ""

city_limits_tiles_centroid = assing_nearest_area_by_whithin(city_limits_tiles_centroid,boundaries)
city_limits_tiles_centroid.head()


# In[83]:


city_limits_tiles['ONS_ID'] = city_limits_tiles_centroid['ONS_ID']
city_limits_tiles['ONS_NAME'] = city_limits_tiles_centroid['ONS_NAME']


# In[84]:


base = boundaries[boundaries['Name']== 'Carleton University'].plot(figsize =(15.0,15.0))
city_limits_tiles[city_limits_tiles['ONS_NAME'] == 'Carleton University'].plot(ax = base, color='white', edgecolor='black',figsize =(15.0,15.0),linewidth=0.4)

