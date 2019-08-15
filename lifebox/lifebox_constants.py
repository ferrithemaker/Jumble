# colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUEGRAPH = (0,0,255,50)
YELLOWGRAPH = (255,255,0,50)
WHITEGRAPH = (255,255,255,50)
MIDGREY = (128,128,128)
BLACK = (0,0,0)
DARKGREY = (30,30,30)
LIGHTGREY = (200,200,200,50)


# species variables

#plants

PLANTS_LIFE_EXPECTANCY = 40 #A0
PLANTS_RANDOM_BORN_CHANCES = 5000 # fixed
PLANTS_NEARBORN_CHANCES = 120 #A1
PLANTS_ENERGY_BASE_PER_CYCLE = 30 #A2
# Each mana invidivual generates a defined amout of energy per cycle. This energy is gathered by the species. Low energy generation means a poor enviroment for the species to survive, and high energy generation a rich one.


#yellow
SPECIE1_LIFE_EXPECTANCY = 40 #A4
# Life expectancy is an statistical measure of the average time an organism is expected to live. Once a pixelic entity becomes stable, life expectancy determines how many reiterations does the pixel survive.
SPECIE1_RANDOM_BORN_CHANCES = 5000 
# Fixed
# Parthenogesis is a rare trait among species which allows them to reproduce without mating. The species inside LifeBox! can reproduce in a similar way. In case they achieve it, offspring is randomly populated inside the grid. 
# Setting this variable with a high value means less chances to reproduce that way. Otherwise, if user choose to reduce this value, parthenogenesis is more probable to happen
SPECIE1_NEARBORN_CHANCES = 120 #A3
# When two pixelic entities of the same specie are adjacent to each other, they can reproduce. This variable determines the reproduction chances, so a higher value means a higher chances to survive.
SPECIE1_ENERGY_BASE = 250
# fixed
# Every spices has a defined base level of energy when it borns, this base level will condition the chances of survival at very first stages of its life.
SPECIE1_ENERGY_NEEDED_PER_CYCLE = 120 #A5
# This parameter defines the species amount of energy consumtion at each iteration. Higher values mean that the species needs more energy per iteration cycle, meaning less efficiency.
SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE = 20 #A6
# As the previous parameter defines the efficiency of energy consumtion, this one defines the efficiency of energy gathering from the mana. Higher values mean more gathering efficiency.
SPECIE1_ENERGY_TO_REPLICATE = 200
# fixed
# To allow the species replication, each individual needs to exceed an energy threshold, the minimum amount of energy needed to be able to reproduce itself. Higher values mean higher threshold.

#blue
SPECIE2_LIFE_EXPECTANCY = 40 #A7
SPECIE2_RANDOM_BORN_CHANCES = 5000 # fixed
SPECIE2_NEARBORN_CHANCES = 120 #A8
SPECIE2_ENERGY_BASE = 250 # fixed
SPECIE2_ENERGY_NEEDED_PER_CYCLE = 120 #A9
SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE = 20 #A10
SPECIE2_ENERGY_TO_REPLICATE = 200 # fixed
