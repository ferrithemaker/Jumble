int[][][] number = new int[10][6][2];
int[][][] position = new int[4][6][2];
float minutesRadius;
float hoursRadius;
float clockDiameter;
int minFirstDigit;
int minSecondDigit;
int hourFirstDigit;
int hourSecondDigit;
int oldMinSecondDigit = -1;
boolean init = true;
int count = 0;
boolean runningAnimation=true;

void initNumbers() {
  number[0][0][0]=6; number[0][0][1]=15;
  number[0][1][0]=6; number[0][1][1]=45;
  number[0][2][0]=0; number[0][2][1]=30;
  number[0][3][0]=0; number[0][3][1]=30;
  number[0][4][0]=0; number[0][4][1]=15;
  number[0][5][0]=0; number[0][5][1]=45;
  number[1][0][0]=7; number[1][0][1]=35;
  number[1][1][0]=6; number[1][1][1]=30;
  number[1][2][0]=7; number[1][2][1]=35;
  number[1][3][0]=0; number[1][3][1]=30;
  number[1][4][0]=7; number[1][4][1]=35;
  number[1][5][0]=0; number[1][5][1]=0;
  number[2][0][0]=3; number[2][0][1]=15;
  number[2][1][0]=9; number[2][1][1]=30;
  number[2][2][0]=3; number[2][2][1]=30;
  number[2][3][0]=0; number[2][3][1]=45;
  number[2][4][0]=0; number[2][4][1]=15;
  number[2][5][0]=9; number[2][5][1]=45;
  number[3][0][0]=3; number[3][0][1]=15;
  number[3][1][0]=6; number[3][1][1]=45;
  number[3][2][0]=3; number[3][2][1]=15;
  number[3][3][0]=0; number[3][3][1]=30;
  number[3][4][0]=3; number[3][4][1]=15;
  number[3][5][0]=0; number[3][5][1]=45;
  number[4][0][0]=6; number[4][0][1]=30;
  number[4][1][0]=2; number[4][1][1]=10;
  number[4][2][0]=0; number[4][2][1]=15;
  number[4][3][0]=9; number[4][3][1]=30;
  number[4][4][0]=7; number[4][4][1]=35;
  number[4][5][0]=0; number[4][5][1]=0;
  number[5][0][0]=3; number[5][0][1]=30;
  number[5][1][0]=9; number[5][1][1]=45;
  number[5][2][0]=0; number[5][2][1]=15;
  number[5][3][0]=9; number[5][3][1]=30;
  number[5][4][0]=3; number[5][4][1]=15;
  number[5][5][0]=0; number[5][5][1]=45;
  number[6][0][0]=6; number[6][0][1]=30;
  number[6][1][0]=2; number[6][1][1]=10;
  number[6][2][0]=0; number[6][2][1]=30;
  number[6][3][0]=9; number[6][3][1]=30;
  number[6][4][0]=0; number[6][4][1]=15;
  number[6][5][0]=0; number[6][5][1]=45;
  number[7][0][0]=9; number[7][0][1]=15;
  number[7][1][0]=9; number[7][1][1]=30;
  number[7][2][0]=7; number[7][2][1]=35;
  number[7][3][0]=0; number[7][3][1]=30;
  number[7][4][0]=7; number[7][4][1]=35;
  number[7][5][0]=0; number[7][5][1]=30;
  number[8][0][0]=6; number[8][0][1]=15;
  number[8][1][0]=6; number[8][1][1]=45;
  number[8][2][0]=0; number[8][2][1]=20;
  number[8][3][0]=0; number[8][3][1]=40;
  number[8][4][0]=0; number[8][4][1]=15;
  number[8][5][0]=0; number[8][5][1]=45;
  number[9][0][0]=6; number[9][0][1]=15;
  number[9][1][0]=9; number[9][1][1]=30;
  number[9][2][0]=0; number[9][2][1]=15;
  number[9][3][0]=0; number[9][3][1]=30;
  number[9][4][0]=7; number[9][4][1]=35;
  number[9][5][0]=0; number[9][5][1]=30;
}

void initPositions() {
  position[0][0][0]=100;position[0][0][1]=100;
  position[0][1][0]=250;position[0][1][1]=100;
  position[0][2][0]=100;position[0][2][1]=250;
  position[0][3][0]=250;position[0][3][1]=250;
  position[0][4][0]=100;position[0][4][1]=400;
  position[0][5][0]=250;position[0][5][1]=400;
  position[1][0][0]=400;position[1][0][1]=100;
  position[1][1][0]=550;position[1][1][1]=100;
  position[1][2][0]=400;position[1][2][1]=250;
  position[1][3][0]=550;position[1][3][1]=250;
  position[1][4][0]=400;position[1][4][1]=400;
  position[1][5][0]=550;position[1][5][1]=400;
  position[2][0][0]=700;position[2][0][1]=100;
  position[2][1][0]=850;position[2][1][1]=100;
  position[2][2][0]=700;position[2][2][1]=250;
  position[2][3][0]=850;position[2][3][1]=250;
  position[2][4][0]=700;position[2][4][1]=400;
  position[2][5][0]=850;position[2][5][1]=400;
  position[3][0][0]=1000;position[3][0][1]=100;
  position[3][1][0]=1150;position[3][1][1]=100;
  position[3][2][0]=1000;position[3][2][1]=250;
  position[3][3][0]=1150;position[3][3][1]=250;
  position[3][4][0]=1000;position[3][4][1]=400;
  position[3][5][0]=1150;position[3][5][1]=400;
}

void drawClock(int cx,int cy,int hour,int min) {
  float m = map(min, 0, 60, 0, TWO_PI) - HALF_PI; 
  float h = map(hour, 0, 24, 0, TWO_PI * 2) - HALF_PI;
  
  noFill();
  strokeWeight(4);
  stroke(200,100,100);
  ellipse(cx, cy, clockDiameter, clockDiameter);
  
  // Draw the hands of the clock
  stroke(200);
  strokeWeight(4);
  line(cx, cy, cx + cos(m) * minutesRadius, cy + sin(m) * minutesRadius);
  strokeWeight(4);
  line(cx, cy, cx + cos(h) * hoursRadius, cy + sin(h) * hoursRadius);
}


void setup() {
  initNumbers();
  initPositions();
  size(1400, 640);
  background(0);
  stroke(255);
  int radius = 100;
  minutesRadius = radius * 0.60;
  hoursRadius = radius * 0.60;
  clockDiameter = radius * 1.3;
}

void draw() {
  int time = millis();
  if (millis() > time + 2000)
  {
    // action
    time = millis();
  }
  if (runningAnimation == false) {
    background(0);
  }
  minFirstDigit=int(minute() / 10);
  minSecondDigit=int(minute() % 10);
  hourFirstDigit=int(hour() / 10);
  hourSecondDigit=int(hour() % 10);
  if (oldMinSecondDigit!=minSecondDigit && init==true) {
    runningAnimation = true;
    count = 0;
    for (int i=0;i<6;i++) {  
      drawClock(position[0][i][0],position[0][i][1],int(random(0,11)),int(random(0,59)));
      drawClock(position[1][i][0],position[1][i][1],int(random(0,11)),int(random(0,59)));
      drawClock(position[2][i][0],position[2][i][1],int(random(0,11)),int(random(0,59)));
      drawClock(position[3][i][0],position[3][i][1],int(random(0,11)),int(random(0,59)));
    }
    init = false;
  } else {
    if (runningAnimation == false) {
      for (int i=0;i<6;i++) {  
        drawClock(position[0][i][0],position[0][i][1],number[hourFirstDigit][i][0],number[hourFirstDigit][i][1]);
        drawClock(position[1][i][0],position[1][i][1],number[hourSecondDigit][i][0],number[hourSecondDigit][i][1]);
        drawClock(position[2][i][0],position[2][i][1],number[minFirstDigit][i][0],number[minFirstDigit][i][1]);
        drawClock(position[3][i][0],position[3][i][1],number[minSecondDigit][i][0],number[minSecondDigit][i][1]);
      }
      oldMinSecondDigit=minSecondDigit;
      init = true;
      count = 0;
    }
  }
  if (count > 500) {
    runningAnimation = false;
  }
  count++;
  println(count);
}
