import requests
import json
import time

#38.2527° N, 85.7585° W -- Louisville

lat = "38.25"	#lattitude
lon = "85.76"	#longitude

url = "https://community-open-weather-map.p.rapidapi.com/weather"

querystring = {"lat": lat,"lon": lon,"units":"%22metric%22 or %22imperial%22"}

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key': "c77d50ffccmsh9acd866d873847ap1cd369jsn9c737f94c410"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data = response.json()
print(data)

#coord = data["coord"]
#wind = data["wind"]
#print("Coordinates: ", coord)
#print("Wind: ", wind)
