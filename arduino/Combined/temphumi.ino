#include "headers.h"

#define TEMPHUMI_UPDATE_INTERVAL 1000

//const int pin_temphumi = 8;
#define PIN_TEMPHUMI 8
DHT dht(PIN_TEMPHUMI, DHTTYPE);

void setupTempHumi(){
  dht.begin();
}


uint32_t last_temphumi_data_time = millis();
void readTempHumi(){
  if(last_temphumi_data_time > millis()) last_temphumi_data_time = millis();
  if(millis()-last_temphumi_data_time < TEMPHUMI_UPDATE_INTERVAL){
    return;
  }
  last_temphumi_data_time = millis();
  Serial.print("th;");
  Serial.print(dht.readTemperature());
  Serial.print(";");
  Serial.println(dht.readHumidity());
}
