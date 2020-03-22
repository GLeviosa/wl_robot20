#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import math

i = int(input("Choose video: "))
lista_videos = ["test0.mp4","test1.mp4","test2.mp4"]

cap = cv2.VideoCapture(lista_videos[i])

def escapePoint(p1,p2,q1,q2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    
    x3 = q1[0]
    y3 = q1[1]
    x4 = q2[0]
    y4 = q2[1]
    
    delta_x0 = x2 - x1
    delta_y0 = y2 - y1
    
    delta_x1 = x4 - x3
    delta_y1 = y4 - y3
    
    m0 = delta_y0/delta_x0
    h0 = y1 - m0*x1
    
    m1 = delta_y1/delta_x1
    h1 = y3 - m1*x3
    
    xi = int((h1-h0)/(m0-m1))
    yi = int(m0*xi +h0)
    
    ps = [xi,yi]
    
    return ps
    
def dist(x,y):
    d = math.sqrt(x**2+y**2)
    return d

def coefAang(a,b):
    x0 = a[0]
    y0 = a[1]
    x1 = b[0]
    y1 = b[1]
    delta_x = x1 - x0
    delta_y = y1 - y0
    if delta_x == 0:
        delta_x = 0.1
    return delta_y/delta_x
    
def mediaPontos(l):
    soma_x = 0
    soma_y = 0
    if len(l) < 1:
        return [0,0]

    else:
        for i in l:
            soma_x += i[0]
            soma_y += i[1]
        media_x = int(soma_x/len(l))
        media_y = int(soma_y/len(l))
        ponto_medio = [media_x,media_y]
        return ponto_medio

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    # Our operations on the frame come here
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blur = cv2.GaussianBlur(gray,(5,5),0)
    bordas = auto_canny(blur)
    
    hough_img = bordas.copy() # Vamos reusar a imagem de canny

    lines = cv2.HoughLinesP(hough_img, 20, math.pi/180.0, 100, np.array([]), 50, 5)

    a,b,c = lines.shape

    hough_img_rgb = cv2.cvtColor(hough_img, cv2.COLOR_GRAY2RGB)

    linhas = [0,0,0,0]

    fuga_points = []
    for i in range(a):
        # Faz uma linha ligando o ponto inicial ao ponto final, com a cor vermelha (BGR)
        xp = lines[i][0][0]
        yp = lines[i][0][1]
        xs = lines[i][0][2]
        ys = lines[i][0][3]

        p = [xp,yp,dist(xp,yp)]
        s = [xs,ys,dist(xp,yp)]
        
        if (coefAang(p,s) > -2.7 and coefAang(p,s) < -0.7):
            if p[2] > linhas[2]:
                linhas[2] = p[2]
                linhas[0] = [p,s]
        elif coefAang(p,s) > 0.7 and coefAang(p,s) < 2.7:
            if p[2] > linhas[3]:
                linhas[3] = p[2]
                linhas[1] = [p,s]

        if linhas[0] == 0 or linhas[1] == 0:
            pass
        else:
            pf = escapePoint(linhas[0][0],linhas[0][1],linhas[1][0],linhas[1][1])
            fuga_points.append([pf[0],pf[1]])
            pm = mediaPontos(fuga_points)

            cv2.circle(hough_img_rgb,(pm[0],pm[1]),2,(0,255,0),2)
            cv2.line(hough_img_rgb, (linhas[0][0][0], linhas[0][0][1]), (linhas[0][1][0], linhas[0][1][1]), (0, 0, 255), 5, cv2.LINE_AA)
            cv2.line(hough_img_rgb, (linhas[1][0][0], linhas[1][0][1]), (linhas[1][1][0], linhas[1][1][1]), (0, 0, 255), 5, cv2.LINE_AA)
    
    cv2.imshow('img', hough_img_rgb)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
