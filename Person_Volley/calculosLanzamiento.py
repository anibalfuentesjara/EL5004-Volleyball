
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import color
import math

def pass_function(x):
    pass

def calculo_elevacion_velocidad(punto_malla, punto_persona, punto_omni=(0, 1)):
    """
    Calculo de la elevacion del omni y la velocidad de lanzamiento
    input:
    punto_malla: (x, y) de la ubicacion de la malla
    punto_persona: (x, y) de la ubicacion de la persona
    punto_omni: (x, y) de la ubicacion del omniwrist
    output:
    elevacion (radianes)
    velocidad (m/s)
    """
    #Ajuste de parabola
    coordenadas_x = [punto_omni[0], punto_malla[0], punto_persona[0]]
    coordenadas_y = [punto_omni[1], punto_malla[1], punto_persona[1]]
    coeficientes_parabola = np.polyfit(coordenadas_x, coordenadas_y, 2)

    #Calculo de elevacion (con pendiente de parabola evaluada en el x del omni)
    elevacion_pendiente = 2*coeficientes_parabola[0]*punto_omni[0]+coeficientes_parabola[1]
    elevacion_angulo = math.atan2(elevacion_pendiente,1)

    #Calculo de velocidad
    gravedad=-9.81
    v_0 = np.sqrt((0.5*gravedad*punto_persona[0]**2) / 
                 (np.cos(elevacion_angulo)**2 * ((punto_persona[1]-punto_omni[1])-
                                                  np.tan(elevacion_angulo)*punto_persona[0])))
    return elevacion_angulo, v_0
    

def calculo_orientacion_elevacion_velocidad(posicion_persona, altura_sobre_malla = 50, posicion_omni = (582, 216)):
    """
    calculo de la orientacion, elevacion y velocidad del omniwrist para el lanzamiento a una persona
    input:
    posicion_persona: (p_x, p_y) pixeles de la ubicacion de la persona en la cancha
    altura_sobre_malla: altura en centimetros por la que pasara el balon sobre la malla
    posicion_omni: (p_x, p_y) posicion (pixeles) del omni wrist en la imagen 
    output:
    orientacion: angulo de orientacion del omniwrist en grados
    elevacion: angulo de elevacion del omniwrist en grados
    velocidad: velocidad de lanzamiento del balon (m/s)
    """

    x_malla = 364
    pixeles_a_metros_x = 18/(572-158)
    pixeles_a_metros_y = 9/(320-113)

    # Distancias en x
    a = (posicion_omni[0] - x_malla)*pixeles_a_metros_x
    b = (x_malla - posicion_persona[0])*pixeles_a_metros_x
    # Distancia en y
    c = (posicion_omni[1] - posicion_persona[1])*pixeles_a_metros_y

    #Si la persona esta a la derecha de la malla
    if posicion_persona[0] > x_malla:
        #print('La persona debe estar al otro lado de la cancha') 
        orientacion = math.atan2(c, (a+b))
        cos_orientacion = np.cos(orientacion)
        d_mas_e = (a+b) / cos_orientacion
        d = d_mas_e/2
        e = d_mas_e/2
        punto_malla = (d, 2.6+altura_sobre_malla/100)
        punto_persona = (d_mas_e, 1)
        elevacion, velocidad = calculo_elevacion_velocidad(punto_malla, punto_persona)
        return orientacion*180/np.pi, elevacion*180/np.pi, velocidad

    #Si la persona esta a la izquierda de la malla
    else:
        # Calculo de orientacion
        orientacion = math.atan2(c, (a+b))

        #
        cos_orientacion = np.cos(orientacion)
        d = a / cos_orientacion
        e = (a+b) / cos_orientacion - d

        punto_malla = (d, 2.6+altura_sobre_malla/100)
        punto_persona = (d+e, 1)
        elevacion, velocidad = calculo_elevacion_velocidad(punto_malla, punto_persona)
        return orientacion*180/np.pi, elevacion*180/np.pi, velocidad

def angulos_motores(orientacion, elevacion):
    """
    Calcula el angulo que se le debe dar a ambos motores para apuntar el omni wrist, dada la orientacion horizontal del omni-wrist
    y la elevacion del mismo
    Input:
    orientacion: orientacion horizontal en la que debe apuntar el omni-wrist (en grados), una orientacion positiva es en sentido horario respecto
    al omni-wrist y una orientacion negativa es en sentido antihorario
    elevacion: angulo de elevacion (en grados) respecto al plano horizontal que debe tener el omni-wrist
    Output:
    angulo_servo_1: angulo que se le debe dar al servomotor 1
    angulo_servo_2: angulo que se le debe dar al servomotor 2
    """
    #Transforma la orientacion y elevacion a coordenadas esfericas
    theta = 90-elevacion
    phi = -1*orientacion

    #Calcula el angulo alpha y beta (angulos respecto a la posicion default del omni-wrist)
    alpha = (np.arcsin(np.sin(theta*np.pi/180)*np.cos(phi*np.pi/180))/2)*180/np.pi
    beta = (np.arcsin(np.sin(theta*np.pi/180)*np.sin(phi*np.pi/180)))*180/np.pi

    #Calcula el angulo que se le indica al servomotor (considerando la posicion default de los servomotores)
    angulo_servo_1 = 92-alpha
    angulo_servo_2 = 90+beta

    return angulo_servo_1, angulo_servo_2