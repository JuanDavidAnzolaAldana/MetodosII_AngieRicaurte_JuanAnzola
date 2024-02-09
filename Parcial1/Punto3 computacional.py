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
        self.a=numpy.array((0,-9.81))
        self.u=0
        for i in colliders:
            if i!=self:
                i.collide(self)
    def move(self,dt:float)->None:
        r=self.pos
        self.pos+=(self.vel*dt)+(self.a*dt*dt/2)
        self.vel+=(self.a*dt)
class bounding_box:
    def __init__(self, size:tuple, pos:tuple):
        self.size=size
        self.pos=pos
    def get_limits_x(self)->tuple:
        return (self.pos[0],self.pos[0]+self.size[0])
    def get_limits_y(self)->tuple:
        return (self.pos[1],self.pos[1]+self.size[1])
    def collide(self,other:particle):
        if (other.pos[0]+other.r>=self.pos[0]+self.size[0])and(other.vel[0]>0):
            other.vel[0]=-other.vel[0]*e
        if (other.pos[0]-other.r<=self.pos[0])and(other.vel[0]<0):
            other.vel[0]=-other.vel[0]*e
        if (other.pos[1]+other.r>=self.pos[1]+self.size[1])and(other.vel[1]>0):
            other.vel[1]=-other.vel[1]*e
        if (other.pos[1]-other.r<=self.pos[1])and(other.vel[1]<0):
            other.vel[1]=-other.vel[1]*e
def simulate(particles:list,bounds:bounding_box,maxtime:float,deltatime:float)->list:
    timeline=numpy.arange(0,maxtime,deltatime)
    colliders=particles.copy()
    colliders.append(bounds)
    info=[]
    for i in tqdm.tqdm(particles, desc="preparando estructuras de datos"):
        info.append(numpy.zeros((len(timeline),5,2)))
    for i in tqdm.tqdm(range(len(timeline)),desc="procesando"):
        for j in range(len(particles)):
            info[j][i]=particles[j].get_status()
            particles[j].interact(colliders)
        for j in particles:
            j.move(deltatime)
    return (info,timeline)
info=0
tl=0
def simulation(tf:float,dt:float,fr:int)->None:
    global info
    global tl
    box=bounding_box((40,40), (-20,-20))
    particles=[particle(numpy.array((-15.0,-10.0)), numpy.array((2.0,0.0)),1.0,2.0, "r")]
    info,tl=simulate(particles,box,tf,dt)
    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(121)
    ax3=fig.add_subplot(122)
    def start():
        ax3.clear()
        ax3.set_title("Energía cinética")
        x3=numpy.zeros_like(tl)
        for j in range(len(info)):
            kinetic=numpy.sum(info[j][:,3]*info[j][:,1],axis=1)/2
            if boo:
                ax3.plot(tl,kinetic,c=particles[j].color)
            x3+=kinetic
        ax3.plot(tl,x3,linestyle="--",c="red",label="total")
        ax3.legend()
    def update(i):
        ax.clear()
        ax.set(xlim=box.get_limits_x(),ylim=box.get_limits_y())
        ax3.set(xlim=(0,tl[i*fr]))
        ax.set_title(r'$ t=%.2f \ s$' %(tl[i*fr]))
        for j in range(len(info)):
            kinetic=numpy.sum(info[j][:,3]*info[j][:,1],axis=1)/2
            st=info[j][i*fr]
            ax.add_patch(plt.Circle((st[0,0],st[0,1]),particles[j].r, fill=True, color=particles[j].color))
            ax.arrow(st[0,0],st[0,1],st[1,0],st[1,1],color='r',head_width=1,length_includes_head=True)
            ax.arrow(st[0,0],st[0,1],st[2,0],st[2,1],color='b',head_width=1,length_includes_head=True)
    Animation = anim.FuncAnimation(fig,update,frames=int(len(tl)/fr),init_func=start,interval=1000*dt*fr)
    plt.show()
boo=True
k=1
e=0.9
simulation(float(10),0.001,200)
maximos=[]
minimos=[]
decreciente=False
for i in range(0,info[0].shape[0]-1):
    if info[0][i,0,1]>info[0][i+1,0,1]:
        if not decreciente:
            maximos.append(i)
        decreciente=True
    else:
        if decreciente:
            minimos.append(i)
        decreciente=False
print(maximos)
print(minimos)
tchoques=[]
for i in range(0,len(minimos)-1):
    tchoques.append(tl[minimos[i+1]]-tl[minimos[i]])
print()
print("Tiempos entre choques:")
print(tchoques)
estima=[]
for i in range(0,len(maximos)-1):
    print(maximos)
    val=(info[0][maximos[i+1],0,1]+20)/(info[0][maximos[i],0,1]+20)
    estima.append(numpy.sqrt(val))
print()
print("Estimaciones del coeficiente de restitución:")
print(estima)