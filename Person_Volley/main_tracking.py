import random
import os.path
import urllib.request
import torch
import numpy as np
import matplotlib.pyplot as plt
import yolov3 as yolo
import cv2
from courtTransformation import getCourtTransformMatrix,transform_point
from calculosLanzamiento import pass_function, calculo_orientacion_elevacion_velocidad, angulos_motores
import time
import serial
from centroidtracker import CentroidTracker

#from sort import Sort

Persons_pos=[]
Person_des=[]
inputw=608
inputh=544
outputw=720
outputh=480
FONT = cv2.FONT_HERSHEY_SIMPLEX

def select(event, x, y, flags, param):
    global Persons_pos,Person_des   
    #Transformacion de tamaños
    x*=inputw/outputw
    y*=inputh/outputh
    if event == cv2.EVENT_LBUTTONUP:
        for Person in Persons_pos:
            if Person[1]<=x and Person[3]>=x and Person[2]<=y and Person[4]>=y:
                Person_des=[Person[0]]


def load_model(tiny = False):

    if tiny:
        weights_path = 'data/yolov3-tiny_final.weights'
        config_path = 'data/yolov3-tiny.cfg'
    else:
        weights_path = 'data/yolov3-spp_final.weights'
        config_path = 'data/yolov3-spp.cfg'
    #labels_path = 'data/obj.names'

    # Create YOLO detector
    model = yolo.Detector(config_path=config_path,
                          weights_path=weights_path,
                          input_size=(544, 608),
                          conf_thresh=0.25,
                          nms_thresh=0.4)

    if torch.cuda.is_available():
        model.cuda()  
    
    return model


def main():
                        
    model = load_model(tiny=False)
    arduino_on = True
    try:
    	arduino = serial.Serial("COM11", 9600)
    	print("Comunicacion con el arduino exitosa")
    except:
    	arduino_on = False
    	print("No se puede comunicar con arduino")

    n_frames_comunicacion=12
    iterador_comunicacion=0

    posicion_omni = (582, 216)

    # Dibujo   
    img_dibujo = cv2.imread("imagenes_videos/dibujo_cancha.png",1)
    img_dibujo_copy = img_dibujo.copy()
    shape_dibujo = img_dibujo.shape

    #Variables para enviar a arduino
    orientacion=0
    elevacion=0 
    velocidad=0
   

    save_video = False    
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter('mapeo.mp4', fourcc, 20.0, (2*shape_dibujo[1],shape_dibujo[0]))
    #Video volley
    cap = cv2.VideoCapture('imagenes_videos/video_volley2.mp4')

    
    #Tracker
    ct = CentroidTracker(maxDisappeared=60)

    #Trackbar para la altura sobre la malla
    cv2.namedWindow('Personas')
    cv2.createTrackbar('H sobre malla [cm]','Personas',100,200,pass_function)
    cv2.namedWindow('Camera')

    cv2.setMouseCallback('Camera', select)
    calculate_detections = True
    detections_aux = None
    while(True):
        #time1 = time.time()
        ret, image = cap.read()

        if ret==False:
            print("Video terminado")
            break
        #Resize por hardcodeo de puntos
        image = cv2.resize(image,(inputw,inputh))#1920,1080  

        #a veces falla por el video mal grabado uwu
        try:   
            transformation_matrix = getCourtTransformMatrix(image, img_dibujo)
        except:
           continue

        #same
        if(transformation_matrix is None):
            continue

        altura_sobre_malla = cv2.getTrackbarPos('H sobre malla [cm]','Personas')

        #detecciones
        if calculate_detections:            
            detections = model(image)   
            detections_aux = detections
            
        else:
            detections= detections_aux     
        calculate_detections = not calculate_detections

        global Persons_pos,Person_des

        if detections[0] is not None:            
        
            rects = detections[0].cpu().detach().numpy()[:,:4]
            objects = ct.update(rects)
            
            for obj_id ,(x1, y1, x2, y2) in objects.items():         

                x1 = int(x1.item())
                y1 = int(y1.item())
                x2 = int(x2.item())
                y2 = int(y2.item())
                
                color = (148.0, 81.0, 165.0)
                color_selection = (82.0, 162.0, 140.0)  
                Persons_pos.append([str(obj_id),x1,y1,x2,y2])

                punto_cancha = np.array([x1, y2])
                punto_proyectado = transform_point(punto_cancha, transformation_matrix)

                if len(Person_des)>0 and str(int(obj_id))==Person_des[0]:
                    color=color_selection
                    orientacion, elevacion, velocidad = calculo_orientacion_elevacion_velocidad(punto_proyectado, altura_sobre_malla = altura_sobre_malla)

                    angulo_servo_1, angulo_servo_2 = angulos_motores(orientacion, elevacion)

                    string_para_arduino = "{:.2f}#{:.2f}#{:.2f}".format(angulo_servo_1,angulo_servo_2,velocidad)
                    string_2 = "orientacion: {} elevacion: {}".format(orientacion,elevacion)

                    print(string_2)
                    if arduino_on:
                    	if (iterador_comunicacion%n_frames_comunicacion==0):
                        	arduino.write(string_para_arduino.encode())

                    	iterador_comunicacion+=1

                # Dibujar en imagen
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
               
                text =  str(obj_id)
                cv2.rectangle(image,(x1-2,y1-25) , (x1 + 10,y1) , color,-1)
                cv2.putText(image,text,(x1,y1-5), FONT, 0.5,(255,255,255),1,cv2.LINE_AA)                

                #Dibujar puntos a dibujo
                cv2.circle(img_dibujo,(int(punto_proyectado[0]),int(punto_proyectado[1])), 10, color, -1)
        
        cv2.circle(img_dibujo,posicion_omni, 10, (0,0,255), -1)
        out_frame = img_dibujo
        cv2.imshow('Personas', out_frame)#out_frame
        cv2.imshow('Camera', cv2.resize(image,(outputw,outputh)))
        
       # print(time.time()-time1)
        # cv2.namedWindow( "court", cv2.WINDOW_NORMAL  )
        # cv2.imshow('court', img_dibujo)

        #Para no sobreescribir dibujo
        img_dibujo = img_dibujo_copy.copy()

        if save_video:
            out.write(out_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #arduino.close()
    cap.release()
    if save_video:
        out.release()
if __name__ == '__main__':
    main()