#include <Servo.h>

Servo servo;
int angle = 180;

void setup() {
  // put your setup code here, to run once:
  servo.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:

  // Guidance servo motor on angle 
  servo.write(angle);
  delay(500);
}
