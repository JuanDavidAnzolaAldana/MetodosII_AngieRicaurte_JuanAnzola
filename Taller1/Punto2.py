#Problema 2.08 Choques de duración finita
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import tqdm
import time
import random
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
    def past(self,dt:float):
        self.pas=self.pos-(self.vel*dt)+(self.a*dt*dt/2)
    def get_status(self)->numpy.ndarray:
        state=numpy.zeros((4,2))
        state[0]=self.pos
        state[1]=self.vel
        state[2]=self.a
        state[3]=self.mass*self.vel
        return state
    def collide(self,other)->None:
        d=other.r+self.r-norm(other.pos-self.pos)
        if d>=0:
            other.a+=k*d*(other.pos-self.pos)/norm(other.pos-self.pos)
    def interact(self,colliders:list)->None:
        self.a=0
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
        info.append(numpy.zeros((len(timeline),4,2)))
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
    particles=[particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "k"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "r"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "orange"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "y"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "green"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "cyan"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "blue"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "purple"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "pink"),
               particle(numpy.array([random.uniform(-19,19),random.uniform(-19,19)]), numpy.array([random.uniform(-5,5),random.uniform(-5,5)]), 1.0, 1.0, "gray")]
    info,tl=simulate(particles,box,tf,dt)
    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(221)
    ax1=fig.add_subplot(222)
    ax2=fig.add_subplot(224)
    def start():
        ax.set(xlim=box.get_limits_x(),ylim=box.get_limits_y())
    def update(i):
        ax.clear()
        ax1.clear()
        ax2.clear()
        start()
        ax.set_title(r'$ t=%.2f \ s$' %(tl[i*fr]))
        ax1.set_title("Momento lineal en x")
        ax2.set_title("Momento lineal en y")
        for j in range(len(info)):
            st=info[j][i*fr]
            ax.add_patch(plt.Circle((st[0,0],st[0,1]),particles[j].r, fill=True, color=particles[j].color))
            ax.arrow(st[0,0],st[0,1],st[1,0],st[1,1],color='r',head_width=1,length_includes_head=True)
            ax.arrow(st[0,0],st[0,1],st[2,0],st[2,1],color='b',head_width=1,length_includes_head=True)
            ax1.plot(tl,info[j][:,3,0],c=particles[j].color)
            ax2.plot(tl,info[j][:,3,1],c=particles[j].color)
        ax1.axvline(tl[i*fr])
        ax2.axvline(tl[i*fr])
    start()
    Animation = anim.FuncAnimation(fig,update,frames=int(len(tl)/fr),init_func=start,interval=1000*dt*fr)
    plt.show()
while True:
    a=input("""\nProblema 2.08 Choques de duración finita\nSeleccione:
1. Correr simulación.\n2. ¿Qué significa la constate K?\n3. Salir.\n""")
    if a=="1":
        k=float(input("Ingrese la constante K.\n"))
        simulation(float(input("Ingrese el tiempo a simular.\n")),
float(input("Ingrese el tiempo de un paso de simulación.\n")),int(input("Ingrese la cantidad de pasos de simulación por fotograma.\n")))
    elif a=="2":
        print("Creo que el significado de la constante K es la resistencia a la deformación del material. Si un material tiene una K pequeña, este se deformará fácilmente y será más fácil atravesar el material en lugar de colisionar con el. Si K es un número grande, el material no se deformará y será más fácil chocar con él que atravesarlo.")
    elif a=="3":
        print("adios")
        break
    else:
        print("opción inválida")

