/*
 * Programa para la calibración del motor.
 * Movimiento de motores stepper asociados al omniwrist.
 * Beauchef Proyecta: Proyecto -> Lanzador Volleyball.
 */

/*
 *Stepper Motor Connections:
  Motor-Driver
  A+ red
  A- green
  B+ yellow
  B- blue
 * 
 */

//Inclusion de la libreria.
#include <AccelStepper.h>

// Variables de fines de carrera
const int interruptPin1 = 2;    // Numero del pin a interrumpir. Fin de carrera 0 grados.
const int interruptPin2 = 3;    // Numero del pin a interrumpir. Fin de carrera 180 grados.

//Variables del motor.
float pulse_per_rev = 5000;   // Numero de pulsos por revolucion (fijar esto mismo en el driver).


//Variables para el movimiento
boolean activar_calibracion = true;
//Sentido de rotación del motor. (Anti-horario).
int directionToGo = -1;

float targetAngle = 90;

// Definir el objeto stepper3 correspondiente a la clase AccelStepper.
// USE: AccelStepper stepper(AccelStepper::FULL2WIRE, direction, pulse);
// Pines: 10 -> Direccion;
//        11 -> Pulso;
AccelStepper stepper3(AccelStepper::FULL2WIRE, 10, 11);

void setup()
{  
    // Pin button as input
    pinMode(interruptPin1, INPUT);
  
    // Interrupciones
    //Interrupcion 0 grados.
    attachInterrupt(digitalPinToInterrupt(interruptPin1), activationFinDeCarrera0,FALLING);
    //Interrupcion 180 grados.
    attachInterrupt(digitalPinToInterrupt(interruptPin2), activationFinDeCarrera1,FALLING);
    // Configuraciones iniciales del motor.
    stepper3.setMaxSpeed(10000.0);
    stepper3.setAcceleration(10000.0);
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

/*
 * Metodos.
 */
 
//Metodo para la calibracion del motor.
void calibrarMotor()
{
  //Lentamente girar hasta llegar al fin de carrera.
  stepper3.setMaxSpeed(1000.0);
  //Fijar posicion a moverse, en este caso se le da una posicion lejana, para que llegue al fin de carrera.
  stepper3.moveTo(3600*pulse_per_rev / 180);  
  //Instruccion de moverse.
  stepper3.run();
}

// Metodos interrupciones.

//Activacion fin de carrera 0 grados.
void activationFinDeCarrera0()
{
  stepper3.setCurrentPosition(0);
  stepper3.moveTo(0);
  stepper3.setMaxSpeed(10000.0);
  activar_calibracion = false;
}

//Activacion fin de carrera 180 grados.
void activationFinDeCarrera180()
{
  stepper3.setCurrentPosition(180);
  stepper3.moveTo(180);
  stepper3.setMaxSpeed(10000.0);
  activar_calibracion = false;
}
