#include <Ultrasonic.h>

#define trigPin 2
#define echoPin 4

Ultrasonic ultrasonic(trigPin,echoPin); // (Trig PIN,Echo PIN)


void setup() {
  Serial.begin (9600);
  
  // put your setup code here, to run once:
  // Motor setup
  pinMode(12, OUTPUT); //Initiates Motor Channel A pin
  pinMode(9, OUTPUT); //Initiates Brake Channel A pin
  pinMode(13, OUTPUT); //Initiates Motor Channel B pin
  pinMode(8, OUTPUT); //Initiates Brake Channel B pin
  // HC-SR04 distance sensor setup
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

}

void loop() {
  delay(100);
  if (isNearObject()) {
    //Serial.println("Stoped");
    stopRobot();
    turn();
    stopRobot();
  } else {
    //Serial.println("Running"); 
    goAhead();
  }
}

boolean isNearObject() {
  int distance;
  distance=ultrasonic.Ranging(CM);
  Serial.print(distance);
  Serial.println(" cm");
  if (distance>8) { return false; } else { return true; }
}

void goAhead() {
  digitalWrite(12, HIGH); //Establishes forward direction of Channel A
  digitalWrite(9, LOW);   //Disengage the Brake for Channel A
  analogWrite(3, 128);   //Spins the motor on Channel A at half speed
  digitalWrite(13, HIGH); //Establishes forward direction of Channel B
  digitalWrite(8, LOW);   //Disengage the Brake for Channel B
  analogWrite(11, 128);   //Spins the motor on Channel B at full speed
}

void stopRobot() {
  digitalWrite(9, HIGH); // engage break Channel A
  digitalWrite(8, HIGH); // engage break Channel B
}

void turn() {
  digitalWrite(12, LOW); //Establishes backward direction of Channel A
  digitalWrite(9, LOW);   //Disengage the Brake for Channel A
  analogWrite(3, 128);   //Spins the motor on Channel A at half speed
  digitalWrite(13, HIGH); //Establishes forward direction of Channel B
  digitalWrite(8, LOW);   //Disengage the Brake for Channel B
  analogWrite(11, 128);   //Spins the motor on Channel B at full speed
  delay(1800);             // turn 1.8 second
}
