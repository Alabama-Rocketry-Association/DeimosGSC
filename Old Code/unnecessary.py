def thrust(t, burnTime, c0, c1, c2, c3, c4, c5, c6, **kwargs):   #calculate thrust offered by motor at any time after ignition
    if (t < burnTime):
        return (c6*t**6 + c5*t**5 + c4*t**4 + c3*t**3 + c2*t**2 + c1*t + c0)
    else:
        return 0.00

def RK4(f, x, y, dx):   #4th-order Runge-Kutta integration
    k1 = f(x, y)
    k2 = f(x + 0.5*dx, y + 0.5*k1*dx)
    k3 = f(x + 0.5*dx, y + 0.5*k2*dx)
    k4 = f(x + dx, y + k3*dx)
    y = y + ((k1 + 2*k2 + 2*k3 + k4)*dx/6)
    return y