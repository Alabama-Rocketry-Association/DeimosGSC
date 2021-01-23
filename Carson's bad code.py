import math
import numpy as np
import scipy
from scipy import integrate
from matplotlib import pyplot as plt
import pandas as pd

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

def rocketMass(t, z, dt):
    return launchMass - thrust / jonConst

def acceleration(THRUST, mass, **kwargs):
    return THRUST / mass

def dVelocity(ACCELERATION, dt, **kwargs):    #Note: this is the delta velocity, not the acceleration
    return ACCELERATION * dt

def dPosition(VELOCITY, dt, **kwargs):
    return VELOCITY * dt

T_0 = 288.16  #Temp initial (ground)
a = 6.5/1000  #Temp change by alt
n = 5.2561    #some bullshit constant i dont even know bro
P_0 = 101325 #pressure (kPa)
#p_0 = 1.225   #air density rho (kg/m^3)
R = 8.314      #(N*m/molK)
M = 0.0289644 # molar Mass of earth's air (kg/mol)
g = 9.81      #gravity earth (m/s^2)
Rspec = R/M   #R specific
L = 0.00976  #(K/m) temperature lapse rate

#Dragging SHIT
def temp(h):        #air temperature profile by altitude
    return T_0 - a*h
def atm(h):         #air pressure profile by altitude
    carsaroni = (M*g)/(R*L)
    return ((T_0 / temp(h))**carsaroni) * P_0  #carson i love you - passionately
def density(h):     #air density profile by altitude
    return atm(h) / (temp(h)*Rspec)
#def latArea(theta = 0):
    #return latCross * math.cos(theta)
def drag(rho, vel, area):
    return (0.5*(1/2)*(rho)*(vel**2)*(area)) #extra 0.5 is Cd for nose cone only (0 angle of attack)

#motor stats
burnTime = 12.4      #burn time of the motor (s)
startTime = 0
endTime = burnTime + 10    #how long the for loop is gonna run for (s)
totalImpulse = 10133
motorMass = 8.492   #mass of motor case + propellant (kgs)
propMass = 4.892   #mass of motor propellant (kgs)
jonConst = totalImpulse / propMass
#rocket stats
dryMass = 15.258     #mass of the rocket (kgs)
launchMass = dryMass + motorMass

#step size up front
h = 0.05
t = 0
dt = h


kwargs = {
    "t"  : 0,
    "h"  : 0.50,
    "dt" : 0.50,
    #Rocket Specs Shit
    "Base Area" : 0.0003236547,
    "DRAG" : 0,
    #Coordinate Local Fuck me daddy
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
    "c0" : 712.75,
    "c1" : 1900.2,
    "c2" : -1346.9,
    "c3" : 384.66,
    "c4" : -52.941,
    "c5" : 3.4619,
    "c6" : -0.0863,
    #motor stats
    "startTime" : 0,
    "burnTime" : 12.4,     #burn time of the motor (s) 
    "mass" : 15.258,
}

#dictionary for each thrust value per time step
thrustDict = {}
time = 0
while time < kwargs["burnTime"]:
    thrustDict[str(time)] = thrust(**kwargs)
    time = time + dt
    kwargs["t"] = kwargs["t"] + dt
kwargs["t"] = 0
kwargs["thirstyBoi"] = thrustDict

funcList = [
    acceleration,
    dVelocity,
    #dPosition,
]

#find direction before loop, index with same variable
direction = [0.70711, 0, 0.70711]
negdirection = [0, 0, 0]
V_mag = 0

t = 0
numberyBois = ([0, 0, 0], [0, 0, 0], [0, 0, 0])     #ae, an, au, ve, vn, vu, se, sn, su
k1 = [0, 0, 0]
k2 = [0, 0, 0]
k3 = [0, 0, 0]
k4 = [0, 0, 0]
fucks_given = 0
while (numberyBois[2][2]>= 0):
    for i in range(0, 3):
        if i == 0 :
            if (t < burnTime) :
                kwargs["THRUST"] = kwargs["thirstyBoi"][str(t)]     #find thrust at time t
                kwargs["mass"] = kwargs["mass"] - (kwargs["THRUST"] *dt / jonConst)
                kwargs["ACCELERATION"] = kwargs["THRUST"]  / kwargs["mass"]  #acceleration at time t = thrust(t) / mass
                if numberyBois[2][2]> 0 :
                    kwargs["DRAG"] = drag(density(numberyBois[2][2]), V_mag, kwargs["Base Area"])
                for j in range(0,3):
                    numberyBois[i][j] = direction[j] * kwargs["ACCELERATION"]
                    numberyBois[i][j] = numberyBois[i][j] + negdirection[j] * kwargs["DRAG"]
                    if j == 2 :
                        numberyBois[i][j] = numberyBois[i][j] - 9.81
                    
                
            else :
                numberyBois[0][0] = 0
                numberyBois[0][1] = 0
                numberyBois[0][2] = -9.81
                kwargs["DRAG"] = drag(density(numberyBois[2][2]), V_mag, kwargs["Base Area"])
                for j in range(0,3):
                    numberyBois[i][j] = numberyBois[i][j] + negdirection[j] * kwargs["DRAG"]
        else :
            for j in range(0,3):
                k1[j] = numberyBois[i-1][j]
                k2[j] = numberyBois[i-1][j] + k1[j] * (dt/2)
                k3[j] = numberyBois[i-1][j] + k2[j] * (dt/2)
                k4[j] = numberyBois[i-1][j] + k3[j] * dt
                val = (1/6)*(k1[j] + 2*k2[j] + 2*k3[j] + k4[j])*dt
                numberyBois[i][j] = numberyBois[i][j] + val
                #print(i)
    t = t+dt
    print(numberyBois)
    dumbo = (numberyBois[1][0])**2+(numberyBois[1][1])**2+(numberyBois[1][2])**2
    V_mag = np.sqrt(dumbo)
    for d in range(0, 3):
        direction[d] = (1/V_mag)*numberyBois[1][d]
        negdirection[d] = -1*direction[d]


#for f, i in zip()

"""
nextVal = {}
n = 0
for keyTerm in kwargs.keys():
    if keyTerm == "t":
        nextVal[keyTerm] = kwargs[keyTerm] + h/2
    else:
        nextVal[keyTerm] = kwargs[keyTerm] + k1[n] * (h/2)
        n = n + 1
"""