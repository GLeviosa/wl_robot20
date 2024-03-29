#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Giovanni Santos, Victor Niubo"


import cv2

# Cria o detector BRISK
brisk = cv2.BRISK_create()

# Configura o algoritmo de casamento de features que vê *como* o objeto que deve ser encontrado aparece na imagem
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# Define o mínimo de pontos similares
MINIMO_SEMELHANCAS = 10


def find_good_matches(descriptor_image1, frame_gray):
    des1 = descriptor_image1
    kp2, des2 = brisk.detectAndCompute(frame_gray,None)

    # Tenta fazer a melhor comparacao usando o algoritmo
    matches = bf.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    return kp2, good

cap = cv2.VideoCapture(0)

original_rgb = cv2.imread("insper_logo.png") 
img_original = cv2.cvtColor(original_rgb, cv2.COLOR_BGR2GRAY)
#original_rgb = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB)

# Encontra os pontos únicos (keypoints) nas duas imagems
kp1, des1 = brisk.detectAndCompute(img_original ,None)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == False:
        print("Problema para capturar o frame da câmera")
        continue

    # Our operations on the frame come here
    frame_rgb = frame 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    kp2, good_matches = find_good_matches(des1, gray)

    if len(good_matches) > MINIMO_SEMELHANCAS:
        img3 = cv2.drawMatches(original_rgb,kp1,frame_rgb,kp2, good_matches, None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow('BRISK features', img3)
    else:
        cv2.imshow("BRISK features", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

