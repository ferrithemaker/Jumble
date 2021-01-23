#include <Arduino.h>
#include <SPI.h>
#include "AdafruitIO_WiFi.h"
#include <Adafruit_Sensor.h>
#include <DHT_U.h>
#include <Wire.h>
#include <Adafruit_TSL2561_U.h>
#include <Adafruit_BMP085.h>
#include "ccs811.h"  // CCS811 library
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library


// For the breakout, you can use any 2 or 3 pins
// These pins will also work for the 1.8" TFT shield
// ST7735 TFT module connections
#define TFT_RST   D4     // TFT RST pin is connected to NodeMCU pin D4 (GPIO2)
#define TFT_CS    D3     // TFT CS  pin is connected to NodeMCU pin D3 (GPIO0)
#define TFT_DC    D0     // TFT DC  pin is connected to NodeMCU pin D2 (GPIO4)

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS,  TFT_DC, TFT_RST);


CCS811 ccs811; 


#define DHTPIN            D6
#define DHTTYPE           DHT22


/************************ Adafruit IO Config *******************************/

// visit io.adafruit.com if you need to create an account,
// or if you need your Adafruit IO key.
#define IO_USERNAME    "xxxx"
#define IO_KEY         "xxxx"

/******************************* WIFI **************************************/

// the AdafruitIO_WiFi client will work with the following boards:
//   - HUZZAH ESP8266 Breakout -> https://www.adafruit.com/products/2471
//   - Feather HUZZAH ESP8266 -> https://www.adafruit.com/products/2821
//   - Feather HUZZAH ESP32 -> https://www.adafruit.com/product/3405
//   - Feather M0 WiFi -> https://www.adafruit.com/products/3010
//   - Feather WICED -> https://www.adafruit.com/products/3056

#define WIFI_SSID       "xxxx"
#define WIFI_PASS       "xxxx"

// Instantiation and pins configurations

// comment out the following two lines if you are using fona or ethernet
AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS);

// Adafruit IO Publish Example
//
// Adafruit invests time and resources providing this open source code.
// Please support Adafruit and open source hardware by purchasing
// products from Adafruit!
//
// Written by Todd Treece for Adafruit Industries
// Copyright (c) 2016 Adafruit Industries
// Licensed under the MIT license.
//
// All text above must be included in any redistribution.


/************************ Example Starts Here *******************************/


// set up the 'counter' feed
AdafruitIO_Feed *adafruit_humitat = io.feed("humitat");
AdafruitIO_Feed *adafruit_temperatura = io.feed("temperatura");
AdafruitIO_Feed *adafruit_pressio = io.feed("pressio");
AdafruitIO_Feed *adafruit_llum = io.feed("llum");
AdafruitIO_Feed *adafruit_vocs = io.feed("VOCs");
AdafruitIO_Feed *adafruit_eco2 = io.feed("eCO2");

//TSL2561 tsl(TSL2561_ADDR_FLOAT);

Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);

Adafruit_BMP085 bmp;

DHT_Unified dht(DHTPIN, DHTTYPE);

float pressio;
float temperatura;

int timecount = 0;


void setup() {

  // start the serial connection
  Serial.begin(9600);

  Serial.println("setup: Starting CCS811 basic demo");
  Serial.print("setup: ccs811 lib  version: "); Serial.println(CCS811_VERSION);

  Wire.begin(); 
  
  // Enable CCS811
  ccs811.set_i2cdelay(50); // Needed for ESP8266 because it doesn't handle I2C clock stretch correctly
  bool ok= ccs811.begin();
  if( !ok ) Serial.println("setup: CCS811 begin FAILED");

  // Print CCS811 versions
  Serial.print("setup: hardware    version: "); Serial.println(ccs811.hardware_version(),HEX);
  Serial.print("setup: bootloader  version: "); Serial.println(ccs811.bootloader_version(),HEX);
  Serial.print("setup: application version: "); Serial.println(ccs811.application_version(),HEX);
  
  // Start measuring
  ok= ccs811.start(CCS811_MODE_1SEC);
  if( !ok ) Serial.println("setup: CCS811 start FAILED");

  


  //tm1637.init();
  //tm1637.set(BRIGHT_TYPICAL);//BRIGHT_TYPICAL = 2,BRIGHT_DARKEST = 0,BRIGHTEST = 7;

  dht.begin();

  Serial.println("DHTxx Unified Sensor Example");
  // Print temperature sensor details.

  // wait for serial monitor to open
  while(! Serial);

  Serial.print("Connecting to Adafruit IO");

  // connect to io.adafruit.com
  io.connect();

  // wait for a connection
  while(io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  // we are connected
  Serial.println();
  Serial.println(io.statusText());

  if (tsl.begin()) {
    Serial.println("Found light sensor");
  } else {
    Serial.println("No light sensor?");
    while (1);
  }


  tsl.enableAutoRange(true);            /* Auto-gain ... switches automatically between 1x and 16x */
  
  /* Changing the integration time gives you better sensor resolution (402ms = 16-bit data) */
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);      /* fast but low resolution */


  if (!bmp.begin()) {
	  Serial.println("Could not find a valid BMP085 sensor, check wiring!");
	  while (1) {}
  }

  // tft setup
  tft.initR(INITR_BLACKTAB);     // initialize a ST7735S chip, black tab
  tft.setRotation(1);

}

void loop() {

  // io.run(); is required for all sketches.
  // it should always be present at the top of your loop
  // function. it keeps the client connected to
  // io.adafruit.com, and processes any incoming data.
  io.run();

  //tm1637.display(0,1);
  //tm1637.point(POINT_ON);
  //tm1637.display(1,2);
  //tm1637.point(POINT_OFF);



  delay(5000);

  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println("Error reading temperature!");
  }
  else {
    Serial.print("Temperature: ");
    Serial.print(event.temperature);
    Serial.println(" *C");
    adafruit_temperatura->save(event.temperature);
  }



  delay(5000);

  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println("Error reading humidity!");
  }
  else {
    Serial.print("Humidity: ");
    Serial.print(event.relative_humidity);
    Serial.println("%");
    adafruit_humitat->save(event.relative_humidity);
  }

  delay(5000);

  sensors_event_t l_event;
  tsl.getEvent(&l_event);
 
  /* Display the results (light is measured in lux) */
  if (l_event.light)
  {
    Serial.print(l_event.light); Serial.println(" lux");
    adafruit_llum->save(l_event.light);
  }

  delay(5000);

  // Adafruit IO is rate limited for publishing, so a delay is required in
  // between feed->save events. In this example, we will wait three seconds
  // (1000 milliseconds == 1 second) during each loop.

  Serial.print("Pressure = ");
  pressio = (float) bmp.readPressure() / (float) 100 ;
  Serial.print(pressio);
  Serial.println(" HPa");
  if (pressio < 1100.0 && pressio > 880.0) { adafruit_pressio->save(pressio); }

  delay(5000);

  temperatura = (float) bmp.readTemperature();
  Serial.print(temperatura);
  Serial.println("C");

  uint16_t eco2, etvoc, errstat, raw;
  ccs811.read(&eco2,&etvoc,&errstat,&raw); 
  
  // Print measurement results based on status
  if( errstat==CCS811_ERRSTAT_OK ) { 
    Serial.print("CCS811: ");
    Serial.print("eco2=");  Serial.print(eco2);     Serial.print(" ppm  ");
    adafruit_eco2->save(eco2);
    delay(5000);
    Serial.print("etvoc="); Serial.print(etvoc);    Serial.print(" ppb  ");
    adafruit_vocs->save(etvoc);
    delay(5000);
    //Serial.print("raw6=");  Serial.print(raw/1024); Serial.print(" uA  "); 
    //Serial.print("raw10="); Serial.print(raw%1024); Serial.print(" ADC  ");
    //Serial.print("R="); Serial.print((1650*1000L/1023)*(raw%1024)/(raw/1024)); Serial.print(" ohm");
    Serial.println();
  } else if( errstat==CCS811_ERRSTAT_OK_NODATA ) {
    Serial.println("CCS811: waiting for (new) data");
  } else if( errstat & CCS811_ERRSTAT_I2CFAIL ) { 
    Serial.println("CCS811: I2C error");
  } else {
    Serial.print("CCS811: errstat="); Serial.print(errstat,HEX); 
    Serial.print("="); Serial.println( ccs811.errstat_str(errstat) ); 
  }

  delay(5000);

  // print info on TFT screen

  tft.fillScreen(ST7735_BLACK);  // fill screen with black color
  tft.setTextSize(2);                                   // text size = 2
  tft.setTextColor(ST7735_BLUE, ST7735_BLACK);       // set text color to magenta and black background
  tft.setCursor(0,10);                              
  tft.print("Tmp C:");
  tft.setTextColor(ST7735_RED, ST7735_BLACK);
  tft.setCursor(80,10);
  tft.print(temperatura);
  tft.setTextColor(ST7735_BLUE, ST7735_BLACK);
  tft.setCursor(0,30);
  tft.print("Hum %:");
  tft.setCursor(80,30);                             
  tft.setTextColor(ST7735_RED, ST7735_BLACK);
  tft.print(event.relative_humidity);
  tft.setCursor(0,50);
  tft.setTextColor(ST7735_BLUE, ST7735_BLACK);
  tft.print("HPa:");
  tft.setCursor(55,50);                             
  tft.setTextColor(ST7735_RED, ST7735_BLACK);
  tft.print(pressio);
  tft.setCursor(0,70);
  tft.setTextColor(ST7735_BLUE, ST7735_BLACK);
  tft.print("Lux:");
  tft.setCursor(55,70);                            
  tft.setTextColor(ST7735_RED, ST7735_BLACK);
  tft.print(int(l_event.light));
  tft.setCursor(0,90);
  tft.setTextColor(ST7735_BLUE, ST7735_BLACK);
  tft.print("CO2:");
  tft.setCursor(120,90);
  tft.print("ppm");
  tft.setCursor(55,90);                            
  tft.setTextColor(ST7735_RED, ST7735_BLACK);
  tft.print(eco2);
  tft.setCursor(0,110);
  tft.setTextColor(ST7735_BLUE, ST7735_BLACK);
  tft.print("VOc:");
  tft.setCursor(120,110);
  tft.print("ppm");
  tft.setCursor(55,110);                             
  tft.setTextColor(ST7735_RED, ST7735_BLACK);
  tft.print(etvoc);

  

  timecount++; // increases every 40 seconds
  if (timecount==500) { ESP.reset(); } // reset ESP every 20000sec (5h:30m)

}
