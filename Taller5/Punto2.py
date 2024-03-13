import numpy
import matplotlib.pyplot as plt
import tqdm
import matplotlib.animation as anim
dt=0.01
x = numpy.arange(0, 1.2, 0.2)
t=numpy.arange(0, 1+dt, dt)
space=numpy.zeros((t.size,x.size,x.size))
X,Y=numpy.meshgrid(x,x)
for i in range(0, x.size):
    for j in range(0, x.size):
        space[0,i,j]=numpy.sin(numpy.pi*(x[i]+x[j]))
    for T in range(0,t.size):
        space[T,i,0]=numpy.sin(numpy.pi*x[i])*numpy.exp(-2*numpy.pi**2*t[T])
        space[T,0,i]=numpy.sin(numpy.pi*x[i])*numpy.exp(-2*numpy.pi**2*t[T])
        space[T,i,-1]=numpy.sin(numpy.pi*(1+x[i]))*numpy.exp(-2*numpy.pi**2*t[T])
        space[T,-1,i]=numpy.sin(numpy.pi*(1+x[i]))*numpy.exp(-2*numpy.pi**2*t[T])
def calor(space,k):
    for T in tqdm.trange(0,t.size-1):
        for i in range(1,x.size-1):
            for j in range(1,x.size-1):
                space[T+1,i,j]=space[T,i,j]+k*(space[T,i+1,j]+space[T,i-1,j]-4*space[T,i,j]+space[T,i,j+1]+space[T,i,j-1])
    return space
space=calor(space,dt/(0.2**2))
def animar(space):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    def update(i):
        ax.clear()
        ax.plot_surface(X, Y, space[i])
        ax.set_title("t={:.2f}".format(t[i]))
        ax.set(xlim=(0,1),ylim=(0,1),zlim=(-5,5))
    Animation = anim.FuncAnimation(fig,update,frames=t.size,interval=50)
    plt.show()
animar(space)