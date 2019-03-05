import sys, pygame
import time
import math

class Values():
    """
    Contains all constants
    """
    def __init__(self):
        self.WHITE = 255,255,255
        self.BLACK = 0,0,0
        self.SIZE = 1440, 800
        self.g = 9.80665

    def trigonometric_ratio(self, ratio, angle):
        sine = math.sin(math.pi*(angle/180))
        cosine = math.cos(math.pi*(angle/180))
        tangent = sine/cosine

        return {'sine':sine, 
        'cosine':cosine, 
        'tangent':tangent}.get(ratio)

class Screen():

    """
    Used to configure pygame scren
    bg_name (string) : backround
    f_name (string)  : font
    """

    def __init__(self,bg_name,f_name):
        global screen,background,font

        self.bg_name = bg_name
        self.f_name = f_name

        pygame.init()
        screen = pygame.display.set_mode(
            Values().SIZE)
        background = pygame.image.load('res/'+self.bg_name+'.jpeg')
        font = pygame.font.SysFont(self.f_name, 20)
        font.set_bold(True)

    def show(self,caption):
        screen.fill(Values().BLACK)        
        screen.blit(background,background.get_rect())  
        screen.blit(obj[0], obj[1])
        screen.blit(Vx,(0,0))
        screen.blit(Vy,(0,20))
        screen.blit(T,(0,40))
        screen.blit(Sx,(900,0))
        screen.blit(Sy,(900,20))
        pygame.display.set_caption(caption)
        pygame.display.flip()


class Object():
    """
    Loads an object
    name (string) : basketball,airplane,etc.
    """

    global img,imgrect

    def __init__(self, name):
        self.name = name

    def load_img(self):
        global img
        global imgrect
        img = pygame.image.load('res/'+self.name+'.png')
        imgrect = img.get_rect() 
        return [img,imgrect]

class Motion():
    """
    Motion in 2D Plane
    ux (float) : Initial velocity in horizontal direction
    uy (float) : Initial velocity in vertical direction
    ax (float) : Initial acceleration in horizontal direction
    ay (float) : Initial acceleration in vertical direction

    """
    global t
    t = 0

    def __init__(self, body=Object('res/'+'basketball'), ux=0, uy=0, ax=0, ay=0):
        global obj
        self.body = body
        self.ux = ux
        self.uy = uy
        self.ax = ax
        self.ay = ay

        obj = self.body.load_img()
        obj[1].top = Values().SIZE[1]-obj[1][3]

    def final_speed(self):
        t = time.time()-ti
        vx = self.ux+self.ax*t
        vy = self.uy+self.ay*t
        return [vx,vy]

    def start(self,start):
        global ti
        global Vx, Vy, T, Sx, Sy

        scr = Screen('bg','Courier New')
        t_complete = 0
        x_displacement = 0
        y_displacement = 0
        height = Values().SIZE[1]

        ti = time.time()
        speed = self.final_speed()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            if obj[1].bottom>height:
                obj[1] = obj[1].move([0,0])
            else:
                t_complete = time.time()-ti
                x_displacement = self.ux*t_complete+0.5*self.ax*(t_complete)**2
                y_displacement = self.uy*t_complete+0.5*self.ay*(t_complete)**2
                speed = self.final_speed()
                speed[1] = -speed[1]
                obj[1] = obj[1].move(speed)

            '''End of motion equations and calculations'''

            Vx = font.render(
                'Vx       : '+str(speed[0])+' m/s', False, Values().WHITE)
            Vy = font.render(
                'Vy(final): '+str(speed[1])+' m/s', False, Values().WHITE)
            T = font.render(
                'Tcomplete: '+str(t_complete)+' s', False, Values().WHITE)
            Sx = font.render(
                'Sx       : '+str(x_displacement)+' m', False, Values().WHITE)
            Sy = font.render(
                'Sy     : '+str(y_displacement)+' m', False, Values().WHITE)

            if start==1:
                scr.show("FLoM: Motion - 2 Dimensional")
            else:
                sys.exit()

class Projectile(Motion):
    """Special case of motion class
    where ax and ay are predefined
    u (float)   : Speed of projection
    angle(float): Angle of projection in degrees
    """
    def __init__(self, u, angle):
        super(Motion, self).__init__()
        global obj
        self.u = u
        self.angle = angle
        self.ux = self.u*Values().trigonometric_ratio(
            'cosine',self.angle)
        self.uy = self.u*Values().trigonometric_ratio(
            'sine',self.angle)
        self.ax = 0
        self.ay = -9.80665

        body = Object('basketball')
        obj = body.load_img()
        obj[1].top = Values().SIZE[1]-obj[1][3]

    def fire(self):
        self.start(1)

Projectile(15,45).fire()