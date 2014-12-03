#include <DHT.h>
#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>

#include "headers.h"


/**
DP00:
DP01:
DP02: Hall sensor
DP03:
DP04: Software Serial GPS (TX)
DP05:
DP06:
DP07: Button 1
DP08: Temperature + Humidity Sensor
DP09:
DP10: Button 3
DP11:
DP12: Software Serial GPS (RX)
DP13:

AP00: Pulse sensor
AP01: Button 2
AP02: Device State multicolor led 1 (blue pin)
AP03: Device State multicolor led 1 (green pin)
AP04: Device State multicolor led 1 (red pin)
AP05:
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
  
