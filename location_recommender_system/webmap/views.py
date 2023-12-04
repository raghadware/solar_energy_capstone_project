from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import sqlite3
import random
import pickle

base_dir = settings.BASE_DIR

con = sqlite3.connect(base_dir/'db.sqlite3')

df = pd.read_sql_query("SELECT * from sa_final", con).reset_index(drop=True)

geom = gpd.points_from_xy(df['lon'], df['lat'], crs='EPSG:4326')
gdf = gpd.GeoDataFrame(df, geometry=geom, crs=geom.crs).to_crs('EPSG:4087')

scaler_uri = base_dir/'utils/raghad_scaler.pkl'
kmeans_uri = base_dir/'utils/raghad_kmeans_20.pkl'

with open(scaler_uri, 'rb') as file:  
    scaler = pickle.load(file)

with open(kmeans_uri, 'rb') as file:  
    kmeans = pickle.load(file)

gdf['labels'] = kmeans.labels_

def generate_random_points(gdf, k, d):
    d *= 1000 #convert distance to metres
    """
    Generate k random points from the input GeoDataFrame with a minimum distance of d.

    Parameters:
    - gdf (GeoDataFrame): Input GeoDataFrame containing point geometries.
    - k (int): Number of random points to generate.
    - d (float): Minimum distance between points.

    Returns:
    - random_points (GeoDataFrame): GeoDataFrame containing k random points.
    """
    random_points = []
    
    # Iterate until k points are generated
    while len(random_points) < k:
        # Randomly select a point from the GeoDataFrame
        random_point = gdf.sample(1)
        
        # Check if the distance between the random_point and existing points is at least d
        if all(random_point.geometry.distance(point).min() >= d for point in random_points):
            random_points.append(random_point)
    
    # Create a GeoDataFrame from the selected points
    random_points_gdf = gpd.GeoDataFrame(random_points, geometry='geometry')
    
    return random_points_gdf

   

def recommend_locations(input_lat, input_long, num_recommendations, max_distance_km):
       """
       Recommends locations based on similarity, excluding those within a specified distance.

       Parameters:
       - input_lat (float): Latitude of the input location.
       - input_long (float): Longitude of the input location.
       - num_recommendations (int): Number of locations to recommend. Default is 5.
       - max_distance_km (float): Maximum distance in kilometers for recommended locations. Default is 10.

       Returns:
       - recommendations (DataFrame): DataFrame containing recommended locations and their attributes.
       """
       input_loc = gpd.GeoSeries(Point(input_long,input_lat), crs='EPSG:4326').to_crs(gdf.crs)[0]
       
       index_of_nearest = gdf.distance(input_loc).idxmin()
       
       nearest_loc = gdf.iloc[index_of_nearest, :]
       cols = ['PVOUT_csi', 'DNI', 'GHI', 'DIF','GTI_opta', 'OPTA', 'TEMP','ELE']

       nearest_scaled = scaler.transform([nearest_loc[cols].values])
       
       cluster = kmeans.predict(nearest_scaled)
       target = gdf[gdf['labels'] == cluster[0]]
       
    #    target = target[(target.distance(input_loc)/1000) > max_distance_km]
       s = random.choices(target.index, k=num_recommendations)
       
       return target.loc[s, :]

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def recommend(request):
       input_lat, input_long = request.GET.get('lat'), request.GET.get('lon')
       num_recommendations = request.GET.get('num_recommendations', 5)
       minimum_distance = request.GET.get('minimum_distance', 50)
       
       recommendations = recommend_locations(
          input_lat, input_long, num_recommendations, minimum_distance)
       
       return HttpResponse(recommendations.loc[:, recommendations.columns != 'geometry'].to_json(orient='index'))