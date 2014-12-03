int counter;
float velocity = 0;
float distance = 0;
long time = 0;
//float radius = 33; //in cm
//Send speed for a wheel of radius 1 cm. 
//Configuration is easier on the RPi, so let the RPi calculate the real speed.
float radius = 1.0; 

/*
Initializes the Hall Sensor.
*/
void setupHall(){
   attachInterrupt(0, counting, RISING);
}

/*
Sends any new data from the hall sensor to the Raspberry Pi.
*/
void readHall(){
   if (counter >= 5) {
     distance = counter*2*radius*0.01*3.14;
     velocity = (distance/(millis()-time))*3600; //in kmph
     time = millis();
     counter = 0;
     Serial.print("v;");
     Serial.print(velocity);
     Serial.print(";");
     Serial.println();
  }
}

void counting(){
   counter++;
}
