
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

// Variables for the GPS
// Configuration based on the examples in the Adafruit_GPS library
SoftwareSerial mySerial(3, 2);
Adafruit_GPS GPS(&mySerial);
#define GPS_UPDATE_INTERVAL 2000
// GPS interrupt
SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
}
void setupGPS(){
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);//Recommended minimum + fix data (including altitude)
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);//Update interval 1 Hz
  
  //configuration of interrupt
  OCR0A = 0xAF;
  TIMSK0 |= _BV(OCIE0A);
  mySerial.println(PMTK_Q_RELEASE);
}
uint32_t last_gps_data_time = millis();
//checks if new GPS data is available and processes it
void readGPSData(){
  if(GPS.newNMEAreceived()){ // is there new data available?
    if(!GPS.parse(GPS.lastNMEA())){ // can this data be parsed? (also sets newNMEAreceived to false)
      return;
    }
  }
  if(last_gps_data_time > millis()) last_gps_data_time = millis();
  if(millis()-last_gps_data_time < GPS_UPDATE_INTERVAL){
    return;
  }
  last_gps_data_time = millis();
  //TODO: insert timing information (see gps_test for examples)
  Serial.print("GPS;");
  //Do we really need time information?
  Serial.print(GPS.hour, DEC); Serial.print(":");
  Serial.print(GPS.minute, DEC); Serial.print(":");
  Serial.print(GPS.seconds, DEC); Serial.print(".");
  Serial.print(GPS.milliseconds); Serial.print(";");
  Serial.print(GPS.day, DEC); Serial.print("/");
  Serial.print(GPS.month, DEC); Serial.print("/");
  Serial.print(GPS.year, DEC); Serial.print(";");
  Serial.print(GPS.fixquality); Serial.print(";");
  if(GPS.fix){
    //Location data
    Serial.print(GPS.latitudeDegrees, 4); Serial.print(";");
    Serial.print(GPS.longitudeDegrees, 4); Serial.print(";");
    Serial.print(GPS.speed); Serial.print(";");
    Serial.print(GPS.altitude); Serial.print(";");
    Serial.print(GPS.satellites); Serial.println();
  }else{
    Serial.println("nofix");
  }
}

void setup(){
  Serial.begin(115200);
  setupGPS();
  delay(1000);
}

void loop(){
  //Serial.println("in loop");
  readGPSData();
}
  



