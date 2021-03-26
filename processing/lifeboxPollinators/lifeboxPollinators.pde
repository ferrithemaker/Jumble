/**
 * Lifebox processing version 
 */
 
 class Pollinator { 
  int pollenF1;
  int pollenF2;
  int xpos;
  int ypos;
  Pollinator (int p1, int p2, int x, int y) {  
    pollenF1 = p1;
    pollenF2 = p2;
    xpos = x;
    ypos = y;
  } 
  void changePollenF1(int p) { 
    pollenF1 = pollenF1 + p;
  }
  void changePollenF2(int p) { 
    pollenF2 = pollenF2 + p;
  }
  int getPollenF1() {
    return pollenF1;
  }
  int getPollenF2() {
    return pollenF2;
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
 
// parlin offset
float xoff = 0.0;

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
int[] flower1Parameters = { 255, 1000, 2, 3}; // life expectancy [max cycles of flower life], reproduction [marginal reproduction chances high value>slow rate 2-X], pollen propagation [quantity of pollen allowed to be relased from flower], pollen generation [quantity of pollen generated per cycle]
int[] flower2Parameters = { 255, 1000, 2, 3}; // life expectancy, reproduction, pollen propagation, pollen generation

int[] pollinator1Parameters = { 10, 20000, 5, 4 }; // number of individuals, movement rate, pollination rate, pollen gathering
int[] pollinator2Parameters = { 10, 20000, 5, 4 }; // number of individuals, movement rate, pollination rate, pollen gathering

final int FLOWER1_LIFE_EXPECTANCY = 70;
final int FLOWER2_LIFE_EXPECTANCY = 70;

final int FLOWER1_REPRODUCTION = 50;
final int FLOWER2_REPRODUCTION = 50;

final int FLOWER1_POLLEN_PROPAGATION = 50;
final int FLOWER2_POLLEN_PROPAGATION = 50;

final int FLOWER1_POLLEN_GENERATION = 50;
final int FLOWER2_POLLEN_GENERATION = 50;

final int FLOWER1_RANDOM_BORN_CHANCES = 5000;
final int FLOWER2_RANDOM_BORN_CHANCES = 5000;

final float PARLIN_NOISE_FACTOR = 0.3; //randomness of pollinators movement



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
    }
  }
  noStroke();
}

void draw() {
  boolean draw;
  flower1CountLastIteration = flower1Count;
  flower2CountLastIteration = flower2Count;
  flower1Count = 0;
  flower2Count = 0;
  
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
    fill(100,100,0);
    rect(pollinator1Individuals.get(i).getX()*(shapeSize+padding), pollinator1Individuals.get(i).getY()*(shapeSize+padding), shapeSize, shapeSize);
  }
  // paint the pollinator2 individuals
  for (int i=0; i < pollinator2Individuals.size(); i++) {
    fill(100,0,100);
    rect(pollinator2Individuals.get(i).getX()*(shapeSize+padding), pollinator2Individuals.get(i).getY()*(shapeSize+padding), shapeSize, shapeSize);
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
  
  int pollinator1PollinationRate = pollinator1Parameters[2];
  int pollinator2PollinationRate = pollinator2Parameters[2];
  
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
    // we are on a potential reproductive spot, we have a pollinator?
    boolean pollinatorOverFlower = false;
    for (int i=0; i < pollinator1Individuals.size(); i++) {
      if (x == pollinator1Individuals.get(i).getX() && y == pollinator1Individuals.get(i).getX()) {
        pollinatorOverFlower = true;
        if (int(random(1, pollinator1PollinationRate))==1) {
          if (pollinator1Individuals.get(i).getPollenF1()>0) {
            pollinator1Individuals.get(i).changePollenF1(-1);
            flower1Matrix[x][y][0] = 1;
            flower1Matrix[x][y][1] = FLOWER1_POLLEN_GENERATION + flower1PollenGeneration;
            println("F1 born");
          }
        }
      }
    }
    for (int i=0; i < pollinator2Individuals.size(); i++) {
      if (x == pollinator2Individuals.get(i).getX() && y == pollinator2Individuals.get(i).getX()) {
        pollinatorOverFlower = true;
        if (int(random(1, pollinator2PollinationRate))==1) {
          if (pollinator2Individuals.get(i).getPollenF1()>0) {
            pollinator2Individuals.get(i).changePollenF1(-1);
            flower1Matrix[x][y][0] = 1;
            flower1Matrix[x][y][1] = FLOWER1_POLLEN_GENERATION + flower1PollenGeneration;
            println("F1 born");
          }
        }
      }
    }
    // if there's no pollinator
    if (!pollinatorOverFlower) {
      if (flower1Reproduction < 2) {
        randomBorn = 2;
      } else {
        randomBorn =  flower1Reproduction;
      }
      randomNumber = int(random(1, randomBorn+1));
      if (randomNumber == 1) {
        //println("REPRODUCTION!");
        flower1Matrix[x][y][0] = 1;
        flower1Matrix[x][y][1] = FLOWER1_POLLEN_GENERATION + flower1PollenGeneration;
        flower1Count += 1;
      }
    }
  }
  // spontaneous generation
  if (flower1Matrix[x][y][0] == 0 && flower1_neighbours == 0 && flower1Count == 0 && flower1CountLastIteration == 0) {
    randomNumber = int(random(1, FLOWER1_RANDOM_BORN_CHANCES));
    if (randomNumber == 1) {
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
    // we are on a potential reproductive spot, we have a pollinator?
    boolean pollinatorOverFlower = false;
    for (int i=0; i < pollinator1Individuals.size(); i++) {
      if (x == pollinator1Individuals.get(i).getX() && y == pollinator1Individuals.get(i).getX()) {
        pollinatorOverFlower = true;
        if (int(random(1, pollinator1PollinationRate))==1) {
          if (pollinator1Individuals.get(i).getPollenF2()>0) {
            pollinator1Individuals.get(i).changePollenF2(-1);
            flower2Matrix[x][y][0] = 1;
            flower2Matrix[x][y][1] = FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;
            println("F2 born");
          }
        }
      }
    }
    for (int i=0; i < pollinator2Individuals.size(); i++) {
      if (x == pollinator2Individuals.get(i).getX() && y == pollinator2Individuals.get(i).getX()) {
        pollinatorOverFlower = true;
        if (int(random(1, pollinator2PollinationRate))==1) {
          if (pollinator2Individuals.get(i).getPollenF2()>0) {
            pollinator2Individuals.get(i).changePollenF2(-1);
            flower2Matrix[x][y][0] = 1;
            flower2Matrix[x][y][1] = FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;
            println("F2 born");
          }
        }
      }
    }
    // if there's no pollinator
    if (!pollinatorOverFlower) {
      if (flower2Reproduction < 2) {
        randomBorn = 2;
      } else {
        randomBorn = flower1Reproduction;
      }
      randomNumber = int(random(1, randomBorn+1));
      if (randomNumber == 1) {
        //println("REPRODUCTION!");
        flower2Matrix[x][y][0] = 1;
        flower2Matrix[x][y][1] = FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;
        flower2Count += 1;
      }
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
  int pollinator1MovementRate = pollinator1Parameters[1];
  int pollinator1PollinationRate = pollinator1Parameters[2];
  int pollinator1GatheringRate = pollinator1Parameters[3];
  int pollinator2Number = pollinator2Parameters[0];
  int pollinator2MovementRate = pollinator2Parameters[1];
  int pollinator2PollinationRate = pollinator2Parameters[2];
  int pollinator2GatheringRate = pollinator2Parameters[3];
  int flower1PollenGeneration = flower1Parameters[3];
  int flower2PollenGeneration = flower2Parameters[3];
  int flower1PollenPropagation = flower1Parameters[2];
  int flower2PollenPropagation = flower2Parameters[2];
  
  // adjust quantity of pollinator1
  
  // add if needed
  for (int i = pollinator1Individuals.size(); i < pollinator1Number; i++) {
    pollinator1Individuals.add(new Pollinator(0,0, int(random(1, matrixSizeX)),int(random(1, matrixSizeY))));
  }
  
  // remove if needed
  for (int i = pollinator1Individuals.size(); i > pollinator1Number; i--) {
    pollinator1Individuals.remove(i-1);
  }
  
  for (int i=0; i < pollinator1Individuals.size(); i++) {
    int pollinatorXpos = pollinator1Individuals.get(i).getX();
    int pollinatorYpos = pollinator1Individuals.get(i).getY();
    // try to get pollen from flower
    if (int(random(1, pollinator1GatheringRate)) == 1) {
      int flower1pollenQuantity = flower1Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1];
      int flower2pollenQuantity = flower2Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1];
      if (flower1pollenQuantity>0) {
        int remainPollenFlower1 = flower1pollenQuantity - flower1PollenPropagation;
        if (remainPollenFlower1 < 0) {
          flower1Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1] = 0;
          pollinator1Individuals.get(i).changePollenF1(flower1pollenQuantity);
        } else {
          flower1Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1] = remainPollenFlower1;
          pollinator1Individuals.get(i).changePollenF1(flower1PollenPropagation);
        }
      }
      if (flower2pollenQuantity>0) {
        int remainPollenFlower2 = flower2pollenQuantity - flower2PollenPropagation;
        if (remainPollenFlower2 < 0) {
          flower2Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1] = 0;
          pollinator1Individuals.get(i).changePollenF2(flower2pollenQuantity);
        } else {
          flower2Matrix[pollinator1Individuals.get(i).getX()][pollinator1Individuals.get(i).getY()][1] = remainPollenFlower2;
          pollinator1Individuals.get(i).changePollenF2(flower2PollenPropagation);
        }
      }
    }
    if (int(random(1,pollinator1MovementRate))==1) {
      // random move
      xoff = xoff + PARLIN_NOISE_FACTOR;
      int randpos = int(map(noise(xoff),0,1,1,16));
      if (randpos == 4 && pollinatorXpos > 0 && pollinatorYpos > 0) { pollinator1Individuals.get(i).changeX(-1); pollinator1Individuals.get(i).changeY(-1); }
      if (randpos == 5 && pollinatorYpos > 0) { pollinator1Individuals.get(i).changeY(-1); }
      if (randpos == 6 && pollinatorXpos < matrixSizeX - 1 && pollinatorYpos > 0) { pollinator1Individuals.get(i).changeX(1); pollinator1Individuals.get(i).changeY(-1); }
      if (randpos == 7 && pollinatorXpos > 0) { pollinator1Individuals.get(i).changeX(-1); }
      if (randpos == 8 && pollinatorXpos < matrixSizeX - 1) { pollinator1Individuals.get(i).changeX(1); }
      if (randpos == 9 && pollinatorXpos > 0 && pollinatorYpos < matrixSizeY - 1) { pollinator1Individuals.get(i).changeX(-1); pollinator1Individuals.get(i).changeY(1); }
      if (randpos == 10 && pollinatorYpos < matrixSizeY - 1) { pollinator1Individuals.get(i).changeY(1); }
      if (randpos == 11 && pollinatorXpos < matrixSizeX - 1 && pollinatorYpos < matrixSizeY - 1) { pollinator1Individuals.get(i).changeX(1); pollinator1Individuals.get(i).changeY(1); }
    }   
  }
  

  // adjust quantity of pollinator2
  
  // add if needed
  for (int i = pollinator2Individuals.size(); i < pollinator2Number; i++) {
    pollinator2Individuals.add(new Pollinator(0,0, int(random(1, matrixSizeX)),int(random(1, matrixSizeY))));
  }
  
  // remove if needed
  for (int i = pollinator2Individuals.size(); i > pollinator2Number; i--) {
    pollinator2Individuals.remove(i-1);
  }
  
  for (int i=0; i < pollinator2Individuals.size(); i++) {
    int pollinatorXpos = pollinator2Individuals.get(i).getX();
    int pollinatorYpos = pollinator2Individuals.get(i).getY();
    // try to get pollen from flower
    if (int(random(1, pollinator2GatheringRate)) == 1) {
      int flower1pollenQuantity = flower1Matrix[pollinator2Individuals.get(i).getX()][pollinator2Individuals.get(i).getY()][1];
      int flower2pollenQuantity = flower2Matrix[pollinator2Individuals.get(i).getX()][pollinator2Individuals.get(i).getY()][1];
      if (flower1pollenQuantity>0) {
        int remainPollenFlower1 = flower1pollenQuantity - flower1PollenPropagation;
        if (remainPollenFlower1 < 0) {
          flower1Matrix[pollinator2Individuals.get(i).getX()][pollinator2Individuals.get(i).getY()][1] = 0;
          pollinator1Individuals.get(i).changePollenF1(flower1pollenQuantity);
        } else {
          flower1Matrix[pollinator2Individuals.get(i).getX()][pollinator2Individuals.get(i).getY()][1] = remainPollenFlower1;
          pollinator2Individuals.get(i).changePollenF1(flower1PollenPropagation);
        }
      }
      if (flower2pollenQuantity>0) {
        int remainPollenFlower2 = flower2pollenQuantity - flower2PollenPropagation;
        if (remainPollenFlower2 < 0) {
          flower2Matrix[pollinator2Individuals.get(i).getX()][pollinator2Individuals.get(i).getY()][1] = 0;
          pollinator2Individuals.get(i).changePollenF2(flower2pollenQuantity);
        } else {
          flower2Matrix[pollinator2Individuals.get(i).getX()][pollinator2Individuals.get(i).getY()][1] = remainPollenFlower2;
          pollinator2Individuals.get(i).changePollenF2(flower2PollenPropagation);
        }
      }
    }
    if (int(random(1,pollinator2MovementRate))==1) {
      // random move
      xoff = xoff + PARLIN_NOISE_FACTOR;
      int randpos = int(map(noise(xoff),0,1,1,16));
      if (randpos == 4 && pollinatorXpos > 0 && pollinatorYpos > 0) { pollinator2Individuals.get(i).changeX(-1); pollinator2Individuals.get(i).changeY(-1); }
      if (randpos == 5 && pollinatorYpos > 0) { pollinator2Individuals.get(i).changeY(-1); }
      if (randpos == 6 && pollinatorXpos < matrixSizeX - 1 && pollinatorYpos > 0) { pollinator2Individuals.get(i).changeX(1); pollinator2Individuals.get(i).changeY(-1); }
      if (randpos == 7 && pollinatorXpos > 0) { pollinator2Individuals.get(i).changeX(-1); }
      if (randpos == 8 && pollinatorXpos < matrixSizeX - 1) { pollinator2Individuals.get(i).changeX(1); }
      if (randpos == 9 && pollinatorXpos > 0 && pollinatorYpos < matrixSizeY - 1) { pollinator2Individuals.get(i).changeX(-1); pollinator2Individuals.get(i).changeY(1); }
      if (randpos == 10 && pollinatorYpos < matrixSizeY - 1) { pollinator2Individuals.get(i).changeY(1); }
      if (randpos == 11 && pollinatorXpos < matrixSizeX - 1 && pollinatorYpos < matrixSizeY - 1) { pollinator2Individuals.get(i).changeX(1); pollinator2Individuals.get(i).changeY(1); }
    }   
  } 
}
