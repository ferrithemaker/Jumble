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
  int getX() {
    return xpos;
  }
  int getY() {
    return ypos;
  }
  void changeX(int x) {
    xpos = xpos + x;
  }
  void changeY(int y) {
    ypos = ypos + y;
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
  size(1920, 1080);
  //size(800,600);

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
  //pollinator1CountLastIteration = pollinator1Count;
  //pollinator2CountLastIteration = pollinator2Count;
  flower1Count = 0;
  flower2Count = 0;
  //pollinator1Count = 0;
  //pollinator2Count = 0;

  
  background(0);
 
  // paint the flowers matrix
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
      
      if (draw) rect(x*(shapeSize+padding), y*(shapeSize+padding), shapeSize, shapeSize);
    }
  }
  // paint the pollinator1 individuals
  for (int i=0; i < pollinator1Individuals.size(); i++) {
    fill(map(pollinator1Individuals.get(i).getPollen(), 0, 100, 0, 255), map(pollinator1Individuals.get(i).getPollen(), 0, 100, 0, 255),0);
    rect(pollinator1Individuals.get(i).getX()*(shapeSize+padding), pollinator1Individuals.get(i).getY()*(shapeSize+padding), shapeSize, shapeSize);
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
  
  // adjust quantity of pollinator1
  
  // add if needed
  for (int i = pollinator1Individuals.size(); i < pollinator1Number; i++) {
    pollinator1Individuals.add(new Pollinator(100,int(random(1, matrixSizeX)),int(random(1, matrixSizeY))));
  }
  
  // remove if needed
  for (int i = pollinator1Individuals.size(); i > pollinator1Number; i--) {
    pollinator1Individuals.remove(i-1);
  }
  
  for (int i=0; i < pollinator1Individuals.size(); i++) {
    // try to get pollen from flower
    if (flower1Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1]>0) {
      flower1Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1]--;
      // FALTA SET POLLEN
    }
    if (flower2Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1]>0) {
      flower2Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1]--;
    }
    if (int(random(1,10000))==1) {
      // random move
      pollinator1Individuals.get(i).changeX(int(random(-2, 2)));
      pollinator1Individuals.get(i).changeY(int(random(-2, 2)));
    }
    // try to pollinate
  }
  
  //println(pollinator1Individuals.size());
  
  
  
  
}