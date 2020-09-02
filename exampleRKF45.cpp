/******************************************************************************

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, PHP, Ruby, 
C#, VB, Perl, Swift, Prolog, Javascript, Pascal, HTML, CSS, JS
Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;
int f(double x, double y);

int main()
{
    
vector<double> x_val;        //zero is initial x value
vector<double> y_val;        //two is initial y value

int h = 2;                          //step size

x_val[0] = 0;
y_val[0] = 2;

//for loop iterating with 'i'

for (int i = 0; i <= 2; i++)
{
    double k1 = f(x_val[i], y_val[i]);
    double k2 = f(x_val[i] + ((1/5) * h), y_val[i] + ((1/5) * k1 * h));
    double k3 = f(x_val[i] + ((3/10) * h), y_val[i] + ((3/40) * k1 * h) + ((9/40) * k2 * h));
    double k4 = f(x_val[i] + ((3/5) * h), y_val[i] + ((3/10) * k1 * h) - ((9/10) * k2 * h) + ((6/5) * k3 * h));
    double k5 = f(x_val[i] + h, y_val[i] - ((11/54) * k1 * h) - ((5/2) * k2 * h) - ((70/27) * k3 * h) + ((35/27) * k4 * h));
    double k6 = f(x_val[i] + ((7/8) * h), y_val[i] + ((1631/55296) * k1 * h) + ((175/512) * k2 * h) - ((575/13824) * k3 * h) + ((44275/110592) * k4 * h) + ((253/4096) * k5 * h));

    y_val.push_back(y_val[i] + (((37 / 378) * k1) + ((250 / 621) * k3) + ((125 / 594) * k4) + ((512 / 1771) * k6)));
}


//4th order estimate -- y_val[i + 1] = y_val[i] + (((37/378) * k1) + ((250/621) * k3) + ((125/594) * k4) + ((512/1771) * k6))
//5th order estimate -- y_val[i + 1] = y_val[i] + (((2825/27648) * k1) + ((18575/48384) * k3) + ((13525/55296) * k4) + ((277/14336) * k5) + ((1/4) * k6))


    return 0;
}

int f(double x, double y)
{    
    return (4 * exp(0.8 * x)) - (0.5 * y);
}
