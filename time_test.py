import numpy as np
from matplotlib import pyplot as plt
import time

def thrust(t):
    if (t < 1.087):
        return 1132.6*t**6 - 3278.2*t**5 + 3442.6*t**4 - 1697.8*t**3 + 427.1*t**2 - 45.276*t + 25.182
    else:
         return 0

mass = 10

vel = list()
height = list()
timePts = list()

vel.append(0)
height.append(12)
timePts.append(0)
g = -9.81

fig, ax1 = plt.subplots()
colorVel = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('velocity', color=colorVel)
#ax1.plot(t, vel, color=colorVel)
ax1.tick_params(axis='y', labelcolor=colorVel)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

colorHeight = 'tab:blue'
ax2.set_ylabel('Height', color=colorHeight)  # we already handled the x-label with ax1
#ax2.plot(t, height, color=colorHeight)
ax2.tick_params(axis='y', labelcolor=colorHeight)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
#plt.show()

time0 = time.time()
i = 1
while(time.time() - time0 < 20):
    t = time.time() - time0
    timePts.append(t)
    deltaT = timePts[i] - timePts[i - 1]
    vel.append( deltaT * (((thrust(t) / mass)) +g) + vel[i-1])
    height.append(deltaT * vel[i-1] + height[i-1])
    i = i + 1

ax1.plot(timePts, vel, color=colorVel)
ax2.plot(timePts, height, color=colorHeight)
plt.show()