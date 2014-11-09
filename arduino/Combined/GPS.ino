#include <Adafruit_GPS.h>

#include "headers.h"
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

// Variables for the GPS
// Configuration based on the examples in the Adafruit_GPS library
SoftwareSerial mySerial(12, 4);
Adafruit_GPS GPS(&mySerial);
#define GPS_UPDATE_INTERVAL 2000
// GPS interrupt
unsigned int current_value_gps = 0;
//uint32_t gps_time = 0;
SIGNAL(TIMER0_COMPB_vect) {
  //cli();
  //Serial.println(millis()-gps_time);
  //gps_time = millis();
  char c = GPS.read();
  ++current_value_gps;
  //Serial.print("gps:");
  //Serial.println(current_value_gps);
//  sei();
  digitalWrite(5, current_value_gps%100 > 50);
  //Serial.println(millis()-gps_time);
}

void setupGPS(){
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);//Recommended minimum + fix data (including altitude)
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);//Recommended minimum + fix data (including altitude)
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);//Update interval 1 Hz
  
  //configuration of interrupt
  //TCCR0A |= _BV(WGM01);
  //TCCR0B |= _BV(CS02);
  
  OCR0B = 0xAF;//compare value = 176
  TIMSK0 |= _BV(OCIE0B);//enable B
  //TIMSK0 &= ~_BV(OCIE0A);
  mySerial.println(PMTK_Q_RELEASE);
}
uint32_t last_gps_data_time = millis();
//checks if new GPS data is available and processes it
void readGPSData(){
  //Serial.println(millis());
  //char c = GPS.read();
  //Serial.print("c = ");Serial.println(c);
  if(GPS.newNMEAreceived()){ // is there new data available?
    //Serial.println("new data");
    if(!GPS.parse(GPS.lastNMEA())){ // can this data be parsed? (also sets newNMEAreceived to false)
      return;
    }
  }else{
  }
  if(last_gps_data_time > millis()) last_gps_data_time = millis();
  if(millis()-last_gps_data_time < GPS_UPDATE_INTERVAL){
    return;
  }
  last_gps_data_time = millis();
  //TODO: insert timing information (see gps_test for examples)
  Serial.print("GPS;");
  //Do we really need time information?
  /*Serial.print(GPS.hour, DEC); Serial.print(":");
  Serial.print(GPS.minute, DEC); Serial.print(":");
  Serial.print(GPS.seconds, DEC); Serial.print(".");
  Serial.print(GPS.milliseconds); Serial.print(";");
  Serial.print(GPS.day, DEC); Serial.print("/");
  Serial.print(GPS.month, DEC); Serial.print("/");
  Serial.print(GPS.year, DEC); Serial.print(";");
  Serial.print(GPS.fixquality); Serial.print(";");*/
  if(GPS.fix){
    //Location data
    Serial.print(GPS.latitudeDegrees, 8); Serial.print(";");
    Serial.print(GPS.longitudeDegrees, 8); Serial.print(";");
    Serial.print(GPS.speed); Serial.print(";");
    Serial.print(GPS.altitude); Serial.print(";");
    Serial.print(GPS.satellites); Serial.println();
  }else{
    Serial.println("nofix");
  }
}
