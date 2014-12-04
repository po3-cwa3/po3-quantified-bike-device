#include <DHT.h>
#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>

#include "headers.h"


/**
DP00:
DP01:
DP02: Hall sensor
DP03: Connection LED (LED 4)
DP04: Software Serial GPS (TX)
DP05: Active Trip LED (LED 1)
DP06: Picture Taking LED (LED 2, blue pin)
DP07: Button 1
DP08: Temperature + Humidity Sensor
DP09: Picture Taking LED (LED 2, green pin)
DP10: Button 3
DP11: Picture Taking LED (LED 2, red pin)
DP12: Software Serial GPS (RX)
DP13: Live vs Batch trips Button

AP00: Pulse sensor
AP01: Button 2
AP02: Device State multicolor LED (LED 3, blue pin)
AP03: Device State multicolor LED (LED 3, green pin)
AP04: Device State multicolor LED (LED 3, red pin)
AP05: Live vs Batch LED (LED 4)
**/

/*
Initializes all modules of the Arduino code
*/
void setup(){
  Serial.begin(115200);
  setupButtons();
  setupTempHumi();
  setupGPS();
  setupHall();
  setupBPM();
  setupStateHandler();
}
/*
Execute code for each of the modules.
*/
void loop(){
  readButtons();
  readGPSData();
  readTempHumi();
  readBPM();
  readHall();
  readState();
}
  
