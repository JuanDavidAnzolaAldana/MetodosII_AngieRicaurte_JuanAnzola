import matplotlib.pyplot as plt
import numpy
def tercer(f,h,time,y0,x0):
    x=numpy.arange(x0,x0+time,h)
    y=numpy.zeros_like(x)
    y[0]=y0
    for i in range(0,x.size-1):
        k1=f(x[i],y[i])
        k2=f(x[i]+(h/2),y[i]+(k1*h/2))
        k3=f(x[i]+h,y[i]+(2*k2*h)-(k1*h))
        y[i+1]=y[i]+((k1+(4*k2)+k3)*h/6)
    plt.plot(x,y)
    plt.show()
def cuarto(f,h,time,y0,x0):
    x=numpy.arange(x0,x0+time,h)
    y=numpy.zeros_like(x)
    y[0]=y0
    for i in range(0,x.size-1):
        k1=f(x[i],y[i])
        k2=f(x[i]+(h/2),y[i]+(k1*h/2))
        k3=f(x[i]+(h/2),y[i]+(k2*h/2))
        y[i+1]=y[i]+((k1+(4*k2)+k3)*h/6)
    plt.plot(x,y)
    plt.show()
def func(x,y):
    return x**2-(3*(x**2)*y)
tercer(func,0.01,10,1,0)