import pygame, math, random
 
pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Stochastic Cutted Fractal Tree")
screen = pygame.display.get_surface()
 
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
		pygame.draw.line(screen, (r,g,b), (x1, y1), (x2, y2), 2)       
		drawTree(x2, y2, angle - random.randint(0,30), depth - 1,r,g,b) # First branch recursive call with random angle
        	drawTree(x2, y2, angle + random.randint(0,30), depth - 1,r,g,b) # Second branch recursive call with random angle
 
def input(event):
    if event.type == pygame.QUIT:
        exit(0)
# Base branch. Is not part of the fractal
pygame.draw.line(screen, (100,50,0), (400, 450), (400, 400), 2)
# Recursive fractal function  
drawTree(400, 400, -90, 16,100,43,0)
pygame.display.flip()
while True:
    input(pygame.event.wait())
