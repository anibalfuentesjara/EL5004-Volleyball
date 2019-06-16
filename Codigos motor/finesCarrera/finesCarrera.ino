// Pines de interrupcion.




// Dos pines, uno para la interrupion de cada fin de carrera.
 const int intPin1 = 2;
 const int intPin2 = 3;

//Estados de los fines de carrera.
volatile int countInt1 = 1;
volatile int countInt2 = 1;


 


void setup() {
  //Declaracion de las interrupciones.
  attachInterrupt(digitalPinToInterrupt(intPin1),finCarreraInt1,RISING);
  attachInterrupt(digitalPinToInterrupt(intPin2),finCarreraInt2,RISING);  
  
}

void loop() {
  // put your main code here, to run repeatedly:


  // En caso de que ocurra una interrupcion.
  if (countInt1%2){
    finCarrera1();
  }
  if (countInt2%2){
    finCarrera1();
  }

}



//Methods.
void finCarrera1(){
  
}

void finCarrera2(){
  
}


// Interruption methods.
void finCarreraInt1(){
  countInt1++;
}

void finCarreraInt2(){
  countInt2++;
}
