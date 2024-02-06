import matplotlib.pyplot as plt
import numpy
def tercer(f,h,time,y0,x0,real):
    x=numpy.arange(x0,x0+time,h)
    y=numpy.zeros_like(x)
    r=numpy.zeros_like(x)
    y[0]=y0
    r[0]=y0
    for i in range(0,x.size-1):
        k1=f(x[i],y[i])
        k2=f(x[i]+(h/2),y[i]+(k1*h/2))
        k3=f(x[i]+h,y[i]+(2*k2*h)-(k1*h))
        y[i+1]=y[i]+((k1+(4*k2)+k3)*h/6)
        r[i]=real(x[i])
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(1,2,1)
    ax2=fig.add_subplot(1,2,2)
    ax.plot(x,y,label="Aproximación")
    ax.plot(x,r,label="valor real")
    ax.set_title("Solución")
    ax.legend()
    ax2.plot(x,y-r)
    ax2.set_yscale("log")
    ax2.set_title("Error")
    plt.show()
def cuarto(f,h,time,y0,x0,real):
    x=numpy.arange(x0,x0+time,h)
    y=numpy.zeros_like(x)
    r=numpy.zeros_like(x)
    y[0]=y0
    r[0]=y0
    for i in range(0,x.size-1):
        k1=f(x[i],y[i])
        k2=f(x[i]+(h/2),y[i]+(k1*h/2))
        k3=f(x[i]+(h/2),y[i]+(k2*h/2))
        k4=f(x[i]+h,y[i]+(k3*h))
        y[i+1]=y[i]+((k1+(2*k2)+(2*k3)+k4)*h/6)
        r[i]=real(x[i])
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(1,2,1)
    ax2=fig.add_subplot(1,2,2)
    ax.plot(x,y,label="Aproximación")
    ax.plot(x,r,label="valor real")
    ax.set_title("Solución")
    ax.legend()
    ax2.set_yscale("log")
    ax2.plot(x,y-r)
    ax2.set_title("Error")
    plt.show()
def func(x,y):
    return x**2-3*x**2*y
def e(x):
    return (2*numpy.exp(-x**3)+1)/3

tercer(func,0.02,10,1,0,e)
