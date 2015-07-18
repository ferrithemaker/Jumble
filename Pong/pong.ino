void setup() {
  pinMode(0,INPUT);
  pinMode(1,INPUT);  // Set pin 0 to be an input
  Serial.begin(9600);   // Start up serial communication at 9600 speed
}

void loop() {
  int readinga0 = analogRead(0);
  int readinga1 = analogRead(1);
  String sendstr=(String)readinga0+"|"+(String)readinga1;
  Serial.println(sendstr);
  delay(50);                      // Wait for a short time, just to slow things a little
}
