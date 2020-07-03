#include <Arduino.h>
#include <BLEDevice.h>
#include <Adafruit_Sensor.h>
#include <DHT_U.h>
#include <Wire.h>
#include "heltec.h"
#include "string.h"
#include <TTN_esp32.h>
#include "TTN_CayenneLPP.h"


/***************************************************************************
 *  Go to your TTN console register a device then the copy fields
 *  and replace the CHANGE_ME strings below
 ****************************************************************************/
const char* devAddr = ""; // Change to TTN Device Address
const char* nwkSKey = ""; // Change to TTN Network Session Key
const char* appSKey = ""; // Change to TTN Application Session Key

TTN_esp32 ttn ;
TTN_CayenneLPP lpp;

#define DHTPIN            23
#define DHTTYPE           DHT11



DHT_Unified dht(DHTPIN, DHTTYPE);

void message(const uint8_t* payload, size_t size, int rssi)
{
    Serial.println("-- MESSAGE");
    Serial.print("Received " + String(size) + " bytes RSSI= " + String(rssi) + "dB");

    for (int i = 0; i < size; i++)
    {
        Serial.print(" " + String(payload[i]));
        // Serial.write(payload[i]);
    }

    Serial.println();
}

void setup() {

  // start the serial connection
  //Serial.begin(9600);

  //Heltec.begin(true /*DisplayEnable Enable*/, false /*LoRa Disable*/, true /*Serial Enable*/);
  Heltec.begin(true /*DisplayEnable Enable*/, false /*Heltec.LoRa Disable*/, true /*Serial Enable*/);


  dht.begin();

  Serial.println("DHTxx Unified Sensor Example");

  Serial.println("Starting");
  ttn.begin();
  ttn.onMessage(message); // declare callback function when is downlink from server
  ttn.personalize(devAddr, nwkSKey, appSKey);
  ttn.showStatus();
}

void loop() {

  sensors_event_t event;
  Heltec.display->clear();
  Heltec.display->setTextAlignment(TEXT_ALIGN_LEFT);
  Heltec.display->setFont(ArialMT_Plain_10);

  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println("Error reading humidity!");
  }
  else {
    Serial.print("Humidity: ");
    Serial.print(event.relative_humidity);
    Serial.println("%");
    Heltec.display->drawString(0, 0,"Humedad:");
    Heltec.display->drawString(76,0,(String)event.relative_humidity);
    Heltec.display->drawString(106,0," %");
    lpp.reset();
    lpp.addRelativeHumidity(0,(float)event.relative_humidity);
    if (ttn.sendBytes(lpp.getBuffer(), lpp.getSize()))
    {
        Serial.printf("Humidity: %f TTN_CayenneLPP: %d %x %02X%02X\n", (float)event.relative_humidity, lpp.getBuffer()[0], lpp.getBuffer()[1],
            lpp.getBuffer()[2], lpp.getBuffer()[3]);
    }
  }
  Heltec.display->display();
 
  delay(10000);
  
}
