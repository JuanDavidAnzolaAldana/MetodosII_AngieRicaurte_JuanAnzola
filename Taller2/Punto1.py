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
        r[i+1]=real(x[i+1])
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(1,2,1)
    ax2=fig.add_subplot(1,2,2)
    ax.plot(x,y,label="Aproximación")
    ax.plot(x,r,label="valor real")
    ax.set_title("Solución")
    ax.legend()
    #ax2.set_yscale("log")
    ax2.plot(x,y-r)
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
        r[i+1]=real(x[i+1])
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(1,2,1)
    ax2=fig.add_subplot(1,2,2)
    ax.plot(x,y,label="Aproximación")
    ax.plot(x,r,label="valor real")
    ax.set_title("Solución")
    ax.legend()
    ax2.plot(x,y-r)
    ax2.set_title("Error")
    plt.show()
def func(x,y):
    return x**2-3*x**2*y
def resp(x):
    return (2*numpy.exp(-x**3)+1)/3
def exp(x,y):
    return -y
def rexp(x):
    return numpy.exp(-x)
def log(x,y):
    return y*numpy.log(x)/x
def reg(x):
    return x**(numpy.log(x)/2)
while True:
    a=input("Elija la ecuación diferencial:\n1. y'=-y\n2. y'=x^2-3x^2y\n3. xy'=ln(x)y\n4. Salir.\n")
    if a=="1":
        b=input("Seleccione el método de aproximación:\n1. Runge-Kutta de tercer orden.\n2. Runge-Kutta de cuarto oden\n")
        if b=="1":
            tercer(exp,0.3,40,1,0,rexp)
        if b=="2":
            cuarto(exp,0.3,40,1,0,rexp) 
        if (b!="1")and(b!="2"):
            print("Error")
    if a=="2":
        b=input("Seleccione el método de aproximación:\n1. Runge-Kutta de tercer orden.\n2. Runge-Kutta de cuarto oden\n")
        if b=="1":
            tercer(func,0.02,7.4,1,0,resp)
        if b=="2":
            cuarto(func,0.02,7.73,1,0,resp)
        if (b!="1")and(b!="2"):
            print("Error")
    if a=="3":
        b=input("Seleccione el método de aproximación:\n1. Runge-Kutta de tercer orden.\n2. Runge-Kutta de cuarto oden\n")
        if b=="1":
            tercer(log,0.02,15,3.651526,0.2,reg)
        if b=="2":
            cuarto(log,0.02,15,3.651526,0.2,reg)
        if (b!="1")and(b!="2"):
            print("Error")
    if a=="4":
        break
