import random
import os.path
import urllib.request
import torch
import numpy as np
import matplotlib.pyplot as plt
import yolov3 as yolo
import cv2
from courtTransformation import getCourtTransformMatrix,transform_point
from calculosLanzamiento import pass_function, calculo_orientacion_elevacion_velocidad
import time


from sort import Sort

Persons_pos=[]
Person_des=[]
inputw=720
inputh=480
outputw=720
outputh=480
def select(event, x, y, flags, param):

    global Persons_pos,Person_des
 
    # if event == cv2.EVENT_LBUTTONDOWN:

    
    #Transformacion de tamaños
    x*=inputw/outputw
    y*=inputh/outputh
    if event == cv2.EVENT_LBUTTONUP:

        for Person in Persons_pos:
            #print(Person[0],Person[1], Person[3]+Person[1] , Person[2], Person[2]+Person[4],"|",x,y)
            if Person[1]<=x and Person[3]+Person[1]>=x and Person[2]<=y and Person[2]+Person[4]>=y:

                Person_des=[Person[0]]


def load_model():
    weights_path = 'data/yolov3-spp_final.weights'
    config_path = 'data/yolov3-spp.cfg'
    #labels_path = 'data/obj.names'

    # Create YOLO detector
    model = yolo.Detector(config_path=config_path,
                          weights_path=weights_path,
                          input_size=(544, 608),
                          conf_thresh=0.5,
                          nms_thresh=0.4)

    if torch.cuda.is_available():
        model.cuda()  
    
    return model


def main():
                        
    model = load_model()

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

    #sort
    mot_tracker = Sort()
    cmap = plt.get_cmap('tab20b')
    colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

    #Trackbar para la altura sobre la malla
    cv2.namedWindow('Personas')
    cv2.createTrackbar('H sobre malla [cm]','Personas',100,200,pass_function)
    cv2.namedWindow('Camera')

    cv2.setMouseCallback('Camera', select)

    while(True):
        ret, image = cap.read()

        #Resize por hardcodeo de puntos
        image = cv2.resize(image,(inputw,inputh))#1920,1080

        

        #a veces falla por el video mal grabado uwu
        try:     
            transformation_matrix = getCourtTransformMatrix(image, img_dibujo)
        except:
            print('error (?)')
            continue

        #same
        if(transformation_matrix is None):
            continue

        altura_sobre_malla = cv2.getTrackbarPos('H sobre malla [cm]','Personas')

        #detecciones
        detections = model(image)  
        #si hay detecciones
        global Persons_pos,Person_des
        if len(detections) > 0:
            tracked_objects = mot_tracker.update(detections[0].cpu())
            unique_labels = detections[0][:, -1].cpu().unique()
            n_cls_preds = len(unique_labels)
            #for i, (x1, y1, x2, y2, obj_conf, cls_conf, cls_pred) in enumerate(detections[0]):
            for x1, y1, x2, y2, obj_id, cls_pred in tracked_objects:

                # x = round(x1.item())
                # y = round(y1.item())
                # w = round(x2.item() - x1.item())
                # h = round(y2.item() - y1.item())

                x = int(x1)
                y = int(y1)
                w = int(x2 - x1)
                h = int(y2 - y1)

                #color = colors[int(obj_id) % len(colors)]
                #color = [i * 255 for i in color]
                color=(255,0,0)
                if len(Person_des)>0 and str(int(obj_id))==Person_des[0]:
                    color=(0,255,0)



                #cls = classes[int(cls_pred)]
                #print(i, ':', label, 'x:', x, 'y:', y, 'w:', w, 'h:', h)


                #Dibujarlas
                #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)                
                cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
                #cv2.rectangle(image, (x, y-35), (x+len(cls)*19+60, y), color, -1)
                cv2.putText(image,  str(int(obj_id)), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                Persons_pos.append([str(int(obj_id)),x,y,w,h])
                #Dibujar puntos a dibujo
                punto_cancha = np.array([x, y+h])
                punto_proyectado = transform_point(punto_cancha, transformation_matrix)
                cv2.circle(img_dibujo,(int(punto_proyectado[0]),int(punto_proyectado[1])), 10, color, -1)

                if len(Person_des)>0 and str(int(obj_id))==Person_des[0]:
                	orientacion, elevacion, velocidad = calculo_orientacion_elevacion_velocidad(punto_proyectado,altura_sobre_malla = altura_sobre_malla)
                	print("")
                	string_para_arduino = "{:.2f}".format(orientacion) + "#" + "{:.2f}".format(elevacion) + "#" + "{:.2f}".format(velocidad)
                	print(string_para_arduino)

            
            #Realizar transformacion            
            #img_transformed = cv2.warpPerspective(image, transformation_matrix, (shape_dibujo[1],shape_dibujo[0]))

        
        #Mostrar
        #cv2.namedWindow( "Personas", cv2.WINDOW_NORMAL)

        #out_frame = np.hstack((img_transformed, img_dibujo))  
        out_frame = img_dibujo
        cv2.imshow('Personas', out_frame)#out_frame
        cv2.imshow('Camera', cv2.resize(image,(outputw,outputh)))
        
        
        # cv2.namedWindow( "court", cv2.WINDOW_NORMAL  )
        # cv2.imshow('court', img_dibujo)

        #Para no sobreescribir dibujo
        img_dibujo = img_dibujo_copy.copy()

        if save_video:
            out.write(out_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if save_video:
        out.release()
if __name__ == '__main__':
    main()

