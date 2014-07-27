from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import pygame, math, random


pygame.init()
pygame.display.set_caption("Stochastic 2D OpenGL Cutted Fractal Tree")
screen=pygame.display.set_mode((800,800),OPENGL|DOUBLEBUF|HWSURFACE)
glViewport(0,0,800,800)
glClearColor(0.,0.,0.,0.)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glLoadIdentity()
glOrtho(0.0,800.0,800.0,0.0,0.0,1.0)
def drawTree(x1, y1, angle, depth, r,g,b):
    if depth:
        # Brown to green gradient
        g=g+7;
        if g>255:
            g=7
        x2 = x1 + int(math.cos(math.radians(angle)) * random.randint(10,30)) # X random component
        y2 = y1 + int(math.sin(math.radians(angle)) * random.randint(10,30)) # Y random component
        # Base cutting function
        if y2<=400 or (y2>400 and random.randint(0,4)==0):
            glBegin(GL_LINES)
            glColor4f(r/255.0,g/255.0,b/255.0,1.0)
            glVertex3f(x1,y1,0.0)
            glVertex3f(x2,y2,0.0)
            glEnd()
            #print "draw line (%i,%i)-(%i,%i)" % (x1,y1,x2,y2)
            drawTree(x2, y2, angle - random.randint(0,30), depth - 1,r,g,b) # First branch recursive call with random angle
            drawTree(x2, y2, angle + random.randint(0,30), depth - 1,r,g,b) # Second branch recursive call with random angle


# Base branch. Is not part of the fractal
glBegin(GL_LINES)
glColor4f(100.0/255.0,43.0/255.0,0.0/255.0,1.0)
glVertex3f(400,450,0.0)
glVertex3f(400,400,0.0)
glEnd()
# Draw tree
drawTree(400, 400, -90, 16,100,43,0)
pygame.display.flip()
ev = pygame.event.poll()
while ev.type!=pygame.QUIT: 
    ev = pygame.event.poll()
pygame.quit()
