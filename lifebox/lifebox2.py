import pygame
import sys
import random
import threading
import time
import os
from pyfirmata import ArduinoMega, util
import rtmidi # midi library

import lifebox_constants as constants

potData = [0] * 11

# potData[0] Vitality [Plants] A0
plantsvitality = 0
# potData[1] Reproduction [Plants] A1
plantsreproduction = 0
# potData[2] Generation [Plants] A2
plantsgeneration = 0

# potData[3] Reproduction [Specie1 (YELLOW)] A3
sp1reproduction = 0
# potData[4] Vitality [Specie1] A4
sp1vitality = 0
# potData[5] Efficiency [Specie1] A5
sp1efficency = 0
# potData[6] Gathering [Specie1] A6
sp1gathering = 0

# potData[7] Vitality [Specie2 (BLUE)] A7
sp2vitality = 0
# potData[8] Reproduction [Specie2] A8
sp2reproduction = 0
# potData[9] Efficiency [Specie2] A9
sp2efficency = 0
# potData[10] Gathering [Specie2] A10
sp2gathering = 0






# lifebox functions

def plants_next_iteration(x,y):
	global plants_individuals
	global full_matrix_plants_energy
	global plantsreproduction
	global plantsvitality
	global plantsgeneration
	neighbours = 0
	# maping plants potData
	plantsreproduction = map(potData[1],0,1023,0,120)
	# potData[0] Vitality [Plants] A0
	plantsvitality = map(potData[0],0,1023,0,120)
	# potData[2] Generation [Plants] A2
	plantsgeneration = map(potData[2],0,1023,0,120)

	#if midi_enable:
	#			midiout.send_message(note_off_white)
	# adjacent coordinates
	xp = (x+1)
	if xp >= matrix_size_x:
		xp = matrix_size_x - 1
	xm = (x-1)
	if xm < 0:
		xm = 0
	yp = (y+1)
	if yp >= matrix_size_y:
		yp = matrix_size_y - 1
	ym = (y-1)
	if ym < 0:
		ym = 0
	# count the number of currently live neighbouring cells
	if plants[x][y][0] == 0 and plants[xm][y][0] > 0:
		neighbours += 1
	if plants[x][y][0] == 0 and plants[xp][y][0] > 0:
		neighbours += 1
	if plants[x][y][0] == 0 and plants[xm][ym][0] > 0:
		neighbours += 1
	if plants[x][y][0] == 0 and plants[x][ym][0] > 0:
		neighbours += 1
	if plants[x][y][0] == 0 and plants[xp][ym][0] > 0:
		neighbours += 1
	if plants[x][y][0] == 0 and plants[xm][yp][0] > 0:
		neighbours += 1
	if plants[x][y][0] == 0 and plants[x][yp][0] > 0:
		neighbours += 1
	if plants[x][y][0] == 0 and plants[xp][yp][0] > 0:
		neighbours += 1
	# if too old, plant dies
	if plants[x][y][0] >= constants.PLANTS_LIFE_EXPECTANCY + int(potData[0]):
		plants[x][y][0] = 0
		plants[x][y][1] = 0
	# if no energy, plant dies
	if plants[x][y][0] > 0 and plants[x][y][0] < constants.PLANTS_LIFE_EXPECTANCY + int(potData[0]) and plants[x][y][1] <= 0:
		plants[x][y][0] = 0
		plants[x][y][1] = 0
	# plant growsplants
	if plants[x][y][0]>0 and plants[x][y][0] < constants.PLANTS_LIFE_EXPECTANCY + int(potData[0]):
		plants[x][y][0] += 1
		plants[x][y][1] = plants[x][y][1] + constants.PLANTS_ENERGY_BASE_PER_CYCLE
		plants_individuals += 1
		full_matrix_plants_energy += plants[x][y][1]
	# plant reproduction
	if int(plantsreproduction) > 0 and plants[x][y][0] == 0 and neighbours > 0 and plants[x][y][2] == 0:
		if constants.PLANTS_NEARBORN_CHANCES - int(plantsreproduction) < 2:
			randomborn = 2
		else:
			randomborn = constants.PLANTS_NEARBORN_CHANCES - int(plantsreproduction)
		random_number = random.randint(1,randomborn)
		if random_number == 1:
			plants[x][y][0] = 1
			plants[x][y][1] = constants.PLANTS_ENERGY_BASE_PER_CYCLE + int(potData[2])
			plants_individuals += 1
			#if midi_enable:
			#	midiout.send_message(note_on_white)
			full_matrix_plants_energy += plants[x][y][1]
	# spontaneous generation
	if int(plants[x][y][0] == 0) and neighbours == 0 and plants[x][y][2] == 0 and ((plants_last_individuals == 0 and plants_individuals == 0 and real_mode == 1) or real_mode == 0):
		random_number = random.randint(1,constants.PLANTS_RANDOM_BORN_CHANCES)
		if random_number == 1:
			plants[x][y][0] = 1
			plants[x][y][1] = constants.PLANTS_ENERGY_BASE_PER_CYCLE + int(potData[2])
			plants_individuals += 1
			full_matrix_plants_energy += plants[x][y][1]
			#if midi_enable:
			#	midiout.send_message(note_on_white)
			

	
def species_next_iteration(x,y):
	global specie1_individuals
	global specie2_individuals
	global full_matrix_specie1_energy
	global full_matrix_specie2_energy
	global sp1reproduction
	global sp1vitality
	global sp1efficency
	global sp1gathering
	global sp2reproduction
	global sp2vitality
	global sp2efficency
	global sp2gathering
	# maping plants potData
	sp1reproduction = map(potData[3],0,1023,0,80)
	sp1vitality = map(potData[4],0,1023,0,100)
	sp1efficency = map(potData[5],0,1023,0,100)
	sp1gathering = map(potData[6],0,1023,0,100)
	sp2reproduction = map(potData[8],0,1023,0,100)
	sp2vitality = map(potData[7],0,1023,0,100)
	sp2efficency = map(potData[9],0,1023,0,100)
	sp2gathering = map(potData[10],0,1023,0,100)

	# midi
	if midi_enable:
		midiout.send_message(note_off_blue)
		midiout.send_message(note_off_yellow)

	# adjacent coordinates
	xp = (x+1)
	if xp >= matrix_size_x:
		xp = matrix_size_x - 1
	xm = (x-1)
	if xm < 0:
		xm = 0
	yp = (y+1)
	if yp >= matrix_size_y:
		yp = matrix_size_y - 1
	ym = (y-1)
	if ym < 0:
		ym = 0
	# count the number of currently live neighbouring cells
	# [Specie1]
	specie1_neighbours = 0
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
	specie2_neighbours = 0
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

		
	# --- SPICE 1 ---
	# individual is alive
	if specie1[x][y][0] > 0:
		#print "("+str(x)+","+str(y)+") is alive"
		# try to eat
		if plants[x][y][1] > 0:
			total_energy=0
			if plants[x][y][1] > constants.SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(potData[6]):
				total_energy = constants.SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(potData[6])
				plants[x][y][1] = plants[x][y][1] - (constants.SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(potData[6]))
			else:
				total_energy = plants[x][y][1]
				plants[x][y][1] = 0
			specie1[x][y][1] = specie1[x][y][1] + total_energy
			#print "("+str(x)+","+str(y)+") eats"
		# grow and decrease energy
		specie1[x][y][0] += 1
		specie1[x][y][1] = specie1[x][y][1] - (constants.SPECIE1_ENERGY_NEEDED_PER_CYCLE  + int(potData[5]))
		#print "("+str(x)+","+str(y)+") grows"
		# die if no energy
		if specie1[x][y][1] < 0:
			specie1[x][y][1] = 0
			specie1[x][y][0] = 0
			#print "("+str(x)+","+str(y)+") dies"
		# try to replicate
		if specie1[x][y][1] > constants.SPECIE1_ENERGY_TO_REPLICATE and specie1[x][y][2] == 0:
			available_spots = [0 for numspots in range(8)]
			pos=0
			if int(sp1reproduction) > 0:
				if constants.SPECIE1_NEARBORN_CHANCES - int(sp1reproduction) < 2:
					randomborn = 2
				else:
					randomborn = constants.SPECIE1_NEARBORN_CHANCES - int(sp1reproduction)
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
							specie1[xm][y][1] = constants.SPECIE1_ENERGY_BASE
							#print "("+str(xm)+","+str(y)+") born"
						if available_spots[rand_pos] == 2:
							specie1[xp][y][0] = 1
							specie1[xp][y][1] = constants.SPECIE1_ENERGY_BASE
							#print "("+str(xp)+","+str(y)+") born"
						if available_spots[rand_pos] == 3:
							specie1[xm][ym][0] = 1
							specie1[xm][ym][1] = constants.SPECIE1_ENERGY_BASE
							#print "("+str(xm)+","+str(ym)+") born"
						if available_spots[rand_pos] == 4:
							specie1[x][ym][0] = 1
							specie1[x][ym][1] = constants.SPECIE1_ENERGY_BASE
							#print "("+str(x)+","+str(ym)+") born"
						if available_spots[rand_pos] == 5:
							specie1[xp][ym][0] = 1
							specie1[xp][ym][1] = constants.SPECIE1_ENERGY_BASE
							#print "("+str(xp)+","+str(ym)+") born"
						if available_spots[rand_pos] == 6:
							specie1[xm][yp][0] = 1
							specie1[xm][yp][1] = constants.SPECIE1_ENERGY_BASE
							#print "("+str(xm)+","+str(yp)+") born"
						if available_spots[rand_pos] == 7:
							specie1[x][yp][0] = 1
							specie1[x][yp][1] = constants.SPECIE1_ENERGY_BASE
							#print "("+str(x)+","+str(yp)+") born"
						if available_spots[rand_pos] == 8:
							specie1[xp][yp][0] = 1
							specie1[xp][yp][1] = constants.SPECIE1_ENERGY_BASE
							#print "("+str(xp)+","+str(yp)+") born"
						#print "end of reproduction"
						if midi_enable:
							midiout.send_message(note_on_yellow)
		# die if too old
		if specie1[x][y][0] > constants.SPECIE1_LIFE_EXPECTANCY + int(potData[4]):
			specie1[x][y][1] = 0
			specie1[x][y][0] = 0
			#print "("+str(x)+","+str(y)+") dies"
		# accounting individuals
		specie1_individuals += 1
		full_matrix_specie1_energy += specie1[x][y][1]
	# if no individual is alive, random born to avoid extintion
	if specie1[x][y][0] == 0 and specie1_neighbours==0 and specie1[x][y][2] == 0 and ((specie1_last_individuals == 0 and specie1_individuals == 0 and real_mode == 1) or real_mode == 0):
		random_number = random.randint(1,constants.SPECIE1_RANDOM_BORN_CHANCES)
		if random_number==1:
			specie1[x][y][0] = 1
			specie1[x][y][1] = constants.SPECIE1_ENERGY_BASE
			#print "("+str(x)+","+str(y)+") random born"
			if midi_enable:
				midiout.send_message(note_on_yellow)
			specie1_individuals += 1
			full_matrix_specie1_energy += specie1[x][y][1]
			
	# --- SPICE 2 ---
	# individual is alive
	if specie2[x][y][0] > 0:
		#print "("+str(x)+","+str(y)+") is alive"
		# try to eat
		if plants[x][y][1] > 0:
			total_energy=0
			if plants[x][y][1] > constants.SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(potData[10]):
				total_energy = constants.SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(potData[10])
				plants[x][y][1] = plants[x][y][1] - (constants.SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(potData[10]))
			else:
				total_energy = plants[x][y][1]
				plants[x][y][1] = 0
			specie2[x][y][1] = specie2[x][y][1] + total_energy
			#print "("+str(x)+","+str(y)+") eats"
		# grow and decrease energy
		specie2[x][y][0] += 1
		specie2[x][y][1] = specie2[x][y][1] - (constants.SPECIE2_ENERGY_NEEDED_PER_CYCLE  + int(potData[9]))
		#print "("+str(x)+","+str(y)+") grows"
		# die if no energy
		if specie2[x][y][1] < 0:
			specie2[x][y][1] = 0
			specie2[x][y][0] = 0
			#print "("+str(x)+","+str(y)+") dies"
		# try to replicate
		if specie2[x][y][1] > constants.SPECIE2_ENERGY_TO_REPLICATE and specie2[x][y][2] == 0:
			available_spots = [0 for numspots in range(8)]
			pos=0
			if int(sp2reproduction) > 0:
				if constants.SPECIE2_NEARBORN_CHANCES - int(sp2reproduction) < 2:
					randomborn = 2
				else:
					randomborn = constants.SPECIE2_NEARBORN_CHANCES - int(sp2reproduction)
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
						#print "ready to reproduce at ("+str(xm)+","+str(ym)+") - ("+str(xp)+","+str(yp)+") - center ("+str(x)+","+str(y)+")"
						if available_spots[rand_pos] == 1:
							specie2[xm][y][0] = 1
							specie2[xm][y][1] = constants.SPECIE2_ENERGY_BASE
							#print "("+str(xm)+","+str(y)+") born"
						if available_spots[rand_pos] == 2:
							specie2[xp][y][0] = 1
							specie2[xp][y][1] = constants.SPECIE2_ENERGY_BASE
							#print "("+str(xp)+","+str(y)+") born"
						if available_spots[rand_pos] == 3:
							specie2[xm][ym][0] = 1
							specie2[xm][ym][1] = constants.SPECIE2_ENERGY_BASE
							#print "("+str(xm)+","+str(ym)+") born"
						if available_spots[rand_pos] == 4:
							specie2[x][ym][0] = 1
							specie2[x][ym][1] = constants.SPECIE2_ENERGY_BASE
							#print "("+str(x)+","+str(ym)+") born"
						if available_spots[rand_pos] == 5:
							specie2[xp][ym][0] = 1
							specie2[xp][ym][1] = constants.SPECIE2_ENERGY_BASE
							#print "("+str(xp)+","+str(ym)+") born"
						if available_spots[rand_pos] == 6:
							specie2[xm][yp][0] = 1
							specie2[xm][yp][1] = constants.SPECIE2_ENERGY_BASE
							#print "("+str(xm)+","+str(yp)+") born"
						if available_spots[rand_pos] == 7:
							specie2[x][yp][0] = 1
							specie2[x][yp][1] = constants.SPECIE2_ENERGY_BASE
							#print "("+str(x)+","+str(yp)+") born"
						if available_spots[rand_pos] == 8:
							specie2[xp][yp][0] = 1
							specie2[xp][yp][1] = constants.SPECIE2_ENERGY_BASE
							#print "("+str(xp)+","+str(yp)+") born"
						#print "end of reproduction"
						if midi_enable:
							midiout.send_message(note_on_blue)
		# die if too old
		if specie2[x][y][0] > constants.SPECIE2_LIFE_EXPECTANCY + int(potData[7]):
			specie2[x][y][1] = 0
			specie2[x][y][0] = 0
			#print "("+str(x)+","+str(y)+") dies"
		# accounting individuals
		specie2_individuals += 1
		full_matrix_specie2_energy += specie2[x][y][1]
	# if no individual is alive, random born to avoid extintion
	if specie2[x][y][0] == 0 and specie2_neighbours==0 and specie2[x][y][2] == 0 and ((specie2_last_individuals == 0 and specie2_individuals == 0 and real_mode == 1) or real_mode == 0):
		random_number = random.randint(1,constants.SPECIE2_RANDOM_BORN_CHANCES)
		if random_number==1:
			specie2[x][y][0] = 1
			specie2[x][y][1] = constants.SPECIE2_ENERGY_BASE
			#print "("+str(x)+","+str(y)+") random born"
			if midi_enable:
				midiout.send_message(note_on_blue)
			specie2_individuals += 1
			full_matrix_specie2_energy += specie2[x][y][1]


def map(x,in_min,in_max,out_min,out_max):
	return int((float(x) - float(in_min)) * (float(out_max) - float(out_min)) / (float(in_max) - float(in_min)) + float(out_min))

def draw_species(x,y):
	if gradient_mode == 1:
		if plants[x][y][1]>200 * rf:
			green = (0,200,0)
		else:
			green = (0,int(plants[x][y][1]/rf),0)
		if specie1[x][y][1]>200 * rf:
			yellow = (200,200,0)
		else:
			yellow = (int(specie1[x][y][1]/rf),int(specie1[x][y][1]/rf),0)
		if specie2[x][y][1]>200 * rf:
			blue = (0,0,200)
		else:
			blue = (0,0,int(specie2[x][y][1]/rf))
		if specie1[x][y][1]+specie2[x][y][1] > 200 * rf:
			magenta = (200,0,200)
		else:
			magenta = (int(specie1[x][y][1]/rf)+int(specie2[x][y][1]/rf),0,int((specie1[x][y][1]+specie2[x][y][1])/rf))
	else:
		white = (255,255,255)
		green = (0,255,0)
		yellow = (255,255,0)
		blue = (0,0,255)
		magenta = (255,0,255)

	if specie1[x][y][0] > 0 and specie2[x][y][0] > 0:
		pygame.draw.circle(screen,magenta,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
	if specie1[x][y][0] > 0 and specie2[x][y][0] == 0:
		pygame.draw.circle(screen,yellow,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
	if specie1[x][y][0] == 0 and specie2[x][y][0] > 0:
		pygame.draw.circle(screen,blue,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
	if specie1[x][y][0] == 0 and specie2[x][y][0] == 0 and plants[x][y][0] > 0:
		pygame.draw.circle(screen,green,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
	if specie1[x][y][0] == 0 and specie2[x][y][0] == 0 and plants[x][y][0] == 0:
		pygame.draw.circle(screen,constants.BLACK,(((x*2*circle_size)+circle_size)+40,((y*2*circle_size)+circle_size)+40),circle_size,0)
	if debug == True:
		deb_prep = textfont.render("plants reproduction: "+str(plantsreproduction),False, constants.MIDGREY, constants.BLACK)
		deb_pvit = textfont.render("plants vitality: "+str(plantsvitality),False, constants.MIDGREY, constants.BLACK)
		deb_pgen = textfont.render("plants generation: "+str(plantsgeneration),False, constants.MIDGREY, constants.BLACK)
		deb_sp1rep = textfont.render("sp1 reproduction: "+str(sp1reproduction),False, constants.MIDGREY, constants.BLACK)
		deb_sp1vit = textfont.render("sp1 vitality: "+str(sp1vitality),False, constants.MIDGREY, constants.BLACK)
		deb_sp1eff = textfont.render("sp1 efficiency: "+str(sp1efficency),False, constants.MIDGREY, constants.BLACK)
		deb_sp1gath = textfont.render("sp1 gathering: "+str(sp1gathering),False, constants.MIDGREY, constants.BLACK)
		deb_sp2rep = textfont.render("sp2 reproduction: "+str(sp2reproduction),False, constants.MIDGREY, constants.BLACK)
		deb_sp2vit = textfont.render("sp2 vitality: "+str(sp2vitality),False, constants.MIDGREY, constants.BLACK)
		deb_sp2eff = textfont.render("sp2 efficiency: "+str(sp2efficency),False, constants.MIDGREY, constants.BLACK)
		deb_sp2gath = textfont.render("sp2 gathering: "+str(sp2gathering),False, constants.MIDGREY, constants.BLACK)	
		screen.blit(deb_pvit,(400,50))
		screen.blit(deb_prep,(400,90))
		screen.blit(deb_pgen,(400,130))
		screen.blit(deb_sp1rep,(400,170))
		screen.blit(deb_sp1vit,(400,210))
		screen.blit(deb_sp1eff,(400,250))
		screen.blit(deb_sp1gath,(400,290))
		screen.blit(deb_sp2rep,(400,330))
		screen.blit(deb_sp2vit,(400,370))
		screen.blit(deb_sp2eff,(400,410))
		screen.blit(deb_sp2gath,(400,450))


def readPotDatafromFile(stop):
	global potData
	while not stop:
		file = open("./controllerdata", "r")
		index = 0
		for x in file:
			#print(x)
			potData[index] = int(x)
			index = index + 1
		file.close()
		time.sleep(1)
		
def readPotDatafromArduino(stop):
	global potData
	board = ArduinoMega('/dev/ttyACM0')
	it = util.Iterator(board)
	it.start()
	for i in range (0,11):
		board.analog[i].enable_reporting()
	while not stop:
		for i in range (0,11):
			time.sleep(0.2)
			prevalue = potData[i]
			potData[i] = board.analog[i].read()
			if potData[i] is not None:
				potData[i] = potData[i] * 1023
			else:
				potData[i] = prevalue
				#if debug == True:
					#print ("Analog input ",i," > ",int(potData[i]))

		# map the values if needed
		#potData[x] = map(potData[x],0,1023,low,high)
		#time.sleep(1)
	#print("Arduino connection error! Change to app mode.")
	#os._exit(1)

midi_enable = 0 # play generative sound through midi out (under development)
graph_mode = 0 # show graphs
real_mode = 1 # respawn control
app_mode = True # via web / app or manual controller
gradient_mode = 1 # individual fade in / out linked to energy
fullscreen_mode = True
fullscreen_graph = 0
debug = True
rf = 2 # reduction factor

# run thread
stop = False
if app_mode == False:
	t = threading.Thread(target=readPotDatafromArduino,args=(stop,))
else:
	t = threading.Thread(target=readPotDatafromFile,args=(stop,))
t.daemon = True
t.start()

#pygame setup

pygame.init()
pygame.font.init()

# midi setup
if midi_enable:
	midiout = rtmidi.MidiOut()
	available_ports = midiout.get_ports()
	midiout.open_port(1) # this is my default Roland JD-Xi port, you must change it, check available_ports.
	note_on_white = [0x90,60,112] # channel 1, note C , velocity 112
	note_on_blue = [0x90,64,112] # channel 1, note E , velocity 112
	note_on_yellow = [0x90,67,112] # channel 1, note G , velocity 112
	note_off_white = [0x80,60,0]
	note_off_blue = [0x80,64,0]
	note_off_yellow = [0x80,67,0]
	

pygame.display.set_caption('LifeBox')

if fullscreen_mode == False:
	screen = pygame.display.set_mode((1000,600))
	matrix_size_x = 32
	matrix_size_y = 32
	circle_size = 5
else:
	# size for full HD screen (1920,1080)
	# if you have other screen size, you need yo change matrix_size_x,matrix_size_y and circle_size
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	matrix_size_x = 70
	matrix_size_y = 52
	circle_size = 7

textfont = pygame.font.SysFont('arial',30)
debugfont = pygame.font.SysFont('arial',15)


# fps management
clock = pygame.time.Clock()

# species matrix
t, w, h = 3,matrix_size_x, matrix_size_y
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

specie1IndividualsArray = [0 for x in range(200)]
specie2IndividualsArray = [0 for x in range(200)]
plantsIndividualsArray = [0 for x in range(200)]
specie1EnergyArray = [0 for x in range(200)]
specie2EnergyArray = [0 for x in range(200)]
plantsEnergyArray = [0 for x in range(200)]

specie2_individuals = 0
specie1_individuals = 0
plants_individuals = 0

# screen for transparent graph
graphsurface = pygame.Surface((1920, 1080), pygame.SRCALPHA, 32)

while (True):
	msElapsed = clock.tick(20)
	# control lifebox exit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			stop = True
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
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
	full_matrix_specie1_energy = 0
	full_matrix_specie2_energy = 0
	full_matrix_plants_energy = 0

	screen.fill(constants.BLACK)

	for x in range(0,matrix_size_x):
		for y in range(0,matrix_size_y):
			
			# [plants logic]
			plants_next_iteration(x,y)

			# [specie1 & species2 logic]
			species_next_iteration(x,y)

			# draw
			draw_species(x,y)
			

	if graph_mode == 1:
		# generate graphs
		for x in range(1,200):
			specie1IndividualsArray[x-1] = specie1IndividualsArray[x]
			specie2IndividualsArray[x-1] = specie2IndividualsArray[x]
			plantsIndividualsArray[x-1] = plantsIndividualsArray[x]
			specie1EnergyArray[x-1] = specie1EnergyArray[x]
			specie2EnergyArray[x-1] = specie2EnergyArray[x]
			plantsEnergyArray[x-1] = plantsEnergyArray[x]
			
		specie1IndividualsArray[199] = specie1_individuals
		specie2IndividualsArray[199] = specie2_individuals
		plantsIndividualsArray[199] = plants_individuals
		specie1EnergyArray[199] = full_matrix_specie1_energy
		specie2EnergyArray[199] = full_matrix_specie2_energy
		plantsEnergyArray[199] = full_matrix_plants_energy

		# draw graphs
		pygame.draw.line(screen,constants.MIDGREY,(450,350),(650,350))
		pygame.draw.line(screen,constants.MIDGREY,(650,350),(650,20))
		pygame.draw.line(screen,constants.MIDGREY,(700,350),(900,350))
		pygame.draw.line(screen,constants.MIDGREY,(900,350),(900,20))
		text_individuals = textfont.render("Individuals",False, constants.MIDGREY, constants.BLACK)
		text_energy = textfont.render("Energy",False, constants.MIDGREY, constants.BLACK)
		screen.blit(text_individuals,(480,400))
		screen.blit(text_energy,(740,400))

		for x in range(0,200):
			pygame.draw.line(screen,constants.YELLOWGRAPH,(450+x,350-int(specie1IndividualsArray[x]/(3*rf))),(450+x,350-int(specie1IndividualsArray[x]/(3*rf))))
			pygame.draw.line(screen,constants.BLUEGRAPH,(450+x,350-int(specie2IndividualsArray[x]/(3*rf))),(450+x,350-int(specie2IndividualsArray[x]/(3*rf))))
			pygame.draw.line(screen,constants.LIGHTGREY,(450+x,350-int(plantsIndividualsArray[x]/(3*rf))),(450+x,350-int(plantsIndividualsArray[x]/(3*rf))))
			pygame.draw.line(screen,constants.YELLOWGRAPH,(700+x,350-int(specie1EnergyArray[x]/(500*rf))),(700+x,350-int(specie1EnergyArray[x]/(500*rf))))
			pygame.draw.line(screen,constants.BLUEGRAPH,(700+x,350-int(specie2EnergyArray[x]/(500*rf))),(700+x,350-int(specie2EnergyArray[x]/(500*rf))))
			pygame.draw.line(screen,constants.LIGHTGREY,(700+x,350-int(plantsEnergyArray[x]/(5000*rf))),(700+x,350-int(plantsEnergyArray[x]/(5000*rf))))

	# transparent graph for fullscreen mode
	if fullscreen_graph == 1 and fullscreen_mode == True:
		# generate fullscreen graphs
		for x in range(1,200):
				specie1IndividualsArray[x-1] = specie1IndividualsArray[x]
				specie2IndividualsArray[x-1] = specie2IndividualsArray[x]
				plantsIndividualsArray[x-1] = plantsIndividualsArray[x]
				
		specie1IndividualsArray[199] = specie1_individuals
		specie2IndividualsArray[199] = specie2_individuals
		plantsIndividualsArray[199] = plants_individuals

		for x in range(0,200):
			pygame.draw.rect(graphsurface,constants.BLUEGRAPH,pygame.Rect(x*10,1080-(int(specie2IndividualsArray[x]/(3*rf))+int(plantsIndividualsArray[x]/(3*rf))+int(specie1IndividualsArray[x]/(3*rf))),10,int(specie2IndividualsArray[x]/(3*rf))))
			pygame.draw.rect(graphsurface,constants.YELLOWGRAPH,pygame.Rect(x*10,1080-(int(specie1IndividualsArray[x]/(3*rf))+int(plantsIndividualsArray[x]/(3*rf))),10,int(specie1IndividualsArray[x]/(3*rf))))
			pygame.draw.rect(graphsurface,constants.WHITEGRAPH,pygame.Rect(x*10,1080-int(plantsIndividualsArray[x]/(3*rf)),10,int(plantsIndividualsArray[x]/(3*rf))))
		screen.blit(graphsurface,(0,0))

	if graph_mode == 1:
		pygame.draw.rect(screen,constants.BLACK,(40,40,320,320),1)
	pygame.display.update()
