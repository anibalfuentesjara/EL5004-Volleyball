# EL5004-Volleyball
EL5004 Taller de diseño - Beauchef Proyecta. Proyecto de lanzador de balones de volleyball.

El objetivo del proyecto es realizar un lanzador de balones de volleyball, con el fin de facilitar los entrenamientos del DR de volleyball de la Universidad de Chile y de la rama de volleyball de la universidad. Para esto se trabaja en conjunto con equipos de Ingeniería Eléctrica e Ingeniería Mecánica. El sistema tiene como requisito el poder apuntar el lanzador, ajustar la velocidad de lanzamiento e incorporar un sistema de detección de personas y distintas rutinas de práctica.

El repositorio cuenta con lo siguiente:

- Informe: informe final del ramo.

- Presentación: presentación final del ramo.

- Omni Wrist III: Diseños stl, Solid Edge y Fusion 360 para la base del sistema. Esta base consiste en el sistema Omni Wrist III, que a través de dos motores logra apuntar en los ejes de libertad Pitch y Roll.

- Códigos motor: códigos en arduino para el movimiento de los motores.

- Person Volley: sistema de visión computacional desarrollado en python mediante la librería pytorch. Es el mismo que se adjunta en el github de visión.

- Parabolas: cálculo de parábolas en el lanzamiento del balón.

- Planos eléctricos y lista de materiales: lista de materiales y hardware eléctrico.

- demo: código de arduino que recibe señales de control desde python y mueve servomotores. Es usado en la demo con el modelo 3D impreso.

- comunicacion_wifi: códigos para comunicación wifi entre python y arduino.

- fin de carrera: códigos de fines de carrera.

## Google Drive

Se presentan diversos videos grabados en prácticas del DR.

https://drive.google.com/drive/folders/1kx5sKdnLs_XCrbL7N90hBN0Ewg4CD0pJ

## Sistema de vision

Se presenta el github del sistema de visión y el google drive con los pesos utilizados por el sistema de visión.

https://github.com/Jackerz312/Person_Volley

https://drive.google.com/drive/folders/1hPUGl7ACIlWxsmZmfyyrUkmBOFc591Y6?usp=sharing

## Demo

Se realiza una remo con el modelo del omniwrist impreso en 3D. Para correr la demo el esquemático del circuito es el siguiente:

![Esquematico demo](https://github.com/anibalfuentesjara/EL5004-Volleyball/blob/master/demo/demo.png)

Se debe tener cuidado de conectar cada servo en el pin correspondiente. El arduino debe estar conectado con el computador mediante usb. Se debe cargar en arduino el programa demo.ino de la carpeta demo, teniendo cuidado de tener conectado el servo 1 al pin 9 y el servo 2 al pin 10. Luego, existen dos programas de python, en la carpeta person_volley:

- demo_seleccion_libre.py: permite seleccionar un punto en la cancha y apuntar el omni-wrist en esa dirección. En la línea 22 del código se debe tener cuidado de seleccionar el puerto donde está conectado el arduino.

- main_tracking.py: permite seleccionar una persona en el sistema de visión computacional y realizar un tracking de la persona. La persona se selecciona haciendo click sobre la persona en el video. En la línea 64 del código se debe tener cuidado de seleccionar el puerto donde está conectado el arduino. Se puede usar un modelo más rápido cambiando en la línea 61 del código por tini=True.
