// Orignal version created by http://www.instructables.com/id/Getting-started-with-Arduino-Potentiometer-Pong/
// Game upgrade by ferri.fc@gmail.com

import ddf.minim.*;
import processing.serial.*;

String serialPortName = "/dev/ttyACM0";
Serial arduino;
Minim minim;
AudioPlayer wallSound, batSound;
PImage ball, bat_p1, bat_p2, back;
float bat_p1_Position, bat_p2_Position;
float ballX, ballY;
float vertSpeed, horiSpeed;
String[] value;
int p1_score=0;
int p2_score=0;
PFont f;
int count=0;

void setup()
{
  size(960,720);
  if(serialPortName.equals("")) scanForArduino();
  else arduino = new Serial(this, serialPortName, 9600);
  imageMode(CENTER);
  ball = loadImage("ball.png");
  bat_p1 = loadImage("bat.png");
  bat_p2 = loadImage("bat.png");
  back = loadImage("back.png");
  f = createFont("Arial",16,true); // Arial, 16 point, anti-aliasing on
  textFont(f,16);
  minim = new Minim(this);
  wallSound = minim.loadFile("wall.mp3");
  batSound = minim.loadFile("bat.mp3");
  bat_p1_Position = bat_p1.width/2;
  bat_p2_Position = bat_p2.width/2;
  resetBall();
}

void resetBall()
{
  ballX = 480;
  ballY = 360;
  vertSpeed = random(-12,12);
  horiSpeed = random(-6,6);
}

void draw()
{
  image(back,width/2,height/2,width,height);
  text("Score player1: "+p1_score+"\nScore player2: "+p2_score,10,100);
  count++;
  // increase the velocity
  if (count==200) {
    count=0;
    if (vertSpeed<0) { vertSpeed--; }
    if (vertSpeed>0) { vertSpeed++; }
  }
  // Move the bat
  if((arduino != null) && (arduino.available()>0)) {
    String message = arduino.readStringUntil('\n');
    if(message != null) {
      value = split(message, '|');
      if (value.length==2) {
        bat_p1_Position = map(int(trim(value[0])),0,1024,0,width);
        bat_p2_Position = map(int(trim(value[1])),0,1024,0,width);
      }
    }
  }
  
  // Draw the bats
  image(bat_p1,bat_p1_Position,height-bat_p1.height);
  image(bat_p2,bat_p2_Position,bat_p2.height);
  
  

  // Calculate new position of ball - being sure to keep it on screen
  ballX = ballX + horiSpeed;
  ballY = ballY + vertSpeed;
  if(ballY >= height) { p1_score++; resetBall(); }
  if(ballY <= 0) { p2_score++; resetBall(); }
  if(ballX >= width) wallBounce();
  if(ballX <= 0) wallBounce();

  // Draw the ball in the correct position and orientation
  translate(ballX,ballY);
  if(vertSpeed > 0) rotate(-sin(horiSpeed/vertSpeed));
  else rotate(PI-sin(horiSpeed/vertSpeed));
  image(ball,0,0);
  
  // Do collision detection between bat and ball
  if(bat_p1_TouchingBall()) {
    float distFromBat_p1_Center = bat_p1_Position-ballX;
    horiSpeed = -distFromBat_p1_Center/10;
    vertSpeed = -vertSpeed;
    ballY = height-(bat_p1.height*2);
    batSound.rewind();
    batSound.play();
  }
  
  if(bat_p2_TouchingBall()) {
    float distFromBat_p2_Center = bat_p2_Position-ballX;
    horiSpeed = -distFromBat_p2_Center/10;
    vertSpeed = -vertSpeed;
    ballY = (bat_p2.height*2);
    batSound.rewind();
    batSound.play();
  }
  
}

boolean bat_p1_TouchingBall()
{
  float distFromBat_p1_Center = bat_p1_Position-ballX;
  return (ballY > height-(bat_p1.height*2)) && (ballY < height-(bat_p1.height/2)) && (abs(distFromBat_p1_Center)<bat_p1.width/2);
}

boolean bat_p2_TouchingBall()
{
  float distFromBat_p2_Center = bat_p2_Position-ballX;
  return (ballY < (bat_p2.height*2)) && (ballY > (bat_p2.height/2)) && (abs(distFromBat_p2_Center)<bat_p2.width/2);
}

void wallBounce()
{
  horiSpeed = -horiSpeed;
  wallSound.rewind();
  wallSound.play();
}


void stop()
{
  arduino.stop();
}

void scanForArduino()
{
  try {
    for(int i=0; i<Serial.list().length ;i++) {
      if(Serial.list()[i].contains("tty.usb")) {
        arduino = new Serial(this, Serial.list()[i], 9600);
      }
    }
  } catch(Exception e) {
    // println("Cannot connect to Arduino !");
  }
}
