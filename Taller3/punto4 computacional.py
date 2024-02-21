import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import tqdm
import matplotlib.patches as patch
delta=6.67e-11*5.9736e24/(3.844e8**3)
mu=0.07349/5.9736
omega=2.6617e-6
#(r=0,f=1,pr=2,pf=3)
def derivada(x:numpy.array,t):
    prime=numpy.sqrt((x[0]**2)+1+(2*x[0]*numpy.cos(x[1]-(omega*t))))
    r=x[2]
    f=x[3]/(x[0]**2)
    pr=((x[3]**2)/(x[0]**3))-(delta*((1/(x[0]**2))+(mu*(x[0]-numpy.cos(x[1]-(omega*t)))/(prime**3))))
    pf=-(delta*mu*x[0]*numpy.sin(x[1]-(omega*t))/(prime**3))
    return numpy.array([r,f,pr,pf])
r0=6.3781e6/3.844e8
rl=1.7374e6/3.844e8
f0=numpy.pi/5
v0=11120/3.844e8
theta=f0
pr0=v0*numpy.cos(f0-theta)
pf0=r0*v0*numpy.sin(theta-f0)
def rungekutta(x,h):
    y=numpy.zeros((x.size,4))
    y[0,0]=r0
    y[0,1]=f0
    y[0,2]=pr0
    y[0,3]=pf0
    for i in tqdm.trange(0,x.size-1):
        k1=derivada(y[i],x[i])
        k2=derivada(y[i]+(k1*h/2),x[i]+(h/2))
        k3=derivada(y[i]+(k2*h/2),x[i]+(h/2))
        k4=derivada(y[i]+(k3*h),x[i]+h)
        y[i+1]=y[i]+((k1+(2*k2)+(2*k3)+k4)*h/6)
    px=y[:,0]*numpy.cos(y[:,1])
    py=y[:,0]*numpy.sin(y[:,1])
    return px,py
def animar(tf)->None:
    h=1.0
    timeline=numpy.arange(0,tf,h)
    px,py=rungekutta(timeline,h)
    fig=plt.figure(figsize=(5,5))
    ax=fig.add_subplot(111)
    def start():
        pass
    def update(i):
        rad=omega*timeline[i*1000]
        ax.clear()
        ax.set(xlim=[-1.2,1.2],ylim=[-1.2,1.2])
        ax.set_title(r'$ t=%.2f \ s$' %(timeline[i*1000]))
        ax.add_patch(plt.Circle((0,0),r0, fill=True, color="b"))
        ax.add_patch(plt.Circle((numpy.cos(rad),numpy.sin(rad)),rl, fill=True, color="k"))
        ax.add_patch(patch.RegularPolygon((px[i*1000],py[i*1000]),3,0.012,color="r"))
    Animation = anim.FuncAnimation(fig,update,frames=int(len(timeline)/1000),init_func=start,interval=2)
    plt.show()
animar(300000)
