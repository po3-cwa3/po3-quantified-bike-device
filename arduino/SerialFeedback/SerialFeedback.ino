void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()>0){
    char incoming = Serial.read();
    char data[2];
    data[0] = incoming;
    data[1] = '\0';
    Serial.println(data);
  }
}
