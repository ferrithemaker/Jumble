from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import pygame, math, random

maxdepth=7
width=1366
height=1000
# Generation of random numbers
randomcounter=0
randomnumbers=[]
for elements in range(0,7**maxdepth):
	randomnumbers.append(random.randint(10,30))
pygame.init()
pygame.display.set_caption("Stochastic 3D OpenGL Cutted Fractal Tree")
screen=pygame.display.set_mode((width,height),OPENGL|DOUBLEBUF|HWSURFACE)
glViewport(0,0,width,height)
glClearColor(0.,0.,0.,0.)
glMatrixMode(GL_PROJECTION);
glLoadIdentity();
gluPerspective(45.0,width/height,1.0,500.0);
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glLoadIdentity()
def drawTree(x1, y1,z1,angle,rotation, depth, r,g,b,randomcounter,randomnumbers):
    if depth:
        # Brown to green gradient
        g=g+7;
        if g>255:
            g=7
        x2 = x1 + math.cos(math.radians(angle)) * randomnumbers[randomcounter]/10.0 # X random component
	randomcounter=randomcounter+1
        y2 = y1 + math.sin(math.radians(angle)) * randomnumbers[randomcounter]/10.0 # Y random component
	randomcounter=randomcounter+1
        z2 = z1 + math.sin(math.radians(rotation)) * randomnumbers[randomcounter]/10.0 # Y random component
	randomcounter=randomcounter+1        
	# Base cutting function
        if y2>0 or (y2<=0 and random.randint(0,4)==0):
            glBegin(GL_LINES)
            glColor4f(r/255.0,g/255.0,b/255.0,1.0)
            glVertex3f(x1,y1,z1)
            glVertex3f(x2,y2,z2)
            glEnd()
            randomcounter=randomcounter+drawTree(x2, y2,z2, angle - randomnumbers[randomcounter],0, depth - 1,r,g,b,randomcounter,randomnumbers) # First branch recursive call
            randomcounter=randomcounter+1  
	    drawTree(x2, y2,z2, angle + randomnumbers[randomcounter],0, depth - 1,r,g,b,randomcounter,randomnumbers) # Second branch recursive call with random angle
            randomcounter=randomcounter+1  
	    drawTree(x2, y2,z2, angle - randomnumbers[randomcounter],rotation+randomnumbers[randomcounter], depth - 1,r,g,b,randomcounter,randomnumbers) # 3th branch recursive call with random angle
            randomcounter=randomcounter+1
	    drawTree(x2, y2,z2, angle + randomnumbers[randomcounter],rotation-randomnumbers[randomcounter], depth - 1,r,g,b,randomcounter,randomnumbers) # 4th branch recursive call with random angle      
    return randomcounter+1
ev = pygame.event.poll()
rotate=0
radius=50.0
while ev.type!=pygame.QUIT: 
    ev = pygame.event.poll()
    keys=pygame.key.get_pressed()
    if keys[K_LEFT]:
    	rotate=rotate+0.05
    if keys[K_RIGHT]:
    	rotate=rotate-0.05
    if keys[K_UP]:
    	radius=radius-0.50
    if keys[K_DOWN]:
    	radius=radius+0.50
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glTranslatef(0.0,-5.0,0.0)	
    gluLookAt(radius*math.sin(rotate) + 0.0, 0.0, radius*math.cos(rotate) -100.0, 0, 0, -100, 0, 1, 0)
    glPushMatrix()
    drawTree(0.0, 0.0, -100,90,0, maxdepth,100,43,0,0,randomnumbers)
    glPopMatrix()
    pygame.display.flip()
pygame.quit()
