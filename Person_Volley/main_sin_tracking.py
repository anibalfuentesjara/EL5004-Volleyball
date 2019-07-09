import random
import os.path
import urllib.request
import torch
import numpy as np
import yolov3 as yolo
import cv2
from courtTransformation import getCourtTransformMatrix,transform_point
import time


def load_labels(path):
    with open(path) as file:
        labels = [line.rstrip('\n') for line in file]
        colors = ['#{:06x}'.format(random.randint(0, 0xFFFFFF)) for i in range(len(labels))]
        return labels, colors

def load_model():
    weights_path = 'data/yolov3-spp_final.weights'
    config_path = 'data/yolov3-spp.cfg'
    labels_path = 'data/obj.names'

    labels, colors = load_labels(labels_path)

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
   

    save_video = False

    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter('mapeo.mp4', fourcc, 20.0, (2*shape_dibujo[1],shape_dibujo[0]))

    #Video volley
    cap = cv2.VideoCapture('imagenes_videos/video_volley.mp4')
    while(True):
        ret, image = cap.read()

        #Resize por hardcodeo de puntos
        image = cv2.resize(image,(1920,1080))

        #detecciones
        detections = model(image)  

        #a veces falla por el video mal grabado uwu
        try:     
            transformation_matrix = getCourtTransformMatrix(image, img_dibujo)
        except:
            print('error (?)')
            continue

        #same
        if(transformation_matrix is None):
            continue

        #si hay detecciones
        if len(detections) > 0:
            for i, (x1, y1, x2, y2, obj_conf, cls_conf, cls_pred) in enumerate(detections[0]):
                x = round(x1.item())
                y = round(y1.item())
                w = round(x2.item() - x1.item())
                h = round(y2.item() - y1.item())

                #Dibujarlas
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)

                #Dibujar puntos a dibujo
                punto_cancha = np.array([x, y+h])
                punto_proyectado = transform_point(punto_cancha, transformation_matrix)
                cv2.circle(img_dibujo,(int(punto_proyectado[0]),int(punto_proyectado[1])), 10, (255,0,0), -1)

            
            #Realizar transformacion            
            img_transformed = cv2.warpPerspective(image, transformation_matrix, (shape_dibujo[1],shape_dibujo[0]))

        
        #Mostrar
        cv2.namedWindow( "Personas", cv2.WINDOW_NORMAL)

        out_frame = np.hstack((img_transformed, img_dibujo))
        cv2.imshow('Personas', out_frame)

        if save_video:
            out.write(out_frame)
        
        # cv2.namedWindow( "court", cv2.WINDOW_NORMAL  )
        # cv2.imshow('court', img_dibujo)

        #Para no sobreescribir dibujo
        img_dibujo = img_dibujo_copy.copy()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    if save_video:
        out.release()
if __name__ == '__main__':
    main()
