/*
Device State reads the state string from the RPi and displays the state by using the LEDs.
*/
#define CONNECTION_LED 3

#define BATCH_LED_BLUE 16
#define BATCH_LED_GREEN 17
#define BATCH_LED_RED 18

#define PICTURE_LED_BLUE 6
#define PICTURE_LED_GREEN 9
#define PICTURE_LED_RED 11

#define ACTIVE_TRIP_LED 5

const boolean GREEN[] = {false, true, false};
const boolean RED[] = {true, false, false};
const boolean BLUE[] = {false, false, true};
/*
State string:
0: 1 if a connection is available
1: 1 if batch-uploading
2: 1 if batch-uploading succeeded
3: 1 if batch-uploading failed
4: 1 if taking picture
5: 1 if taking picture failed
6: 1 if taking picture succeeded
7: 1 if trip active
8:
*/
/*
Initialize the LEDs
*/
void setupStateHandler(){
  pinMode(CONNECTION_LED, OUTPUT);
  pinMode(BATCH_LED_BLUE, OUTPUT);
  pinMode(BATCH_LED_GREEN, OUTPUT);
  pinMode(BATCH_LED_RED, OUTPUT);
  pinMode(PICTURE_LED_BLUE, OUTPUT);
  pinMode(PICTURE_LED_GREEN, OUTPUT);
  pinMode(PICTURE_LED_RED, OUTPUT);
  pinMode(ACTIVE_TRIP_LED, OUTPUT);
}
#define PATTERN_LENGTH 19
//buffer containing the latest PATTERN_LENGTH characters
char currently_received[PATTERN_LENGTH];
int current_receive_index = 0;

//the first part of the data sent by the Raspberry Pi should match this string.
//As this pattern has length 10, the state string can have length up to 9
char pattern_check[] = "1111100000";
char current_pattern[] = "000000000";

boolean getOnline(){
  return current_pattern[0] == '1';
}

boolean getBatchUploading(){
  return current_pattern[1] == '1';
}

boolean getBatchSuccess(){
  return current_pattern[2] == '1';
}

boolean getBatchFailed(){
  return current_pattern[3] == '1';
}

boolean getTakingPicture(){
  return current_pattern[4] == '1';
}

boolean getPictureFailed(){
  return current_pattern[5] == '1';
}

boolean getPictureSuccess(){
  return current_pattern[6] == '1';
}

boolean getTripActive(){
  return current_pattern[7] == '1';
}


/*
Sets the picture taking LED.
*/
void setPictureLED(const boolean values[]){
  digitalWrite(PICTURE_LED_RED, values[0]);
  digitalWrite(PICTURE_LED_GREEN, values[1]);
  digitalWrite(PICTURE_LED_BLUE, values[2]);
}/*
Sets the batch uploading LED.
*/
void setBatchLED(const boolean values[]){
  digitalWrite(BATCH_LED_RED, values[0]);
  digitalWrite(BATCH_LED_GREEN, values[1]);
  digitalWrite(BATCH_LED_BLUE, values[2]);
}
/*
Sets the connection LED.
*/
void setConnectionLED(boolean value){
  digitalWrite(CONNECTION_LED, value);
}/*
Sets the active trip LED.
*/
void setTripLED(boolean value){
  digitalWrite(ACTIVE_TRIP_LED, value);
}

int batch_success_start = 0;
int batch_failed_start = 0;
int picture_success_start = 0;
int picture_failed_start = 0;
/*
A new state string has been received, so the status of the LEDs should be updated.
*/
void patternUpdated(){
  if(getBatchSuccess()){
    batch_success_start = millis();
  }
  if(getBatchFailed()){
    batch_failed_start = millis();
  }
  if(getPictureSuccess()){
    picture_success_start = millis();
  }
  if(getPictureFailed()){
    picture_failed_start = millis();
  }
}
const int batch_result_notification_time = 2000;
const int picture_result_notification_time = 2000;
boolean getBatchSuccessLED(){
  return millis() - batch_success_start <= batch_result_notification_time;
}
boolean getBatchFailedLED(){
  return millis() - batch_failed_start <= batch_result_notification_time;
}
boolean getPictureSuccessLED(){
  return millis() - picture_success_start <= picture_result_notification_time;
}
boolean getPictureFailedLED(){
  return millis() - picture_failed_start <= picture_result_notification_time;
}
/*
Update LEDs depending on status.
*/
void updateLEDs(){
  if(getOnline()){
    setConnectionLED(true);
  }else{
    setConnectionLED(false);
  }
  if(getBatchUploading()){
    setBatchLED(BLUE);
  }
  if(getBatchSuccessLED()){
    setBatchLED(GREEN);
  }
  if(getBatchFailedLED()){
    setBatchLED(RED);
  }
  if(getTakingPicture()){
    setPictureLED(BLUE);
  }
  if(getPictureSuccessLED()){
    setPictureLED(GREEN);
  }
  if(getPictureFailedLED()){
    setPictureLED(RED);
  }
  if(getTripActive()){
    setTripLED(true);
  }else{
    setTripLED(false);
  }
}
/*
Check if there is a state string in the received data.
*/
void check_pattern(){
  for(int i = current_receive_index; i < current_receive_index + PATTERN_LENGTH; ++i){
    if(i-current_receive_index < 10){
      if(currently_received[i%PATTERN_LENGTH] != pattern_check[i-current_receive_index]){
        return;
      }
    }else{
      current_pattern[i-current_receive_index-10] = currently_received[i%PATTERN_LENGTH];
    }
  }
  patternUpdated();
}
/*
Checks whether there is new data.
*/
void readState(){
  if(Serial.available() > 0){
    currently_received[current_receive_index] = Serial.read();
    ++current_receive_index;
    current_receive_index %= PATTERN_LENGTH;
    check_pattern();
  }
  updateLEDs();
}
