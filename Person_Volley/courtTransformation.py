import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import color

#Utils
def bgr2rgb(bgr_img):
    b,g,r = cv2.split(bgr_img)       
    rgb_img = cv2.merge([r,g,b])     
    return rgb_img

def find_nearest_line(lines, lineAprox):
    n_lines =len(lines)
    dist=np.zeros(n_lines)
    
    for i in range(n_lines):
        #Calculate similarity 
        dist[i] = np.linalg.norm(lineAprox-lines[i])

    sorted_index=np.argsort(dist)
    return lines[sorted_index[0]]

def transform_point(point, transformation_matrix):
    point = np.append(np.array(point),1)
    num1 = np.dot(transformation_matrix[0,:],point)
    num2 = np.dot(transformation_matrix[1,:],point)
    den = np.dot(transformation_matrix[2,:],point)
    return np.array([num1/den,num2/den])

def line_intersection(line1, line2):
    rho1, theta1 = line1[0]
    rho2, theta2 = line2[0]
    A = np.array([[np.cos(theta1),np.sin(theta1)],[np.cos(theta2),np.sin(theta2)]])
    B = np.array([[rho1],[rho2]])
    A_inv = np.linalg.inv(A)
    out = np.matmul(A_inv,B)
    return out[:,0]

def getCourtTransformMatrix(img, img_dibujo):
    puntos_conocidos = True
    if not puntos_conocidos:
        ### Esta parte del codigo se utiliza para encontrar los puntos para hacer la transformacion cuando los puntos son desconocidos
        ### En el caso del video presentado, los puntos para hacer la transformacion son conocidos, por lo que no se utiliza esta seccion
        ### del codigo
        #Initial approximation for the lines
        l0_aprox = [445, 1.57]
        l1_aprox = [544, 1.57]
        l2_aprox = [828.25, 0.349]
        l3_aprox = [946.75, 0]
        l4_aprox = [-940.25, 2.783]
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        lines = cv2.HoughLines(edges,0.5,np.pi/360,200)

        
        l0 = find_nearest_line(lines, l0_aprox)
        l1 = find_nearest_line(lines, l1_aprox)
        l2 = find_nearest_line(lines, l2_aprox)
        l3 = find_nearest_line(lines, l3_aprox)
        l4 = find_nearest_line(lines, l4_aprox)

        lines = [l0,l1,l2,l3,l4]
        line_length = 20000

        for line in lines:
            rho,theta=line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + line_length*(-b))
            y1 = int(y0 + line_length*(a))
            x2 = int(x0 - line_length*(-b))
            y2 = int(y0 - line_length*(a))

            #cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

        p2 = line_intersection(l1,l2)
        p3 = line_intersection(l0,l2)
        p4 = line_intersection(l1,l3)
        p5 = line_intersection(l0,l3)
        p6 = line_intersection(l1,l4)
        p7 = line_intersection(l0,l4)


    else: #Cuando los puntos para hacer la transformacion son conocidos (se tiene la camara fija)
        ### Puntos hardcodeados para el video
        escala_x = np.shape(img)[1]/1920
        escala_y = np.shape(img)[0]/1080
        p2 = [int(678*escala_x), int(298*escala_y)]
        p3 = [int(712*escala_x), int(189*escala_y)]
        p4 = [int(936*escala_x), int(304*escala_y)]
        p5 = [int(939*escala_x), int(195*escala_y)]
        p6 = [int(1200*escala_x), int(301*escala_y)]
        p7 = [int(1174*escala_x), int(199*escala_y)]

    intersection_points = np.array([p2,p3,p4,p5,p6,p7])
    puntos_dibujo_cancha = np.array([[296,113],[296,45],[365,113],[365,45],[433,113],[435,45]])

    #Plot points
    #for puntos in intersection_points:
    #    cv2.circle(img, (puntos[0], puntos[1]), 2, (0,0,255), -1)

    #Encontrar homografia y transformar imagen
    transformation_matrix, mask = cv2.findHomography(intersection_points, puntos_dibujo_cancha, method=cv2.RANSAC)

    return transformation_matrix