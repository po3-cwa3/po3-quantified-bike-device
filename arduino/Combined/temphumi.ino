#include "headers.h"

#define TEMPHUMI_UPDATE_INTERVAL 2000

//const int pin_temphumi = 8;
#define PIN_TEMPHUMI 8
DHT dht(PIN_TEMPHUMI, DHTTYPE);

void setupTempHumi(){
  dht.begin();
}


uint32_t last_temphumi_data_time = millis();
void readTempHumi(){
  //Serial.println(millis());
  
  //noInterrupts();
  uint32_t current_millis = millis();
  if(last_temphumi_data_time > current_millis) last_temphumi_data_time = current_millis;
  if(current_millis-last_temphumi_data_time < TEMPHUMI_UPDATE_INTERVAL){
    //interrupts();
    return;
  }
  last_temphumi_data_time = current_millis;
  Serial.print("th;");
  //noInterrupts();
  Serial.print(dht.readTemperature());
  Serial.print(";");
  Serial.println(dht.readHumidity());
  //interrupts();
}
