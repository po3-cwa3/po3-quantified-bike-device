// NOG NIET AF!!!


/*
Om de library te installeren, heb je de file DHT11.zip nodig.
Deze is te vinden op https://drive.google.com/uc?export=download&id=0B3L4pZE60Jv0SzRsTTMxZGZNblU
Klik nu in het arduinoprogramma op Sketch -> Import Library... -> Add Library...
Vind de zip-file en voeg deze toe.
Herstart nu het arduinoprogramma om de library volledig in te laden.

Dezelfde methode is nodig om de library van de GPS-module te installeren. Deze files zijn te vinden op https://github.com/adafruit/Adafruit-GPS-Library
*/
//De GPS zit op pin 2 en pin 3, de TempHumi-sensor zit op pin 4, de Button op pin 5

#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
#include <DHT11.h>
const int TempHumiPin=4;
const int ButtonPin = 5;
int i=0;
int buttonState=0;
DHT11 dht11(TempHumiPin);

// Connect the GPS Power pin to 5V
// Connect the GPS Ground pin to ground
// Connect the GPS TX (transmit) pin to Digital 3
// Connect the GPS RX (receive) pin to Digital 2
// Wiring image can be found here: https://learn.adafruit.com/adafruit-ultimate-gps/arduino-wiring

// Change the pin numbers to match your wiring
SoftwareSerial mySerial(3, 2);
Adafruit_GPS GPS(&mySerial);
boolean usingInterrupt = false;
void useInterrupt(boolean);

void setup(){
  Serial.begin(115200);
  while (!Serial){;}
  pinMode(ButtonPin, INPUT);
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  useInterrupt(true);
}

SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
}

void useInterrupt(boolean v) {
  if (v) {
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } else {
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}

uint32_t timer = millis();
void loop(){
  if (GPS.newNMEAreceived()){
    if (!GPS.parse(GPS.lastNMEA())){
      return;
    }
  }
  if (timer > millis())  timer = millis();
  
  if (i%100==0){
    int err;
    float temp, humi;
    if((err=dht11.read(humi, temp))==0)
    {
      Serial.print("th;");
      Serial.print(temp);
      Serial.print(";");
      Serial.print(humi);
      Serial.print(";");
      Serial.println();
    }else{
      Serial.println();
      Serial.print("Error No :");
      Serial.print(err);
      Serial.println();    
    }
  }
  buttonState = digitalRead(ButtonPin);
  if (buttonState == LOW) {
    Serial.println("pb;1;");
  }else{
    Serial.println("pb;0;");
  }
  if (i%100==0){
    if (millis() - timer > 2000) {
      if (GPS.fix){
        timer = millis();
        Serial.print("gps;");
        Serial.print(GPS.hour, DEC); Serial.print(':');
        Serial.print(GPS.minute, DEC); Serial.print(':');
        Serial.print(GPS.seconds, DEC); Serial.print('.');
        Serial.print(GPS.milliseconds);
        Serial.print(';');
        Serial.print(GPS.day, DEC); Serial.print('/');
        Serial.print(GPS.month, DEC); Serial.print("/20");
        Serial.print(GPS.year, DEC);
        Serial.print(';');
        Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
        Serial.print(";"); 
        Serial.print(GPS.longitude, 4); Serial.print(GPS.lon);
        Serial.print(';');
        Serial.println(GPS.speed);
        Serial.print(';');
        Serial.println(GPS.angle);
        Serial.print(';');
        Serial.println(GPS.altitude);
        Serial.print(';');
        //Serial.println((int)GPS.satellites);
        //Serial.print(';');
      }
    }
  }
  delay(10);
  i++;
}
