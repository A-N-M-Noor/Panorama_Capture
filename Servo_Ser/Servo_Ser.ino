#include <Servo.h>
//#include <ESP32Servo.h>

Servo s;

int target = 0, current = 90;
int angSpd = 1;
int angDel = 20;
int stabilizeDel = 500;

bool reached = true;

void setup() {
  Serial.begin(9600);
  s.attach(9);
//  s.attach(16);
}

void loop() {
  while(Serial.available()>0){
    target = Serial.readStringUntil('\n').toInt();
    reached = false;
  }

  while(current != target){
    if(abs(current - target) > angSpd){
      current += (target > current)? angSpd : -angSpd;
    }
    else{
      current = target;
    }
    s.write(int(current));
    delay(angDel);
  }

  if(current == target && reached == false){
    reached = true;
    delay(stabilizeDel);
    Serial.println("done");
  }
  
}
