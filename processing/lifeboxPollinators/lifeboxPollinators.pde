/**
 * Lifebox processing version 
 */
 
 class Pollinator { 
  int pollenF1;
  int pollenF2;
  int energy;
  int xpos;
  int ypos;
  int localMovement; // 50000 to 0, 0 = no local movement
  Pollinator (int p1, int p2, int e, int x, int y, int lm) {  
    pollenF1 = p1;
    pollenF2 = p2;
    xpos = x;
    ypos = y;
    energy = e;
    localMovement = lm;
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
  int getEnergy() {
    return energy;
  }
  int getX() {
    return xpos;
  }
  int getY() {
    return ypos;
  }
  int getLocalMovement() {
    return localMovement;
  }
  void changeX(int x) {
    xpos = xpos + x;
  }
  void changeEnergy(int e) {
    energy = energy + e;
  }
  void changeY(int y) {
    ypos = ypos + y;
  }
  void changeLocalMovement(int x) {
    localMovement = localMovement + x;
  }
  void setLocalMovement(int x) {
    localMovement =  x;
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
int[][][] flower1Matrix = new int[matrixSizeX][matrixSizeY][5]; // [0] age [1] pollen [2] xpos [3] ypos [4] energy available (nectar)
int[][][] flower2Matrix = new int[matrixSizeX][matrixSizeY][5]; // [0] age [1] pollen [2] xpos [3] ypos [4] energy available (nectar)

ArrayList<Pollinator> pollinator1Individuals = new ArrayList<Pollinator>();
ArrayList<Pollinator> pollinator2Individuals = new ArrayList<Pollinator>();
ArrayList<Pollinator> pollinator3Individuals = new ArrayList<Pollinator>();


int[] available_spots = new int[8];

int flower1Count = 0;
int flower2Count = 0;
int pollinator1Count = 0;
int pollinator2Count = 0;

int flower1CountLastIteration = 0;
int flower2CountLastIteration = 0;


// hardcoded web app controller parameters (only for testing)
int[] flower1Parameters = { 400, 1000, 2, 3}; // life expectancy [max cycles of flower life], reproduction [marginal reproduction chances high value>slow rate 2-X], pollen propagation [quantity of pollen allowed to be relased from flower], pollen generation [quantity of pollen generated per cycle]
int[] flower2Parameters = { 400, 1000, 2, 3}; // life expectancy, reproduction, pollen propagation, pollen generation

int[] pollinator1Parameters = { 10, 20000, 2, 4, 1000 }; // number of individuals, movement rate, pollination rate, pollen gathering, energy gatherning
int[] pollinator2Parameters = { 10, 20000, 2, 4, 1000 }; // number of individuals, movement rate, pollination rate, pollen gathering, energy gatherning
int[] pollinator3Parameters = { 10, 20000, 2, 4, 1000 }; // number of individuals, movement rate, pollination rate, pollen gathering, energy gatherning

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

final int FLOWER1_ENERGY_GENERATION = 1000;
final int FLOWER2_ENERGY_GENERATION = 1000;

final int FLOWER1_MAXENERGY = 10000000;
final int FLOWER2_MAXENERGY = 10000000;

final float PARLIN_NOISE_FACTOR = 0.3; //randomness of pollinators movement



void setup() {
  size(1920, 1080);
  //size(800,600);

  colorMode(RGB);

  for (int x = 0; x < matrixSizeX; x++) {
    for (int y = 0; y < matrixSizeY; y++) {
      flower1Matrix[x][y][0]=0; // set age to 0
      flower1Matrix[x][y][1]=0; // set pollen to 0
      flower1Matrix[x][y][4]=0; // set energy (nectar) available to 0
      flower1Matrix[x][y][2]=((x)*(shapeSize+padding));
      flower1Matrix[x][y][3]=((y)*(shapeSize+padding));
      flower2Matrix[x][y][0]=0; // set age to 0
      flower2Matrix[x][y][1]=0; // set pollen to 0
      flower2Matrix[x][y][4]=0; // set energy (nectar) available to 0
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
      pollinator1Individuals = calculatePollinatorNextIteration(pollinator1Individuals,pollinator1Parameters);
      pollinator2Individuals = calculatePollinatorNextIteration(pollinator2Individuals,pollinator2Parameters);
      pollinator3Individuals = calculatePollinatorNextIteration(pollinator3Individuals,pollinator3Parameters);
      //println(plantsMatrix[x][y][1]);
      draw = false;
      if (flower1Matrix[x][y][0]>0) {
        fill(0, 0, map(flower1Matrix[x][y][0], 0, flower1Parameters[0], 0, 255));
        draw = true;
      }
      
      if (flower2Matrix[x][y][0]>0) {
        fill(map(flower2Matrix[x][y][0], 0, flower1Parameters[0], 0, 255), 0, 0);
        draw = true;
      }
      
      if (draw) rect(x*(shapeSize+padding), y*(shapeSize+padding), shapeSize, shapeSize);
    }
  }
  // paint the pollinator1 individuals
  for (int i=0; i < pollinator1Individuals.size(); i++) {
    fill(100,200,100,map(pollinator1Individuals.get(i).getEnergy(),0,10000000,0,255));
    ellipse((pollinator1Individuals.get(i).getX()+1)*(shapeSize+padding), (pollinator1Individuals.get(i).getY()+1)*(shapeSize+padding), shapeSize, shapeSize);
  }
  // paint the pollinator2 individuals
  for (int i=0; i < pollinator2Individuals.size(); i++) {
    fill(100,0,100,map(pollinator2Individuals.get(i).getEnergy(),0,10000000,100,255));
    ellipse((pollinator2Individuals.get(i).getX()+1)*(shapeSize+padding), (pollinator2Individuals.get(i).getY()+1)*(shapeSize+padding), shapeSize, shapeSize);
  }
  // paint the pollinator3 individuals
  for (int i=0; i < pollinator3Individuals.size(); i++) {
    fill(150,100,50,map(pollinator3Individuals.get(i).getEnergy(),0,10000000,100,255));
    ellipse((pollinator3Individuals.get(i).getX()+1)*(shapeSize+padding), (pollinator3Individuals.get(i).getY()+1)*(shapeSize+padding), shapeSize, shapeSize);
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
    flower1Matrix[x][y][4] = 0;
  }

  // flower grows
  if (flower1Matrix[x][y][0]>0 && flower1Matrix[x][y][0] < FLOWER1_LIFE_EXPECTANCY + flower1Vitality) {
    flower1Matrix[x][y][0] += 1;
    flower1Matrix[x][y][1] = flower1Matrix[x][y][1] + FLOWER1_POLLEN_GENERATION + flower1PollenGeneration;  // increase pollen available
    flower1Count += 1;
    if (int(random(1, 10))==1) {
      flower1Matrix[x][y][4] = flower1Matrix[x][y][4] + FLOWER1_ENERGY_GENERATION;
      if (flower1Matrix[x][y][4] > FLOWER1_MAXENERGY) { flower1Matrix[x][y][4] = FLOWER1_MAXENERGY; }
    }
      
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
            flower1Matrix[x][y][4] = FLOWER1_ENERGY_GENERATION;
            flower1Count += 1;
            println("CREATED POLLINATED!");
          }
        }
      }
    }
    if (!pollinatorOverFlower) {
      for (int i=0; i < pollinator2Individuals.size(); i++) {
        if (x == pollinator2Individuals.get(i).getX() && y == pollinator2Individuals.get(i).getX()) {
          pollinatorOverFlower = true;
          if (int(random(1, pollinator2PollinationRate))==1) {
            if (pollinator2Individuals.get(i).getPollenF1()>0) {
              pollinator2Individuals.get(i).changePollenF1(-1);
              flower1Matrix[x][y][0] = 1;
              flower1Matrix[x][y][1] = FLOWER1_POLLEN_GENERATION + flower1PollenGeneration;
              flower1Matrix[x][y][4] = FLOWER1_ENERGY_GENERATION;
              flower1Count += 1;
              println("CREATED POLLINATED!");
            }
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
        flower1Matrix[x][y][4] = FLOWER1_ENERGY_GENERATION;
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
      flower1Matrix[x][y][4] = FLOWER1_ENERGY_GENERATION;
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
    flower2Matrix[x][y][4] = 0;
  }

  // flower grows
  if (flower2Matrix[x][y][0]>0 && flower2Matrix[x][y][0] < FLOWER2_LIFE_EXPECTANCY + flower2Vitality) {
    flower2Matrix[x][y][0] += 1;
    flower2Matrix[x][y][1] = flower2Matrix[x][y][1] + FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;  // increase pollen available
    flower2Count += 1;
    if (int(random(1, 10))==1) {
      flower2Matrix[x][y][4] = flower2Matrix[x][y][4] + FLOWER2_ENERGY_GENERATION;
      if (flower2Matrix[x][y][4] > FLOWER2_MAXENERGY) { flower2Matrix[x][y][4] = FLOWER2_MAXENERGY; }
    }
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
            flower2Matrix[x][y][4] = FLOWER2_ENERGY_GENERATION;
            flower2Count += 1;
            println("CREATED POLLINATED!");
          }
        }
      }
    }
    if (!pollinatorOverFlower) {
      for (int i=0; i < pollinator2Individuals.size(); i++) {
        if (x == pollinator2Individuals.get(i).getX() && y == pollinator2Individuals.get(i).getX()) {
          pollinatorOverFlower = true;
          if (int(random(1, pollinator2PollinationRate))==1) {
            if (pollinator2Individuals.get(i).getPollenF2()>0) {
              pollinator2Individuals.get(i).changePollenF2(-1);
              flower2Matrix[x][y][0] = 1;
              flower2Matrix[x][y][1] = FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;
              flower2Matrix[x][y][4] = FLOWER2_ENERGY_GENERATION;
              flower2Count += 1;
              println("CREATED POLLINATED!");
            }
          }
        }
      }
    }
    // if there's no pollinator
    if (!pollinatorOverFlower) {
      if (flower2Reproduction < 2) {
        randomBorn = 2;
      } else {
        randomBorn = flower2Reproduction;
      }
      randomNumber = int(random(1, randomBorn+1));
      if (randomNumber == 1) {
        //println("REPRODUCTION!");
        flower2Matrix[x][y][0] = 1;
        flower2Matrix[x][y][1] = FLOWER2_POLLEN_GENERATION + flower2PollenGeneration;
        flower2Matrix[x][y][4] = FLOWER2_ENERGY_GENERATION;
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


ArrayList<Pollinator> calculatePollinatorNextIteration(ArrayList<Pollinator> pollinatorIndividuals,int[] pollinatorParameters) {
  
  int pollinatorNumber = pollinatorParameters[0];
  int pollinatorMovementRate = pollinatorParameters[1];
  int pollinatorGatheringRate = pollinatorParameters[3];
  int pollinatorGatheringEnergy = pollinatorParameters[4];
  
  int flower1PollenPropagation = flower1Parameters[2];
  int flower2PollenPropagation = flower2Parameters[2];
  
  // adjust quantity of pollinator1
  
  // add if needed
  for (int i = pollinatorIndividuals.size(); i < pollinatorNumber; i++) {
    if (int(random(1, 1000000)) == 1) { 
      pollinatorIndividuals.add(new Pollinator(0, 0, 10000000, int(random(10, matrixSizeX)), int(random(1, matrixSizeY)),0)); // each pollinator starts with  energy to avoid inminent dying
    }
  }
  
  // remove if needed
  for (int i = pollinatorIndividuals.size(); i > pollinatorNumber; i--) {
    pollinatorIndividuals.remove(i-1);
  }
  
  for (int i=0; i < pollinatorIndividuals.size(); i++) {
    int pollinatorXpos = pollinatorIndividuals.get(i).getX();
    int pollinatorYpos = pollinatorIndividuals.get(i).getY();   
    // try to get pollen from flower
    if (int(random(1, pollinatorGatheringRate)) == 1) {
      int flower1pollenQuantity = flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1];
      int flower2pollenQuantity = flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1];
      if (flower1pollenQuantity>0) {
        pollinatorIndividuals.get(i).setLocalMovement(500000); // if pollinator find pollen, star local movement instead of "big jumps"
        int remainPollenFlower1 = flower1pollenQuantity - flower1PollenPropagation;
        if (remainPollenFlower1 < 0) {
          flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = 0;
          pollinatorIndividuals.get(i).changePollenF1(flower1pollenQuantity);
        } else {
          flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = remainPollenFlower1;
          pollinatorIndividuals.get(i).changePollenF1(flower1PollenPropagation);
        }
        // get energy from flowers
        if (flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]>pollinatorGatheringEnergy) {
          pollinatorIndividuals.get(i).changeEnergy(pollinatorGatheringEnergy);
        } else {
          pollinatorIndividuals.get(i).changeEnergy(flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]);
        }
        
      }
      if (flower2pollenQuantity>0) {
        pollinatorIndividuals.get(i).setLocalMovement(500000); // if pollinator find pollen, star local movement instead of "big jumps"
        int remainPollenFlower2 = flower2pollenQuantity - flower2PollenPropagation;
        if (remainPollenFlower2 < 0) {
          flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = 0;
          pollinatorIndividuals.get(i).changePollenF2(flower2pollenQuantity);
        } else {
          flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = remainPollenFlower2;
          pollinatorIndividuals.get(i).changePollenF2(flower2PollenPropagation);
        }
        // get energy from flowers
        if (flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]>pollinatorGatheringEnergy) {
          pollinatorIndividuals.get(i).changeEnergy(pollinatorGatheringEnergy);
        } else {
          pollinatorIndividuals.get(i).changeEnergy(flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]);
        }
      }
    }
    int movementAlteration = 1;
    if (pollinatorIndividuals.get(i).getLocalMovement()>0) { movementAlteration = 4; }
    if (int(random(1,pollinatorMovementRate*movementAlteration))==1) {
      // random move
      xoff = xoff + PARLIN_NOISE_FACTOR;
      int randpos = int(map(noise(xoff),0,1,1,16));
      if (randpos == 4 && pollinatorXpos > 0 && pollinatorYpos > 0) { pollinatorIndividuals.get(i).changeX(-1); pollinatorIndividuals.get(i).changeY(-1); }
      if (randpos == 5 && pollinatorYpos > 0) { pollinatorIndividuals.get(i).changeY(-1); }
      if (randpos == 6 && pollinatorXpos < matrixSizeX - 1 && pollinatorYpos > 0) { pollinatorIndividuals.get(i).changeX(1); pollinatorIndividuals.get(i).changeY(-1); }
      if (randpos == 7 && pollinatorXpos > 0) { pollinatorIndividuals.get(i).changeX(-1); }
      if (randpos == 8 && pollinatorXpos < matrixSizeX - 1) { pollinatorIndividuals.get(i).changeX(1); }
      if (randpos == 9 && pollinatorXpos > 0 && pollinatorYpos < matrixSizeY - 1) { pollinatorIndividuals.get(i).changeX(-1); pollinatorIndividuals.get(i).changeY(1); }
      if (randpos == 10 && pollinatorYpos < matrixSizeY - 1) { pollinatorIndividuals.get(i).changeY(1); }
      if (randpos == 11 && pollinatorXpos < matrixSizeX - 1 && pollinatorYpos < matrixSizeY - 1) { pollinatorIndividuals.get(i).changeX(1); pollinatorIndividuals.get(i).changeY(1); }
    }
    // comsume energy and reduce local movement
    pollinatorIndividuals.get(i).changeEnergy(-1);
    pollinatorIndividuals.get(i).changeLocalMovement(-1);
    // die
    if (pollinatorIndividuals.get(i).getEnergy() <1) { pollinatorIndividuals.remove(i);}
  }
  return pollinatorIndividuals;
}
