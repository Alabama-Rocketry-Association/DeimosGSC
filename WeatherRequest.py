import requests
import json
import time

lat = ""	#lattitude
lon = ""	#longitude

url = "https://community-open-weather-map.p.rapidapi.com/weather"

querystring = {"lat": lat,"lon": lon,"callback":"test","units":"%22metric%22 or %22imperial%22"}

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key': "c77d50ffccmsh9acd866d873847ap1cd369jsn9c737f94c410"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)