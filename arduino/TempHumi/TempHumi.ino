/*
Om de library te installeren, heb je de file DHT11.zip nodig.
Deze is te vinden op https://drive.google.com/uc?export=download&id=0B3L4pZE60Jv0SzRsTTMxZGZNblU
Klik nu in het arduinoprogramma op Sketch -> Import Library... -> Add Library...
Vind de zip-file en voeg deze toe.
Herstart nu het arduinoprogramma om de library volledig in te laden.
*/


#include <DHT11.h>
int pin=2;
DHT11 dht11(pin); 
void setup()
{
   Serial.begin(9600);
  while (!Serial) {
      ; // wait for serial port to connect. Needed for Leonardo only
    }
}

void loop()
{
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
  }
  else
  {
    Serial.println();
    Serial.print("Error No :");
    Serial.print(err);
    Serial.println();    
  }
  delay(DHT11_RETRY_DELAY); //delay for reread
}
