#include <Servo.h>
#include <Wire.h>
#include <SoftwareSerial.h>

// deklarasi pin
#define relay 42
#define rain 45
#define kanan_belakang 6
#define kiri_belakang 2
#define kanan_atas 3
#define kanan_depan 4
#define kiri_atas 5
#define kiri_depan 7
#define gripper 8
#define button 41

// Ultrasonik
#define COM1 0x55
#define COM2 0x56
unsigned char buffer_RTT[4];
uint8_t CS;
int distance1;
int distance2;

// deklarasi servo
Servo ESC1; // kanan depan
Servo ESC2; // kiri depan
Servo ESC3; // kanan belakang
Servo ESC4; // kiri belakang
Servo ESC5; // kanan atas
Servo ESC6; // kiri atas 
Servo GRIPPER; // gripper

//Compass Init
int Yaw, Pitch, Roll;
int ErrorYaw = 0;
int ErrorYawCal = 0;
int ErrorPitch = 0;
int ErrorPitchCal = 0;
int ErrorRoll = 0;
int ErrorRollCal = 0;
int YawA, PitchA, RollA;

int ErrorKiri;
int ErrorKanan;
int ErrorDepan;
int ErrorBelakang;
int ErrorSaKiri;
int ErrorSaKanan;

int pwmSignal2 = 1460;
int pwmSignal3 = 1460;
// int pwmSignal4 = 1100;
// int pwmSignal5 = 1100;
// int pwmSignal6 = 1100;
// int pwmSignal7 = 1100;

const int neutralThrust = 1900; // Neutral position for the ESCs
const int maxThrust = 2000; // Maximum thrust
const int minThrust = 1200; // Minimum thrust

float Kp = 100; // Proportional control term
float Ki = 0; // Integral control term
float Kd = 0; // Derivative control term
float P;
float I;
float D;
float lastError = 0;
float error;

bool testonce2 = false;
bool state = false;

unsigned long currentMillis = 0;
unsigned long previousMillis = 0;
const long interval = 8000;
const long maju_interval = 40000;
const long maju1_interval = 40000;
const long kanan_interval = 15000;
const long kiri_interval = 12000;
const long maju2_interval = 45000;
const long maju3_interval = 8000;

int counter = 0;
int start = 0;
bool debounce = 0;
bool belok_kanan = false;
bool belok_kiri = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  ESC1.attach(kanan_depan);
  ESC2.attach(kiri_depan);
  ESC3.attach(kanan_belakang);
  ESC4.attach(kiri_belakang);
  ESC5.attach(kanan_atas);
  ESC6.attach(kiri_atas);
  GRIPPER.attach(gripper);

  pinMode(rain, INPUT);
  pinMode(relay, OUTPUT);
  pinMode(button, INPUT_PULLUP);

  ESC1.writeMicroseconds(1100);
  ESC2.writeMicroseconds(1100);
  ESC3.writeMicroseconds(1100);
  ESC4.writeMicroseconds(1100);
  ESC5.writeMicroseconds(1460);
  ESC6.writeMicroseconds(1460);
  GRIPPER.write(0);

  delay(2000);
  Serial.println("Motor Siap!!");

  // // Handshake with Raspberry Pi
  // while (true) {
  //   if (Serial.available() > 0) {
  //     char data = Serial.read();
  //     if (data == 'H') { // Received handshake signal from Raspberry Pi
  //       Serial.println("ACK"); // Send ACK as response
  //       break; // Exit handshake loop
  //     }
  //   }
  // }

}

void loop() {
  // put your main code here, to run repeatedly:
  ReadErrorYPR();
  readSensor1();
  readSensor2();
  // GRIPPER.write(50);

  // unsigned currentMillis = millis();

  if (!digitalRead(button)) {
    if (!debounce) {
      uint32_t entry_millis = millis();
      if (start < 1) start++;
      else start = 0;
      debounce = 1;
    }
  } else {
    if (debounce) {
      delay(10);
      debounce = 0;
    }
  }

  if(rain == 0){
    digitalWrite(relay, HIGH);
  }else{
    digitalWrite(relay, LOW);
  }

  tembak_bro();

  // delay(50);
}
