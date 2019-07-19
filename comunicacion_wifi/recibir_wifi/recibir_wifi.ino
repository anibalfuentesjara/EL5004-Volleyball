/*
 * Codigo final para el envio de datos
 */

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



void setup(){
  Serial.begin(115200);
  Serial.print("setup begin\r\n");
  delay(3000);
  
  if (wifi.joinAP(SSID, PASSWORD)) {
        Serial.print("Join AP success\r\n");
        Serial.print("IP: ");       
        Serial.println(wifi.getLocalIP());
  } 
  else {
        Serial.print("Join AP failure\r\n");
  }
 
  Serial.print("setup end\r\n");
  
}

void loop(){

  //Lectura de los datos
  delay(500);

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
    }
    
  }
  else {
    Serial.print("create tcp err\r\n");
  }   
  
}
