/* Sweep
 by BARRAGAN <http://barraganstudio.com> 
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://arduino.cc/en/Tutorial/Sweep
*/ 

#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
 
int pos = 0;    // variable to store the servo position 
 
void setup() 
{ 
  pinMode(11,OUTPUT);  // attaches the servo on pin 9 to the servo object 
} 
 
void loop() 
{ 
  //myservo.write(180);
  int pulsetime(1600000);
  digitalWrite(11,HIGH);
  delayMicroseconds(pulsetime);
  digitalWrite(11,LOW);
  delay(1000);
} 

