#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Giovanni Santos, Victor Niubo"


import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import auxiliar as aux
import math

# If you want to open a video, just change v2.VideoCapture(0) from 0 to the filename, just like below
#cap = cv2.VideoCapture('hall_box_battery.mp4')

# Parameters to use when opening the webcam.
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

lower = 0
upper = 1

font = cv2.FONT_HERSHEY_SIMPLEX

print("Press q to QUIT")

# Returns an image containing the borders of the image
# sigma is how far from the median we are setting the thresholds
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

H = 14
h = 243.2
D = 30

f = D*h / H

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # A gaussian blur to get rid of the noise in the image
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #blur = gray
    # Detect the edges present in the image
    bordas = auto_canny(blur)

    circles = []

    # Obtains a version of the edges image where we can draw in color
    bordas_color = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)

    # HoughCircles - detects circles using the Hough Method. For an explanation of
    # param1 and param2 please see an explanation here http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
    circles = None
    circles=cv2.HoughCircles(bordas,cv2.HOUGH_GRADIENT,2,40,param1=50,param2=100,minRadius=5,maxRadius=60)

    if circles is not None:        
        circles = np.uint16(np.around(circles))
        lista_c = []

        for i in circles[0,:]:
            lista_c.append(i)
            if len(lista_c) == 2:
                x0 = int(lista_c[0][0])
                x1 = int(lista_c[1][0]) 
                y0 = int(lista_c[0][1])
                y1 = int(lista_c[1][1])
                
                xf = abs(x0 - x1)

                yf = abs(y0 - y1)
            

                if xf > 1000 or yf > 1000:
                    pass
                else:
                    pit = math.sqrt(xf**2 + yf**2)
                    dist = f*H/pit

                    if xf == 0:
                        cv2.putText(bordas_color,str(90)+'graus',(100,100), font, 1,(255,255,255),2,cv2.LINE_AA)
                    else:
                        tang = float(yf)/float(xf)
                        seng = yf/dist
                        aang_rad = math.atan(tang)
                        aang_deg = math.degrees(aang_rad)
                        #print(tang,aang_deg,aang_rad,xf,yf)
                        cv2.putText(bordas_color,str(round(aang_deg, 2))+'graus',(0,100), font, 1,(255,255,255),2,cv2.LINE_AA)
    
                cv2.putText(bordas_color,str(round(dist,2))+'cm',(0,50), font, 1,(255,255,255),2,cv2.LINE_AA)
                

                cv2.line(bordas_color,(x0,y0),(x1,y1),(255,0,0),5)

            # draw the outer circle

            # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
            cv2.circle(bordas_color,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(bordas_color,(i[0],i[1]),2,(0,0,255),3)



    #More drawing functions @ http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html

    # Display the resulting frame
    cv2.imshow('Detector de circulos',bordas_color)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#  When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
