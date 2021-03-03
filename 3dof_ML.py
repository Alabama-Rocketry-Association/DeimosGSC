import time
import math
import numpy as np
import scipy
from scipy import integrate
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import pandas as pd
from mpl_toolkits import mplot3d
import requests
import json
import time
from classes import *
from tkinter import *

##################################
#step size up front
dt = 0.01
t = 0
##################################
filename = 'Cesaroni_5506M1230-P.csv'
coord = (32.99, -106.98)
#this is the azimuth direction as a unit vector (e, n, u)
direction = [3/7.07, 4/7.07, 5/7.07]    #3-4-5 triangle
direction = [0.0872, 0, 0.9962]     #85-degrees east
negdirection = [0, 0, 0]    #initialized to zero
V_abs = 0       #initialized to zero
##################################
#object declaration
weather = weatherData(coord)
rocket = rocket()
log = logData()
##################################
def drag(rho, vel, area, C_d = 0.5):        #C_d = 0.5 for a cone
    return (C_d*(1/2)*(rho)*(vel**2)*(area))
def p_atm(h):       #air pressure profile by altitude (Pa)
    carsaroni = (M_air * g) / (R * T_lapse)       #unsure if g should be positive or negative (g is hardcoded as negative)
    return ((weather.ambientTemp / temp(h))**carsaroni) * weather.ambientPressure  #carson i love you - passionately
def density(h):
    return p_atm(h) / (temp(h) * R_spec)
def temp(h):        #air temperature profile by altitude
    return weather.ambientTemp - dTdh*h
def GENERATE_THRUST_DICT(t, dt, filename):
    ###########
    #MACHINE LEARNING (Polynomial Regression)
    ###########

    #import dataset
    dataset = pd.read_csv(filename)
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
    burnTime = rocket.burnTime

    while (t < burnTime):
        if ((pol_reg.predict(poly_reg.fit_transform([[t]]))[0]) < 0):
            thrustDict[str(t)] = 0
        else:
            thrustDict[str(t)] = 3 * pol_reg.predict(poly_reg.fit_transform([[t]]))[0]      #change 3 to kwargs['cluster']
        t += dt

    #lists = sorted(thrustDict.items()) # sorted by key, return a list of tuples
    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.plot(x, y)
    #plt.show()
    return thrustDict
def INTEGRATE(rocket, log):
    while (log.AVS_Temp[2][2]>= 0):      #while height >= 0
        for i in range(0, 3):       #iterate through A, V, S
            if i == 0:     #for acceleration vector
                if (log.t < rocket.burnTime):     #while motor is burning
                    log.THRUST = thrustDict[str(log.t)]     #find thrust at time t
                    rocket.mass = rocket.mass - (log.THRUST * log.dt / rocket.jonConst)     #find mas at time t
                    log.ACCELERATION = log.THRUST / rocket.mass      #acceleration at time t = thrust(t) / mass
                    V_mag = np.linalg.norm(log.AVS_Temp[1])     #find magnitude of velocity vector
                    if (V_mag > 0 and log.t > 0.25):  # since this value is a denominator, it cannot be zero
                        for d in range(0, 3):  # calculate the direction vector and its negative
                            direction[d] = (1 / V_mag) * log.AVS_Temp[1][d]
                            negdirection[d] = -1 * direction[d]
                    log.DRAG = drag(density(log.AVS_Temp[2][2]), V_mag, rocket.baseArea)      #calculate drag     #need to add C_d
                    for j in range(0,3):    #iterate through acceleration vector
                        log.AVS_Temp[i][j] = direction[j] * log.ACCELERATION   #implement unit vector of direction
                        log.AVS_Temp[i][j] = log.AVS_Temp[i][j] + negdirection[j] * log.DRAG
                        if j == 2 :     #for gravity always acting on "up" (z axis)
                            log.AVS_Temp[i][j] = log.AVS_Temp[i][j] + g
                            log.AVS_Store[i][j].append(log.AVS_Temp[i][j])
                else :  #after motor burnout, acceleration is (0, 0, -9.81) m/s^2
                    log.AVS_Temp[0][0] = 0
                    log.AVS_Temp[0][1] = 0
                    log.AVS_Temp[0][2] = g
                    log.AVS_Store[0][2].append(log.AVS_Temp[0][2])
                    V_mag = np.linalg.norm(log.AVS_Temp[1])     #find magnitude of velocity vector
                    if (V_mag > 0):     #since this value is a denominator, it cannot be zero
                        for d in range(0,3):    #calculate the direction vector and its negative
                            direction[d] = (1/V_mag)*log.AVS_Temp[1][d]
                            negdirection[d] = -1 * direction[d]
                    log.DRAG = drag(density(log.AVS_Temp[2][2]), V_mag, rocket.baseArea)  # calculate drag    #need to add C_d
                    for j in range(0,3):
                        log.AVS_Temp[i][j] = log.AVS_Temp[i][j] + negdirection[j] * log.DRAG
            else :      #for velocity and position vectors
                for j in range(0,3):    #integrated runge kutta to solve Ve, Vn, Vu, Se, Sn, Su
                    log.k1[j] = log.AVS_Temp[i-1][j]
                    log.k2[j] = log.AVS_Temp[i-1][j] + log.k1[j] * (dt/2)
                    log.k3[j] = log.AVS_Temp[i-1][j] + log.k2[j] * (dt/2)
                    log.k4[j] = log.AVS_Temp[i-1][j] + log.k3[j] * dt
                    val = (1/6)*(log.k1[j] + 2*log.k2[j] + 2*log.k3[j] + log.k4[j])*dt
                    log.AVS_Temp[i][j] = log.AVS_Temp[i][j] + val
                    log.AVS_Store[i][j].append(log.AVS_Temp[i][j] + val)
                    #print(i)
        log.t = log.t+log.dt
def PLOT3D(log):
    xLine = log.AVS_Store[2][0]
    yLine = log.AVS_Store[2][1]
    zLine = log.AVS_Store[2][2]
    fig = plt.figure()
    ax = plt.axes(projection = '3d')
    ax.plot3D(xLine, yLine, zLine, 'blue')
    plt.show()

thrustDict = GENERATE_THRUST_DICT(t, dt, filename)

start_time = time.time()
INTEGRATE(rocket, log)
print("--- %s seconds ---" % (time.time() - start_time))
PLOT3D(log)
"""
def graph(log):
    fig = Figure(figsize = (5,5), dpi = 100)
    xLine = log.AVS_Store[2][0]
    yLine = log.AVS_Store[2][1]
    zLine = log.AVS_Store[2][2]
    fig = plt.figure()
    ax = plt.axes(projection = '3d')
    ax.plot3D(xLine, yLine, zLine, 'blue')

    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()

window = Tk()
window.title("3DOF Sim")
window.geometry("500x500")
plot_button = Button(master=window, command=graph(log), height=20, width=20, text="plot")
plot_button.pack()
window.mainloop()
    """