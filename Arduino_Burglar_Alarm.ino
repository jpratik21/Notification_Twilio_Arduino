/*
CSC 895: DO IT YOURSELF BURGLAR ALARM
Arno Puder, Pratik Jaiswal

Arduino program to detect motion with an ultransonic sensor, make LED blink and 
output serial data that can be utilized by python scripts and Android Applications. 
*/

/*
Setting up the pins - using the default on-board LED that is connected
to digital pin 13.
*/
#define LED 13
#define trigPIN 9
#define echoPIN 8
   
int sensorDIST = 200;
boolean triggered = false;
 
void setup() 
{
  Serial.begin (9600);
  pinMode(LED, OUTPUT);
  pinMode(trigPIN, OUTPUT);
  pinMode(echoPIN, INPUT);
 
  long duration, distance;
 
  //Begin calibration: Arduino takes around 5 seconds to set itself and so, hold on.
 
  digitalWrite(LED, HIGH);
  
  while (millis() < 5000) {
      digitalWrite(trigPIN, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPIN, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPIN, LOW);
      duration = pulseIn(echoPIN, HIGH);
      distance = (duration / 2) / 29.1;
      if (distance < sensorDIST) {
        sensorDIST = distance;
      }
   }
   
   // finish calibration
   digitalWrite(LED, LOW); 
}
 
void loop() {
  if (triggered) {
    /* Motion is detected. So, tell the host computer 
    by sending a byte "1" */
    Serial.print(1);
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);
  } else {
    long duration, distance;
    digitalWrite(trigPIN, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPIN, LOW);
    duration = pulseIn(echoPIN, HIGH);
    distance = (duration/2) / 29.1;
    if (distance < sensorDIST - 10) {
      triggered = true;
    }
    delay(20);
  }
}