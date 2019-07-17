# EL5004-Volleyball
EL5004 Taller de diseño - Beauchef Proyecta. Proyecto de lanzador de balones de volleyball.

El objetivo del proyecto es realizar un lanzador de balones de volleyball, con el fin de facilitar los entrenamientos del DR de volleyball de la Universidad de Chile y de la rama de volleyball de la universidad. Para esto se trabaja en conjunto con equipos de Ingeniería Eléctrica e Ingeniería Mecánica. El sistema tiene como requisito el poder apuntar el lanzador, ajustar la velocidad de lanzamiento e incorporar un sistema de detección de personas y distintas rutinas de práctica.

El repositorio cuenta con lo siguiente:

- Omni Wrist III: Diseños stl, Solid Edge y Fusion 360 para la base del sistema. Esta base consiste en el sistema Omni Wrist III, que a través de dos motores logra apuntar en los ejes de libertad Pitch y Roll.

- Códigos motor: códigos en arduino para el movimiento de los motores.

- Person Volley: sistema de visión computacional desarrollado en python mediante la librería pytorch. Es el mismo que se adjunta en el github de visión.

- Parabolas: cálculo de parábolas en el lanzamiento del balón.

- Planos eléctricos y lista de materiales: lista de materiales y hardware eléctrico.

- arduino_python: código de arduino que recibe señales de control desde python y mueve servomotores. Es usado en la demo con el modelo 3D impreso.

- comunicacion_wifi: códigos para comunicación wifi entre python y arduino.

- fin de carrera: códigos de fines de carrera.

## Google Drive

Se presentan diversos videos grabados en prácticas del DR.

https://drive.google.com/drive/folders/1kx5sKdnLs_XCrbL7N90hBN0Ewg4CD0pJ

## Sistema de vision

Se presenta el github del sistema de visión y el google drive con los pesos utilizados por el sistema de visión.

https://github.com/Jackerz312/Person_Volley

https://drive.google.com/drive/folders/1hPUGl7ACIlWxsmZmfyyrUkmBOFc591Y6?usp=sharing
