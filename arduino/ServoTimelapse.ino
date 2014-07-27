/* Sweep
 by BARRAGAN <http://barraganstudio.com> 
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://arduino.cc/en/Tutorial/Sweep
*/ 

//#include <Servo.h> 
 
//Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
 
int pos = 0;    // variable to store the servo position 
int potentiometerValue=0;
int PinReading;
int lenMicroSecondsOfPeriod = 20 * 1000; // 20 milliseconds (ms)
int lenMicroSecondsOfPulse = 1.8 * 1000; // 1.0 ms is 0 degrees
//Servo srv;

void setup() 
{ 
  Serial.begin(9600);
  pinMode(11,OUTPUT);  // attaches the servo on pin 11 to the servo object
  //srv.attach(11);
  
} 
 
void loop() 
{ 
  //myservo.write(180);
  PinReading=analogRead(3);
  delay(10);
  potentiometerValue=map(PinReading,0,1023,0,180);
  potentiometerValue=constrain(potentiometerValue,0,180);
  //Serial.print(potentiometerValue);
  //Serial.print("\n");
  int pulsetime(1600000);
  digitalWrite(11,HIGH);
  delayMicroseconds(pulsetime);
  //delayMicroseconds(1600000);
  digitalWrite(11,LOW);
  //delayMicroseconds(1600000);
  //delay(PinReading);
  //srv.write(potentiometerValue);
  delay(1000);
}

