/*
example code for leds: https://sites.google.com/site/summerfuelrobots/arduino-sensor-tutorials/3-color-rgb-led-module
*/

int ledDigitalOne[] = {6, 11, 3}; // 3 = red, 6 = green, 11 = blue
int i = 0;
const boolean ON = HIGH;
const boolean OFF = LOW;
boolean stat = false;
char string[] = "";
char test[11];
char pattern[] = "1111100000";

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
    string[sizeof(string)] = incoming;
    if (stat == false){
      if (sizeof(string)>9){
        for (i=0;i<11;i++){
          test[i]=string[sizeof(string)-10+i];
          Serial.println(test);
        }
        if (strcmp(test, pattern)){
          stat = true;
          char string[] = "";
          Serial.println("Pattern confirmed!");
        }
        else{
          Serial.println("Wrong pattern.");
        }
      }
    }
    else{
      if (sizeof(string) == 9){
        Serial.println("Receiving data.");      
        Color(string);
        char string[] = "";
        stat = false;
      }
    }
  }
}

void Color(char* string){
  if (string[1]=='1'){
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
