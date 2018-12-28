#include <Arduino.h>
#include "AdafruitIO_WiFi.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Wire.h>
#include "TSL2561.h"
#include <Adafruit_BMP085.h>


#define DHTPIN            D6
#define DHTTYPE           DHT22

/************************ Adafruit IO Config *******************************/

// visit io.adafruit.com if you need to create an account,
// or if you need your Adafruit IO key.
#define IO_USERNAME    "xxxx"
#define IO_KEY         "xxxxxxxx"

/******************************* WIFI **************************************/

// the AdafruitIO_WiFi client will work with the following boards:
//   - HUZZAH ESP8266 Breakout -> https://www.adafruit.com/products/2471
//   - Feather HUZZAH ESP8266 -> https://www.adafruit.com/products/2821
//   - Feather HUZZAH ESP32 -> https://www.adafruit.com/product/3405
//   - Feather M0 WiFi -> https://www.adafruit.com/products/3010
//   - Feather WICED -> https://www.adafruit.com/products/3056

#define WIFI_SSID       "xxxxx"
#define WIFI_PASS       "xxxxxxx"


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


DHT_Unified dht(DHTPIN, DHTTYPE);

// set up the 'counter' feed
AdafruitIO_Feed *adafruit_humitat = io.feed("humitat");
AdafruitIO_Feed *adafruit_temperatura = io.feed("temperatura");
AdafruitIO_Feed *adafruit_pressio = io.feed("pressio");
AdafruitIO_Feed *adafruit_llum = io.feed("llum");

TSL2561 tsl(TSL2561_ADDR_FLOAT);

Adafruit_BMP085 bmp;

float pressio;

int timecount = 0;


void setup() {

  // start the serial connection
  Serial.begin(9600);

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

  // You can change the gain on the fly, to adapt to brighter/dimmer light situations
  //tsl.setGain(TSL2561_GAIN_0X);         // set no gain (for bright situtations)
  tsl.setGain(TSL2561_GAIN_16X);      // set 16x gain (for dim situations)

  // Changing the integration time gives you a longer time over which to sense light
  // longer timelines are slower, but are good in very low light situtations!
  tsl.setTiming(TSL2561_INTEGRATIONTIME_13MS);  // shortest integration time (bright light)
  //tsl.setTiming(TSL2561_INTEGRATIONTIME_101MS);  // medium integration time (medium light)
  //tsl.setTiming(TSL2561_INTEGRATIONTIME_402MS);  // longest integration time (dim light)

  // Now we're ready to get readings!

  if (!bmp.begin()) {
	Serial.println("Could not find a valid BMP085 sensor, check wiring!");
	while (1) {}
  }


}

void loop() {

  // io.run(); is required for all sketches.
  // it should always be present at the top of your loop
  // function. it keeps the client connected to
  // io.adafruit.com, and processes any incoming data.
  io.run();



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

  delay(10000);

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

  delay(10000);

  // Simple data read example. Just read the infrared, fullspecrtrum diode
  // or 'visible' (difference between the two) channels.
  // This can take 13-402 milliseconds! Uncomment whichever of the following you want to read
  //uint16_t x = tsl.getLuminosity(TSL2561_VISIBLE);
  //uint16_t x = tsl.getLuminosity(TSL2561_FULLSPECTRUM);
  //uint16_t x = tsl.getLuminosity(TSL2561_INFRARED);

  //Serial.println(x, DEC);

  // More advanced data read example. Read 32 bits with top 16 bits IR, bottom 16 bits full spectrum
  // That way you can do whatever math and comparisons you want!
  uint32_t lum = tsl.getFullLuminosity();
  uint16_t ir, full;
  ir = lum >> 16;
  full = lum & 0xFFFF;
  //Serial.print("IR: "); Serial.print(ir);   Serial.print("\t\t");
  Serial.print("Full: "); Serial.println(full);
  //Serial.print("Visible: "); Serial.print(full - ir);   Serial.print("\t");

  //Serial.print("Lux: "); Serial.println(tsl.calculateLux(full, ir));
  adafruit_llum->save(full);

  delay(10000);

  // Adafruit IO is rate limited for publishing, so a delay is required in
  // between feed->save events. In this example, we will wait three seconds
  // (1000 milliseconds == 1 second) during each loop.

  Serial.print("Pressure = ");
  pressio = (float) bmp.readPressure() / (float) 100 ;
  Serial.print(pressio);
  Serial.println(" HPa");
  if (pressio < 1100.0 && pressio > 880.0) { adafruit_pressio->save(pressio); }

  delay(10000);

  timecount++; // increases every 40 seconds
  if (timecount==500) { ESP.reset(); } // reset ESP every 20000sec (5h:30m)

}

