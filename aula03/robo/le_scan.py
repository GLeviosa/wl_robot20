#! /usr/bin/env python
# -*- coding:utf-8 -*-


import rospy
import numpy as np
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

dist = 0

def scaneou(dado):
    global dist
    print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
    print("Leituras:")
    x = (np.array(dado.ranges).round(decimals=2))[0]
    print(x)
    dist = x
    #print("Intensities")
    #print(np.array(dado.intensities).round(decimals=2))

    


if __name__=="__main__":

    rospy.init_node("le_scan")

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
    recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)



    while not rospy.is_shutdown():
        if dist >= 1.02:
            v = 0.05
        elif dist <= 1:
            v = -0.05
        velocidade = Twist(Vector3(v, 0, 0), Vector3(0, 0, 0))
        velocidade_saida.publish(velocidade)
        rospy.sleep(0.2)