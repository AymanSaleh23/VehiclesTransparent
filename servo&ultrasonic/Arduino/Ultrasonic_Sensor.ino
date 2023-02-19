
#define trig 11
#define echo 12
// defition two varible of ditance and time 
int distance=0,timet=0;
void setup() 
{
  Serial.begin(9600);
  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);
}

void loop() 
{
  // to get 
  digitalWrite(trig,LOW);
  delayMicroseconds(5);
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(trig,LOW);
  timet=pulseIn(echo,HIGH);
  distance=timet/57;   //Distance = (Speed of Sound * Time/2) = t/(1/((350*0.0001)/2))
  //Serial.println(distance);
  delay(50);

  
}
