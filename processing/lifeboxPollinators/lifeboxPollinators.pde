/**
 * Lifebox pollinators version 
 */
 
 import mqtt.*; // you will need to install mqtt library to connect to lifebox app
 
 MQTTClient client;

class Adapter implements MQTTListener {
  void clientConnected() {
    println("client connected");
    client.subscribe("/lifeboxPollinatorData/data1");
    client.subscribe("/lifeboxPollinatorData/data2");
  }
  void messageReceived(String topic, byte[] payload) {
    println("new message: " + topic + " - " + new String(payload));
  }

  void connectionLost() {
    println("connection lost");
  }
}

Adapter adapter;


 class Pollinator { 
  int pollenF1;
  int pollenF2;
  int pollenF3;
  int energy;
  int xpos;
  int ypos;
  int localMovement; // 50000 to 0, 0 = no local movement
  Pollinator (int p1, int p2, int p3, int e, int x, int y, int lm) {  
    pollenF1 = p1;
    pollenF2 = p2;
    pollenF3 = p3;
    xpos = x;
    ypos = y;
    energy = e;
    localMovement = lm;
  } 
  void changePollen(int p, int nf) { 
    if (nf==1) { pollenF1 = pollenF1 + p; }
    if (nf==2) { pollenF2 = pollenF2 + p; }
    if (nf==3) { pollenF3 = pollenF1 + p; }
  }
  int getPollen(int nf) {
    int p = 0;
    if (nf==1) { p = pollenF1; }
    if (nf==2) { p = pollenF2; }
    if (nf==3) { p = pollenF3; }
    return p;
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
 
// debug mode
boolean debug = true;

// enable mqtt?
boolean enableMQTT = true;

// messages list
String[] messages = new String[35];
int message_index = 0;

int[] totalPollinations = new int[3];

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
int[][][] flower3Matrix = new int[matrixSizeX][matrixSizeY][5]; // [0] age [1] pollen [2] xpos [3] ypos [4] energy available (nectar)

ArrayList<Pollinator> pollinator1Individuals = new ArrayList<Pollinator>();
ArrayList<Pollinator> pollinator2Individuals = new ArrayList<Pollinator>();
ArrayList<Pollinator> pollinator3Individuals = new ArrayList<Pollinator>();

int[] available_spots = new int[8];

int[] flowerCount = {0,0,0};

int[] flowerCountLastIteration = {0,0,0};


// hardcoded web app controller parameters (only for testing)
int[] flower1Parameters = { 400, 1000, 2, 3, 5000}; // life expectancy [max cycles of flower life], reproduction [marginal reproduction chances high value>slow rate 2-X], pollen propagation [quantity of pollen allowed to be relased from flower], pollen generation [quantity of pollen generated per cycle]
int[] flower2Parameters = { 400, 1000, 2, 3, 5000}; // life expectancy, reproduction, pollen propagation, pollen generation, random born chances
int[] flower3Parameters = { 400, 1000, 2, 3, 5000};

int[] pollinator1Parameters = { 10, 20000, 2, 4, 1000 }; // number of individuals, movement rate, pollination rate, pollen gathering, energy gatherning
int[] pollinator2Parameters = { 10, 20000, 2, 4, 1000 }; // number of individuals, movement rate, pollination rate, pollen gathering, energy gatherning
int[] pollinator3Parameters = { 10, 20000, 2, 4, 1000 }; // number of individuals, movement rate, pollination rate, pollen gathering, energy gatherning

final int FLOWER_ENERGY_GENERATION = 1000;

final int FLOWER_MAXENERGY = 10000000;

final float PARLIN_NOISE_FACTOR = 0.3; //randomness of pollinators movement



void setup() {
  size(1920, 1080);
  //size(800,600);
  
  if (enableMQTT) {
    adapter = new Adapter();
    client = new MQTTClient(this, adapter);
    client.connect("mqtt://test.mosquitto.org", "lifeboxpollinator");
  }
  colorMode(RGB);
  
  for (int i=0;i<35;i++) { messages[i]=""; }
  
  totalPollinations[0] = 1;
  totalPollinations[1] = 1;
  totalPollinations[2] = 1;

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
  flowerCountLastIteration[0] = flowerCount[0];
  flowerCountLastIteration[1] = flowerCount[1];
  flowerCountLastIteration[2] = flowerCount[2];
  flowerCount[0] = 0;
  flowerCount[1] = 0;
  flowerCount[2] = 0;
  
  background(0);
 
  // paint the flowers matrix
  for (int x = 0; x < matrixSizeX; x++) {
    for (int y = 0; y < matrixSizeY; y++) {
      flower1Matrix = calculateFlowerNextIteration(x, y,flower1Matrix,flower1Parameters,0);
      flower2Matrix = calculateFlowerNextIteration(x, y,flower2Matrix,flower2Parameters,1);
      flower3Matrix = calculateFlowerNextIteration(x, y,flower3Matrix,flower3Parameters,2);
      pollinator1Individuals = calculatePollinatorNextIteration(pollinator1Individuals,pollinator1Parameters);
      pollinator2Individuals = calculatePollinatorNextIteration(pollinator2Individuals,pollinator2Parameters);
      pollinator3Individuals = calculatePollinatorNextIteration(pollinator3Individuals,pollinator3Parameters);
      //println(plantsMatrix[x][y][1]);
      draw = false;
      if (flower1Matrix[x][y][0]>0) {
        fill(0, 0, 255, map(flower1Matrix[x][y][0], 0, flower1Parameters[0], 0, 255));
        draw = true;
      }
      
      if (flower2Matrix[x][y][0]>0) {
        fill(255, 0, 0,map(flower2Matrix[x][y][0], 0, flower2Parameters[0], 0, 255));
        draw = true;
      }
      if (flower3Matrix[x][y][0]>0) {
        fill(0, 255, 0,map(flower3Matrix[x][y][0], 0, flower3Parameters[0], 0, 255));
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
  if (enableMQTT) {
  client.publish("/lifeboxPollinatorData/flowerData", str(flowerCount[0])+"/"+str(totalPollinations[0])+"Red flowers:"+str(flowerCount[1])+"/"+str(totalPollinations[1])+"Green flowers:"+str(flowerCount[2])+"/"+st(totalPollinations[2]));
  }
  if (debug) {
    fill(150, 150, 150, 255);
    textSize(32);
    text("Blue flowers:"+flowerCount[0]+"/"+totalPollinations[0]+"          Red flowers:"+flowerCount[1]+"/"+totalPollinations[1]+"          Green flowers:"+flowerCount[2]+"/"+totalPollinations[2], 40, 1000);
    textSize(20);
    for (int i=0;i<35;i++) {
      text(messages[i],1650,50+(i*30));
    }
  }
}

int[][][] calculateFlowerNextIteration(int x,int y, int[][][] flowerMatrix, int[] flowerParameters, int numberOfFlower) {
  int flower_neighbours = 0;
  int flowerVitality = flowerParameters[0];
  int flowerReproduction = flowerParameters[1];
  int flowerPollenGeneration = flower1Parameters[3];
  int flowerRandomBornChances = flower1Parameters[4];

  // number of pollinators ARE not dynamic!!
  int pollinator1PollinationRate = pollinator1Parameters[2];
  int pollinator2PollinationRate = pollinator2Parameters[2];
  int pollinator3PollinationRate = pollinator3Parameters[2];
  
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
  
  // count the number of currently live neighbouring cells
  if (flowerMatrix[x][y][0] == 0 && flowerMatrix[xm][y][0] > 0) {
    flower_neighbours += 1;
  }
  if (flowerMatrix[x][y][0] == 0 && flowerMatrix[xp][y][0] > 0) {
    flower_neighbours += 1;
  }
  if (flowerMatrix[x][y][0] == 0 && flowerMatrix[xm][ym][0] > 0) {
    flower_neighbours += 1;
  }
  if (flowerMatrix[x][y][0] == 0 && flowerMatrix[x][ym][0] > 0) {
    flower_neighbours += 1;
  }
  if (flowerMatrix[x][y][0] == 0 && flowerMatrix[xp][ym][0] > 0) {
    flower_neighbours += 1;
  }
  if (flowerMatrix[x][y][0] == 0 && flowerMatrix[xm][yp][0] > 0) {
    flower_neighbours += 1;
  }
  if (flowerMatrix[x][y][0] == 0 && flowerMatrix[x][yp][0] > 0) {
    flower_neighbours += 1;
  }
  if (flowerMatrix[x][y][0] == 0 && flowerMatrix[xp][yp][0] > 0) {
    flower_neighbours += 1;
  }
  // if too old, the flower dies
  if (flowerMatrix[x][y][0] >= flowerVitality) {
    flowerMatrix[x][y][0] = 0;
    flowerMatrix[x][y][1] = 0;
    flowerMatrix[x][y][4] = 0;
  }

  // flower grows
  if (flowerMatrix[x][y][0]>0 && flowerMatrix[x][y][0] < flowerVitality) {
    flowerMatrix[x][y][0] += 1;
    flowerMatrix[x][y][1] = flowerMatrix[x][y][1] + flowerPollenGeneration;  // increase pollen available
    flowerCount[numberOfFlower] += 1;
    if (int(random(1, 10))==1) {
      flowerMatrix[x][y][4] = flowerMatrix[x][y][4] + FLOWER_ENERGY_GENERATION;
      if (flowerMatrix[x][y][4] > FLOWER_MAXENERGY) { flowerMatrix[x][y][4] = FLOWER_MAXENERGY; }
    }
      
  }
  // flower reproduction
  if (flowerReproduction > 0 && flowerMatrix[x][y][0] == 0 && flower_neighbours > 0) {
    // we are on a potential reproductive spot, we have a pollinator?
    boolean pollinatorOverFlower = false;
    for (int i=0; i < pollinator1Individuals.size(); i++) {
      if (x == pollinator1Individuals.get(i).getX() && y == pollinator1Individuals.get(i).getY()) {
        pollinatorOverFlower = true;
        if (int(random(1, pollinator1PollinationRate))==1) {
          if (pollinator1Individuals.get(i).getPollen(1)>0) {
            pollinator1Individuals.get(i).changePollen(-1,1);
            flowerMatrix[x][y][0] = 1;
            flowerMatrix[x][y][1] = flowerPollenGeneration;
            flowerMatrix[x][y][4] = FLOWER_ENERGY_GENERATION;
            flowerCount[numberOfFlower] += 1;
            if (numberOfFlower == 0) { totalPollinations[0]++; addMessage("Blue flower pollinated"); }
            if (numberOfFlower == 1) { totalPollinations[1]++; addMessage("Red flower pollinated"); }
            if (numberOfFlower == 2) { totalPollinations[2]++; addMessage("Green flower pollinated"); }
          }
        }
      }
    }
    if (!pollinatorOverFlower) {
      for (int i=0; i < pollinator2Individuals.size(); i++) {
        if (x == pollinator2Individuals.get(i).getX() && y == pollinator2Individuals.get(i).getY()) {
          pollinatorOverFlower = true;
          if (int(random(1, pollinator2PollinationRate))==1) {
            if (pollinator2Individuals.get(i).getPollen(2)>0) {
              pollinator2Individuals.get(i).changePollen(-1,2);
              flowerMatrix[x][y][0] = 1;
              flowerMatrix[x][y][1] = flowerPollenGeneration;
              flowerMatrix[x][y][4] = FLOWER_ENERGY_GENERATION;
              flowerCount[numberOfFlower] += 1;
              if (numberOfFlower == 0) { totalPollinations[0]++; addMessage("Blue flower pollinated"); }
              if (numberOfFlower == 1) { totalPollinations[1]++; addMessage("Red flower pollinated"); }
              if (numberOfFlower == 2) { totalPollinations[2]++; addMessage("Green flower pollinated"); }
            }
          }
        }
      }
    }
    if (!pollinatorOverFlower) {
      for (int i=0; i < pollinator3Individuals.size(); i++) {
        if (x == pollinator3Individuals.get(i).getX() && y == pollinator3Individuals.get(i).getY()) {
          pollinatorOverFlower = true;
          if (int(random(1, pollinator3PollinationRate))==1) {
            if (pollinator3Individuals.get(i).getPollen(3)>0) {
              pollinator3Individuals.get(i).changePollen(-1,3);
              flowerMatrix[x][y][0] = 1;
              flowerMatrix[x][y][1] = flowerPollenGeneration;
              flowerMatrix[x][y][4] = FLOWER_ENERGY_GENERATION;
              flowerCount[numberOfFlower] += 1;
              if (numberOfFlower == 0) { totalPollinations[0]++; addMessage("Blue flower pollinated"); }
              if (numberOfFlower == 1) { totalPollinations[1]++; addMessage("Red flower pollinated"); }
              if (numberOfFlower == 2) { totalPollinations[2]++; addMessage("Green flower pollinated"); }
            }
          }
        }
      }
    }
    // if there's no pollinator
    if (!pollinatorOverFlower) {
      if (flowerReproduction < 2) {
        randomBorn = 2;
      } else {
        randomBorn =  flowerReproduction;
      }
      randomNumber = int(random(1, randomBorn+1));
      if (randomNumber == 1) {
        //println("REPRODUCTION!");
        flowerMatrix[x][y][0] = 1;
        flowerMatrix[x][y][1] = flowerPollenGeneration;
        flowerMatrix[x][y][4] = FLOWER_ENERGY_GENERATION;
        flowerCount[numberOfFlower] += 1;
      }
    }
  }
  // spontaneous generation
  if (flowerMatrix[x][y][0] == 0 && flower_neighbours == 0 && flowerCount[numberOfFlower] == 0 && flowerCountLastIteration[numberOfFlower] == 0) {
    randomNumber = int(random(1, flowerRandomBornChances));
    if (randomNumber == 1) {
      flowerMatrix[x][y][0] = 1;
      flowerMatrix[x][y][1] = flowerPollenGeneration;
      flower1Matrix[x][y][4] = FLOWER_ENERGY_GENERATION;
      flowerCount[numberOfFlower] += 1;
    }
  }
  return flowerMatrix;
}


ArrayList<Pollinator> calculatePollinatorNextIteration(ArrayList<Pollinator> pollinatorIndividuals,int[] pollinatorParameters) {
  
  int pollinatorNumber = pollinatorParameters[0];
  int pollinatorMovementRate = pollinatorParameters[1];
  int pollinatorGatheringRate = pollinatorParameters[3];
  int pollinatorGatheringEnergy = pollinatorParameters[4];
  
  int flower1PollenPropagation = flower1Parameters[2];
  int flower2PollenPropagation = flower2Parameters[2];
  int flower3PollenPropagation = flower3Parameters[2];
  
  // adjust quantity of pollinator1
  
  // add if needed
  for (int i = pollinatorIndividuals.size(); i < pollinatorNumber; i++) {
    if (int(random(1, 1000000)) == 1) { 
      pollinatorIndividuals.add(new Pollinator(0, 0, 0, 10000000, int(random(10, matrixSizeX)), int(random(1, matrixSizeY)),0)); // each pollinator starts with  energy to avoid inminent dying
      addMessage("Pollinator born");
    }
  }
  
  // remove if needed
  for (int i = pollinatorIndividuals.size(); i > pollinatorNumber; i--) {
    pollinatorIndividuals.remove(i-1);
  }
  
  for (int i=0; i < pollinatorIndividuals.size(); i++) {
    int pollinatorXpos = pollinatorIndividuals.get(i).getX();
    int pollinatorYpos = pollinatorIndividuals.get(i).getY();   
    // try to get pollen from flower (flower dependant)
    if (int(random(1, pollinatorGatheringRate)) == 1) {
      int flower1pollenQuantity = flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1];
      int flower2pollenQuantity = flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1];
      int flower3pollenQuantity = flower3Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1];
      
      if (flower1pollenQuantity>0) {
        pollinatorIndividuals.get(i).setLocalMovement(500000); // if pollinator find pollen, start local movement instead of "big jumps"
        int remainPollenFlower1 = flower1pollenQuantity - flower1PollenPropagation;
        if (remainPollenFlower1 < 0) {
          flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = 0;
          pollinatorIndividuals.get(i).changePollen(flower1pollenQuantity,0);
        } else {
          flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = remainPollenFlower1;
          pollinatorIndividuals.get(i).changePollen(flower1PollenPropagation,0);
        }
        // get energy from flowers
        if (flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]>pollinatorGatheringEnergy) {
          pollinatorIndividuals.get(i).changeEnergy(pollinatorGatheringEnergy);
        } else {
          pollinatorIndividuals.get(i).changeEnergy(flower1Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]);
        }     
      }
      
      if (flower2pollenQuantity>0) {
        pollinatorIndividuals.get(i).setLocalMovement(500000); // if pollinator find pollen, start local movement instead of "big jumps"
        int remainPollenFlower2 = flower2pollenQuantity - flower2PollenPropagation;
        if (remainPollenFlower2 < 0) {
          flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = 0;
          pollinatorIndividuals.get(i).changePollen(flower2pollenQuantity,1);
        } else {
          flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = remainPollenFlower2;
          pollinatorIndividuals.get(i).changePollen(flower2PollenPropagation,1);
        }
        // get energy from flowers
        if (flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]>pollinatorGatheringEnergy) {
          pollinatorIndividuals.get(i).changeEnergy(pollinatorGatheringEnergy);
        } else {
          pollinatorIndividuals.get(i).changeEnergy(flower2Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]);
        }
      }
      
      if (flower3pollenQuantity>0) {
        pollinatorIndividuals.get(i).setLocalMovement(500000); // if pollinator find pollen, start local movement instead of "big jumps"
        int remainPollenFlower3 = flower3pollenQuantity - flower3PollenPropagation;
        if (remainPollenFlower3 < 0) {
          flower3Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = 0;
          pollinatorIndividuals.get(i).changePollen(flower1pollenQuantity,2);
        } else {
          flower3Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][1] = remainPollenFlower3;
          pollinatorIndividuals.get(i).changePollen(flower3PollenPropagation,2);
        }
        // get energy from flowers
        if (flower3Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]>pollinatorGatheringEnergy) {
          pollinatorIndividuals.get(i).changeEnergy(pollinatorGatheringEnergy);
        } else {
          pollinatorIndividuals.get(i).changeEnergy(flower3Matrix[pollinatorIndividuals.get(i).getX()][pollinatorIndividuals.get(i).getY()][4]);
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
    if (pollinatorIndividuals.get(i).getEnergy() <1) { pollinatorIndividuals.remove(i); addMessage("Pollinator dies"); }
  }
  return pollinatorIndividuals;
}

void addMessage(String m) {
  if (message_index < 35) {
    messages[message_index] = m;
    message_index = message_index + 1;
  } else {
    for (int i=1;i<35;i++) {
      messages[i-1] = messages[i];
    }
    messages[34] = m;
    message_index = 34;
  }
}
