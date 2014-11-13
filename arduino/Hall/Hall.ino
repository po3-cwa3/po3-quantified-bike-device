// nog niet af !!!
// nog niet getest !!!

int hallPin = 3;
int hallState = 0;
int radius = 33; //in cm
int counter_1 = 0;
int counter_2 = 0;

void setup() {
  Serial.begin(115200);
  pinMode(hallPin, INPUT); 
}

void loop() {
  hallState = digitalRead(hallPin);
  ++counter_2;
  if (hallState==HIGH){
    time = (counter_2 - counter_1)/100;
    counter_1 = counter_2
    vel = ((2*radius*0.01*3.14)/time)*3.6 //in km/u
    Serial.print("km/h;");
    Serial.print(vel);
    Serial.println();    
  delay(10);
}
