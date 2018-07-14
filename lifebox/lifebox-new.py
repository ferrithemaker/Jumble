import pygame
import sys
import random
import threading
import time
from pyfirmata import ArduinoMega, util

datafromfile = [0] * 21

def map(x,in_min,in_max,out_min,out_max):
	return float((float(x) - float(in_min)) * (float(out_max) - float(out_min)) / (float(in_max) - float(in_min)) + float(out_min))


def readdatafromfile(stop):
	global datafromfile
	while not stop:
		file = open("/var/www/html/lifeboxdata", "r")
		datafromfile = file.read().split("|")
		#print (datafromfile[2])
		time.sleep(2)
		
def readdatafromArduino(stop):
	global datafromfile
	# load default values from 
	file = open("/var/www/html/lifeboxdata", "r")
	datafromfile = file.read().split("|")
	# remove 
	board = ArduinoMega('/dev/ttyACM0')
	it = util.Iterator(board)
	it.start()
	for i in range (0,11):
		board.analog[i].enable_reporting()
	while not stop:
		#for i in range (0,11):
			#if board.analog[i].read() is not None:
				#print("Pin:"+str(i)+" Value:"+str(int(board.analog[i].read()*1000)))
		if board.analog[i].read() is not None:
			#datafromfile[16] = board.analog[8].read() # plants life expectancy
			#datafromfile[20] = board.analog[10].read() # plants energy generation
			print("Value:"+str(int(board.analog[9].read()*1000)))
			datafromfile[17] = int(map(int(board.analog[9].read()*1000),0,1000,1,2000)) # plants nearborn chances
			print ("Return:" +str(datafromfile[17]))
			#datafromfile[6] = board.analog[3].read() # sp1 gathering
			#datafromfile[5] = board.analog[2].read() # sp1 efficency
			#datafromfile[0] = board.analog[0].read() # sp1 life exp
			#datafromfile[1] = board.analog[1].read() # sp1 nearborn chances
			#datafromfile[14] = board.analog[7].read() # sp2 gathering
			#datafromfile[13] = board.analog[6].read() # sp2 efficency
			#datafromfile[8] = board.analog[4].read() # sp2 life exp
			#datafromfile[9] = board.analog[5].read() # sp2 nearborn chances
		time.sleep(1)

graph_mode = 0 # show graphs
real_mode = 1 # respawn control
app_mode = 0 # via web / app or manual controller
gradient_mode = 1 # individual fade in / out linked to energy
fullscreen_mode = 0
fullscreen_graph = 0
rf = 1 # reduction factor

# run thread
stop = False
if app_mode == 0:
	t = threading.Thread(target=readdatafromArduino,args=(stop,))
else:
	t = threading.Thread(target=readdatafromfile,args=(stop,))
t.daemon = True
t.start()

#pygame setup

pygame.init()
pygame.font.init()

pygame.display.set_caption('LifeBox')

if fullscreen_mode == 0:
	screen = pygame.display.set_mode((1000,600))
	x_array = 32
	y_array = 32
	circle_size = 5
else:
	# size for full HD screen (1920,1080)
	# if you have other screen size, you need yo change x_array,y_array and circle_size
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	x_array = 70
	y_array = 52
	circle_size = 7

textfont = pygame.font.SysFont('arial',30)

# colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
bluegraph = (0,0,255,50)
yellow = (255,255,0)
yellowgraph = (255,255,0,50)
magenta = (255,0,255)
white = (255,255,255)
whitegraph = (255,255,255,50)
midgrey = (128,128,128)
black = (0,0,0)
darkgrey = (30,30,30)
lightgrey = (200,200,200,50)

# fps management
clock = pygame.time.Clock()

# species matrix
t, w, h = 3,x_array, y_array
# age 0 at z
# energy 1 at z
specie1 = [[[0 for x in range(t)] for y in range(h)] for z in range(w)]
specie2 = [[[0 for x in range(t)] for y in range(h)] for z in range(w)]
plants = [[[0 for x in range(t)] for y in range(h)] for z in range(w)]

# mask
#for x in range(0,10):
#	for y in range(0,10):
#		specie1[x][y][2] = 1
#		specie2[x][y][2] = 1
#		plants[x][y][2] = 1


# [x][y] [0]:age [1]:energy [2]:mask

# graph arrays

specie1_Iarray = [0 for x in range(200)]
specie2_Iarray = [0 for x in range(200)]
plants_Iarray = [0 for x in range(200)]
specie1_Earray = [0 for x in range(200)]
specie2_Earray = [0 for x in range(200)]
plants_Earray = [0 for x in range(200)]

# species variables

PLANTS_LIFE_EXPECTANCY = 40
PLANTS_RANDOM_BORN_CHANCES = 5100 # fixed
PLANTS_NEARBORN_CHANCES = 150
PLANTS_RANDOM_DIE_CHANCES = 2 # not used
PLANTS_ENERGY_BASE_PER_CYCLE = 100
# Each mana invidivual generates a defined amout of energy per cycle. This energy is gathered by the species. Low energy generation means a poor enviroment for the species to survive, and high energy generation a rich one.

#yellow
SPECIE1_LIFE_EXPECTANCY = 40
# Life expectancy is an statistical measure of the average time an organism is expected to live. Once a pixelic entity becomes stable, life expectancy determines how many reiterations does the pixel survive.
SPECIE1_RANDOM_BORN_CHANCES = 5100 
# Fixed
# Parthenogesis is a rare trait among species which allows them to reproduce without mating. The species inside LifeBox! can reproduce in a similar way. In case they achieve it, offspring is randomly populated inside the grid. 
# Setting this variable with a high value means less chances to reproduce that way. Otherwise, if user choose to reduce this value, parthenogenesis is more probable to happen
SPECIE1_NEARBORN_CHANCES = 25
# When two pixelic entities of the same specie are adjacent to each other, they can reproduce. This variable determines the reproduction chances, so a higher value means a higher chances to survive.
SPECIE1_RANDOM_DIE_CHANCES = 2
# NOT USED
# As in real life, LifeBox! pixelic species can die before reaching their life expectancy. Setting a low value, will allow pixelic entities to arrive at their expected life time. While a higher value will reduce seriously their chances to survive until the expected average life time.
SPECIE1_ENERGY_BASE = 250
# NOT USED
# Every spices has a defined base level of energy when it borns, this base level will condition the chances of survival at very first stages of its life.
SPECIE1_ENERGY_NEEDED_PER_CYCLE = 50
# This parameter defines the species amount of energy consumtion at each iteration. Higher values mean that the species needs more energy per iteration cycle, meaning less efficiency.
SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE = 100
# As the previous parameter defines the efficiency of energy consumtion, this one defines the efficiency of energy gathering from the mana. Higher values mean more gathering efficiency.
SPECIE1_ENERGY_TO_REPLICATE = 150
# NOT USED
# To allow the species replication, each individual needs to exceed an energy threshold, the minimum amount of energy needed to be able to reproduce itself. Higher values mean higher threshold.

#blue
SPECIE2_LIFE_EXPECTANCY = 40
SPECIE2_RANDOM_BORN_CHANCES = 5100 # fixed
SPECIE2_NEARBORN_CHANCES = 30 
SPECIE2_RANDOM_DIE_CHANCES = 2 # not used
SPECIE2_ENERGY_BASE = 250 # not used
SPECIE2_ENERGY_NEEDED_PER_CYCLE = 50
SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE = 100
SPECIE2_ENERGY_TO_REPLICATE = 150 # not used

specie2_individuals = 0
specie1_individuals = 0
plants_individuals = 0

# screen for transparent graph
graphsurface = pygame.Surface((1920, 1080), pygame.SRCALPHA, 32)

while (True):
	print (datafromfile[17])
	msElapsed = clock.tick(20)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			stop = True
        		pygame.quit()
	 		sys.exit()

	# init totals
	plants_last_individuals = plants_individuals
        specie2_last_individuals = specie2_individuals
        specie1_last_individuals = specie1_individuals
	specie2_individuals = 0
	specie1_individuals = 0
	plants_individuals = 0
	specie2_energy = 0
	specie1_energy = 0
	plants_energy = 0

	screen.fill(black)

	for x in range(0,x_array):
		# adjacent coordinates
		xp = (x+1)
		if xp >= x_array:
			xp = x_array - 1
		xm = (x-1)
		if xm < 0:
			xm = 0
		for y in range(0,y_array):
			# calculations
			# adjacent coordinates
			yp = (y+1)
			if yp >= y_array:
				yp = y_array - 1
			ym = (y-1)
			if ym < 0:
				ym = 0
			# count the number of currently live neighbouring cells
  			plants_neighbours = 0
  			specie1_neighbours = 0
  			specie2_neighbours = 0
  			# [Plants]

  			if plants[x][y][0] == 0 and plants[xm][y][0] > 0:
				plants_neighbours += 1
  			if plants[x][y][0] == 0 and plants[xp][y][0] > 0:
				plants_neighbours += 1
  			if plants[x][y][0] == 0 and plants[xm][ym][0] > 0:
				plants_neighbours += 1
  			if plants[x][y][0] == 0 and plants[x][ym][0] > 0:
				plants_neighbours += 1
  			if plants[x][y][0] == 0 and plants[xp][ym][0] > 0:
				plants_neighbours += 1
  			if plants[x][y][0] == 0 and plants[xm][yp][0] > 0:
				plants_neighbours += 1
  			if plants[x][y][0] == 0 and plants[x][yp][0] > 0:
				plants_neighbours += 1
  			if plants[x][y][0] == 0 and plants[xp][yp][0] > 0:
				plants_neighbours += 1
  			# [Specie1]
  			if specie1[x][y][0] == 0 and specie1[xm][y][0] > 0:
				specie1_neighbours += 1
  			if specie1[x][y][0] == 0 and specie1[xp][y][0] > 0:
				specie1_neighbours += 1
  			if specie1[x][y][0] == 0 and specie1[xm][ym][0] > 0:
				specie1_neighbours += 1
  			if specie1[x][y][0] == 0 and specie1[x][ym][0] > 0:
				specie1_neighbours += 1
  			if specie1[x][y][0] == 0 and specie1[xp][ym][0] > 0:
				specie1_neighbours += 1
  			if specie1[x][y][0] == 0 and specie1[xm][yp][0] > 0:
				specie1_neighbours += 1
  			if specie1[x][y][0] == 0 and specie1[x][yp][0] > 0:
				specie1_neighbours += 1
  			if specie1[x][y][0] == 0 and specie1[xp][yp][0] > 0:
				specie1_neighbours += 1
  			# [Specie2]
  			if specie2[x][y][0] == 0 and specie2[xm][y][0] > 0:
				specie2_neighbours += 1
  			if specie2[x][y][0] == 0 and specie2[xp][y][0] > 0:
				specie2_neighbours += 1
  			if specie2[x][y][0] == 0 and specie2[xm][ym][0] > 0:
				specie2_neighbours += 1
  			if specie2[x][y][0] == 0 and specie2[x][ym][0] > 0:
				specie2_neighbours += 1
  			if specie2[x][y][0] == 0 and specie2[xp][ym][0] > 0:
				specie2_neighbours += 1
  			if specie2[x][y][0] == 0 and specie2[xm][yp][0] > 0:
				specie2_neighbours += 1
  			if specie2[x][y][0] == 0 and specie2[x][yp][0] > 0:
				specie2_neighbours += 1
  			if specie2[x][y][0] == 0 and specie2[xp][yp][0] > 0:
				specie2_neighbours += 1

			# [plants logic]

			# if old, plant dies
			if plants[x][y][0] >= PLANTS_LIFE_EXPECTANCY + int(datafromfile[16]):
				plants[x][y][0] = 0
				plants[x][y][1] = 0
			# if no energy, plant dies
			if plants[x][y][0] > 0 and plants[x][y][0] < PLANTS_LIFE_EXPECTANCY + int(datafromfile[16]) and plants[x][y][1] <= 0:
 				plants[x][y][0] = 0
				plants[x][y][1] = 0
			# plant grows
			if plants[x][y][0]>0 and plants[x][y][0] < PLANTS_LIFE_EXPECTANCY + int(datafromfile[16]):
 				plants[x][y][0] += 1
				plants[x][y][1] = plants[x][y][1] + PLANTS_ENERGY_BASE_PER_CYCLE + int(datafromfile[20])
				plants_individuals += 1
				plants_energy += plants[x][y][1]
			# plant reproduction
                        if int(datafromfile[17]) > 0 and plants[x][y][0] == 0 and plants_neighbours > 0 and plants[x][y][2] == 0:
				if PLANTS_NEARBORN_CHANCES - int(datafromfile[17]) < 2:
					randomborn = 2
				else:
					randomborn = PLANTS_NEARBORN_CHANCES - int(datafromfile[17])
                                random_number = random.randint(1,randomborn)
                                if random_number == 1:
                                        plants[x][y][0] = 1
                                        plants[x][y][1] = PLANTS_ENERGY_BASE_PER_CYCLE + int(datafromfile[20])
                                        plants_individuals += 1
                                        plants_energy += plants[x][y][1]
			# spontaneous generation
			if int(plants[x][y][0] == 0) and plants_neighbours == 0 and plants[x][y][2] == 0 and ((plants_last_individuals == 0 and plants_individuals == 0 and real_mode == 1) or real_mode == 0):
				random_number = random.randint(1,PLANTS_RANDOM_BORN_CHANCES)
				if random_number == 1:
					plants[x][y][0] = 1
					plants[x][y][1] = PLANTS_ENERGY_BASE_PER_CYCLE + int(datafromfile[20])
					plants_individuals += 1
					plants_energy += plants[x][y][1]

			# [specie1 logic]

			# individual alive
			if specie1[x][y][0] > 0:
				#print "("+str(x)+","+str(y)+") is alive"
				# try to eat
  				if plants[x][y][1] > 0:
  					total_energy=0
  					if plants[x][y][1] > SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(datafromfile[6]):
						total_energy = SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(datafromfile[6])
						plants[x][y][1] = plants[x][y][1] - (SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(datafromfile[6]))
  					else:
						total_energy = plants[x][y][1]
						plants[x][y][1] = 0
  					specie1[x][y][1] = specie1[x][y][1] + total_energy
					#print "("+str(x)+","+str(y)+") eats"
  				# grow and decrease energy
  				specie1[x][y][0] += 1
  				specie1[x][y][1] = specie1[x][y][1] - (SPECIE1_ENERGY_NEEDED_PER_CYCLE  + int(datafromfile[5]))
				#print "("+str(x)+","+str(y)+") grows"
 				# die if no energy
				if specie1[x][y][1] < 0:
					specie1[x][y][1] = 0
					specie1[x][y][0] = 0
					#print "("+str(x)+","+str(y)+") dies"
  				# try to replicate
  				if specie1[x][y][1] > SPECIE1_ENERGY_TO_REPLICATE and specie1[x][y][2] == 0:
  					available_spots = [0 for numspots in range(8)]
  					pos=0
					if int(datafromfile[1]) > 0:
						if SPECIE1_NEARBORN_CHANCES - int(datafromfile[1]) < 2:
                                        		randomborn = 2
                                		else:
                                        		randomborn = SPECIE1_NEARBORN_CHANCES - int(datafromfile[1])
  						random_number = random.randint(1,randomborn)
  						if specie1[xm][y][0] == 0:
							available_spots[pos] = 1
							pos += 1
  						if specie1[xp][y][0] == 0:
							available_spots[pos] = 2
							pos += 1
  						if specie1[xm][ym][0] == 0:
							available_spots[pos] = 3
							pos += 1
  						if specie1[x][ym][0] == 0:
							available_spots[pos] = 4
							pos += 1
  						if specie1[xp][ym][0] == 0:
							available_spots[pos] = 5
							pos += 1
  						if specie1[xm][yp][0] == 0:
							available_spots[pos] = 6
							pos += 1
  						if specie1[x][yp][0] == 0:
							available_spots[pos] = 7
							pos += 1
 						if specie1[xp][yp][0] == 0:
							available_spots[pos] = 8
							pos += 1
  						if pos > 0:
  							rand_pos=random.randint(0,pos-1)
							if random_number == 1:
								#print "ready to reproduce at ("+str(xm)+","+str(ym)+") - ("+str(xp)+","+str(yp)+") - center ("+str(x)+","+str(y)+")"
								if available_spots[rand_pos] == 1:
									specie1[xm][y][0] = 1
									specie1[xm][y][1] = SPECIE1_ENERGY_BASE
									#print "("+str(xm)+","+str(y)+") born"
								if available_spots[rand_pos] == 2:
                                                                	specie1[xp][y][0] = 1
                                                                	specie1[xp][y][1] = SPECIE1_ENERGY_BASE
									#print "("+str(xp)+","+str(y)+") born"
								if available_spots[rand_pos] == 3:
                                                                	specie1[xm][ym][0] = 1
                                                                	specie1[xm][ym][1] = SPECIE1_ENERGY_BASE
									#print "("+str(xm)+","+str(ym)+") born"
								if available_spots[rand_pos] == 4:
                                                                	specie1[x][ym][0] = 1
                                                                	specie1[x][ym][1] = SPECIE1_ENERGY_BASE
									#print "("+str(x)+","+str(ym)+") born"
								if available_spots[rand_pos] == 5:
                                                                	specie1[xp][ym][0] = 1
                                                                	specie1[xp][ym][1] = SPECIE1_ENERGY_BASE
									#print "("+str(xp)+","+str(ym)+") born"
								if available_spots[rand_pos] == 6:
                                                                	specie1[xm][yp][0] = 1
                                                                	specie1[xm][yp][1] = SPECIE1_ENERGY_BASE
									#print "("+str(xm)+","+str(yp)+") born"
								if available_spots[rand_pos] == 7:
                                                                	specie1[x][yp][0] = 1
                                                                	specie1[x][yp][1] = SPECIE1_ENERGY_BASE
									#print "("+str(x)+","+str(yp)+") born"
								if available_spots[rand_pos] == 8:
                                                                	specie1[xp][yp][0] = 1
                                                                	specie1[xp][yp][1] = SPECIE1_ENERGY_BASE
									#print "("+str(xp)+","+str(yp)+") born"
								#print "end of reproduction"
  				# die if too old
  				if specie1[x][y][0] > SPECIE1_LIFE_EXPECTANCY + int(datafromfile[0]):
					specie1[x][y][1] = 0
					specie1[x][y][0] = 0
					#print "("+str(x)+","+str(y)+") dies"
				specie1_individuals += 1
				specie1_energy += specie1[x][y][1]
			# if no individual is alive, random born to avoid extintion
  			if specie1[x][y][0] == 0 and specie1_neighbours==0 and specie1[x][y][2] == 0 and ((specie1_last_individuals == 0 and specie1_individuals == 0 and real_mode == 1) or real_mode == 0):
				random_number = random.randint(1,SPECIE1_RANDOM_BORN_CHANCES)
				if random_number==1:
					specie1[x][y][0] = 1
					specie1[x][y][1] = SPECIE1_ENERGY_BASE
					#print "("+str(x)+","+str(y)+") random born"
					specie1_individuals += 1
					specie1_energy += specie1[x][y][1]

			# [species 2 logic]

			# individual alive
                        if specie2[x][y][0] > 0:
                                # try to eat
                                if plants[x][y][1] > 0:
                                        total_energy=0
                                        if plants[x][y][1] > SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(datafromfile[14]):
                                                total_energy = SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(datafromfile[14])
                                                plants[x][y][1] = plants[x][y][1] - (SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(datafromfile[14]))
                                        else:
                                                total_energy = plants[x][y][1]
                                                plants[x][y][1] = 0
                                        specie2[x][y][1] = specie2[x][y][1] + total_energy
                                # grow and decrease energy
                                specie2[x][y][0] += 1
                                specie2[x][y][1] = specie2[x][y][1] - (SPECIE2_ENERGY_NEEDED_PER_CYCLE + int(datafromfile[13]))
                                # die if no energy
                                if specie2[x][y][1] < 0:
                                         specie2[x][y][1] = 0
                                         specie2[x][y][0] = 0
				# try to replicate
                                if specie2[x][y][1] > SPECIE2_ENERGY_TO_REPLICATE and specie2[x][y][2] == 0:
                                        available_spots = [0 for numspots in range(8)]
                                        pos=0
					if int(datafromfile[9]) > 0:
						if SPECIE2_NEARBORN_CHANCES - int(datafromfile[9]) < 2:
                                                        randomborn = 2
                                                else:
                                                        randomborn = SPECIE2_NEARBORN_CHANCES - int(datafromfile[9])
                                                random_number = random.randint(1,randomborn)
                                        	if specie2[xm][y][0] == 0:
                                                	available_spots[pos] = 1
                                                	pos += 1
                                        	if specie2[xp][y][0] == 0:
                                                	available_spots[pos] = 2
                                                	pos += 1
                                        	if specie2[xm][ym][0] == 0:
                                                	available_spots[pos] = 3
                                                	pos += 1
                                        	if specie2[x][ym][0] == 0:
                                                	available_spots[pos] = 4
                                                	pos += 1
                                        	if specie2[xp][ym][0] == 0:
                                                	available_spots[pos] = 5
                                                	pos += 1
                                        	if specie2[xm][yp][0] == 0:
                                                	available_spots[pos] = 6
                                                	pos += 1
                                        	if specie2[x][yp][0] == 0:
                                                	available_spots[pos] = 7
                                                	pos += 1
                                        	if specie2[xp][yp][0] == 0:
                                                	available_spots[pos] = 8
                                                	pos += 1
						if pos > 0:
                                                	rand_pos=random.randint(0,pos-1)
                                                	if random_number == 1:
                                                        	if available_spots[rand_pos] == 1:
                                                                	specie2[xm][y][0] = 1
                                                                	specie2[xm][y][1] = SPECIE2_ENERGY_BASE
                                                        	if available_spots[rand_pos] == 2:
                                                                	specie2[xp][y][0] = 1
                                                                	specie2[xp][y][1] = SPECIE2_ENERGY_BASE
                                                        	if available_spots[rand_pos] == 3:
                                                                	specie2[xm][ym][0] = 1
                                                                	specie2[xm][ym][1] = SPECIE2_ENERGY_BASE
                                                        	if available_spots[rand_pos] == 4:
                                                                	specie2[x][ym][0] = 1
                                                                	specie2[x][ym][1] = SPECIE2_ENERGY_BASE
                                                        	if available_spots[rand_pos] == 5:
                                                                	specie2[xp][ym][0] = 1
                                                                	specie2[xp][ym][1] = SPECIE2_ENERGY_BASE
                                                        	if available_spots[rand_pos] == 6:
                                                                	specie2[xm][yp][0] = 1
                                                                	specie2[xm][yp][1] = SPECIE2_ENERGY_BASE
                                                        	if available_spots[rand_pos] == 7:
                                                                	specie2[x][yp][0] = 1
                                                                	specie2[x][yp][1] = SPECIE2_ENERGY_BASE
                                                        	if available_spots[rand_pos] == 8:
                                                                	specie2[xp][yp][0] = 1
                                                                	specie2[xp][yp][1] = SPECIE2_ENERGY_BASE
				# die if too old
                                if specie2[x][y][0] > SPECIE2_LIFE_EXPECTANCY + int(datafromfile[8]):
                                        specie2[x][y][1] = 0
                                        specie2[x][y][0] = 0
                        	specie2_individuals += 1
				specie2_energy += specie2[x][y][1]
			# if no individual is alive, random born to avoid extintion
                        if specie2[x][y][0] == 0 and specie2_neighbours == 0 and specie2[x][y][2] == 0 and ((specie2_last_individuals == 0 and specie2_individuals == 0 and real_mode == 1) or real_mode == 0):
				random_number = random.randint(1,SPECIE2_RANDOM_BORN_CHANCES)
                        	if random_number==1:
					specie2[x][y][0] = 1
                                	specie2[x][y][1] = SPECIE2_ENERGY_BASE
					specie2_individuals +=1
					specie2_energy += specie2[x][y][1]


			# draw
			if gradient_mode == 1:
				if plants[x][y][1]>255 * rf:
					white = (255,255,255)
				else:
					white = (int(plants[x][y][1]/rf),int(plants[x][y][1]/rf),int(plants[x][y][1]/rf))
				if specie1[x][y][1]>255:
					yellow = (255,255,0)
				else:
					yellow = (int(specie1[x][y][1]/rf),int(specie1[x][y][1]/rf),0)
				if specie2[x][y][1]>255 * rf:
					blue = (0,0,255)
				else:
					blue = (0,0,int(specie2[x][y][1]/rf))
				if specie1[x][y][1]+specie2[x][y][1] > 255 * rf:
					magenta = (255,0,255)
				else:
					magenta = (int(specie1[x][y][1]/rf)+int(specie2[x][y][1]/rf),0,int((specie1[x][y][1]+specie2[x][y][1])/rf))

			if specie1[x][y][0] > 0 and specie2[x][y][0] > 0:
				pygame.draw.circle(screen,magenta,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
			if specie1[x][y][0] > 0 and specie2[x][y][0] == 0:
                                pygame.draw.circle(screen,yellow,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
			if specie1[x][y][0] == 0 and specie2[x][y][0] > 0:
                                pygame.draw.circle(screen,blue,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
			if specie1[x][y][0] == 0 and specie2[x][y][0] == 0 and plants[x][y][0] > 0:
                                pygame.draw.circle(screen,white,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
			if specie1[x][y][0] == 0 and specie2[x][y][0] == 0 and plants[x][y][0] == 0:
                                pygame.draw.circle(screen,black,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)

	if graph_mode == 1:
		# generate graphs
		for x in range(1,200):
			specie1_Iarray[x-1] = specie1_Iarray[x]
			specie2_Iarray[x-1] = specie2_Iarray[x]
			plants_Iarray[x-1] = plants_Iarray[x]
			specie1_Earray[x-1] = specie1_Earray[x]
			specie2_Earray[x-1] = specie2_Earray[x]
			plants_Earray[x-1] = plants_Earray[x]
		specie1_Iarray[199] = specie1_individuals
		specie2_Iarray[199] = specie2_individuals
		plants_Iarray[199] = plants_individuals
		specie1_Earray[199] = specie1_energy
		specie2_Earray[199] = specie2_energy
		plants_Earray[199] = plants_energy

		# draw graphs
		pygame.draw.line(screen,midgrey,(450,350),(650,350))
		pygame.draw.line(screen,midgrey,(650,350),(650,20))
		pygame.draw.line(screen,midgrey,(700,350),(900,350))
		pygame.draw.line(screen,midgrey,(900,350),(900,20))
		text_individuals = textfont.render("Individuals",False, midgrey, black)
		text_energy = textfont.render("Energy",False, midgrey, black)
		screen.blit(text_individuals,(480,400))
		screen.blit(text_energy,(740,400))

		for x in range(0,200):
			pygame.draw.line(screen,yellowgraph,(450+x,350-int(specie1_Iarray[x]/(3*rf))),(450+x,350-int(specie1_Iarray[x]/(3*rf))))
			pygame.draw.line(screen,bluegraph,(450+x,350-int(specie2_Iarray[x]/(3*rf))),(450+x,350-int(specie2_Iarray[x]/(3*rf))))
			pygame.draw.line(screen,lightgrey,(450+x,350-int(plants_Iarray[x]/(3*rf))),(450+x,350-int(plants_Iarray[x]/(3*rf))))
			pygame.draw.line(screen,yellowgraph,(700+x,350-int(specie1_Earray[x]/(500*rf))),(700+x,350-int(specie1_Earray[x]/(500*rf))))
	        	pygame.draw.line(screen,bluegraph,(700+x,350-int(specie2_Earray[x]/(500*rf))),(700+x,350-int(specie2_Earray[x]/(500*rf))))
	        	pygame.draw.line(screen,lightgrey,(700+x,350-int(plants_Earray[x]/(5000*rf))),(700+x,350-int(plants_Earray[x]/(5000*rf))))

		# transparent graph for fullscreen mode
	if fullscreen_graph == 1 and fullscreen_mode == 1:
		# generate fullscreen graphs
                for x in range(1,200):
                        specie1_Iarray[x-1] = specie1_Iarray[x]
                        specie2_Iarray[x-1] = specie2_Iarray[x]
                        plants_Iarray[x-1] = plants_Iarray[x]
                specie1_Iarray[199] = specie1_individuals
                specie2_Iarray[199] = specie2_individuals
                plants_Iarray[199] = plants_individuals

		for x in range(0,200):
			pygame.draw.rect(graphsurface,bluegraph,pygame.Rect(x*10,1080-(int(specie2_Iarray[x]/(3*rf))+int(plants_Iarray[x]/(3*rf))+int(specie1_Iarray[x]/(3*rf))),10,int(specie2_Iarray[x]/(3*rf))))
			pygame.draw.rect(graphsurface,yellowgraph,pygame.Rect(x*10,1080-(int(specie1_Iarray[x]/(3*rf))+int(plants_Iarray[x]/(3*rf))),10,int(specie1_Iarray[x]/(3*rf))))
                        pygame.draw.rect(graphsurface,whitegraph,pygame.Rect(x*10,1080-int(plants_Iarray[x]/(3*rf)),10,int(plants_Iarray[x]/(3*rf))))
		screen.blit(graphsurface,(0,0))

	if graph_mode == 1:
		pygame.draw.rect(screen,black,(40,40,320,320),1)
	pygame.display.update()
