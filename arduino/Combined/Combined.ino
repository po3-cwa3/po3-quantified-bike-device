#include <DHT.h>
#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>

#include "headers.h"
void setup(){
  Serial.begin(115200);
  setupButtons();
  setupTempHumi();
  setupBPM();
  setupGPS();
  delay(1000);
}
void loop(){
  //readButtons();
  readGPSData();
  readTempHumi();
  readBPM();
  //delay(100);
}
  
