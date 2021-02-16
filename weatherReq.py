import requests
import json

#38.2527° N, 85.7585° W -- Louisville
#33.2098° N, 87.5692° W -- Tuscaloosa
#32.9904° N, 106.9750° W -- Spaceport America

class weatherData():
    lat = "33.2098"	#lattitude, USE POSITIVE FOR NORTH
    lon = "-97.5692"	#longitude, USE NEGATIVE FOR WEST
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"lat": lat,"lon": lon,"units":"%22metric%22 or %22imperial%22"}
    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "c77d50ffccmsh9acd866d873847ap1cd369jsn9c737f94c410"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    location = data["name"]
    ambientTemp = data["main"]["temp"]  #KELVIN
    windSpeed = data["wind"]["speed"]
    windDirection = data["wind"]["deg"]
    ambientPressure = 100 * data["main"]["pressure"]      #HECTOPASCHALS (multiply by 100 to yield Pa)
    humidity = data["main"]["humidity"]
    
    def __init__(self, coord):  #pass a tuple with coordinates 
        self.lat = coord[0]
        self.lon = coord[1]
