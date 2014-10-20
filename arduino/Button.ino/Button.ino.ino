/*
Button
Turns on and of a LED when the button attached to pin 4 is pushed 
*/
// constants won't change. They're used here to set pin numbers:
const int button = 4; // the number of the hall effect sensor pin
const int ledPin = 13; // the number of the LED pin
// variables will change:
int buttonState = 0; // variable for reading the Button
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
    }
    // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the button pin as an input:
  pinMode(button, INPUT);
}
void loop(){
  // read the state of the button:
  buttonState = digitalRead(button);
  if (buttonState == LOW) {
    Serial.println("pb;1;");
  }
  else{
    Serial.println("pb;0;");
  }
  delay(10);
}
