#include <Servo.h>
#include "ESP8266.h"
#include <SoftwareSerial.h>

//Nombre de la red wifi a la que todos los dispositivos se conectan
#define SSID        "Danig"

//Password de la red wifi
#define PASSWORD    "volleyball"

//Nombre del host. Se obtiene del sv en Python.
//Usando la libreria socket, se llama a socket.gethostname()
#define HOST_NAME "DESKTOP-NS8ENN1"

//Puerto. Dejarlo asi
#define HOST_PORT (88)



SoftwareSerial ESP(3, 2); // RX, TX 
ESP8266 wifi(ESP,115200);

Servo myservo1;
Servo myservo2;
float datos[3] = {92.0, 83.0, 10.0};
int pos = 0;
 
void setup() 
{
   Serial.begin(115200);
   myservo1.attach(9);  // attaches the servo on pin 9 to the servo object
   myservo2.attach(10);  // attaches the servo on pin 9 to the servo object
   Serial.print("setup begin\r\n");
   delay(3000);
  
   if (wifi.joinAP(SSID, PASSWORD)) {
         Serial.print("Join AP success\r\n");
   }  
   else {
         Serial.print("Join AP failure\r\n");
   }
 
   Serial.print("setup end\r\n");
 
 
}
 
void loop()
{
  //Lectura de los datos
  delay(1000);

  //Conexion con la API
  uint8_t buffer[256] = {0};  

  if (wifi.createTCP(HOST_NAME, HOST_PORT)){
    //Serial.print("create tcp ok\r\n");

    
    uint32_t len = wifi.recv(buffer, sizeof(buffer), 5000);
    char coordenadas[len+1] = "";
    if (len >= 0) {
        for(uint32_t i = 0; i < len; i++) {
            coordenadas[i] = (char)buffer[i];
        }
        coordenadas[len]='\0';
        Serial.println(coordenadas);
        obtenerDatos(coordenadas);
        myservo1.write(datos[0]);
        myservo2.write(datos[1]);
     
    }
    
  }
  else {
    Serial.print("create tcp err\r\n");
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
