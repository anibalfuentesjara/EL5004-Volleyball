/*
 *   Connections:
  Motor-Driver
  A+ red
  A- green
  B+ yellow
  B- blue
 * 
 */

#include <AccelStepper.h>

// Variables de fines de carrera
const int button1Pin = 2;     // the number of the pushbutton pin
int button1State = 0;         // variable for reading the pushbutton status

// Define some steppers and the pins the will use

// USE: AccelStepper stepper(AccelStepper::FULL2WIRE, direction, pulse);

//AccelStepper stepper2(AccelStepper::FULL2WIRE, 6, 7);
//AccelStepper stepper2(AccelStepper::FULL2WIRE, 8, 9);
AccelStepper stepper3(AccelStepper::FULL2WIRE, 10, 11);
float pulse_per_rev = 5000;

//Variables para el movimiento
boolean activar_calibracion = true;
int directionToGo = -1;
float targetAngle = 90;

void setup()
{  
    // Pin button as input
    pinMode(button1Pin, INPUT);
  
    // Interrupciones
    attachInterrupt(digitalPinToInterrupt(button1Pin), activationFinDeCarrera,FALLING);
  
  /*
    stepper1.setMaxSpeed(200.0);
    stepper1.setAcceleration(100.0);
    stepper1.moveTo(24);
    
    stepper2.setMaxSpeed(300.0);
    stepper2.setAcceleration(100.0);
    stepper2.moveTo(1000000);*/

    float angle = 360;
    
    stepper3.setMaxSpeed(10000.0);
    stepper3.setAcceleration(10000.0);
    stepper3.moveTo(angle*pulse_per_rev / 180); 

    calibrarMotor();
}

void loop()
{
    if (activar_calibracion)
    {
        calibrarMotor();
    }
    else{
      stepper3.setMaxSpeed(10000.0);
      // Change direction at the limits
      if (stepper3.distanceToGo() == 0)
        directionToGo = -1*directionToGo;
        stepper3.moveTo(directionToGo*targetAngle*pulse_per_rev / 180);
      //stepper1.run();
      //stepper2.run();
      stepper3.run();
    }
}

void calibrarMotor()
{
  stepper3.setMaxSpeed(1000.0);
  stepper3.moveTo(3600*pulse_per_rev / 180);  
  stepper3.run();
}

void activationFinDeCarrera()
{
  stepper3.setCurrentPosition(0);
  stepper3.moveTo(0);
  stepper3.setMaxSpeed(10000.0);
  activar_calibracion = false;
}
