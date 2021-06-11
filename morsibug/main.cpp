#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define MORSIBUG_ID_YOU "morsibug1"
#define MORSIBUG_ID_FRIEND "morsibug2"

// WiFi network
const char* ssid     = "xxx";
const char* password = "xxx";

const char* mqttServer = "test.mosquitto.org";
const int mqttPort = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  if (((char)payload[0])=='1') {
    digitalWrite(D1,HIGH);
    digitalWrite(D0,HIGH);
  }
  if (((char)payload[0])=='0') {
    digitalWrite(D1,LOW);
    digitalWrite(D0,LOW);
  }
}

void connectMQTT() {
  while (!client.connected()) {
  Serial.println("connecting to MQTT Server...");
  if (client.connect(MORSIBUG_ID_YOU)) {
    Serial.println("Connected to MQTT Server");
  }
  else {
    Serial.print("failed with state ");
    Serial.print(client.state());
    delay(2000);
  }
}
  client.subscribe(MORSIBUG_ID_FRIEND);
  client.setCallback(callback);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(D4,OUTPUT); // output button
  pinMode(D3,INPUT_PULLUP); // input button
  pinMode(D1,OUTPUT); // output buzzer
  pinMode(D0,OUTPUT); // output led 
  Serial.begin(9600);
  digitalWrite(D4,LOW);

  // Connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password); // the program sets up the WiFi ssid and password using the WiFi.begin() function del ESP32 library.
 
  while (WiFi.status() != WL_CONNECTED) { // and the executes the WiFi.status() function to try to connect to WiFi Network. The program checks whether the WiFi.status() function returns a true value when its connect.
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  // when the ESP32 connects to WiFi network, the sketch displays a message, WiFi connected and the IP address of the ESP32 shows on the serial monitor.
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqttServer, mqttPort);
}

void loop() {
  client.loop();
  if (!client.connected()) {
    connectMQTT();
  }
  if (digitalRead(D3)==0) {
    client.publish(MORSIBUG_ID_YOU, "1");
  } else {
    client.publish(MORSIBUG_ID_YOU, "0");
  }
  delay(100);
}