// Arduino robot camera code by Jordi Binefa & Ferran Fabregas

#include <ecat.h>
#include <Servo.h>

Servo servoP1B2; Servo servoP1B3;

#define MAX_GRAUS 170
#define MIN_GRAUS 20
#define ROBOT_ATURAT      0
#define ROBOT_ENDAVANT    1
#define ROBOT_ENDARRERA   2
#define ROBOT_DRETA       3
#define ROBOT_ESQUERRA    4

String szMissatge;
Ecat ecat;
int valorServoV;
int valorServoH;

void setup(){
  ecat.setupNibbleMode(NIBBLE_H_P1,OUTPUT);
  ecat.vUltrasonicSensorP1b0b1_init();
  
  valorServoV=90;
  valorServoH=90;
  nEstatActual = ROBOT_ATURAT;
  pinMode(ecat.nPinP1B2,OUTPUT);
  pinMode(ecat.nPinP1B3,OUTPUT); 
  servoP1B2.attach(ecat.nPinP1B2);
  servoP1B3.attach(ecat.nPinP1B3);
  servoP1B2.write(valorServoV);
  servoP1B3.write(valorServoH);  
  pinMode(ecat.nPinP2B7,OUTPUT);
  pinMode(ecat.nPinP2B6,INPUT);
  pinMode(ecat.nPinP2B5,INPUT);
  pinMode(ecat.nPinP2B4,INPUT);
  ecat.setupNibbleMode(NIBBLE_L_P2,INPUT);
  Serial.begin(115200);
}

void vRobotAturat(){
  ecat.vWriteHighNibbleP1(0x00);
  nEstatActual = ROBOT_ATURAT;
}

void vRobotEndarrera(){
  ecat.vWriteHighNibbleP1(B00000110);
  nEstatActual = ROBOT_ENDARRERA;
}

void vRobotEndavant(){
  ecat.vWriteHighNibbleP1(B00001001);
  nEstatActual = ROBOT_ENDAVANT;
}

void vRobotEsquerra(){
  ecat.vWriteHighNibbleP1(B00000101);
  nEstatActual = ROBOT_ESQUERRA;
}

void vRobotDreta(){
  ecat.vWriteHighNibbleP1(B00001010);
  nEstatActual = ROBOT_DRETA;
}



void vManageMsg(){
 
  if(szMissatge == "b"){
    vRobotEndarrera();
  }
  if(szMissatge == "f"){
    if (ecat.nUsDistanceCmP1b0b1()>=7) {
        vRobotEndavant();
    }
  }
  if(szMissatge == "s"){
    vRobotAturat();
  }
  if(szMissatge == "l"){
    vRobotEsquerra();
  }
  if(szMissatge == "r"){
    vRobotDreta();
  }
  if(szMissatge == "w"){
    if (valorServoH<MAX_GRAUS) {
      valorServoH++;
    }
  }
  if(szMissatge == "x"){
    if (valorServoH>MIN_GRAUS) {
      valorServoH--;
    }
  }
  if(szMissatge == "a"){
    if (valorServoV>MIN_GRAUS) {
      valorServoV--;
    }
  }
  if(szMissatge == "d"){
    if (valorServoV<MAX_GRAUS) {
      valorServoV++;
    }
  }
}

void loop(){

  while(Serial.available()){
    delay(3);
    char c = Serial.read();
    szMissatge += c;
  }
  vManageMsg();
  szMissatge = "";
  if (ecat.nUsDistanceCmP1b0b1()<7 && nEstatActual == ROBOT_ENDAVANT) {
    vRobotAturat();
    nEstatActual = ROBOT_ATURAT;
  }
  servoP1B2.write(valorServoV);
  servoP1B3.write(valorServoH);
}
