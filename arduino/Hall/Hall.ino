int counter;
float velocity = 0;
float distance = 0;
long time = 0;
float radius = 33; //in cm

void setup(){
   Serial.begin(115200);
   attachInterrupt(0, counting, RISING);
}

void loop(){
   if (counter >= 5) {
     distance = counter*2*radius*0.01*3.14;
     velocity = (distance/(millis()-time))*3600; //in km/u
     time = millis();
     counter = 0;
     Serial.print("km/h;");
     Serial.print(velocity);
     Serial.print(";");
     Serial.println();
  }
}

void counting(){
   counter++;
}
