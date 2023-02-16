String receive = "0";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() != 0){
    receive = Serial.readString();
    if (receive == "1"){
      Serial.println("31.3, 52.2, 23.25");
    }
    else if (receive == "2"){
      Serial.println("xxx, yyy, zzz");
    }
    
  }
}
