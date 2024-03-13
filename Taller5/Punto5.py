import numpy
import matplotlib.pyplot as plt
import tqdm
import matplotlib.animation as anim
dx=0.1
dt=0.05
x = numpy.arange(0, 2+dx, dx)
t=numpy.arange(0, 3+dt, dt)
space=numpy.zeros((t.size,x.size,x.size))
for i in range(0,x.size):
    for j in range(0,x.size):
        space[0,i,j]=numpy.sin(numpy.pi*x[i])*numpy.sin(numpy.pi*x[j])
space[1]=space[0]
X,Y=numpy.meshgrid(x,x)
def ondaBodreFijo(space,k):
    for T in tqdm.trange(1,t.size-1):
        for i in range(1,x.size-1):
            for j in range(1,x.size-1):
                space[T+1,i,j]=2*space[T,i,j]-space[T-1,i,j]+k**2*(space[T,i+1,j]+space[T,i-1,j]-4*space[T,i,j]+space[T,i,j+1]+space[T,i,j-1])
    return space
space=ondaBodreFijo(space,2*dt**2/dx**2)
def animar(space):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    def update(i):
        ax.clear()
        ax.plot_surface(X, Y, space[i])
        ax.set_title("t={:.2f}".format(t[i]))
        ax.set(xlim=(0,2),ylim=(0,2),zlim=(-1,1))
    Animation = anim.FuncAnimation(fig,update,frames=int(t.size),interval=5)
    plt.show()
animar(space)