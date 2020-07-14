import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class multiClock extends PApplet {

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
int count = 0;
boolean runningAnimation=true;
int time;

public void initNumbers() {
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
  number[4][1][0]=1; number[4][1][1]=5;
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
  number[6][1][0]=1; number[6][1][1]=5;
  number[6][2][0]=0; number[6][2][1]=30;
  number[6][3][0]=9; number[6][3][1]=30;
  number[6][4][0]=0; number[6][4][1]=15;
  number[6][5][0]=0; number[6][5][1]=45;
  number[7][0][0]=3; number[7][0][1]=15;
  number[7][1][0]=9; number[7][1][1]=30;
  number[7][2][0]=7; number[7][2][1]=35;
  number[7][3][0]=0; number[7][3][1]=30;
  number[7][4][0]=7; number[7][4][1]=35;
  number[7][5][0]=0; number[7][5][1]=0;
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

public void initPositions() {
  int centerDistance = 27;
  int upRow = 90;
  int midRow = 170;
  int downRow = 250;
  position[0][0][0]=centerDistance;position[0][0][1]=upRow;
  position[0][1][0]=centerDistance*3;position[0][1][1]=upRow;
  position[0][2][0]=centerDistance;position[0][2][1]=midRow;
  position[0][3][0]=centerDistance*3;position[0][3][1]=midRow;
  position[0][4][0]=centerDistance;position[0][4][1]=downRow;
  position[0][5][0]=centerDistance*3;position[0][5][1]=downRow;
  position[1][0][0]=centerDistance*5;position[1][0][1]=upRow;
  position[1][1][0]=centerDistance*7;position[1][1][1]=upRow;
  position[1][2][0]=centerDistance*5;position[1][2][1]=midRow;
  position[1][3][0]=centerDistance*7;position[1][3][1]=midRow;
  position[1][4][0]=centerDistance*5;position[1][4][1]=downRow;
  position[1][5][0]=centerDistance*7;position[1][5][1]=downRow;
  position[2][0][0]=centerDistance*9;position[2][0][1]=upRow;
  position[2][1][0]=centerDistance*11;position[2][1][1]=upRow;
  position[2][2][0]=centerDistance*9;position[2][2][1]=midRow;
  position[2][3][0]=centerDistance*11;position[2][3][1]=midRow;
  position[2][4][0]=centerDistance*9;position[2][4][1]=downRow;
  position[2][5][0]=centerDistance*11;position[2][5][1]=downRow;
  position[3][0][0]=centerDistance*13;position[3][0][1]=upRow;
  position[3][1][0]=centerDistance*15;position[3][1][1]=upRow;
  position[3][2][0]=centerDistance*13;position[3][2][1]=midRow;
  position[3][3][0]=centerDistance*15;position[3][3][1]=midRow;
  position[3][4][0]=centerDistance*13;position[3][4][1]=downRow;
  position[3][5][0]=centerDistance*15;position[3][5][1]=downRow;
}

public void drawClock(int cx,int cy,int hour,int min) {
  float m = map(min, 0, 60, 0, TWO_PI) - HALF_PI; 
  float h = map(hour, 0, 24, 0, TWO_PI * 2) - HALF_PI;
  
  //noFill();
  fill(0);
  strokeWeight(1);
  stroke(200,100,100);
  ellipse(cx, cy, clockDiameter, clockDiameter);
  
  // Draw the hands of the clock
  stroke(200);
  strokeWeight(2);
  line(cx, cy, cx + cos(m) * minutesRadius, cy + sin(m) * minutesRadius);
  strokeWeight(2);
  line(cx, cy, cx + cos(h) * hoursRadius, cy + sin(h) * hoursRadius);
}


public void setup() {
  initNumbers();
  initPositions();
  
  background(0);
  stroke(255);
  int radius = 48;
  minutesRadius = radius * 0.5f;
  hoursRadius = radius * 0.5f;
  clockDiameter = radius * 1;
  time = millis();
}

public void draw() {
  if (runningAnimation == true) {
    if (millis() > time + 500)
    {
      for (int i=0;i<6;i++) {
        if (PApplet.parseInt(random(0,12))==0) {
          drawClock(position[0][i][0],position[0][i][1],PApplet.parseInt(random(0,11)),PApplet.parseInt(random(0,59)));
        }
        if (PApplet.parseInt(random(0,12))==0) {
          drawClock(position[1][i][0],position[1][i][1],PApplet.parseInt(random(0,11)),PApplet.parseInt(random(0,59)));
        }
        if (PApplet.parseInt(random(0,12))==0) {
          drawClock(position[2][i][0],position[2][i][1],PApplet.parseInt(random(0,11)),PApplet.parseInt(random(0,59)));
        }
        if (PApplet.parseInt(random(0,12))==0) {
          drawClock(position[3][i][0],position[3][i][1],PApplet.parseInt(random(0,11)),PApplet.parseInt(random(0,59)));
        }
      }
      count++;
      time = millis();
      if (count == 10) {
        runningAnimation = false;
        count = 0;
      }
    }
  }
  minFirstDigit=PApplet.parseInt(minute() / 10);
  minSecondDigit=PApplet.parseInt(minute() % 10);
  hourFirstDigit=PApplet.parseInt(hour() / 10);
  hourSecondDigit=PApplet.parseInt(hour() % 10);
  if (oldMinSecondDigit!=minSecondDigit) {
    runningAnimation = true;
  } else {
    if (runningAnimation == false) {
      //background(0);
      for (int i=0;i<6;i++) {
        if (PApplet.parseInt(random(0,4))==0) {
          drawClock(position[0][i][0],position[0][i][1],number[hourFirstDigit][i][0],number[hourFirstDigit][i][1]);
        }
        if (PApplet.parseInt(random(0,4))==0) {
          drawClock(position[1][i][0],position[1][i][1],number[hourSecondDigit][i][0],number[hourSecondDigit][i][1]);
        }
        if (PApplet.parseInt(random(0,4))==0) {
          drawClock(position[2][i][0],position[2][i][1],number[minFirstDigit][i][0],number[minFirstDigit][i][1]);
        }
        if (PApplet.parseInt(random(0,4))==0) {
          drawClock(position[3][i][0],position[3][i][1],number[minSecondDigit][i][0],number[minSecondDigit][i][1]);
        }
        delay(100);
      }
    }
  }
  oldMinSecondDigit=minSecondDigit;
}
  public void settings() {  size(480, 320); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "--present", "--window-color=#000000", "--hide-stop", "multiClock" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
