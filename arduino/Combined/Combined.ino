#include <DHT.h>
#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>

#include "headers.h"
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
  
