const int redPin = 11;
const int greenPin = 10;
const int bluePin = 9;
void setup(){
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  Serial.begin(115200);
}
#define PATTERN_LENGTH 19
char currently_received[PATTERN_LENGTH];
int current_receive_index = 0;
char pattern_check[] = "1111100000";
char current_pattern[] = "000000000";
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
  analogWrite(redPin, (current_pattern[0]=='1')?255:0);
  analogWrite(greenPin, (current_pattern[1]=='1')?255:0);
  analogWrite(bluePin, (current_pattern[2]=='1')?255:0);
}
void loop(){
  if(Serial.available() > 0){
    currently_received[current_receive_index] = Serial.read();
    ++current_receive_index;
    current_receive_index %= PATTERN_LENGTH;
    check_pattern();
  }
}
