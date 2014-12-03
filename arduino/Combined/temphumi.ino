#include "headers.h"

#define TEMPHUMI_UPDATE_INTERVAL 2000

#define PIN_TEMPHUMI 8
DHT dht(PIN_TEMPHUMI, DHTTYPE);

/*
Initializes the temperature and humidity sensor.
*/
void setupTempHumi(){
  dht.begin();
}


uint32_t last_temphumi_data_time = millis();
/*
Sends any new data from the temperature and humidity sensor to the Raspberry.
*/
void readTempHumi(){
  uint32_t current_millis = millis();
  if(last_temphumi_data_time > current_millis) last_temphumi_data_time = current_millis;
  if(current_millis-last_temphumi_data_time < TEMPHUMI_UPDATE_INTERVAL){
    return;
  }
  last_temphumi_data_time = current_millis;
  Serial.print("TH;");
  Serial.print(dht.readTemperature());
  Serial.print(";");
  Serial.println(dht.readHumidity());
}
