#Problema 2.08 Choques de duración finita
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import tqdm
k=1
def dot(a:numpy.ndarray,b:numpy.ndarray)->float:
    if a.shape!=b.shape:
        raise Exception("Should have the same size")
    return numpy.sum(a*b)
def norm(a:numpy.ndarray)->float:
    return dot(a,a)**0.5
def normal_dot(a:numpy.ndarray,b:numpy.ndarray)->float:
    return dot(a/norm(a),b)
class particle:
    def __init__(self, pos:numpy.ndarray, vel:numpy.ndarray, mass:float, radius:float, color:str="k"):
        self.pos=pos
        self.vel=vel
        self.mass=mass
        self.r=radius
        self.color=color
        self.a=0
        self.u=0
        self.pas=numpy.zeros(2)
    def past(self,dt:float):
        self.pas=self.pos-(self.vel*dt)+(self.a*dt*dt/2)
    def get_status(self)->numpy.ndarray:
        state=numpy.zeros((5,2))
        state[0]=self.pos
        state[1]=self.vel
        state[2]=self.a
        state[3]=self.mass*self.vel
        state[4,0]=self.u
        state[4,1]=((self.pos[0]*self.vel[1])-(self.pos[1]*self.vel[0]))*self.mass
        return state
    def collide(self,other)->None:
        d=other.r+self.r-norm(other.pos-self.pos)
        if d>=0:
            other.a+=k*d*(other.pos-self.pos)/norm(other.pos-self.pos)
            other.u+=k*d*d/2
    def interact(self,colliders:list)->None:
        self.a=0
        self.u=0
        for i in colliders:
            if i!=self:
                i.collide(self)
    def move(self,dt:float)->None:
        r=self.pos
        self.pos=(2*self.pos)-self.pas+(self.a*dt*dt)
        self.vel=(self.pos-self.pas)/(2*dt)
        self.pas=r
class bounding_box:
    def __init__(self, size:tuple, pos:tuple):
        self.size=size
        self.pos=pos
    def get_limits_x(self)->tuple:
        return (self.pos[0],self.pos[0]+self.size[0])
    def get_limits_y(self)->tuple:
        return (self.pos[1],self.pos[1]+self.size[1])
    def collide(self,other:particle):
        #if other.pos[0]+other.r>=self.pos[0]+self.size[0]:
        #    other.vel[0]=-abs(other.vel[0])
        #if other.pos[0]-other.r<=self.pos[0]:
        #    other.vel[0]=abs(other.vel[0])
        #if other.pos[1]+other.r>=self.pos[1]+self.size[1]:
        #    other.vel[1]=-abs(other.vel[1])
        #if other.pos[1]-other.r<=self.pos[1]:
        #    other.vel[1]=abs(other.vel[1])
        pass
def simulate(particles:list,bounds:bounding_box,maxtime:float,deltatime:float)->list:
    timeline=numpy.arange(0,maxtime,deltatime)
    colliders=particles.copy()
    colliders.append(bounds)
    info=[]
    for i in tqdm.tqdm(particles, desc="preparando estructuras de datos"):
        info.append(numpy.zeros((len(timeline),5,2)))
    for i in range(len(particles)):
        particles[i].interact(colliders)
        particles[i].past(deltatime)
    for i in tqdm.tqdm(range(len(timeline)),desc="procesando"):
        for j in range(len(particles)):
            info[j][i]=particles[j].get_status()
            particles[j].interact(colliders)
        for j in particles:
            j.move(deltatime)
    return (info,timeline)
def simulation(tf:float,dt:float,fr:int)->None:
    box=bounding_box((40,40), (-20,-20))
    particles=[particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "k"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "r"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "orange"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "y"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "green"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "cyan"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "blue"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "purple"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "pink"),
               particle(numpy.random.uniform(-19,19,size=2), numpy.random.uniform(-5,5,size=2), 1.0, 1.0, "gray")]
    info,tl=simulate(particles,box,tf,dt)
    fig=plt.figure(figsize=(16,8))
    ax=fig.add_subplot(241)
    ax1=fig.add_subplot(242)
    ax2=fig.add_subplot(243)
    ax3=fig.add_subplot(245)
    ax4=fig.add_subplot(246)
    ax5=fig.add_subplot(247)
    ax6=fig.add_subplot(244)
    def start():
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()
        ax6.clear()
        ax1.set_title("Momento lineal en x")
        ax2.set_title("Momento lineal en y")
        ax3.set_title("Energía cinética")
        ax4.set_title("Energía potencial")
        ax5.set_title("Energía mecánica")
        ax6.set_title("Momento angular")
        x1=numpy.zeros_like(tl)
        x2=numpy.zeros_like(tl)
        x3=numpy.zeros_like(tl)
        x4=numpy.zeros_like(tl)
        x6=numpy.zeros_like(tl)
        for j in range(len(info)):
            kinetic=numpy.sum(info[j][:,3]*info[j][:,1],axis=1)/2
            ax1.plot(tl,info[j][:,3,0],c=particles[j].color)
            ax2.plot(tl,info[j][:,3,1],c=particles[j].color)
            ax3.plot(tl,kinetic,c=particles[j].color)
            ax4.plot(tl,info[j][:,4,0],c=particles[j].color)
            ax5.plot(tl,info[j][:,4,0]+kinetic,c=particles[j].color)
            ax6.plot(tl,info[j][:,4,1],c=particles[j].color)
            x1+=info[j][:,3,0]
            x2+=info[j][:,3,1]
            x3+=kinetic
            x4+=info[j][:,4,0]
            x6+=info[j][:,4,1]
        ax1.plot(tl,x1,linestyle="--",c="red",label="total")
        ax2.plot(tl,x2,linestyle="--",c="red",label="total")
        ax3.plot(tl,x3,linestyle="--",c="red",label="total")
        ax4.plot(tl,x4/2,linestyle="--",c="red",label="total")
        ax5.plot(tl,x4/2+x3,linestyle="--",c="red",label="total")
        ax6.plot(tl,x6,linestyle="--",c="red",label="total")
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        ax5.legend()
        ax6.legend()
    def update(i):
        ax.clear()
        ax.set(xlim=box.get_limits_x(),ylim=box.get_limits_y())
        ax1.set(xlim=(0,tl[i*fr]))
        ax2.set(xlim=(0,tl[i*fr]))
        ax3.set(xlim=(0,tl[i*fr]))
        ax4.set(xlim=(0,tl[i*fr]))
        ax5.set(xlim=(0,tl[i*fr]))
        ax6.set(xlim=(0,tl[i*fr]))
        ax.set_title(r'$ t=%.2f \ s$' %(tl[i*fr]))
        for j in range(len(info)):
            kinetic=numpy.sum(info[j][:,3]*info[j][:,1],axis=1)/2
            st=info[j][i*fr]
            ax.add_patch(plt.Circle((st[0,0],st[0,1]),particles[j].r, fill=True, color=particles[j].color))
            ax.arrow(st[0,0],st[0,1],st[1,0],st[1,1],color='r',head_width=1,length_includes_head=True)
            ax.arrow(st[0,0],st[0,1],st[2,0],st[2,1],color='b',head_width=1,length_includes_head=True)
    Animation = anim.FuncAnimation(fig,update,frames=int(len(tl)/fr),init_func=start,interval=1000*dt*fr)
    plt.show()
print("Se va a correr la simulación y se va a mostrar todas las gráficas de momento lineal, momento angular y energía al mismo tiempo.")
print("las respuestas a las preguntas se encuentran en un archivo llamado \"punto 2 teórico\".")
k=float(input("Ingrese la constante K.\n"))
simulation(float(10), float(0.001),200)

