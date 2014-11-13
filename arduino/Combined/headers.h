#ifndef _HEADERS_H
#define _HEADERS_H

#include <DHT.h>
#define DHTTYPE DHT11

SoftwareSerial mySerial(12, 4);
Adafruit_GPS GPS(&mySerial);

void setupGPS();
void readGPSData();
void setupTempHumi();
void setupBPM();
void setupHall();

void setupButtons();
void readButtons();
void readTempHumi();
void readBPM();
void readHall();
#endif
