/*
  Code for programming stepper motor with arduino, using driver DQ860MA

  Connections:
  Motor-Driver
  A+ red
  A- green
  B+ yellow
  B- blue
*/

const int enable_1 = 9;        // enable - driver stepper 1
const int direction_1 = 10;    // direction - driver stepper 1
const int pulse_1 = 11;        // pulse - driver stepper 1

//Pulse per revolution
const float pulse_per_rev = 10000.0;
float rps = 0.10;
float delay_1;
long delay_1_long;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pins as an output.
  pinMode(enable_1, OUTPUT);
  pinMode(direction_1, OUTPUT);
  pinMode(pulse_1, OUTPUT);

  // Define enable = HIGH
  digitalWrite(enable_1, HIGH);
  digitalWrite(direction_1, HIGH);

  // delay
  delay_1 = 1000.0/(pulse_per_rev*rps);
  delay_1_long = (long) delay_1;

  Serial.print(delay_1);
  Serial.print(delay_1_long);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(pulse_1, HIGH);   // turn the pulse_1 on (HIGH is the voltage level)
  delay(delay_1_long);                // wait for a delay 1 time
  digitalWrite(pulse_1, LOW);    // turn the pulse_1 off by making the voltage LOW
  delay(delay_1_long);                // wait for a delat 1 time
}
