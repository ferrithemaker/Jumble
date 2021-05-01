#include <Arduino.h>
// Copyright 2015 chaeplin
// Copyright 2017 xpokor22
// This is based on:
// https://github.com/z3t0/Arduino-IRremote/blob/master/examples/LGACSendDemo/LGACSendDemo.ino

#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <PubSubClient.h>
#include <ESP8266WiFi.h>

const char* ssid = "";
const char* password = "";
const char* mqtt_server = "";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


IRsend irsend(14);  // An IR LED is controlled by GPIO pin 14 (D5)

// 0 : TOWER
// 1 : WALL
const unsigned int kAc_Type  = 1;

// 0 : cooling
// 1 : heating
unsigned int ac_heat = 1;

// 0 : off
// 1 : on
unsigned int ac_power_on = 0;

// 0 : off
// 1 : on --> power on
unsigned int ac_air_clean_state = 0;

// temperature : 18 ~ 30
unsigned int ac_temperature = 24;

// 0 : low
// 1 : mid
// 2 : high
// if kAc_Type = 1, 3 : change
unsigned int ac_flow = 1;

const uint8_t kAc_Flow_Tower[3] = {0, 4, 6};
const uint8_t kAc_Flow_Wall[4] = {0, 2, 4, 5};

uint32_t ac_code_to_sent;

void Ac_Send_Code(uint32_t code) {
  Serial.print("code to send : ");
  Serial.print(code, BIN);
  Serial.print(" : ");
  Serial.println(code, HEX);

#if SEND_LG
  irsend.sendLG(code, 28);
#else  // SEND_LG
  Serial.println("Can't send because SEND_LG has been disabled.");
#endif  // SEND_LG
}

void Ac_Activate(unsigned int temperature, unsigned int air_flow,
                 unsigned int heat) {
  ac_heat = heat;
  unsigned int ac_msbits1 = 8;
  unsigned int ac_msbits2 = 8;
  unsigned int ac_msbits3 = 0;
  unsigned int ac_msbits4;
  if (ac_heat == 1)
    ac_msbits4 = 4;  // heating
  else
    ac_msbits4 = 0;  // cooling
  unsigned int ac_msbits5 =  (temperature < 15) ? 0 : temperature - 15;
  unsigned int ac_msbits6 = 0;

  if (air_flow <= 2) {
    if (kAc_Type == 0)
      ac_msbits6 = kAc_Flow_Tower[air_flow];
    else
      ac_msbits6 = kAc_Flow_Wall[air_flow];
  }

  // calculating using other values
  unsigned int ac_msbits7 = (ac_msbits3 + ac_msbits4 + ac_msbits5 +
                             ac_msbits6) & B00001111;
  ac_code_to_sent = ac_msbits1 << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits2) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits3) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits4) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits5) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits6) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits7);

  Ac_Send_Code(ac_code_to_sent);

  ac_power_on = 1;
  ac_temperature = temperature;
  ac_flow = air_flow;
}

void Ac_Change_Air_Swing(int air_swing) {
  if (kAc_Type == 0) {
    if (air_swing == 1)
      ac_code_to_sent = 0x881316B;
    else
      ac_code_to_sent = 0x881317C;
  } else {
    if (air_swing == 1)
      ac_code_to_sent = 0x8813149;
    else
      ac_code_to_sent = 0x881315A;
  }
  Ac_Send_Code(ac_code_to_sent);
}

void Ac_Power_Down() {
  ac_code_to_sent = 0x88C0051;

  Ac_Send_Code(ac_code_to_sent);

  ac_power_on = 0;
}

void Ac_Air_Clean(int air_clean) {
  if (air_clean == '1')
    ac_code_to_sent = 0x88C000C;
  else
    ac_code_to_sent = 0x88C0084;

  Ac_Send_Code(ac_code_to_sent);

  ac_air_clean_state = air_clean;
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  // heating
  if ((char)payload[0] == '1') {
    Ac_Activate(ac_temperature, ac_flow, 1);
    Serial.println("Heat");
  }
  // stop
  if ((char)payload[0] == '2') {
    Ac_Power_Down();
    Serial.println("Off");
  }
  // cooling
  if ((char)payload[0] == '0') {
    Ac_Activate(ac_temperature, ac_flow, 0);
    Serial.println("Cool");
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("nodemcu-airspider", "", "")) {
      Serial.println("connected");
      client.subscribe("statusac");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void setup() {
  Serial.begin(9600);
  delay(1000);
  irsend.begin();
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  client.setServer(mqtt_server, 1883);
  
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
