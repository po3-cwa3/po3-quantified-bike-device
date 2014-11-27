/*
example code for leds: https://sites.google.com/site/summerfuelrobots/arduino-sensor-tutorials/3-color-rgb-led-module
*/

int ledDigitalOne[] = {10, 11, 9}; // 10 = red, 11 = green, 9 = blue
const boolean ON = HIGH;
const boolean OFF = LOW;
boolean stat = false;
String string = "";
String pattern = "1111100000";

//Predefined Colors
const boolean RED[] = {ON, OFF, OFF};    
const boolean GREEN[] = {OFF, ON, OFF}; 
const boolean BLUE[] = {OFF, OFF, ON};  
const boolean BLACK[] = {OFF, OFF, OFF}; 

void setup(){
  for(int i = 0; i < 3; i++){
   pinMode(ledDigitalOne[i], OUTPUT);   //Set the three LED pins as outputs
  }
  Serial.begin(115200);
}

void loop(){
  if (Serial.available()>0){
    char incoming = Serial.read();
    string += incoming;
    if (stat == false){
      if (string.length() == 10){
        if (string == pattern){
          stat = true;
          string = "";
          Serial.println("Pattern confirmed!");
        }
        else{
          string.setCharAt(1,'\0');
          Serial.println("Wrong pattern.");
        }
      }
    }
    else{
      Serial.println("Receiving data.");      
      if (string.length() == 9){
        Color(string);
        string = "";
        stat = false;
      }
    }
  }
}

void Color(String string){
  if (string.charAt(string.length()-1)=='1'){
    setColor(ledDigitalOne, GREEN);
    Serial.println("online");
  }
  else{
    setColor(ledDigitalOne, RED);
    Serial.println("offline");
  }
}

void setColor(int* led, const boolean* color){
 for(int i = 0; i < 3; i++){
   digitalWrite(led[i], color[i]);
 }
}
