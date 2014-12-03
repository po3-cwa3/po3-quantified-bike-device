#include <DHT.h>
#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>

#include "headers.h"


/**
DP00: Hall sensor
DP01:
DP02:
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
void setup(){
  Serial.begin(115200);
  setupButtons();
  setupTempHumi();
  setupGPS();
  setupHall();
  setupBPM();
  setupStateHandler();
  //digitalWrite(9, LOW);
  //delay(1000);
}
void loop(){
  //Serial.println("in loop");
  readButtons();
  readGPSData();
  readTempHumi();
  readBPM();
  readHall();
  readState();
  //delay(1);
}
  
