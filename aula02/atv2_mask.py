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
     
    segmentado_cor = cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,np.ones((15, 15)))
    cv2.imshow('img', segmentado_cor)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
