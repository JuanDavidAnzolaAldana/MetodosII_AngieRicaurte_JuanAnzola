import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as anim
def simulate(dt,time):
    p=1
    v=1
    a=-(numpy.pi**2)*p
    past=p+(a*(dt**2)/2)-(v*dt)
    t=numpy.arange(0,time,dt)
    P=numpy.zeros_like(t)
    Rp=numpy.zeros_like(t)
    for i in range(t.size):
        P[i]=p
        Rp[i]=numpy.cos(numpy.pi*t[i])+(numpy.sin(numpy.pi*t[i])/numpy.pi)
        a=-(numpy.pi**2)*p
        temp=p
        p=(2*p)+(a*dt*dt)-past
        past=temp
        v=(p-past)/dt
    return t,P,Rp
def Animar(dt,fr,time,b):
    t,P,Rp=simulate(dt,time)
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(121)
    ax1=fig.add_subplot(122)
    def start():
        ax1.clear()
        ax1.set_title("Posición vs tiempo")
        ax1.plot(t,P,c="g",label="Verlet")
        ax1.plot(t,Rp,c="m",label="Real")
        ax1.legend()
        if b:
            ax1.set_yscale("symlog")
    def update(i):
        ax.clear()
        ax.set(xlim=[-2,2],ylim=[-2,2])
        ax1.set(xlim=(0,t[i*fr]))
        ax.set_title(r'$ t=%.2f \ s$' %(t[i*fr]))
        ax.add_patch(plt.Circle((-1,P[i*fr]),0.5, fill=True, color="g"))
        ax.add_patch(plt.Circle((1,Rp[i*fr]),0.5, fill=True, color="m"))
    Animation = anim.FuncAnimation(fig,update,frames=int(len(t)/fr),init_func=start,interval=1000*dt*fr)
    plt.show()
a=input("""Elija:\n1. Zona estable lejos del punto crítico.\n2. Zona estable cerca del punto crítico.
3. Zona inestable cerca del punto crítico.\n4. Zona inestable lejos del punto crítico.\n""")
if a=="1":
    Animar(0.1,1,30,False)
if a=="2":
    Animar(0.6,1,30,False)
if a=="3":
    Animar(0.7,1,30,True)
if a=="4":
    Animar(1.2,1,30,True)