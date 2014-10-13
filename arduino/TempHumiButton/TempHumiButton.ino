/*
Om de library te installeren, heb je de file DHT11.zip nodig.
Deze is te vinden op https://drive.google.com/uc?export=download&id=0B3L4pZE60Jv0SzRsTTMxZGZNblU
Klik nu in het arduinoprogramma op Sketch -> Import Library... -> Add Library...
Vind de zip-file en voeg deze toe.
Herstart nu het arduinoprogramma om de library volledig in te laden.
*/
//De TempHumi-sensor zit op pin 2, de Button op pin 4

#include <DHT11.h>
const int pin=2;
const int button = 4;
int i=0;
int buttonState=0;
DHT11 dht11(pin); 
void setup(){
  Serial.begin(9600);
  while (!Serial){
    ;
    }
  pinMode(button, INPUT);
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
  buttonState = digitalRead(button);
  if (buttonState == LOW) {
    Serial.println("pb;1;");
    }
    else{
      Serial.println("pb;0;");
    }
  delay(10);
  i++;
}
