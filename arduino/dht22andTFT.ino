// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"
#include <SPI.h>
#include <TFT.h>

#define DHTPIN 9     // what pin we're connected to



// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

#define CS   6
#define DC   7
#define RESET  8


DHT dht(DHTPIN, DHTTYPE);

int lightPin=2;

TFT TFTscreen = TFT(CS, DC, RESET);

char tempSensorPrintout[6];
char hSensorPrintout[7];
char lightSensorPrintout[11];



void setup() {
  Serial.begin(9600); 
  Serial.println("DHT22 humidity and temperature sensor + light photo resistor.");
 
  dht.begin();
  
  // TFT Screen setup
TFTscreen.begin();
TFTscreen.background(0, 0, 0);
TFTscreen.stroke(255,20,20);
TFTscreen.setTextSize(1);
TFTscreen.text("Temperature (c): ",0,0);
TFTscreen.text("Light (0-10): ",0,40);
TFTscreen.text("Humidity (%): ",0,80);
TFTscreen.setTextSize(1);
  
}

void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  int lightLevel= analogRead(lightPin);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  lightLevel=map(lightLevel,0,900,0,10);
  lightLevel= constrain(lightLevel,0,10);
  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT");
  } else {
    Serial.print("Humidity: "); 
    Serial.print(h);
    Serial.println("%");
    Serial.print("Temperature: "); 
    Serial.print(t);
    Serial.println("c");
    Serial.print("Light Level (0-10): ");
    Serial.println(lightLevel);
    String tempSensorVal = String(t);
    String hSensorVal= String(h);
    String lightSensorVal= String(lightLevel);
    tempSensorVal.toCharArray(tempSensorPrintout, 6);
    hSensorVal.toCharArray(hSensorPrintout,6);
    lightSensorVal.toCharArray(lightSensorPrintout,3);
    TFTscreen.stroke(20,255,20);
    TFTscreen.text(tempSensorPrintout, 0, 20);
    TFTscreen.text(lightSensorPrintout, 0, 60);
    TFTscreen.text(hSensorPrintout,0,100);
    delay(1000);
    TFTscreen.stroke(0,0,0);
    TFTscreen.text(tempSensorPrintout, 0, 20);
    TFTscreen.text(lightSensorPrintout, 0, 60);
    TFTscreen.text(hSensorPrintout,0,100);
  }
}
