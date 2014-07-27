#include <SD.h>
#include <SPI.h>
#include <TFT.h>
#include "DHT.h"

#define DHTPIN 2     // what pin we're connected to


#define DHTTYPE DHT11   // DHT 11 


#define cs   10
#define dc   9
#define rst  8  

File dataFile;
const int chipSelect = 4;
TFT TFTscreen = TFT(cs, dc, rst);
char tempSensorPrintout[6];
char hSensorPrintout[7];
char lightSensorPrintout[11];
int step=0;
int temperaturePin = 0;
int lightPin = 1;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  // SD Card setup
  //Serial.print("Initializing SD card...");
  //pinMode(cs, OUTPUT);

  //if (!SD.begin(chipSelect)) {
  //  Serial.println("Initialization failed!");
  //  return;
  //}
  //Serial.println("Initialization done.");
  dht.begin();
  // TFT Screen setup
  TFTscreen.begin();
  TFTscreen.background(0, 0, 0);
  TFTscreen.stroke(255,20,20);
  TFTscreen.setTextSize(2);
  TFTscreen.text("Temperature: ",0,0);
  TFTscreen.text("Light: ",0,40);
  TFTscreen.text("Humidity: ",0,80);
  TFTscreen.setTextSize(2);
  
}
void loop() {
  int lightLevel=analogRead(lightPin); 
  lightLevel = map(lightLevel,0,900,0,500);
  lightLevel = constrain(lightLevel,0,500);
  float h = dht.readHumidity();
  float temp=getVoltage(temperaturePin);
  temp=((temp - .5) *100);
  String tempSensorVal = String(temp);
  String lightSensorVal="";
  String hSensorVal= String(h);
  tempSensorVal.toCharArray(tempSensorPrintout, 6);
  hSensorVal.toCharArray(hSensorPrintout,6);
  tempSensorPrintout[strlen(tempSensorPrintout)-1]=0; // remove second decimal from temp
  strcat(tempSensorPrintout,"c");
  strcat(hSensorPrintout,"%");
  Serial.print("Humidity: "); 
  Serial.print(h);
  if (lightLevel>=0 && lightLevel<100) { lightSensorVal="Very Low"; }
  if (lightLevel>=100 && lightLevel<200) { lightSensorVal="Low"; }
  if (lightLevel>=200 && lightLevel<300) { lightSensorVal="Medium"; }
  if (lightLevel>=300 && lightLevel<400) { lightSensorVal="High"; }
  if (lightLevel>=400 && lightLevel<=500) { lightSensorVal="Very High"; }
  lightSensorVal.toCharArray(lightSensorPrintout,11);
  // so you have to close this one before opening another.
  //dataFile = SD.open("dtasens.csv", FILE_WRITE);
  // if the file is available, write to it:
  /*if (dataFile) {
    step++;
    if (step==1) { dataFile.println("****DATA BEGIN****"); }
    dataFile.print(step);
    dataFile.print(";");
    dataFile.print(temp);
    dataFile.print(";");
    dataFile.print(lightLevel);
    dataFile.println(";");
    dataFile.close();
    // print to the serial port too:
    Serial.print(step);
    Serial.print(";");
    Serial.print(temp);
    Serial.print(";");
    Serial.print(lightLevel);
    Serial.println(";");
  }  
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening dtasens.csv");
  } */
  TFTscreen.stroke(20,255,20);
  TFTscreen.text(tempSensorPrintout, 0, 20);
  TFTscreen.text(lightSensorPrintout, 0, 60);
  TFTscreen.text(hSensorPrintout,0,100);
  delay(2000); // one data input every second
  TFTscreen.stroke(0,0,0);
  TFTscreen.text(tempSensorPrintout, 0, 20);
  TFTscreen.text(lightSensorPrintout, 0, 60);
  TFTscreen.text(hSensorPrintout,0,100);
  
}

float getVoltage(int pin) {
  return (analogRead(pin) * 0.00482814);
}

