import random
from flask import Flask, jsonify
from global_land_mask import globe
import reverse_geocoder as rg
import requests
import numpy as np

app = Flask(__name__)

def random_lat():
    lat = round(random.uniform( -85,  85), 1)
    return lat

def random_long():
    long = round(random.uniform(-180, 180), 1)
    return long

def reverse_geocode(lat, long):
    coords = (lat, long)
    location_data = rg.search(coords)
    return location_data

def coord_wave_height(lat, long):
    coords = (lat, long)
    wave_height = globe.get_wave_height(coords)
    return wave_height


@app.route("/rand_coords")
def rand_coords():
    
    lat = random_lat()
    long = random_long()
    
    coords = {
            'latitude': lat,
            'longitude': long,
            'is_in_ocean': str(globe.is_ocean(lat, long)),
    }
        
    return jsonify(coords)


@app.route("/rand_ocean_coords")
def rand_ocean_coords():
    
    lat = random_lat()
    long = random_long()
    
    while globe.is_ocean(lat, long) == False:
        lat = random_lat()
        long = random_long()
    
    coords = {'latitude': lat,
              'longitude': long,
              'is_in_ocean': str(globe.is_ocean(lat, long))}
        
    return jsonify(coords)


@app.route("/rand_land_coords")
def rand_land_coords():
    
    lat = random_lat()
    long = random_long()
    
    while globe.is_ocean(lat, long) == True:
        lat = random_lat()
        long = random_long()
    
    coords = {'latitude': lat,
              'longitude': long,
              'is_in_ocean': str(globe.is_ocean(lat, long)),
              'location': reverse_geocode(lat, long)[0]['cc']
              }
        
    
    return jsonify(coords)



#Down
@app.route("/rand_wave_height")
def rand_wave_height():
    
    lat = str(random_lat())
    long = str(random_long())
    headers = {'Authorization': 'e904ad00-b9b7-11ec-8e08-0242ac130002-e904ad78-b9b7-11ec-8e08-0242ac130002'}
    url = 'https://api.stormglass.io/v2/weather/point'
    
    
    
    response = requests.get(url,
    params={
        'lat': 58.7984,
        'lng': 17.8081,
        'params': 'waveHeight',
    },
    headers=headers
    )
    
    return response.json()