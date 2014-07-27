from Box2D import *
import pygame, sys, math, random
from pygame.locals import *

# set up pygame-box2d constants
box_size=1
pillar_height=15.0
pygame_box2d_ratio=10.0
ground_height=10.0
pygame_screen_x=800
pygame_screen_y=500
margin=0.0

# shoot variables
force=0.0
angle=0.0

# set up pygame
pygame.init()
 
# set up the window
windowSurface = pygame.display.set_mode((pygame_screen_x, pygame_screen_y))
pygame.display.set_caption('Scorched Earth / Worms / Angry Birds concept with box2D!')
 
#setup boxes list
 
boxeslist=[]
 
# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up  box2d world
world=b2World()

# setup font

# pick a font you have and set its size... and static labels
myfont = pygame.font.SysFont("Arial", 18)
label_info = myfont.render("Gorillas / Scorched Earth / Worms / Angry Birds. Python + Pygame + Box2D demo concept", 1, BLUE)
label_ginfo = myfont.render("UP/DOWN angle | LEFT/RIGHT force | SPACE to shoot", 1, BLUE)


 
# ground body
groundBody=world.CreateStaticBody(
    position=((pygame_screen_x/pygame_box2d_ratio)/2.0,ground_height/2.0),
    shapes=b2PolygonShape(box=((pygame_screen_x/pygame_box2d_ratio)/2.0,(ground_height+margin)/2.0)),
    )

# function to create boxes
def create_dynamic_box(xpos,ypos,f,a):
    body=world.CreateDynamicBody(position=(xpos/pygame_box2d_ratio,ypos/pygame_box2d_ratio))
    box=body.CreatePolygonFixture(box=(box_size/2.0,box_size/2.0), density=1, friction=0.3)
    body.linearVelocity=(math.cos(math.radians(a))*f,math.sin(math.radians(a))*-f)
    return body

# load box image
redbox=pygame.image.load("./redbox.png").convert()

# load roof image
roofimg=pygame.image.load("./roof.png").convert()

# load cannon image
cannon=pygame.image.load("./cannon.png").convert()

# create the boxes layout
for x in xrange (int(10*pygame_box2d_ratio),int(30*pygame_box2d_ratio),int(1*pygame_box2d_ratio)): #virtual 'meters' unit to pixel based location
    boxeslist.append(create_dynamic_box(10*pygame_box2d_ratio,x+(box_size/2.0)*pygame_box2d_ratio,0,0))
    boxeslist.append(create_dynamic_box(11*pygame_box2d_ratio,x+(box_size/2.0)*pygame_box2d_ratio,0,0))
    boxeslist.append(create_dynamic_box(25*pygame_box2d_ratio,x+(box_size/2.0)*pygame_box2d_ratio,0,0))
    boxeslist.append(create_dynamic_box(26*pygame_box2d_ratio,x+(box_size/2.0)*pygame_box2d_ratio,0,0))

# create dynamic roof
roof=world.CreateDynamicBody(position=(18,30.5))
roofbox=roof.CreatePolygonFixture(box=(16.0/2.0,1.0/2.0), density=1, friction=0.3)
 
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
    # key control
    if ev.type==KEYDOWN and keys[K_RIGHT]:
        force=force+1
        if force>0:
            force=0
    if ev.type==KEYDOWN and keys[K_LEFT]:
        force=force-1
    if ev.type==KEYDOWN and keys[K_UP]:
        angle=angle+1
    if ev.type==KEYDOWN and keys[K_DOWN]:
        angle=angle-1
    if ev.type==KEYDOWN and keys[K_SPACE]:
        boxeslist.append(create_dynamic_box(pygame_screen_x-30,(pygame_screen_y/2)-((box_size*pygame_box2d_ratio)/2),force,angle))
    
    # Instruct the world to perform a single step of simulation. It is
    # generally best to keep the time step and iterations fixed.
    world.Step(timeStep, vel_iters, pos_iters)
 
    # Clear applied body forces. We didn't apply any forces, but you
    # should know about this function.
    world.ClearForces()
 
    # clean screen
    windowSurface.fill(BLACK)

    
    # put the label object on the screen
    label_force = myfont.render("Force: %i" %(-force), 1, BLUE)
    label_angle = myfont.render("Angle: %i" %(angle), 1, BLUE)
    windowSurface.blit(label_force, (pygame_screen_x-100, 10))
    windowSurface.blit(label_angle, (pygame_screen_x-100, 40))
    windowSurface.blit(label_ginfo, (pygame_screen_x/4, 30))

    # draw ground
    pygame.draw.rect(windowSurface, GREEN, (0, pygame_screen_y-(ground_height*pygame_box2d_ratio), pygame_screen_x,pygame_screen_y ))
    
    # draw cannon
    rotatedcannon=pygame.transform.rotozoom(cannon, -angle,1)
    rotatedcannon.set_colorkey(0)
    windowSurface.blit(rotatedcannon,(pygame_screen_x-30,pygame_screen_y/2))

    # draw info
    windowSurface.blit(label_info, (10, pygame_screen_y-50))
    
    # draw roof
    rotatedroof =  pygame.transform.rotozoom(roofimg, math.degrees(roof.angle),1)
    rot_rect=rotatedroof.get_rect()
    rotatedroof.set_colorkey(0)
    windowSurface.blit(rotatedroof, ((((roof.position.x*pygame_box2d_ratio))-(((rot_rect.w/pygame_box2d_ratio)/2.0)*pygame_box2d_ratio)),pygame_screen_y-(roof.position.y*pygame_box2d_ratio)-(((rot_rect.h/pygame_box2d_ratio)/2.0)*pygame_box2d_ratio)))

    # draw boxes 
    for box in boxeslist: 
        #rotate surf by DEGREE amount degrees
        rotatedredbox =  pygame.transform.rotozoom(redbox, math.degrees(box.angle),1)
        rotatedredbox.set_colorkey(0)
        windowSurface.blit(rotatedredbox, ((box.position.x*pygame_box2d_ratio)-((box_size/2.0)*pygame_box2d_ratio),pygame_screen_y-(box.position.y*pygame_box2d_ratio)-((box_size/2.0)*pygame_box2d_ratio)))
    pygame.display.flip()
pygame.quit()
