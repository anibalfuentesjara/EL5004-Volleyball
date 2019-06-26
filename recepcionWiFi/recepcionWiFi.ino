float datos[3];
String textoRecibido = "1.32#23.5#44.5";

void setup()
{
  Serial.begin(115200);  
}


void loop(){
  obtenerDatos(textoRecibido);
  delay(2000);
  Serial.println(datos[0]);  
  Serial.println(datos[1]);  
  Serial.println(datos[2]);  
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
