import numpy
import matplotlib.pyplot as plt
y0=1
z0=1000
h=float(input("Ingrese el valor de un intervalo de tiempo: "))
x=numpy.arange(0,5,h)
y=numpy.zeros_like(x)
z=numpy.zeros_like(x)
y[0]=y0
z[0]=z0
for i in range(1,x.size):
    y[i]=y[i-1]+h*(0.01*z[i-1]*y[i-1]-y[i-1])
    z[i]=z[i-1]+h*(-0.01*z[i-1]*y[i-1])
fig=plt.figure(figsize=(5,5))
ax=fig.add_subplot(111)
ax.plot(x,y,label="enfermos")
ax.plot(x,z,label="suceptibles")
ax.legend()
plt.show()
