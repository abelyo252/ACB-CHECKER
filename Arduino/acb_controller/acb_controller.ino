
/*
  ACB CHECKER GAME SIMULATOR

  ACB CHECKER GAME : The major goal of the computer 
  game ACB Checker, which uses computer vision and robot manipulation, 
  is to analyse manipulator behaviour.

  The circuit:
  - 4 Servo , LCD 16x2(I2C) and 1 switch is used

  created 21 FEB 2023
  by Abel Yohannes
*/


#include <Servo.h>
#include <string.h>
#include <Adafruit_LiquidCrystal.h>

int pos = 0;

int deg1 = 0;
int deg2 = 0;
int deg3 = 0;
int deg4 = 0;

Servo servo_9;
Servo servo_8;
Servo servo_7;
Servo servo_6;


Adafruit_LiquidCrystal lcd_1(0);

void setup()
{
  lcd_1.begin(16, 2);
  Serial.begin(9600);


  lcd_1.print("ACB Checker");
  servo_9.attach(9, 500, 2500);
  servo_8.attach(8, 500, 2500);
  servo_7.attach(7, 500, 2500);
  servo_6.attach(6, 500, 2500);
  pinMode(13, OUTPUT);

  Serial.print("ACB instantiated !");

}

void loop()
{.

  digitalWrite(13, LOW);  
  delay(1000);
  
  if(Serial.available()) {
    
    // read one byte from serial buffer and save to data_rcvd
    string data_rcvd = Serial.readLine();

	deg1 = getdeg(data_rcvd.substr(3, 2));
	deg2 = getdeg(data_rcvd.substr(3, 2));
	deg3 = getdeg(data_rcvd.substr(3, 2));
	deg4 = getdeg(data_rcvd.substr(3, 2));
	
	
	for (pos = 0; pos <= deg1; pos += 1) {
    servo_9.write(pos);
    delay(15); 
  }
  
  for (pos = 0; pos <= deg2; pos += 1) {
    servo_8.write(pos);
    delay(15); 
  }
  
  
  for (pos = 0; pos <= deg3; pos += 1) {
    servo_7.write(pos);
    delay(15); 
  }
  
  for (pos = 0; pos <= deg4; pos += 1) {
    servo_6.write(pos);
    delay(15); 
  }
  
  digitalWrite(13, HIGH);
  delay(1000); 
 

    
  }
  
  
  
  lcd_1.setCursor(0, 1);
  lcd_1.print("SM:45 64 135 78");
 
}

int getdeg(string deg){
return deg.toInt();
}