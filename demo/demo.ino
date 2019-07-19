#include <Servo.h>

Servo myservo1;
Servo myservo2;
float datos[3] = {92.0, 83.0, 10.0};
int pos = 0;
 
void setup() 
{
   Serial.begin(9600);
   myservo1.attach(9);  // attaches the servo on pin 9 to the servo object
   myservo2.attach(10);  // attaches the servo on pin 9 to the servo object
}
 
void loop()
{
   if (Serial.available()>0) 
   {
      String textoRecibido = Serial.readString();
      obtenerDatos(textoRecibido);
      myservo1.write(datos[0]);
      myservo2.write(datos[1]);
   }
}

void obtenerDatos(String textoRecibido){
  int contador = 0;
  int inicio = 0;
  for (int i = 0; i < textoRecibido.length(); i++)
  {
    if (textoRecibido.substring(i, i+1) == "#")
    {
      if (contador==1){
        datos[contador] = textoRecibido.substring(inicio,i).toFloat();
        datos[contador + 1] = textoRecibido.substring(i+1).toFloat();
      }
      else{
        datos[contador] = textoRecibido.substring(inicio,i).toFloat();
      }
      contador = contador + 1;
      inicio = inicio + i + 1;
    } 
  }  
}
