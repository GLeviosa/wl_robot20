#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import auxiliar as aux

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #hsv1, hsv2 = aux.ranges("#516679")
    #hsv3 , hsv4 = aux.ranges("#95434f")
    hsv1 = np.array([150,  50,  50])
    hsv2 = np.array([180, 255, 255])
    
    hsv3 = np.array([90, 45, 45])
    hsv4 = np.array([110, 255, 255])
    
    mask0 = cv2.inRange(frame_hsv, hsv1, hsv2)   
    mask1 = cv2.inRange(frame_hsv, hsv3, hsv4)

    mask2 = mask0 + mask1
     
    segmentado = cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,np.ones((15, 15)))

    contornos, arvore = cv2.findContours(segmentado.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    contornos_img = frame.copy()
    cv2.drawContours(contornos_img, contornos, -1, [0, 0, 255], 3)

    maior = [None]
    maior_area = [0]
    for c in contornos:
        area = cv2.contourArea(c)
        if area > maior_area:
            maior_area = area
            maior = c


    cv2.imshow('img', contornos_img)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
