/*
  Code for programming stepper motor with arduino, using driver DQ860MA

  Connections:
  Motor-Driver
  A+ red
  A- green
  B+ yellow
  B- blue
*/

//PIN's DEFINITION.
const int enable_1 = 9;        // enable - driver stepper 1
const int direction_1 = 10;    // direction - driver stepper 1
const int pulse_1 = 11;        // pulse - driver stepper 1

//FIXED VARIABLES.

//Pulse per revolution
float pulse_per_rev = 2000.0;
float rps = 4.0;
long pulseDelay;

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
  pulseDelay = delayValue(pulse_per_rev,rps);
  Serial.print("Delay: ");
  Serial.println(pulseDelay);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(pulse_1, HIGH);   // turn the pulse_1 on (HIGH is the voltage level)
  delayMicroseconds(pulseDelay);                // wait for a delay 1 time
  digitalWrite(pulse_1, LOW);    // turn the pulse_1 off by making the voltage LOW
  delayMicroseconds(pulseDelay);                // wait for a delat 1 time
  Serial.println(pulseDelay);
}


//FUNCTIONS
//Function that calculates the delay value for a certain number of rps.
long delayValue (float pulses_per_revolution, float rps){
  // Variables definition
  float delays;
  float delayms;
  float pulses_per_second;
  long delaymslong;
    
  //pulses per second.
  pulses_per_second = pulses_per_revolution * rps;
  //duration of values LOW or HIGH.
  delays = 1.0 / (2.0*pulses_per_second);
  //conversion to miliseconds
  delayms = delays * 1000000.0;
  delaymslong = (long) delayms;
  return delaymslong;
}
