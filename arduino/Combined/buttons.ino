#include "headers.h"

//const int pin_button1 = 7;
#define PIN_BUTTON1 7
#define PIN_BUTTON2 15
#define PIN_BUTTON3 10

void setupButtons(){
  pinMode(PIN_BUTTON1, INPUT);
}

uint32_t previous_button_time = millis();
void readButtons(){
  if(millis() < previous_button_time+10){
    return;
  }
  previous_button_time = millis();
  Serial.print("PB1;");//pushbutton -> start or stop trip
  Serial.println(digitalRead(PIN_BUTTON1));
  Serial.print("PB2;");//normal button -> camera
  Serial.println(digitalRead(PIN_BUTTON2));
  Serial.print("PB3;");//normal button
  Serial.println(digitalRead(PIN_BUTTON3));
}
