import numpy
import matplotlib.pyplot as plt
y0=1
h=float(input("Ingrese el valor de un intervalo de tiempo: "))
a=-1
x=numpy.arange(0,20,h)
y=numpy.zeros_like(x)
y2=numpy.zeros_like(x)
y[0]=y0
y2[0]=y0
for i in range(1,x.size):
    y[i]=y[i-1]+h*y[i-1]*a
    y2[i]=numpy.exp(a*x[i])
fig=plt.figure(figsize=(5,5))
ax=fig.add_subplot(111)
ax.plot(x,y,label="método de euler")
ax.plot(x,y2,label="solución analítica")
ax.legend()
plt.show()
