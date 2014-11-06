/*
Om de library te installeren, heb je de file DHT11.zip nodig.
Deze is te vinden op https://drive.google.com/uc?export=download&id=0B3L4pZE60Jv0SzRsTTMxZGZNblU
Klik nu in het arduinoprogramma op Sketch -> Import Library... -> Add Library...
Vind de zip-file en voeg deze toe.
Herstart nu het arduinoprogramma om de library volledig in te laden.
*/
//De TempHumi-sensor zit op pin 5, de Button op pin 4

#include <DHT11.h>
const int TempHumiPin = 5;
const int ButtonPin = 4;

int i = 0;
int buttonState = 0;
int pulsePin = 0;
int BPM;

volatile int IBI = 600;
volatile boolean Pulse = false;
volatile boolean QS = false;

DHT11 dht11(TempHumiPin);

void setup(){
  Serial.begin(115200);
  while (!Serial){;}
  pinMode(ButtonPin, INPUT);
  interruptSetup();
  }

void loop(){
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
