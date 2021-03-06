// MultiStepper.pde
// -*- mode: C++ -*-
//
// Shows how to multiple simultaneous steppers
// Runs one stepper forwards and backwards, accelerating and decelerating
// at the limits. Runs other steppers at the same time
//
// Copyright (C) 2009 Mike McCauley
// $Id: MultiStepper.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

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

// Define some steppers and the pins the will use

// USE: AccelStepper stepper(AccelStepper::FULL2WIRE, direction, pulse);

//AccelStepper stepper2(AccelStepper::FULL2WIRE, 6, 7);
//AccelStepper stepper2(AccelStepper::FULL2WIRE, 8, 9);
AccelStepper stepper3(AccelStepper::FULL2WIRE, 10, 11);
float pulse_per_rev = 5000;

void setup()
{  
  /*
    stepper1.setMaxSpeed(200.0);
    stepper1.setAcceleration(100.0);
    stepper1.moveTo(24);
    
    stepper2.setMaxSpeed(300.0);
    stepper2.setAcceleration(100.0);
    stepper2.moveTo(1000000);*/

    float angle = 360;
    
    stepper3.setMaxSpeed(10000.0);
    stepper3.setAcceleration(5000.0);
    stepper3.moveTo(angle*pulse_per_rev / 180); 
}

void loop()
{
    // Change direction at the limits
    if (stepper3.distanceToGo() == 0)
      stepper3.moveTo(-stepper3.currentPosition());
    //stepper1.run();
    //stepper2.run();
    stepper3.run();
}
