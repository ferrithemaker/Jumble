/**
 * Lifebox processing version 
 */

// screen variables
int matrixSizeX = 10;
int matrixSizeY = 10;
int shapeSize = 40; // 10 for small screen size, 20 for fullHD
int padding = 0;
boolean noColor = false;
boolean simulationAlterations = true;
boolean metaballs = true;

int style = 1;
// best setup for style 0 (circles)int matrixSizeX = 75; int matrixSizeY = 42; int shapeSize = 20; int padding = 5; boolean noColor = false; boolean simulationAlterations = false;
// best setup for style 1 (squares)int matrixSizeX = 95; int matrixSizeY = 53; int shapeSize = 20; int padding = 0; boolean noColor = true; boolean simulationAlterations = true;

// plants variables
int[][][] plantsMatrix = new int[matrixSizeX][matrixSizeY][4]; // [0] age [1] energy [2] xpos [3] ypos
int plantsCount = 0;
int plantsCountLastIteration = 0;

// hardcoded plants data parameters only for testing)
int[] plantsParameters={ 160, 200, 70} ;
final int PLANTS_LIFE_EXPECTANCY = 70;
final int PLANTS_ENERGY_BASE_PER_CYCLE = 50; 
final int PLANTS_RANDOM_BORN_CHANCES = 2000;
final int PLANTS_NEARBORN_CHANCES = 220;

void setup() {
  //size(1920, 1080);
  size(400, 400); // smaller screen
  //fullScreen(P2D);
  //smooth(1);
  // init the plantsMatrix
  if (metaballs==true) {
    colorMode(HSB); 
  } else {
    colorMode(RGB);
  }
  
 for (int x = 0; x < matrixSizeX; x++) {
    for (int y = 0; y < matrixSizeY; y++) {
      plantsMatrix[x][y][0]=0; // set age to 0
      plantsMatrix[x][y][1]=0; // set energy to 0
      plantsMatrix[x][y][2]=((x)*(shapeSize+padding));
      plantsMatrix[x][y][3]=((y)*(shapeSize+padding));  
    }
  }
  noStroke();
}

void draw() {
  plantsCountLastIteration = plantsCount;
  plantsCount = 0;
  background(0);
  if (metaballs == false) {
    for (int x = 0; x < matrixSizeX; x++) {
      for (int y = 0; y < matrixSizeY; y++) {
        calculatePlantsNextIteration(x, y);
        //println(plantsMatrix[x][y][1]);
        if (noColor) {
          fill(map(plantsMatrix[x][y][1], 0, 8000, 0, 255));
        } else {
          fill(0, map(plantsMatrix[x][y][1], 0, 8000, 0, 255), 0);
        }
        if (style == 0) {
          ellipse((x+1)*(shapeSize+padding), (y+1)*(shapeSize+padding), shapeSize, shapeSize);
        }
        if (style == 1) {
          rect(x*(shapeSize+padding), y*(shapeSize+padding), shapeSize, shapeSize);
        }
      }
    }
  } else {
  // make calculations
  for (int x = 0; x < matrixSizeX; x++) {
    for (int y = 0; y < matrixSizeY; y++) {
      calculatePlantsNextIteration(x, y);
      plantsMatrix[x][y][2] += int(random(-5,5));
      plantsMatrix[x][y][3] += int(random(-5,5));
    }
  }
  // set pixels color
  loadPixels();
  for (int xPixel = 0; xPixel < width; xPixel++) {
    for (int yPixel = 0; yPixel < height; yPixel++) {
      int indexPixel = xPixel + yPixel * width;
      float sumA = 0;
      float sumB = 0;
      for (int x = 0; x < matrixSizeX; x++) {
        for (int y = 0; y < matrixSizeY; y++) {
          //println(plantsMatrix[x][y][2],plantsMatrix[x][y][3]);
          float d;
          if (xPixel != plantsMatrix[x][y][2] || yPixel != plantsMatrix[x][y][3]) {
            d = dist(xPixel, yPixel,plantsMatrix[x][y][2],plantsMatrix[x][y][3])/1.5;
          } else {
            d = 0.1;
          }
          float intensityA = (float((plantsMatrix[x][y][0])/10) / d);
          float intensityB = (float((plantsMatrix[x][y][1])/10) / d);
          sumA += intensityA * 0.8;
          sumB += intensityB * 2.8;
        }
      }
      if (noColor) {
        pixels[indexPixel] = color(sumA);
      } else {
        pixels[indexPixel] = color(constrain(sumA,10,220),constrain(sumB,10,220),200);
      }
      //println(sum);
    }
   }
  updatePixels();
  }
  //delay(10);
}

void calculatePlantsNextIteration(int x, int y) {
  int neighbours = 0;
  int plantsReproduction = plantsParameters[0];
  int plantsVitality = plantsParameters[1];
  int plantsGeneration = plantsParameters[2];
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
  if (plantsMatrix[x][y][0] == 0 && plantsMatrix[xm][y][0] > 0) {
    neighbours += 1;
  }
  if (plantsMatrix[x][y][0] == 0 && plantsMatrix[xp][y][0] > 0) {
    neighbours += 1;
  }
  if (plantsMatrix[x][y][0] == 0 && plantsMatrix[xm][ym][0] > 0) {
    neighbours += 1;
  }
  if (plantsMatrix[x][y][0] == 0 && plantsMatrix[x][ym][0] > 0) {
    neighbours += 1;
  }
  if (plantsMatrix[x][y][0] == 0 && plantsMatrix[xp][ym][0] > 0) {
    neighbours += 1;
  }
  if (plantsMatrix[x][y][0] == 0 && plantsMatrix[xm][yp][0] > 0) {
    neighbours += 1;
  }
  if (plantsMatrix[x][y][0] == 0 && plantsMatrix[x][yp][0] > 0) {
    neighbours += 1;
  }
  if (plantsMatrix[x][y][0] == 0 && plantsMatrix[xp][yp][0] > 0) {
    neighbours += 1;
  }
  // if too old, the plant dies
  if (plantsMatrix[x][y][0] >= PLANTS_LIFE_EXPECTANCY + plantsVitality) {
    plantsMatrix[x][y][0] = 0;
    plantsMatrix[x][y][1] = 0;
  }
  // if no energy, the plant dies
  if (plantsMatrix[x][y][0] > 0 && plantsMatrix[x][y][0] < (PLANTS_LIFE_EXPECTANCY + plantsVitality) && plantsMatrix[x][y][1] <= 0) {
    plantsMatrix[x][y][0] = 0;
    plantsMatrix[x][y][1] = 0;
  }
  // plant grows
  if (plantsMatrix[x][y][0]>0 && plantsMatrix[x][y][0] < PLANTS_LIFE_EXPECTANCY + plantsVitality) {
    plantsMatrix[x][y][0] += 1;
    plantsMatrix[x][y][1] = plantsMatrix[x][y][1] + PLANTS_ENERGY_BASE_PER_CYCLE + plantsGeneration;
    if (simulationAlterations) {
      plantsMatrix[x][y][1] = plantsMatrix[x][y][1] - (plantsMatrix[x][y][0] * int(PLANTS_ENERGY_BASE_PER_CYCLE/7));
    }    
    plantsCount += 1;
  }
  // plant reproduction
  if (plantsReproduction > 0 && plantsMatrix[x][y][0] == 0 && neighbours > 0) {
    if (PLANTS_NEARBORN_CHANCES - plantsReproduction < 2) {
      randomBorn = 2;
    } else {
      randomBorn = PLANTS_NEARBORN_CHANCES - plantsReproduction;
    }
    randomNumber = int(random(1, randomBorn));
    if (randomNumber == 1) {
      //println("REPRODUCTION!");
      plantsMatrix[x][y][0] = 1;
      plantsMatrix[x][y][1] = PLANTS_ENERGY_BASE_PER_CYCLE + plantsGeneration;
      plantsCount += 1;
    }
  }
  // spontaneous generation
  if (plantsMatrix[x][y][0] == 0 && neighbours == 0 && plantsCount == 0 && plantsCountLastIteration == 0) {
    randomNumber = int(random(1, PLANTS_RANDOM_BORN_CHANCES));
    if (randomNumber == 1) {
      //println("BORN!!");
      plantsMatrix[x][y][0] = 1;
      plantsMatrix[x][y][1] = PLANTS_ENERGY_BASE_PER_CYCLE + plantsGeneration;
      plantsCount += 1;
    }
  }
}
