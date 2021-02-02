import math
import numpy as np
import scipy
from scipy import integrate
from matplotlib import pyplot as plt
import pandas as pd
from mpl_toolkits import mplot3d
import requests
import json
import time

#38.2527° N, 85.7585° W -- Louisville
#33.2098° N, 87.5692° W -- Tuscaloosa
#32.9904° N, 106.9750° W -- Spaceport America

lat = "32.99"	#lattitude, USE POSITIVE FOR NORTH
lon = "-106.98"	#longitude, USE NEGATIVE FOR WEST

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
print("Location: ", location)
print("Wind: ", windSpeed)
print("Temp: ", ambientTemp)
print("Ambient Pressure: ", ambientPressure)

#######################
#end of weather request
#######################

#MECHANICAL FUNCTIONS

def RK4(f, x, y, dx):   #4th-order Runge-Kutta integration
    k1 = f(x, y)
    k2 = f(x + 0.5*dx, y + 0.5*k1*dx)
    k3 = f(x + 0.5*dx, y + 0.5*k2*dx)
    k4 = f(x + dx, y + k3*dx)
    y = y + ((k1 + 2*k2 + 2*k3 + k4)*dx/6)
    return y

def thrust(t, burnTime, c0, c1, c2, c3, c4, c5, c6, **kwargs):   #calculate thrust offered by motor at any time after ignition
    if (t < burnTime):
        return (c6*t**6 + c5*t**5 + c4*t**4 + c3*t**3 + c2*t**2 + c1*t + c0)
    else:
        return 0.00

def rocketMass(launchMass, thrust, jonConst, **kwargs):
    return launchMass - thrust / jonConst

###########
# Drag Functions
###########
def drag(rho, vel, area, C_d = 0.5):        #C_d = 0.5 for a cone
    return (C_d*(1/2)*(rho)*(vel**2)*(area))

def p_atm(h):       #air pressure profile by altitude (Pa)
    carsaroni = (M_air * g) / (R * T_lapse)       #unsure if g should be positive or negative (g is hardcoded as negative)
    return ((ambientTemp / temp(h))**carsaroni) * ambientPressure  #carson i love you - passionately

def density(h):
    return p_atm(h) / (temp(h) * R_spec)

def temp(h):        #air temperature profile by altitude
    return ambientTemp - dTdh*h

###########
#END OF FUNCTIONS
###########

###########
#MACHINE LEARNING (Polynomial Regression)
###########

#import dataset
dataset = pd.read_csv('Cesaroni_5506M1230-P.csv')
X = dataset.iloc[4:, 0:1].values
y = dataset.iloc[4:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=0)

# Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

# Fitting Linear Regression to the dataset
from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X, y)

# Fitting Polynomial Regression to the dataset
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree=6)
X_poly = poly_reg.fit_transform(X)
pol_reg = LinearRegression()
pol_reg.fit(X_poly, y)

thrustDict = {}
burnTime = 4.6
dt = 0.01
t = 0

while (t < burnTime):
    if ((pol_reg.predict(poly_reg.fit_transform([[t]]))[0]) < 0):
        thrustDict[str(t)] = 0
    else:
        thrustDict[str(t)] = 3 * pol_reg.predict(poly_reg.fit_transform([[t]]))[0]      #change 3 to kwargs['cluster']
    t += dt

lists = sorted(thrustDict.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.plot(x, y)
#plt.show()

##########
#END OF ML
##########

#this is the azimuth direction as a unit vector (e, n, u)
direction = [3/7.07, 4/7.07, 5/7.07]    #3-4-5 triangle
direction = [0.0872, 0, 0.9962]     #85-degrees east
negdirection = [0, 0, 0]    #initialized to zero
V_abs = 0       #initialized to zero

#step size up front
dt = 0.01
t = 0

kwargs = {
    "t"  : 0,
    "h"  : 0.50,
    "dt" : 0.50,
    #The following are respective to the local coordinate system
    "Ae" : 0,
    "An" : 0,
    "Au" : 0,
    "Ve" : 0,
    "Vn" : 0,
    "Vu" : 0,
    "Se" : 0,
    "Sn" : 0,
    "Su" : 0,
    #constants in the six-degree polynomial. global so its easier to change
    "c0" : -23.528,
    "c1" : 6587.4,
    "c2" : -8901.7,
    "c3" : 5369.7,
    "c4" : -1607.9,
    "c5" : 232.9,
    "c6" : -13.113,
    #motor stats
    "startTime" : 0,
    "burnTime" : 4.6,     #burn time of the motor (s)
    "mass" : 50,    #gross estimate
    "cluster" : 3,      #the number of motors in the cluster
    #DRAG (AKA "Rocket Specs Shit")
    "Base Area" : 0.0003236547,      #area of rocket head
    "DRAG" : 0,     #must be initialized to zero (since zero velocity at t = 0)
    "thrustVals" : thrustDict
}

#motor stats
burnTime = 4.6      #burn time of the motor (s)
impulse = 5500  #total impulse of each motor
totalImpulse = kwargs["cluster"] * impulse
propMass = kwargs["cluster"] * 3.00   #mass of motor propellant (kgs)
jonConst = totalImpulse / propMass

#Aero Specs
dTdh = 6/1000     #Kelvin / Meter
R = 8.314   #N*m / mol * K
M_air = 0.0289644   #Molar mass of Earth's air
g = -9.81    #gravity (m/s^2)
R_spec = R/M_air
T_lapse = 0.00976   #K/m
########

############################################
#the following begins the integration method
############################################
#this list of lists of lists holds each value generated by the RK4
#used mostly for plotting at the end; this may or may not stick around to the final product

#              Ae, An, Au      Ve, Vn, Vu      Se, Sn, Su
AVS_Store = [   [[],[],[]],     [[],[],[]],     [[],[],[]]   ]
t = 0   #try to get rid of this
AVS_Temp = ([0, 0, 0], [0, 0, 0], [0, 0, 10])     #ae, an, au, ve, vn, vu, se, sn, su -- this triple holds the temporary AVS vectors
#vectors to store K values
k1 = [0, 0, 0]
k2 = [0, 0, 0]
k3 = [0, 0, 0]
k4 = [0, 0, 0]
fucks_given = 0
while (AVS_Temp[2][2]>= 0):      #while height >= 0
    for i in range(0, 3):       #iterate through A, V, S
        if i == 0:     #for acceleration vector
            if (t < burnTime):     #while motor is burning
                kwargs["THRUST"] = kwargs["thrustVals"][str(t)]     #find thrust at time t
                kwargs["mass"] = kwargs["mass"] - (kwargs["THRUST"] * dt / jonConst)     #find mas at time t
                kwargs["ACCELERATION"] = kwargs["THRUST"] / kwargs["mass"]      #acceleration at time t = thrust(t) / mass
                V_mag = np.linalg.norm(AVS_Temp[1])     #find magnitude of velocity vector
                if (V_mag > 0 and t > 0.25):  # since this value is a denominator, it cannot be zero
                    for d in range(0, 3):  # calculate the direction vector and its negative
                        direction[d] = (1 / V_mag) * AVS_Temp[1][d]
                        negdirection[d] = -1 * direction[d]
                kwargs["DRAG"] = drag(density(AVS_Temp[2][2]), V_mag, kwargs["Base Area"])      #calculate drag     #need to add C_d
                for j in range(0,3):    #iterate through acceleration vector
                    AVS_Temp[i][j] = direction[j] * kwargs["ACCELERATION"]   #implement unit vector of direction
                    AVS_Temp[i][j] = AVS_Temp[i][j] + negdirection[j] * kwargs["DRAG"]
                    if j == 2 :     #for gravity always acting on "up" (z axis)
                        AVS_Temp[i][j] = AVS_Temp[i][j] + g
                        AVS_Store[i][j].append(AVS_Temp[i][j])
            else :  #after motor burnout, acceleration is (0, 0, -9.81) m/s^2
                AVS_Temp[0][0] = 0
                AVS_Temp[0][1] = 0
                AVS_Temp[0][2] = g
                AVS_Store[0][2].append(AVS_Temp[0][2])
                V_mag = np.linalg.norm(AVS_Temp[1])     #find magnitude of velocity vector
                if (V_mag > 0):     #since this value is a denominator, it cannot be zero
                    for d in range(0,3):    #calculate the direction vector and its negative
                        direction[d] = (1/V_mag)*AVS_Temp[1][d]
                        negdirection[d] = -1 * direction[d]
                kwargs["DRAG"] = drag(density(AVS_Temp[2][2]), V_mag, kwargs["Base Area"])  # calculate drag    #need to add C_d
                for j in range(0,3):
                    AVS_Temp[i][j] = AVS_Temp[i][j] + negdirection[j] * kwargs["DRAG"]
        else :      #for velocity and position vectors
            for j in range(0,3):    #integrated runge kutta to solve Ve, Vn, Vu, Se, Sn, Su
                k1[j] = AVS_Temp[i-1][j]
                k2[j] = AVS_Temp[i-1][j] + k1[j] * (dt/2)
                k3[j] = AVS_Temp[i-1][j] + k2[j] * (dt/2)
                k4[j] = AVS_Temp[i-1][j] + k3[j] * dt
                val = (1/6)*(k1[j] + 2*k2[j] + 2*k3[j] + k4[j])*dt
                AVS_Temp[i][j] = AVS_Temp[i][j] + val
                AVS_Store[i][j].append(AVS_Temp[i][j] + val)
                #print(i)
    t = t+dt

#########
#PLOTTING
#first index indicates plotting A, V, S (0, 1, 2 respectively)

xLine = AVS_Store[2][0]
yLine = AVS_Store[2][1]
zLine = AVS_Store[2][2]
fig = plt.figure()
ax = plt.axes(projection = '3d')
ax.plot3D(xLine, yLine, zLine, 'blue')
plt.show()
