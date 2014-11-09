#include "headers.h"

//const int pin_button1 = 7;
#define PIN_BUTTON1 7

void setupButtons(){
  pinMode(PIN_BUTTON1, INPUT);
}

void readButtons(){
  Serial.print("pb1;");
  Serial.println(digitalRead(PIN_BUTTON1));
}
