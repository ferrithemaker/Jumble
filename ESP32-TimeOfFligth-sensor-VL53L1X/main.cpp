#include <Arduino.h>
#include <ESP32Servo.h>

// lifebox new controller testing

/*
This example shows how to take simple range measurements with the VL53L1X. The
range readings are in units of mm.
*/

#include <Wire.h>
#include <VL53L1X.h> // PlatformIO VL53L1X library by pololu

VL53L1X sensor;


Servo myservo;  // create servo object to control a servo
// 16 servo objects can be created on the ESP32

int pos = 20;    // variable to store the servo position
// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33 
int servoPin = 25;


void setup()
{
  Serial.begin(115200);
  //Wire.begin(); // for heltec
  Wire.begin(23,22); // for TTGO - WROOM32 ESP32

	// platform.ini for TTGO - WROOM32

	//[env:nodemcu-32s]
	//platform = espressif32
	//board = nodemcu-32s
	//framework = arduino
	//monitor_speed = 115200

	// platform.ini for HELTEC LORA - WIFI

	//[env:heltec_wifi_lora_32]
	//platform = espressif32
	//board = heltec_wifi_lora_32
	//framework = arduino
	//monitor_speed = 115200
  
  Wire.setClock(400000); // use 400 kHz I2C

  sensor.setTimeout(500);
  if (!sensor.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
    while (1);
  }
  
  // Use long distance mode and allow up to 50000 us (50 ms) for a measurement.
  // You can change these settings to adjust the performance of the sensor, but
  // the minimum timing budget is 20 ms for short distance mode and 33 ms for
  // medium and long distance modes. See the VL53L1X datasheet for more
  // information on range and timing limits.
  sensor.setDistanceMode(VL53L1X::Long);
  sensor.setMeasurementTimingBudget(50000);

  // Start continuous readings at a rate of one measurement every 50 ms (the
  // inter-measurement period). This period should be at least as long as the
  // timing budget.
  sensor.startContinuous(50);

  // Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50);    // standard 50 hz servo
	myservo.attach(servoPin, 1000, 2000);
}

void loop() {
myservo.write(pos);
pos = pos + 60;
if (pos>180) { pos = 20; }
Serial.print(sensor.read());
if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }

Serial.println();

delay(500);
}
