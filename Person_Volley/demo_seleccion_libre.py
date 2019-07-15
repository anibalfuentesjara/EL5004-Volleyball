import numpy as np
import cv2
from calculosLanzamiento import pass_function, calculo_orientacion_elevacion_velocidad, angulos_motores
import time
import serial


global punto_lanzamiento
punto_lanzamiento=(224,215)


def select(event, x, y, flags, param):
    global punto_lanzamiento
    if event == cv2.EVENT_LBUTTONUP:
        punto_lanzamiento=(x, y)


def main():
                        
    arduino_on = True
    try:
        arduino = serial.Serial("COM11", 9600)
        print("Comunicacion con el arduino exitosa")
    except:
        arduino_on = False
        print("No se puede comunicar con arduino")

    posicion_omni = (582, 216)

    # Dibujo
    img_dibujo = cv2.imread("imagenes_videos/dibujo_cancha.png",1)
    img_dibujo_copy = img_dibujo.copy()
    shape_dibujo = img_dibujo.shape

    #Variables para enviar a arduino
    orientacion=0
    elevacion=0
    velocidad=0

    #Trackbar para la altura sobre la malla
    cv2.namedWindow('Personas')
    cv2.createTrackbar('H sobre malla [cm]','Personas',100,200,pass_function)

    cv2.setMouseCallback('Personas', select)

    while(True):

        altura_sobre_malla = cv2.getTrackbarPos('H sobre malla [cm]','Personas')

        cv2.circle(img_dibujo, punto_lanzamiento, 10, (0,255,0), -1)

        orientacion, elevacion, velocidad = calculo_orientacion_elevacion_velocidad(punto_lanzamiento, 
            altura_sobre_malla = altura_sobre_malla, posicion_omni = posicion_omni)

        angulo_servo_1, angulo_servo_2 = angulos_motores(orientacion, elevacion)

        string_para_arduino = "{:.2f}".format(angulo_servo_1) + "#" + "{:.2f}".format(angulo_servo_2) + "#" + "{:.2f}".format(velocidad)
        string_2 = "orientacion: " + str(orientacion)+ " elevacion: " + str(elevacion)

        print(string_para_arduino)

        if arduino_on:
            arduino.write(string_para_arduino.encode())
 
        cv2.circle(img_dibujo,posicion_omni, 10, (0,0,255), -1)
        out_frame = img_dibujo
        cv2.imshow('Personas', out_frame)

        #Para no sobreescribir dibujo
        img_dibujo = img_dibujo_copy.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1.5)

    if arduino_on:
        arduino.close()

if __name__ == '__main__':
    main()