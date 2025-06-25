/*
  Keyestudio Mini Tank Robot V3 (Popular Edition)
  lesson 20
  multiple functions
  http://www.keyestudio.com
*/
#include <IRremote.h>
#include <PWMServo.h>
#include <TimerFreeTone.h>
#include <Wire.h>

PWMServo myservo;

//Array, used to save data of images, can be calculated by yourself or gotten from modulus tool
unsigned char start01[] = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01 };
unsigned char STOP01[] = { 0x2E, 0x2A, 0x3A, 0x00, 0x02, 0x3E, 0x02, 0x00, 0x3E, 0x22, 0x3E, 0x00, 0x3E, 0x0A, 0x0E, 0x00 };
unsigned char front[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x24, 0x12, 0x09, 0x12, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
unsigned char back[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x24, 0x48, 0x90, 0x48, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
unsigned char left[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x44, 0x28, 0x10, 0x44, 0x28, 0x10, 0x44, 0x28, 0x10, 0x00 };
unsigned char right[] = { 0x00, 0x10, 0x28, 0x44, 0x10, 0x28, 0x44, 0x10, 0x28, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

unsigned char Smile[] = { 0x00, 0x00, 0x1c, 0x02, 0x02, 0x02, 0x5c, 0x40, 0x40, 0x5c, 0x02, 0x02, 0x02, 0x1c, 0x00, 0x00 };
unsigned char Disgust[] = { 0x00, 0x00, 0x02, 0x02, 0x02, 0x12, 0x08, 0x04, 0x08, 0x12, 0x22, 0x02, 0x02, 0x00, 0x00, 0x00 };
unsigned char Happy[] = { 0x02, 0x02, 0x02, 0x02, 0x08, 0x18, 0x28, 0x48, 0x28, 0x18, 0x08, 0x02, 0x02, 0x02, 0x02, 0x00 };
unsigned char Squint[] = { 0x00, 0x00, 0x00, 0x41, 0x22, 0x14, 0x48, 0x40, 0x40, 0x48, 0x14, 0x22, 0x41, 0x00, 0x00, 0x00 };
unsigned char Despise[] = { 0x00, 0x00, 0x06, 0x04, 0x04, 0x04, 0x24, 0x20, 0x20, 0x26, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00 };
unsigned char Heart[] = { 0x00, 0x00, 0x0C, 0x1E, 0x3F, 0x7F, 0xFE, 0xFC, 0xFE, 0x7F, 0x3F, 0x1E, 0x0C, 0x00, 0x00, 0x00 };

unsigned char clear[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

#define SCL_Pin 8   //set the pin of clock to D8
#define SDA_Pin 11  //set the data pin to D11

#define ML_Ctrl 4        //define the direction control pin of the left motor as 4
#define ML_PWM 6         //define the PWM control pin of the left motor
#define MR_Ctrl 2        //define the direction control pin of the right sensor
#define MR_PWM 5         //define the PWM control pin of the right motor
char ble_val;            //used to save the Bluetooth value
byte speeds_L = 200;     //the initial speed of the left motor is 200
byte speeds_R = 200;     //the initial speed of the right motor is 200
byte speeds_turn = 200;  //speed for turning left/right

#define servoPin 10     //servo Pin
#define light_L_Pin A1  //define the pin of the left photoresistor
#define light_R_Pin A2  //define the pin of the right photoresistor
int left_light;
int right_light;

#define Trig 12
#define Echo 13  // built-in led
float distance;  //Store the distance values detected by ultrasonic for following

// ----------- IR Remote ------------
#define IR_HOLD_DOWN_CODE 0xFFFFFFFF
#define IR_UP_CODE 0xFF629D
#define IR_DOWN_CODE 0xFFA857
#define IR_LEFT_CODE 0xFF22DD
#define IR_RIGHT_CODE 0xFFC23D
#define IR_OK_CODE 0xFF02FD
#define IR_1_CODE 0xFF6897
#define IR_2_CODE 0xFF9867
// IR Remote repeats button hold down signal about every 100 ms (+ some tolerance)
#define IR_TIMEOUT_MILLIS 200

IRrecv irrecv(3);
decode_results results;
unsigned long last_timestamp = 0;

//Store the distance values detected by ultrasonic for obstacle avoidance
int a;
int a1;
int a2;

bool flag;  //flag invariable, used to enter and exit a mode

String buffer = "";
String i2c_response = "";
bool received = false;
bool has_wire_command = false;

void setup() {
  Serial.begin(115200);

  Wire.begin(0x8);
  Wire.onReceive(onReceiveEvent);
  Wire.onRequest(onRequestEvent);

  irrecv.enableIRIn();  //Initialize the library of the IR remote

  myservo.attach(servoPin);

  pinMode(SCL_Pin, OUTPUT);
  pinMode(SDA_Pin, OUTPUT);

  pinMode(ML_Ctrl, OUTPUT);
  pinMode(ML_PWM, OUTPUT);
  pinMode(MR_Ctrl, OUTPUT);
  pinMode(MR_PWM, OUTPUT);

  matrix_display(clear);    //clear screen
  matrix_display(start01);  //show start

  pinMode(light_L_Pin, INPUT);
  pinMode(light_R_Pin, INPUT);

  pinMode(Trig, OUTPUT);
  pinMode(Echo, INPUT);
  RotateServo(90);  //set the angle of the servo to 90°
}

void loop() {
  while (Serial.available()) {
    buffer += (char)Serial.read();
    received = true;
    delay(2);
  }

  if (received)  //if there is data in the serial buffer
  {
    if (buffer.length() > 0) {
      ble_val = buffer[0];
    }

    Serial.println("Received string: " + buffer);
    buffer = "";
    received = false;

    switch (ble_val) {
      case 'F': Car_front(); break;  //the command to go front

      case 'B': Car_back(); break;  //the command to go back

      case 'L': Car_left(); break;  //the command to turn left

      case 'R': Car_right(); break;  //the command to turn right

      case 'S': Car_Stop(); break;  //stop

      case 'g': Avoid(); break;  //enter obstacle avoidance mode

      case 'h': Follow(); break;  //enter light following mode

      case 'i': Light_following(); break;  //enter light following mode

      case 'u':
        String speeds_l = Serial.readStringUntil('#');
        speeds_L = String(speeds_l).toInt();
        break;  //start by receiving u, end by receiving characters # and convert into the integer

      case 'v':
        String speeds_r = Serial.readStringUntil('#');
        speeds_R = String(speeds_r).toInt();
        break;  //start by receiving u, end by receiving characters # and convert into the integer

      case 'k': matrix_display(Smile); break;    //show "smile" face
      case 'l': matrix_display(Disgust); break;  //show "disgust" face
      case 'm': matrix_display(Happy); break;    //show "happy" face
      case 'n': matrix_display(Squint); break;   //show "Sad" face
      case 'o': matrix_display(Despise); break;  //show "despise" face
      case 'p': matrix_display(Heart); break;    //show the hearbeat image
      case 'z': matrix_display(clear); break;    //clear images

      default: break;
    }
  }

  //The following three signals are mainly used for cyclic printing
  if (ble_val == 'x') {
    distance = checkdistance();
    Serial.println(distance);
    delay(50);
  } else if (ble_val == 'w') {
    left_light = analogRead(light_L_Pin);
    Serial.println(left_light);
    delay(50);
  } else if (ble_val == 'y') {
    right_light = analogRead(light_R_Pin);
    Serial.println(right_light);
    delay(50);
  }

  if (!has_wire_command) {
    handleIRSignal();
  }
}

void handleIRSignal() {
  if (irrecv.decode(&results)) {  //Receive infrared remote control value
    unsigned long ir_rec = results.value;
    Serial.println(ir_rec, HEX);

    switch (ir_rec) {
      case IR_HOLD_DOWN_CODE:
        {
          Serial.println("Hold down");
          last_timestamp = millis();
          break;
        }
      case IR_UP_CODE:
        {
          last_timestamp = millis();
          Car_front();
          break;
        }
      case IR_DOWN_CODE:
        {
          last_timestamp = millis();
          Car_back();
          break;
        }
      case IR_LEFT_CODE:
        {
          last_timestamp = millis();
          Car_left();
          break;
        }
      case IR_RIGHT_CODE:
        {
          last_timestamp = millis();
          Car_right();
          break;
        }
      case IR_1_CODE: Avoid(); break;
      case IR_2_CODE: Dance(); break;
      default: break;
    }

    irrecv.resume();
  }

  if (isIRHoldReleased()) {
    Car_Stop();
  }
}

bool isIRHoldReleased() {
  long delta = millis() - last_timestamp;
  return delta > IR_TIMEOUT_MILLIS;
}

// Function that executes whenever data is received from master
void onReceiveEvent(int howMany) {
  String data = "";

  while (Wire.available()) {    // loop through all but the last
    data += String((char) Wire.read());  // receive byte as a character
  }

  if (data.length() == 0) {
    return;
  }

  Serial.println("Received data: '" + data + "', length: " + data.length());

  i2c_response = data;
  has_wire_command = true;

  char charCommand = data[0];

  switch (charCommand) {
    case 'F': Car_front(); break;
    case 'B': Car_back(); break;
    case 'L': Car_left(); break;
    case 'R': Car_right(); break;
    case 'S':
      {
        Car_Stop();
        has_wire_command = false;
        break;
      }
    case 'u':
    {
      String value = data.substring(1, data.length() - 1);
      speeds_L = value.toInt();
    }
    case 'v':
    {
      String value = data.substring(1, data.length() - 1);
      speeds_R = value.toInt();
    }
    case 't':
    {
      String value = data.substring(1, data.length() - 1);
      speeds_turn = value.toInt();
    }

  }
}

void onRequestEvent() {
  Wire.print(i2c_response); // Note: some responses may be skipped if onReceiveEvent receives events too quick

  Serial.println("SENT ON REQUEST: " + i2c_response);
}

//Control the ultrasonic sensor
float checkdistance() {
  float distance;
  digitalWrite(Trig, LOW);
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig, LOW);
  distance = pulseIn(Echo, HIGH) / 58.20;  //
  delay(10);
  return distance;
}

//the function to control the servo
void RotateServo(int myangle) {
  myservo.write(myangle);
}

void MakeTone(int frequency, int duration) {
  TimerFreeTone(9, frequency, duration);
}

void Dance() {
  RotateServo(90);

  // part 1

  for (int i = 0; i < 2; i++) {
    RotateServo(45);
    MakeTone(1300, 100);
    delay(400);

    RotateServo(135);
    MakeTone(1300, 100);
    delay(400);

    RotateServo(45);
    MakeTone(1300, 100);
    delay(400);

    RotateServo(135);
    MakeTone(1300, 100);
    delay(400);

    RotateServo(90);

    Car_left();
    delay(500);
    Car_right();
    delay(500);
    Car_left();
    delay(500);
    Car_right();
    delay(500);

    Car_Stop();
  }

  // part 2

  for (int i = 0; i < 2; i++) {
    RotateServo(45);
    MakeTone(1300, 100);
    Car_left();
    delay(300);
    MakeTone(1600, 100);

    RotateServo(135);
    MakeTone(1300, 100);
    Car_right();
    delay(300);
    MakeTone(1600, 100);

    RotateServo(45);
    MakeTone(1300, 100);
    Car_left();
    delay(300);
    MakeTone(1300, 100);

    RotateServo(135);
    MakeTone(1300, 100);
    Car_right();
    delay(300);
    MakeTone(1600, 100);

    RotateServo(90);

    Car_left();
    MakeTone(1450, 500);
    delay(500);

    Car_right();
    MakeTone(1300, 500);
    delay(500);

    Car_left();
    MakeTone(1600, 500);
    delay(500);

    Car_right();
    MakeTone(1450, 500);
    delay(500);

    Car_Stop();
  }

  // part 3

  for (int i = 0; i < 2; i++) {
    RotateServo(45);
    MakeTone(1300, 100);
    Car_front();
    delay(300);
    MakeTone(1150, 100);
    Car_Stop();

    RotateServo(135);
    MakeTone(1300, 100);
    Car_back();
    delay(300);
    MakeTone(1150, 100);
    Car_Stop();

    RotateServo(45);
    MakeTone(1300, 100);
    Car_front();
    delay(300);
    MakeTone(1150, 100);
    Car_Stop();

    RotateServo(135);
    MakeTone(1300, 100);
    Car_back();
    delay(300);
    MakeTone(1150, 100);
    Car_Stop();

    RotateServo(45);
    MakeTone(1300, 100);
    Car_left();
    delay(300);
    MakeTone(1150, 100);

    RotateServo(135);
    MakeTone(1300, 100);
    Car_right();
    delay(300);
    MakeTone(1150, 100);

    RotateServo(45);
    MakeTone(1300, 100);
    Car_left();
    delay(300);
    MakeTone(1300, 100);

    RotateServo(135);
    MakeTone(1300, 100);
    Car_right();
    delay(300);
    MakeTone(1600, 100);

    Car_Stop();
  }

  RotateServo(90);

  Car_right();
  MakeTone(1150, 250);
  MakeTone(1300, 250);
  MakeTone(1450, 250);
  MakeTone(1600, 250);
  MakeTone(1450, 1000);
  MakeTone(1300, 1000);

  Car_Stop();
}

/*****************obstacle avoidance******************/
void Avoid() {
  flag = 0;
  while (flag == 0) {
    a = checkdistance();     //the front distance is set to a
    if (a < 20) {            //When the distance in front is less than 20cm
      Car_Stop();            //stop
      delay(500);            //delay in 500ms
      RotateServo(180);      //servo turns left
      delay(500);            //delay in 500ms
      a1 = checkdistance();  //the left distance is set to a1
      delay(100);            //read value

      RotateServo(0);        //servo turns right
      delay(500);            //delay in 500ms
      a2 = checkdistance();  ///the right distance is set to a2
      delay(100);            //read value

      RotateServo(90);  //back to 90°
      delay(500);
      if (a1 > a2) {  //When the distance on the left is greater than the distance on the right
        Car_left();   //the robot turns left
        delay(700);   //turn left 700ms
      } else {
        Car_right();  //turn right
        delay(700);
      }
    } else {        //if the front distance ≥20cm，robot goes front
      Car_front();  //go front
    }
    //receive the Bluetooth value to exit the loop
    if (Serial.available()) {
      ble_val = Serial.read();
      if (ble_val == 'S')  //receive S
      {
        flag = 1;  //Set flag to 1 to exit the loop
        Car_Stop();
      }
    }

    if (irrecv.decode(&results)) {  //Receive infrared remote control value
      unsigned long ir_rec = results.value;
      Serial.println(ir_rec, HEX);
      switch (ir_rec) {
        case IR_OK_CODE:
          {
            flag = 1;
            Car_Stop();
            break;
          }
        default: break;
      }
      irrecv.resume();
    }
  }
}

/*******************following***************/
void Follow() {
  flag = 0;
  while (flag == 0) {
    distance = checkdistance();            //set the distance value to distance
    if (distance >= 20 && distance <= 60)  //go front
    {
      Car_front();
    } else if (distance > 10 && distance < 20)  // stop
    {
      Car_Stop();
    } else if (distance <= 10)  //go back
    {
      Car_back();
    } else  //stop
    {
      Car_Stop();
    }
    if (Serial.available()) {
      ble_val = Serial.read();
      if (ble_val == 'S') {
        flag = 1;  //exit the loop
        Car_Stop();
      }
    }
  }
}

/****************light following******************/
void Light_following() {
  flag = 0;
  while (flag == 0) {
    left_light = analogRead(light_L_Pin);
    right_light = analogRead(light_R_Pin);
    if (left_light > 650 && right_light > 650)  //go forward
    {
      Car_front();
    } else if (left_light > 650 && right_light <= 650)  //turn left
    {
      Car_left();
    } else if (left_light <= 650 && right_light > 650)  //turn right
    {
      Car_right();
    } else  //or else, stop
    {
      Car_Stop();
    }
    if (Serial.available()) {
      ble_val = Serial.read();
      if (ble_val == 'S') {
        flag = 1;
        Car_Stop();
      }
    }
  }
}

/***************dot matrix******************/
//this function is used for the display of dot matrix
void matrix_display(unsigned char matrix_value[]) {
  IIC_start();                  //use the function to start transmitting data
  IIC_send(0xc0);               //select an address
  for (int i = 0; i < 16; i++)  //image data have 16 characters
  {
    IIC_send(matrix_value[i]);  //data to transmit pictures
  }
  IIC_end();  //end the data transmission of pictures
  IIC_start();
  IIC_send(0x8A);  //show control and select pulse width 4/16
  IIC_end();
}

//the condition that data starts transmitting
void IIC_start() {
  digitalWrite(SDA_Pin, HIGH);
  digitalWrite(SCL_Pin, HIGH);
  delayMicroseconds(3);
  digitalWrite(SDA_Pin, LOW);
  delayMicroseconds(3);
  digitalWrite(SCL_Pin, LOW);
}

//transmit data
void IIC_send(unsigned char send_data) {
  for (byte mask = 0x01; mask != 0; mask <<= 1)  //each character has 8 digits, which is detected one by one
  {
    if (send_data & mask) {  //set high or low levels in light of each bit(0 or 1)
      digitalWrite(SDA_Pin, HIGH);
    } else {
      digitalWrite(SDA_Pin, LOW);
    }
    delayMicroseconds(3);
    digitalWrite(SCL_Pin, HIGH);  //pull up the clock pin SCL_Pin to end the transmission of data
    delayMicroseconds(3);
    digitalWrite(SCL_Pin, LOW);  //pull down the clock pin SCL_Pin to change signals of SDA
  }
}

//the sign that transmission of data ends
void IIC_end() {
  digitalWrite(SCL_Pin, LOW);
  digitalWrite(SDA_Pin, LOW);
  delayMicroseconds(3);
  digitalWrite(SCL_Pin, HIGH);
  delayMicroseconds(3);
  digitalWrite(SDA_Pin, HIGH);
  delayMicroseconds(3);
}

/***************motor runs****************/
void Car_back() {
  Serial.println("Car_back");

  digitalWrite(MR_Ctrl, LOW);
  analogWrite(MR_PWM, speeds_R);

  digitalWrite(ML_Ctrl, LOW);
  analogWrite(ML_PWM, speeds_L);

  matrix_display(back);  //show the image of going back
}

void Car_front() {
  Serial.println("Car_front");

  digitalWrite(MR_Ctrl, HIGH);
  analogWrite(MR_PWM, 255 - speeds_R);

  digitalWrite(ML_Ctrl, HIGH);
  analogWrite(ML_PWM, 255 - speeds_L);

  matrix_display(front);  //show the image of going front
}

void Car_left() {
  Serial.println("Car_left");

  digitalWrite(MR_Ctrl, HIGH);
  analogWrite(MR_PWM, 255 - speeds_turn);

  digitalWrite(ML_Ctrl, LOW);
  analogWrite(ML_PWM, speeds_turn);

  matrix_display(left);  //show the image of turning left
}

void Car_right() {
  Serial.println("Car_right");

  digitalWrite(MR_Ctrl, LOW);
  analogWrite(MR_PWM, speeds_turn);

  digitalWrite(ML_Ctrl, HIGH);
  analogWrite(ML_PWM, 255 - speeds_turn);

  matrix_display(right);  //show the image of turning right
}

void Car_Stop() {
  digitalWrite(MR_Ctrl, LOW);
  analogWrite(MR_PWM, 0);

  digitalWrite(ML_Ctrl, LOW);
  analogWrite(ML_PWM, 0);

  matrix_display(STOP01);  //show the stop image
}
//**************************************************************
