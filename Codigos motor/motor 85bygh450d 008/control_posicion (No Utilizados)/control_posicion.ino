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
float rps = 0.2;
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
  deltaAngle(180.0, pulse_per_rev, 0.1, pulse_1, direction_1);
  delay(2000);                // wait for a 2 sec delay
  deltaAngle(-90.0, pulse_per_rev, 0.2, pulse_1, direction_1);
  delay(3000);                // wait for a 2 sec delay
  deltaAngle(90.0, pulse_per_rev, 0.2, pulse_1, direction_1);
  delay(3000);                // wait for a 2 sec delay
  deltaAngle(-180.0, pulse_per_rev, 0.1, pulse_1, direction_1);
  delay(2000);                // wait for a 2 sec delay
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

void deltaAngle (float angle, float pulses_per_revolution, float rps, int pulse_pin, int direction_pin) {
  long delayVal;
  int n_pulsos;

  if (angle>=0){
    digitalWrite(direction_pin, HIGH);
  }
  else {
    digitalWrite(direction_pin, LOW);
  }
  
  delayVal = delayValue(pulses_per_revolution, rps);
  n_pulsos = (int) pulses_per_revolution*abs(angle) / 360.0;
  for (int i=0; i<n_pulsos; i++){
    digitalWrite(pulse_pin, HIGH);   // turn the pulse_1 on (HIGH is the voltage level)
    delayMicroseconds(delayVal);                // wait for a delay 1 time
    digitalWrite(pulse_pin, LOW);    // turn the pulse_1 off by making the voltage LOW
    delayMicroseconds(delayVal);                // wait for a delat 1 time
  }
}
