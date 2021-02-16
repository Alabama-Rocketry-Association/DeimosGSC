def f(x, y):
    return (4 * exp(0.8 * x)) - (0.5 * y)


x_val = [0]         #zero is initial x value
y_val = [2]         #two is initial y value

h = 2               #step size
est4 = []           #list for 4th order estimation
est5 = []           # list for 5th order estimation
#for loop iterating with 'i'

for i in range(0, 2):
    k1 = f(x_val[i], y_val[i])
    k2 = f(x_val[i] + ((1/5) * h), y_val[i] + ((1/5) * k1 * h))
    k3 = f(x_val[i] + ((3/10) * h), y_val[i] + ((3/40) * k1 * h) + ((9/40) * k2 * h))
    k4 = f(x_val[i] + ((3/5) * h), y_val[i] + ((3/10) * k1 * h) - ((9/10) * k2 * h) + ((6/5) * k3 * h))
    k5 = f(x_val[i] + h, y_val[i] - ((11/54) * k1 * h) - ((5/2) * k2 * h) - ((70/27) * k3 * h) + ((35/27) * k4 * h))
    k6 = f(x_val[i] + ((7/8) * h), y_val[i] + ((1631/55296) * k1 * h) + ((175/512) * k2 * h) - ((575/13824) * k3 * h) + ((44275/110592) * k4 * h) + ((253/4096) * k5 * h))

    y_val.append(y_val[i] + (((37 / 378) * k1) + ((250 / 621) * k3) + ((125 / 594) * k4) + ((512 / 1771) * k6)))

for num in y_val:
    print(num)


#4th order estimate -- y_val[i + 1] = y_val[i] + (((37/378) * k1) + ((250/621) * k3) + ((125/594) * k4) + ((512/1771) * k6))
#5th order estimate -- y_val[i + 1] = y_val[i] + (((2825/27648) * k1) + ((18575/48384) * k3) + ((13525/55296) * k4) + ((277/14336) * k5) + ((1/4) * k6))
