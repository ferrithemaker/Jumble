import sys, pygame
import time
import random


pygame.init()

width = 500
height = 700
size = [width, height]

black = [0, 0, 0]
red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]

punts = 0
vides = 10

screen = pygame.display.set_mode(size)

font = pygame.font.Font('freesansbold.ttf', 32)

spaceshipIMG = pygame.image.load("spaceship.png") # (48x48) from opengameart.org
enemyshipIMG = pygame.image.load("enemy.png")  # (48x24) from dlf.pt

spaceshiprect = spaceshipIMG.get_rect()

spaceshiprect.x = 202
spaceshiprect.y = 600

projectils = []
projectilsenemics = []
enemyships = []

pygame.mixer.music.load("BioUnit-GroundEffect.ogg") # music from BioUnit (https://freemusicarchive.org/)
pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceshiprect.x = spaceshiprect.x - 20
            if event.key == pygame.K_RIGHT:
                spaceshiprect.x = spaceshiprect.x + 20
            if event.key == pygame.K_SPACE:
                projectils.append(pygame.Vector2(spaceshiprect.x + 24,spaceshiprect.y - 3))

    if spaceshiprect.x < 0:
        spaceshiprect.x = 0
    if spaceshiprect.x > width - 48:
        spaceshiprect.x = width - 48

    nivell = int(punts / 10)  # augmenta la feqüència cada 10 punts
    if nivell > 29: nivell = 29  # màxim nivell possible

    # generació aleatoria d'enemics
    if random.randint(0,50-nivell) == 0:
        enemyshiprect = enemyshipIMG.get_rect()
        enemyshiprect.y = random.randint(50,400)
        enemyships.append(enemyshiprect)

    # generació aleatoria de projectils enemics
    if random.randint(0,30-nivell) == 0:
        if len(enemyships) > 0:
            enemic_dispara = random.randint(0,len(enemyships)-1)
            projectilsenemics.append(pygame.Vector2(enemyships[enemic_dispara].x + 24,enemyships[enemic_dispara].y + 5))

    # col.lisió de projectil amb enemics
    enemyshipsActuals = []
    for enemyship in enemyships:
        impacte = False
        for projectil in projectils:
            if enemyship.collidepoint(projectil.x,projectil.y):
                impacte = True
                punts = punts + 1
                projectils.remove([projectil.x,projectil.y])
        if enemyship.x < width and impacte is False:
            enemyship.x = enemyship.x + 2 + nivell
            enemyshipsActuals.append(enemyship)
    enemyships = enemyshipsActuals

    # col.lisió de projectils enemic amb jugador
    for projectil in projectilsenemics:
        if spaceshiprect.collidepoint(projectil.x, projectil.y):
            vides = vides - 1
            projectilsenemics.remove([projectil.x, projectil.y])

    # moviment i destruccio dels projectils que surten de la pantalla
    projectilsActuals = []
    for projectil in projectils:
        if projectil.y > 0:
            projectil.y = projectil.y - 5
            projectilsActuals.append(projectil)
    projectils = projectilsActuals

    # moviment i destruccio dels projectils enemics que surten de la pantalla
    projectilsenemicsActuals = []
    for projectil in projectilsenemics:
        if projectil.y < height:
            projectil.y = projectil.y + 5
            projectilsenemicsActuals.append(projectil)
    projectilsenemics = projectilsenemicsActuals

    if vides <= 0:
        # si no queden vides
        screen.fill(black)
        text = font.render("Game Over", True, green, black)
        textRect = text.get_rect()
        textRect.x = 160
        textRect.y = height / 2
        screen.blit(text, textRect)
    else:
        screen.fill(black)
        # pintem projectils
        for projectil in projectils:
            pygame.draw.circle(screen,red,(projectil.x,projectil.y),6)
        # pintem naus enemigues
        for enemyship in enemyships:
            screen.blit(enemyshipIMG,enemyship)
        # pintem projectils enemics
        for projectil in projectilsenemics:
            pygame.draw.circle(screen, blue, (projectil.x, projectil.y), 6)
        # pintem la nostra nau
        screen.blit(spaceshipIMG, spaceshiprect)
        # pintem punts i vides
        text = font.render("Vides:"+str(vides)+" Punts:" + str(punts), True, green, black)
        textRect = text.get_rect()
        textRect.x = 200
        textRect.y = 20
        screen.blit(text, textRect)
    pygame.display.flip()
    time.sleep(0.01)
