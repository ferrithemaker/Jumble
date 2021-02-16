import sys, pygame
import time

pygame.init()

width = 1500
height = 900
size = [width, height]

speed1 = [5, 5]
speed2 = [-5, 5]

black = [87, 45, 81]

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect1 = ball.get_rect()
ballrect2 = ball.get_rect()
ballrect1.x = 0
ballrect1.y = 0
ballrect2.x = 150
ballrect2.y = 80

while 1:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           sys.exit()
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_a:
               if speed1[0] == 0:
                  speed1 = oldspeed1
               else:
                   oldspeed1 = speed1
                   speed1 = [0,0]
           if event.key == pygame.K_SPACE:
              if speed2[0] == 0:
               speed2 = oldspeed2
              else:
               oldspeed2 =  speed2
               speed2 = [0, 0]


   ballrect1 = ballrect1.move(speed1)
   ballrect2 = ballrect2.move(speed2)

   if ballrect1.left < 0 or ballrect1.right > width:
       speed1[0] = -speed1[0]
   if ballrect1.top < 0 or ballrect1.bottom > height:
       speed1[1] = -speed1[1]
   if ballrect2.left < 0 or ballrect2.right > width:
       speed2[0] = -speed2[0]
   if ballrect2.top < 0 or ballrect2.bottom > height:
       speed2[1] = -speed2[1]

   screen.fill(black)
   screen.blit(ball, ballrect1)
   screen.blit(ball, ballrect2)
   pygame.display.flip()
   time.sleep(0.01)