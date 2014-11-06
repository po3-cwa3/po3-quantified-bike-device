/*
DHT-library: https://github.com/adafruit/DHT-sensor-library
Klik nu in het arduinoprogramma op Sketch -> Import Library... -> Add Library...
Vind de zip-file en voeg deze toe.
Herstart nu het arduinoprogramma om de library volledig in te laden.
De TempHumi-sensor zit op pin 8, de Button op pin 7, puls sensor op pin 0.
Voor code puls sensor (en referenties) zie BPM.ino.
*/

#include <DHT.h>
#define DHTTYPE DHT11

// VARIABLES
const int TempHumiPin = 8;
const int ButtonPin = 7;

int i = 0;
int buttonState = 0;
int pulsePin = 0;
int blinkPin = 13;
int fadePin = 5;
int fadeRate = 0;
int BPM;

volatile int Signal;
volatile int IBI = 600;
volatile boolean Pulse = false;
volatile boolean QS = false;

DHT dht(TempHumiPin, DHTTYPE);

void setup(){
  Serial.begin(115200);
  dht.begin();
  while (!Serial){;}
  pinMode(ButtonPin, INPUT);
  interruptSetup();
  }

void loop(){
  if (i%100==0){
      Serial.print("th;");
      Serial.print(dht.readTemperature());
      Serial.print(";");
      Serial.print(dht.readHumidity());
      Serial.print(";");
      Serial.println();
  }
  buttonState = digitalRead(ButtonPin);
  if (buttonState == LOW) {
      Serial.println("pb1;1;");
    }else{
      Serial.println("pb1;0;");
    }
  if (QS == true){                      
      Serial.print("BPM;");
      Serial.print(BPM);
      Serial.print(";");
      Serial.println();
      QS = false;    
     }
  delay(10);
  i++;
}
