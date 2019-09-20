// by Ray Burnette 20161013 compiled on Linux 16.3 using Arduino 1.6.12
//Hacked by Kosme 20170520 compiled on Ubuntu 14.04 using Arduino 1.6.11

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "./functions.h"

#define disable 0
#define enable  1
unsigned int channel = 1;
unsigned long lastchange;
unsigned long timer;
bool sniffing = true;

const char* ssid     = "xxx";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "xxx";

const char* mqttServer = "xxx";
const int mqttPort = 1883;
const char* mqttUser = "xxx";
const char* mqttPassword = "xxx";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(57600);
  Serial.printf("\n\nSDK version:%s\n\r", system_get_sdk_version());
  Serial.println(F("ESP8266 enhanced sniffer by Kosme https://github.com/kosme"));
  enablesniffer();
}

void loop() {
  timer = millis();
  if (timer-lastchange>10000) {
    if (sniffing == true) {
      enablesender();
      sniffing = false;
    } else {
      enablesniffer();
      sniffing = true;
    }
  }
  if (sniffing == true) {
    channel = 1;
    wifi_set_channel(channel);
    while (true) {
      nothing_new++;                          // Array is not finite, check bounds and adjust if required
      if (nothing_new > 100) {
        nothing_new = 0;
        channel++;
        if (channel == 15) break;             // Only scan channels 1 to 14
          wifi_set_channel(channel);
        }
      delay(1);  // critical processing timeslice for NONOS SDK! No delay(0) yield()
    }
  }
}


void enablesniffer() {
  wifi_set_opmode(STATION_MODE);            // Promiscuous works only with station mode
  wifi_set_channel(channel);
  // Send the IP address of the ESP8266 to the computer
  wifi_promiscuous_enable(disable);
  wifi_set_promiscuous_rx_cb(promisc_cb);   // Set up promiscuous callback
  wifi_promiscuous_enable(enable);
  lastchange = millis();
}

void enablesender() {
  wifi_promiscuous_enable(disable);
  WiFi.begin(ssid, password);             // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(ssid); 
  Serial.println(" ...");
  int i = 0;
  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(1000);
    Serial.print(++i); 
    Serial.print(' ');
  }

  Serial.println('\n');
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
  
  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
 
  client.publish("esp/test", "Hello from ESP8266");
   
  lastchange = millis(); 
}
