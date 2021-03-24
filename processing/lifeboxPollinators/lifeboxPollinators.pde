/**
 * Lifebox processing version 
 */
 
 class Pollinator { 
  int pollen;
  int xpos;
  int ypos;
  Pollinator (int p, int x, int y) {  
    pollen = p;  
    xpos = x;
    ypos = y;
  } 
  void updatePollen(int p) { 
    pollen = p;
  }
  int getPollen() {
    return pollen;
  }
 }

// screen variables
int matrixSizeX = 95;
int matrixSizeY = 53;
int shapeSize = 20; // 10 for small screen size, 20 for fullHD
int padding = 0;

// best setup for style 1 (squares)int matrixSizeX = 95; int matrixSizeY = 53; int shapeSize = 20; int padding = 0; boolean noColor = true; boolean simulationAlterations = true;

// plants variables
int[][][] flower1Matrix = new int[matrixSizeX][matrixSizeY][4]; // [0] age [1] pollen [2] xpos [3] ypos
int[][][] flower2Matrix = new int[matrixSizeX][matrixSizeY][4]; // [0] age [1] pollen [2] xpos [3] ypos

//int[][][] pollinator1Matrix = new int[matrixSizeX][matrixSizeY][4]; // [0] pollen [1] not used [2] xpos [3] ypos
//int[][][] pollinator2Matrix = new int[matrixSizeX][matrixSizeY][4]; // [0] pollen [1] not used [2] xpos [3] ypos
ArrayList<Pollinator> pollinator1Individuals = new ArrayList<Pollinator>();
ArrayList<Pollinator> pollinator2Individuals = new ArrayList<Pollinator>();



int[] available_spots = new int[8];

int flower1Count = 0;
int flower2Count = 0;
int pollinator1Count = 0;
int pollinator2Count = 0;

int flower1CountLastIteration = 0;
int flower2CountLastIteration = 0;

int pollinator1CountLastIteration = 0;
int pollinator2CountLastIteration = 0;

// hardcoded web app controller parameters (only for testing)
int[] flower1Parameters = { 160, 5, 70, 3}; // life expectancy, reproduction, pollen propagation, pollen generation
int[] flower2Parameters = { 160, 5, 70, 3}; // life expectancy, reproduction, pollen propagation, pollen generation

int[] pollinator1Parameters = { 80 }; // number of individuals
int[] pollinator2Parameters = { 80, 80, 80, 80};

final int FLOWER1_LIFE_EXPECTANCY = 70;
final int FLOWER2_LIFE_EXPECTANCY = 70;

final int FLOWER1_REPRODUCTION = 50;
final int FLOWER2_REPRODUCTION = 50;

final int FLOWER1_POLLEN_PROPAGATION = 50;
final int FLOWER2_POLLEN_PROPAGATION = 50;

final int FLOWER1_POLLEN_GENERATION = 50;
final int FLOWER2_POLLEN_GENERATION = 50;

final int FLOWER1_NEARBORN_CHANCES = 120;
final int FLOWER2_NEARBORN_CHANCES = 120;

final int FLOWER1_RANDOM_BORN_CHANCES = 5000;
final int FLOWER2_RANDOM_BORN_CHANCES = 5000;


final int SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE = 20;
final int SPECIE1_LIFE_EXPECTANCY = 40;
final int SPECIE1_ENERGY_TO_REPLICATE = 200;
final int SPECIE1_ENERGY_BASE = 250;
final int SPECIE1_NEARBORN_CHANCES = 120;
final int SPECIE1_ENERGY_NEEDED_PER_CYCLE = 120;
final int SPECIE1_RANDOM_BORN_CHANCES = 5000;

final int SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE = 20;
final int SPECIE2_LIFE_EXPECTANCY = 40;
final int SPECIE2_ENERGY_TO_REPLICATE = 200;
final int SPECIE2_ENERGY_BASE = 250;
final int SPECIE2_NEARBORN_CHANCES = 120;
final int SPECIE2_ENERGY_NEEDED_PER_CYCLE = 120;
final int SPECIE2_RANDOM_BORN_CHANCES = 5000;


void setup() {
  //size(1920, 1080);
  size(800,600);

  colorMode(RGB);

  for (int x = 0; x < matrixSizeX; x++) {
    for (int y = 0; y < matrixSizeY; y++) {
      flower1Matrix[x][y][0]=0; // set age to 0
      flower1Matrix[x][y][1]=0; // set pollen to 0
      flower1Matrix[x][y][2]=((x)*(shapeSize+padding));
      flower1Matrix[x][y][3]=((y)*(shapeSize+padding));
      flower2Matrix[x][y][0]=0; // set age to 0
      flower2Matrix[x][y][1]=0; // set pollen to 0
      flower2Matrix[x][y][2]=((x)*(shapeSize+padding));
      flower2Matrix[x][y][3]=((y)*(shapeSize+padding));
      //pollinator1Matrix[x][y][0]=0; // set pollen to 0
      //pollinator1Matrix[x][y][1]=0; // set UNUSED VARIABLE to 0
      //pollinator2Matrix[x][y][0]=0; // set pollen to 0
      //pollinator2Matrix[x][y][1]=0; // set UNUSED VARIABLE to 0
    }
  }
  noStroke();
}

void draw() {
  boolean draw;
  flower1CountLastIteration = flower1Count;
  flower2CountLastIteration = flower2Count;
  pollinator1CountLastIteration = pollinator1Count;
  pollinator2CountLastIteration = pollinator2Count;
  flower1Count = 0;
  flower2Count = 0;
  pollinator1Count = 0;
  pollinator2Count = 0;

  
  background(0);
 
  for (int x = 0; x < matrixSizeX; x++) {
    for (int y = 0; y < matrixSizeY; y++) {
      calculatePlantsNextIteration(x, y);
      calculatePollinatorsNextIteration();
      //println(plantsMatrix[x][y][1]);
      draw = false;
      if (flower1Matrix[x][y][0]>0) {
        fill(0, 0, map(flower1Matrix[x][y][0], 0, 1500, 0, 255));
        draw = true;
      }
      
      if (flower2Matrix[x][y][0]>0) {
        fill(map(flower2Matrix[x][y][0], 0, 1500, 0, 255), 0, 0);
        draw = true;
      }
      
      /*
      if (specie1Matrix[x][y][0]>0) {
        fill(map(specie1Matrix[x][y][1], 0, 8000, 0, 255),0 , 0);
        //print("specie1 alive!");
      }
      if (specie2Matrix[x][y][0]>0) {
        fill(0, 0, map(specie2Matrix[x][y][1], 0, 8000, 0, 255));
        //print("specie2 alive!");
      }*/
      if (draw) rect(x*(shapeSize+padding), y*(shapeSize+padding), shapeSize, shapeSize);
    }
  }
  //delay(10);
}


void calculatePlantsNextIteration(int x, int y) {
  int flower1_neighbours = 0;
  int flower2_neighbours = 0;
  int flower1Vitality = flower1Parameters[0];
  int flower1Reproduction = flower1Parameters[1];
  int flower1PollenGeneration = flower1Parameters[3];
  int flower2Vitality = flower2Parameters[0];
  int flower2Reproduction = flower2Parameters[1];
  int flower2PollenGeneration = flower2Parameters[3];
  
  int randomBorn, randomNumber;

  // adjacent coordinates
  int xp = x+1;
  if (xp >= matrixSizeX) {
    xp = matrixSizeX - 1;
  }
  int xm = x-1;
  if (xm < 0) {
    xm = 0;
  }
  int yp = y+1;
  if (yp >= matrixSizeY) {
    yp = matrixSizeY - 1;
  }
  int ym = y-1;
  if (ym < 0) {
    ym = 0;
  }
  
  // Flower 1 species
  
  // count the number of currently live neighbouring cells
  if (flower1Matrix[x][y][0] == 0 && flower1Matrix[xm][y][0] > 0) {
    flower1_neighbours += 1;
  }
  if (flower1Matrix[x][y][0] == 0 && flower1Matrix[xp][y][0] > 0) {
    flower1_neighbours += 1;
  }
  if (flower1Matrix[x][y][0] == 0 && flower1Matrix[xm][ym][0] > 0) {
    flower1_neighbours += 1;
  }
  if (flower1Matrix[x][y][0] == 0 && flower1Matrix[x][ym][0] > 0) {
    flower1_neighbours += 1;
  }
  if (flower1Matrix[x][y][0] == 0 && flower1Matrix[xp][ym][0] > 0) {
    flower1_neighbours += 1;
  }
  if (flower1Matrix[x][y][0] == 0 && flower1Matrix[xm][yp][0] > 0) {
    flower1_neighbours += 1;
  }
  if (flower1Matrix[x][y][0] == 0 && flower1Matrix[x][yp][0] > 0) {
    flower1_neighbours += 1;
  }
  if (flower1Matrix[x][y][0] == 0 && flower1Matrix[xp][yp][0] > 0) {
    flower1_neighbours += 1;
  }
  // if too old, the flower dies
  if (flower1Matrix[x][y][0] >= FLOWER1_LIFE_EXPECTANCY + flower1Vitality) {
    flower1Matrix[x][y][0] = 0;
    flower1Matrix[x][y][1] = 0;
  }

  // flower grows
  if (flower1Matrix[x][y][0]>0 && flower1Matrix[x][y][0] < FLOWER1_LIFE_EXPECTANCY + flower1Vitality) {
    flower1Matrix[x][y][0] += 1;
    flower1Matrix[x][y][1] = flower1Matrix[x][y][1] + FLOWER1_POLLEN_GENERATION + flower1PollenGeneration;  // increase pollen available
    flower1Count += 1;
  }
  // flower reproduction
  if (flower1Reproduction > 0 && flower1Matrix[x][y][0] == 0 && flower1_neighbours > 0) {
    if (FLOWER1_NEARBORN_CHANCES - flower1Reproduction < 2) {
      randomBorn = 2;
    } else {
      randomBorn = FLOWER1_NEARBORN_CHANCES - flower1Reproduction;
    }
    randomNumber = int(random(1, randomBorn+1));
    if (randomNumber == 1) {
      //println("REPRODUCTION!");
      flower1Matrix[x][y][0] = 1;
      flower1Matrix[x][y][1] = FLOWER1_POLLEN_GENERATION + flower1PollenGeneration;
      flower1Count += 1;
    }
  }
  // spontaneous generation
  if (flower1Matrix[x][y][0] == 0 && flower1_neighbours == 0 && flower1Count == 0 && flower1CountLastIteration == 0) {
    randomNumber = int(random(1, FLOWER1_RANDOM_BORN_CHANCES));
    if (randomNumber == 1) {
      //println("BORN!!");
      flower1Matrix[x][y][0] = 1;
      flower1Matrix[x][y][1] = FLOWER1_POLLEN_GENERATION + flower1PollenGeneration;
      flower1Count += 1;
    }
  }
  
  // Flower 2 species
  
  // count the number of currently live neighbouring cells
  if (flower2Matrix[x][y][0] == 0 && flower2Matrix[xm][y][0] > 0) {
    flower2_neighbours += 1;
  }
  if (flower2Matrix[x][y][0] == 0 && flower2Matrix[xp][y][0] > 0) {
    flower2_neighbours += 1;
  }
  if (flower2Matrix[x][y][0] == 0 && flower2Matrix[xm][ym][0] > 0) {
    flower2_neighbours += 1;
  }
  if (flower2Matrix[x][y][0] == 0 && flower2Matrix[x][ym][0] > 0) {
    flower2_neighbours += 1;
  }
  if (flower2Matrix[x][y][0] == 0 && flower2Matrix[xp][ym][0] > 0) {
    flower2_neighbours += 1;
  }
  if (flower2Matrix[x][y][0] == 0 && flower2Matrix[xm][yp][0] > 0) {
    flower2_neighbours += 1;
  }
  if (flower2Matrix[x][y][0] == 0 && flower2Matrix[x][yp][0] > 0) {
    flower2_neighbours += 1;
  }
  if (flower2Matrix[x][y][0] == 0 && flower2Matrix[xp][yp][0] > 0) {
    flower2_neighbours += 1;
  }
  // if too old, the flower dies
  if (flower2Matrix[x][y][0] >= FLOWER2_LIFE_EXPECTANCY + flower2Vitality) {
    flower2Matrix[x][y][0] = 0;
    flower2Matrix[x][y][1] = 0;
  }

  // flower grows
  if (flower2Matrix[x][y][0]>0 && flower2Matrix[x][y][0] < FLOWER2_LIFE_EXPECTANCY + flower2Vitality) {
    flower2Matrix[x][y][0] += 1;
    flower2Matrix[x][y][1] = flower2Matrix[x][y][1] + FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;  // increase pollen available
    flower2Count += 1;
  }
  // flower reproduction
  if (flower2Reproduction > 0 && flower2Matrix[x][y][0] == 0 && flower2_neighbours > 0) {
    if (FLOWER2_NEARBORN_CHANCES - flower2Reproduction < 2) {
      randomBorn = 2;
    } else {
      randomBorn = FLOWER2_NEARBORN_CHANCES - flower1Reproduction;
    }
    randomNumber = int(random(1, randomBorn+1));
    if (randomNumber == 1) {
      //println("REPRODUCTION!");
      flower2Matrix[x][y][0] = 1;
      flower2Matrix[x][y][1] = FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;
      flower2Count += 1;
    }
  }
  // spontaneous generation
  if (flower2Matrix[x][y][0] == 0 && flower2_neighbours == 0 && flower2Count == 0 && flower2CountLastIteration == 0) {
    randomNumber = int(random(1, FLOWER2_RANDOM_BORN_CHANCES));
    if (randomNumber == 1) {
      //println("BORN!!");
      flower2Matrix[x][y][0] = 1;
      flower2Matrix[x][y][1] = FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;
      flower2Count += 1;
    }
  }
  
}

void calculatePollinatorsNextIteration() {
  
  int pollinator1Number = pollinator1Parameters[0];
  int pollinator2Number = pollinator2Parameters[0];
  
  // adjust quantity of pollinators1
  
  // add if needed
  for (int i = pollinator1Individuals.size(); i < pollinator1Number; i++) {
    pollinator1Individuals.add(new Pollinator(0,int(random(1, matrixSizeX)),int(random(1, matrixSizeY))));
  }
  
  // remove if needed
  for (int i = pollinator1Individuals.size(); i > pollinator1Number; i--) {
    pollinator1Individuals.remove(i-1);
  }
  
  //println(pollinator1Individuals.size());
  
  
}

/*
void calculateSpeciesNextIteration(int x, int y) {
  int pos;
  int rand_pos;
  int random_number;
  int energy_gathered;
  float randomborn;
  
  int species1Count = 0;
  int species2Count = 0;
  
  int flower1Propagation = flower1Parameters[2];
  int flower2Propagation = flower2Parameters[2]; 

  int sp1Gathering = specie1Parameters[0];
  int sp1Efficiency = specie1Parameters[1];
  int sp1Reproduction = specie1Parameters[2];
  int sp1Vitality = specie1Parameters[3];
 


  int sp2Gathering = specie2Parameters[0];
  int sp2Efficiency = specie2Parameters[1];
  int sp2Reproduction = specie2Parameters[2];
  int sp2Vitality = specie2Parameters[3];

  // adjacent coordinates
  int xp = x+1;
  if (xp >= matrixSizeX) {
    xp = matrixSizeX - 1;
  }
  int xm = x-1;
  if (xm < 0) {
    xm = 0;
  }
  int yp = y+1;
  if (yp >= matrixSizeY) {
    yp = matrixSizeY - 1;
  }
  int ym = y-1;
  if (ym < 0) {
    ym = 0;
  }

  // count the number of currently live neighbouring cells

  // [Pollinator1]
  int pollinator1_neighbours = 0;  
  if (pollinator1Matrix[x][y][0] == 0 && pollinator1Matrix[xm][y][0] > 0) {
    pollinator1_neighbours += 1;
  }
  if (pollinator1Matrix[x][y][0] == 0 && pollinator1Matrix[xp][y][0] > 0) {
    pollinator1_neighbours += 1;
  }
  if (pollinator1Matrix[x][y][0] == 0 && pollinator1Matrix[xm][ym][0] > 0) {
    pollinator1_neighbours += 1;
  }
  if (pollinator1Matrix[x][y][0] == 0 && pollinator1Matrix[x][ym][0] > 0) {
    pollinator1_neighbours += 1;
  }
  if (pollinator1Matrix[x][y][0] == 0 && pollinator1Matrix[xp][ym][0] > 0) {
    pollinator1_neighbours += 1;
  }
  if (pollinator1Matrix[x][y][0] == 0 && pollinator1Matrix[xm][yp][0] > 0) {
    pollinator1_neighbours += 1;
  }
  if (pollinator1Matrix[x][y][0] == 0 && pollinator1Matrix[x][yp][0] > 0) {
    pollinator1_neighbours += 1;
  }
  if (pollinator1Matrix[x][y][0] == 0 && pollinator1Matrix[xp][yp][0] > 0) {
    pollinator1_neighbours += 1;
  }

  // [Pollinator2]
  int pollinator2_neighbours = 0;
  if (pollinator2Matrix[x][y][0] == 0 && pollinator2Matrix[xm][y][0] > 0) {
    pollinator2_neighbours += 1;
  }
  if (pollinator2Matrix[x][y][0] == 0 && pollinator2Matrix[xp][y][0] > 0) {
    pollinator2_neighbours += 1;
  }
  if (pollinator2Matrix[x][y][0] == 0 && pollinator2Matrix[xm][ym][0] > 0) {
    pollinator2_neighbours += 1;
  }
  if (pollinator2Matrix[x][y][0] == 0 && pollinator2Matrix[x][ym][0] > 0) {
    pollinator2_neighbours += 1;
  }
  if (pollinator2Matrix[x][y][0] == 0 && pollinator2Matrix[xp][ym][0] > 0) {
    pollinator2_neighbours += 1;
  }
  if (pollinator2Matrix[x][y][0] == 0 && pollinator2Matrix[xm][yp][0] > 0) {
    pollinator2_neighbours += 1;
  }
  if (pollinator2Matrix[x][y][0] == 0 && pollinator2Matrix[x][yp][0] > 0) {
    pollinator2_neighbours += 1;
  }
  if (pollinator2Matrix[x][y][0] == 0 && pollinator2Matrix[xp][yp][0] > 0) {
    pollinator2_neighbours += 1;
  }


  // --- SPICE 1 ---
  // individual is alive?
  if (specie1Matrix[x][y][0] > 0) {
    //println("esta viva");
    // try to eat
    if (plantsMatrix[x][y][1] > 0) {
      energy_gathered=0;
      if (plantsMatrix[x][y][1] > SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(sp1Gathering)) {
        energy_gathered = SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(sp1Gathering);
        plantsMatrix[x][y][1] = plantsMatrix[x][y][1] - (SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE + int(sp1Gathering));
      } else {
        energy_gathered = plantsMatrix[x][y][1];
        plantsMatrix[x][y][1] = 0;
      }
      specie1Matrix[x][y][1] = specie1Matrix[x][y][1] + energy_gathered;
    }


    // grow and decrease energy
    specie1Matrix[x][y][0] += 1;
    specie1Matrix[x][y][1] = specie1Matrix[x][y][1] - (SPECIE1_ENERGY_NEEDED_PER_CYCLE  - int(sp1Efficiency));

    // die if no energy
    if (specie1Matrix[x][y][1] < 0) {
      specie1Matrix[x][y][1] = 0;
      specie1Matrix[x][y][0] = 0;
    }

    // try to replicate
    if (specie1Matrix[x][y][1] > SPECIE1_ENERGY_TO_REPLICATE) {
      for (int elem = 0; elem<8; elem++) { 
        available_spots[elem] = 0;
      }
      pos=0;
      if (int(sp1Reproduction) > 0) {
        if (SPECIE1_NEARBORN_CHANCES - int(sp1Reproduction) < 2) {
          randomborn = 2;
        } else {
          randomborn = map(SPECIE1_NEARBORN_CHANCES - int(sp1Reproduction), 2, 120, 2, 20);
        }
        random_number = int(random(1, randomborn+1));
        if (specie1Matrix[xm][y][0] == 0) {
          available_spots[pos] = 1;
          pos += 1;
        }
        if (specie1Matrix[xp][y][0] == 0) {
          available_spots[pos] = 2;
          pos += 1;
        }
        if (specie1Matrix[xm][ym][0] == 0) {
          available_spots[pos] = 3;
          pos += 1;
        }
        if (specie1Matrix[x][ym][0] == 0) {
          available_spots[pos] = 4;
          pos += 1;
        }
        if (specie1Matrix[xp][ym][0] == 0) {
          available_spots[pos] = 5;
          pos += 1;
        }
        if (specie1Matrix[xm][yp][0] == 0) {
          available_spots[pos] = 6;
          pos += 1;
        }
        if (specie1Matrix[x][yp][0] == 0) {
          available_spots[pos] = 7;
          pos += 1;
        }
        if (specie1Matrix[xp][yp][0] == 0) {
          available_spots[pos] = 8;
          pos += 1;
        }
        if (pos > 0) {
          rand_pos=int(random(0, pos));
          if (random_number == 1) {
            specie1Matrix[x][y][1] = specie1Matrix[x][y][1] - SPECIE1_ENERGY_TO_REPLICATE;
            if (available_spots[rand_pos] == 1) {
              specie1Matrix[xm][y][0] = 1;
              specie1Matrix[xm][y][1] = SPECIE1_ENERGY_BASE;
            }
            if (available_spots[rand_pos] == 2) {
              specie1Matrix[xp][y][0] = 1;
              specie1Matrix[xp][y][1] = SPECIE1_ENERGY_BASE;
            }
            if (available_spots[rand_pos] == 3) {
              specie1Matrix[xm][ym][0] = 1;
              specie1Matrix[xm][ym][1] = SPECIE1_ENERGY_BASE;
            }
            if (available_spots[rand_pos] == 4) {
              specie1Matrix[x][ym][0] = 1;
              specie1Matrix[x][ym][1] = SPECIE1_ENERGY_BASE;
            }
            if (available_spots[rand_pos] == 5) {
              specie1Matrix[xp][ym][0] = 1;
              specie1Matrix[xp][ym][1] = SPECIE1_ENERGY_BASE;
            }
            if (available_spots[rand_pos] == 6) {
              specie1Matrix[xm][yp][0] = 1;
              specie1Matrix[xm][yp][1] = SPECIE1_ENERGY_BASE;
            }
            if (available_spots[rand_pos] == 7) {
              specie1Matrix[x][yp][0] = 1;
              specie1Matrix[x][yp][1] = SPECIE1_ENERGY_BASE;
            }
            if (available_spots[rand_pos] == 8) {
              specie1Matrix[xp][yp][0] = 1;
              specie1Matrix[xp][yp][1] = SPECIE1_ENERGY_BASE;
            }
          }
        }
      }
    }
    // die if too old
    if (specie1Matrix[x][y][0] > SPECIE1_LIFE_EXPECTANCY + int(sp1Vitality)) {
      specie1Matrix[x][y][1] = 0;
      specie1Matrix[x][y][0] = 0;
    }
    // accounting individuals (even if it dies in this turn)
      species1Count += 1;
  }
  // if no individual is alive, random born to avoid extintion
  if (specie1Matrix[x][y][0] == 0 && specie1_neighbours==0 && species1Count == 0) {
      //println("TRY TO BORN");
      random_number = int(random(1, SPECIE1_RANDOM_BORN_CHANCES+1));
      //println(random_number);
    if (random_number==1) {
      //println("BORN");
      specie1Matrix[x][y][0] = 1;
      specie1Matrix[x][y][1] = SPECIE1_ENERGY_BASE;
      species1Count += 1;
    }
  }
} */
