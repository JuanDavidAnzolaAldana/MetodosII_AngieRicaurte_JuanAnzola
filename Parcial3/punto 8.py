import numpy
import matplotlib.pyplot as plt
import tqdm
import matplotlib.animation as anim
a=0.2
b=0.3
D=0.01
e=0.03
t=numpy.linspace(0,10,1000)
x=numpy.linspace(0,1,50)
dt=t[1]-t[0]
dx=x[1]-x[0]
print("Punto a")
print("el valor de λ es DΔt/Δx^2")
print("Este valor es",D*dt/dx**2)
print("lo cual es menor que  que 0.5")
input("Presione enter para continuar")
u=numpy.zeros((t.size,x.size))
w=numpy.zeros((t.size,x.size))
u[0]=numpy.random.uniform(0,0.3,x.size)
print("Punto b")
print("Se está mostrando la gráfica con la condición inicial de u")
plt.plot(x,u[0])
plt.show()
u[:,0]=numpy.ones_like(t)*0.1
u[:,-1]=numpy.ones_like(t)*0.2
print("Punto c")
print("se pusieron las condiciones de frontera.")
input("Presione enter para continuar")
def calor(u,w):
    for T in tqdm.trange(0,t.size-1):
        for i in range(1,x.size-1):
                u[T+1,i]=u[T,i]+(D*dt/dx**2)*(u[T,i+1]+u[T,i-1]-2*u[T,i])+dt*(w[T,i]-u[T,i]*(u[T,i]-a)*(1-u[T,i]))
                w[T+1,i]=w[T,i]+e*dt*(u[T,i]-b*w[T,i])
    return u,w
print("Punto d")
print("el sistema de ecuaciones se está integrando…")
u,w=calor(u,w)
print("el sistema de ecuaciones se integró")
def animar():
    fig=plt.figure(figsize=(5,5))
    ax=fig.add_subplot(111)
    def update(i):
        ax.clear()
        ax.plot(x, u[i],label="u")
        ax.plot(x, w[i],label="w")
        ax.legend()
        ax.set_title("t={:.2f}".format(t[4*i]))
        ax.set_xlabel("posición")
        ax.set_ylabel("voltaje")
        ax.set(ylim=(0,0.35))
    Animation = anim.FuncAnimation(fig,update,frames=int(t.size/4),interval=5)
    plt.show()
print("Punto e")
print("se muestra la animación")
animar()
print("Punto f")
print("Dependiendo de la condición inicial, que es aleatoria, la neurona puede activarse cerca de la posición 0.7 o puede no activarse en el intervalo de tiempo.")