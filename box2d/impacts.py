from Box2D import *
import pygame, sys, math, random
from pygame.locals import *

# set up pygame-box2d constants
car_x_size=3
car_y_size=1
pillar_height=15.0
pygame_box2d_ratio=10.0
ground_height=10.0
pygame_screen_x=500
pygame_screen_y=400
margin=0.0

# set up pygame
pygame.init()
 
# set up the window
windowSurface = pygame.display.set_mode((pygame_screen_x, pygame_screen_y))
pygame.display.set_caption('Car impacts')
 
#setup boxes list
 
carlist=[]
 
# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up  box2d world -no gravity-
world=b2World(gravity=(0,0), doSleep=True)
 
def create_dynamic_car(xpos,ypos,velocity):
    body=world.CreateDynamicBody(position=(xpos/pygame_box2d_ratio,ypos/pygame_box2d_ratio))
    box=body.CreatePolygonFixture(box=(car_x_size/2.0,car_y_size/2.0), density=1, friction=0.8)
    body.linearVelocity=(velocity,0)
    body.angularDamping=0.6
    return body

# load image
redcar=pygame.image.load("d:\\car.png").convert()
 
# Prepare for simulation. Typically we use a time step of 1/60 of a
# second (60Hz) and 6 velocity/2 position iterations. This provides a 
# high quality simulation in most game scenarios.
timeStep = 1.0 / 300
vel_iters, pos_iters = 3, 1
 
# This is our little animation loop.
ev = pygame.event.poll()
while ev.type!=pygame.QUIT:
    ev = pygame.event.poll()
    keys=pygame.key.get_pressed()
    # create random boxes
    if random.randint(1,1000)==2:
        carlist.append(create_dynamic_car(0,random.randint(1,400),random.randint(1,10)))
        carlist.append(create_dynamic_car(500,random.randint(1,400),-(random.randint(1,10))))
    # Instruct the world to perform a single step of simulation. It is
    # generally best to keep the time step and iterations fixed.
    world.Step(timeStep, vel_iters, pos_iters)
 
    # Clear applied body forces. We didn't apply any forces, but you
    # should know about this function.
    world.ClearForces()
 
    # clean screen
    windowSurface.fill(BLACK)
 
    for car in carlist:
        # Increase linearDamping every frame (to simulate friction)
        car.linearDamping+=0.00005
        # Rotate car by DEGREE amount degrees
        rotatedredcar =  pygame.transform.rotozoom(redcar, math.degrees(car.angle),1)
        rotatedredcar.set_colorkey(0)
        windowSurface.blit(rotatedredcar, ((car.position.x*pygame_box2d_ratio)-((car_x_size/2.0)*pygame_box2d_ratio),pygame_screen_y-(car.position.y*pygame_box2d_ratio)-((car_y_size/2.0)*pygame_box2d_ratio)))
    pygame.display.flip()
pygame.quit()
