#include<iostream>
#include<math.h>
#include<graphics.h>
const int WIDTH = 800; HEIGHT = 600;

void drawLine(int moveToX, int moveToY, int drawX, int drawY, int color, int textX, int textY, char* name)
{
     moveto(moveToX, moveToY);
     setcolor(color);
     lineto(drawX, drawY);
     outtextxy(textX, textY, name);
}


using namespace std;
double thrust(double x, double y)
{
	if(x<3.45)
	{
		double ret = -5.0731*pow(x, 6) + 55.601*pow(x,5) - 237.1*pow(x,4) + 494.88*pow(x,3) - 518.95*pow(x,2) + 245.45*x -19.926;
		return ret;
	}
	else
		return 0.00;
}
double orderFour(double x, double y, double dx)
{
	double k1 = thrust(x, y);
	double k2 = thrust(x + 0.5*dx, y + 0.5*k1*dx);
	double k3 = thrust(x + 0.5*dx, y + 0.5*k2*dx);
	double k4 = thrust(x + dx, y + k3*dx);
	y = y + (double)(k1 + 2*k2 + 2*k3 + k4)*dx/6;
	return y;
}
int main()
{
	double y=0;
	double dx=0.00001;
	moveto(WIDTH/2, HEIGHT/2);
	for(double x = 0.00; x<WIDTH; x+=0.01)
	{
		y=orderFour(x, y, dx);
		setcolor(14);
		lineto(WIDTH/2 + (x*100) , HEIGHT/2 + (y*100));
	}
	getch();
	closegraph();
	system("PAUSE");
	return 0;
}
