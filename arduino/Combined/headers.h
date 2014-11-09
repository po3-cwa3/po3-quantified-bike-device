#ifndef _HEADERS_H
#define _HEADERS_H

#include <DHT.h>
#define DHTTYPE DHT11

void setupGPS();
void readGPSData();
void setupTempHumi();
void setupBPM();

void setupButtons();
void readButtons();
void readTempHumi();
void readBPM();
#endif
