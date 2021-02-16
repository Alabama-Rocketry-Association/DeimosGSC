import requests

class rocket:
    startTime = 0.0
    #motor
    burnTime = 4.6
    mass = 50
    propMass = 2.9  #kg
    cluster = 1
    impulse = 5506.5    #(N*s)
    totalImpulse = cluster * impulse
    totalPropMass = propMass * cluster
    jonConst = totalImpulse / totalPropMass
    #drag
    baseArea = 0.0003236547

class logData:
    t = 0
    dt = 0.01
    AVS_Temp = ([0, 0, 0], [0, 0, 0], [0, 0, 10])
    #                Ae, An, Au      Ve, Vn, Vu      Se, Sn, Su
    AVS_Store = [   [[],[],[]],     [[],[],[]],     [[],[],[]]   ]
    k1 = [0, 0, 0]
    k2 = [0, 0, 0]
    k3 = [0, 0, 0]
    k4 = [0, 0, 0]
    THRUST = 0
    ACCELERATION = 0
    DRAG = 0.0

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

#Aero Specs
dTdh = 6/1000     #Kelvin / Meter
R = 8.314   #N*m / mol * K
M_air = 0.0289644   #Molar mass of Earth's air
g = -9.81    #gravity (m/s^2)
R_spec = R/M_air
T_lapse = 0.00976   #K/m
########