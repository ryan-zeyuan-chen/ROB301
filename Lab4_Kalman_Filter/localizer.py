#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String

import matplotlib.pyplot as plt
import math
import numpy as np
import sys, select, os
if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class KalmanFilter(object):
    def __init__(self, h, d, x_0, Q, R, P_0):
        self.h = h
        self.d = d

        self.Q = Q
        self.R = R
        self.P = P_0
        self.x = x_0

        self.u = 0 # initialize the cmd_vel input
        self.phi = np.nan #initialize the measurement input
        self.phip = 0
        self.S = 0
        self.D = 0
        self.W = 0

        self.time = rospy.Time.now().to_sec()
        self.dt = 0.0
        
        self.state_pub = rospy.Publisher('state', String, queue_size = 1)
        self.xl = []
        self.Pl = []
        self.end = False

    def cmd_callback(self, cmd_msg):
        self.u = cmd_msg.linear.x

    ## scall_callback updates self.phi with the most recent measurement of the tower.
    def scan_callback(self, data):
        self.phi = float(data.data)*math.pi/180

    ## call within run_kf to update the state with the measurement 
    def predict(self, u = 0):
        self.dt = rospy.Time.now().to_sec() - self.time
        self.x = self.x + self.u * self.dt
        self.time = rospy.Time.now().to_sec()
        self.P = self.P + self.Q
        self.D = h/(h**2 +(d - self.x)**2)
        self.S = self.D*self.P*self.D + self.R
        self.W = self.P*self.D/self.S
        self.P = self.P - self.W*self.S*self.W
        self.Pl = self.Pl + [self.P]
        ##rospy.loginfo("TODO: update state via the motion model, and update the covariance with the process noise")
        return 

    ## call within run_kf to update the state with the measurement 
    def measurement_update(self):
        self.phip = math.atan2(h,d-self.x)
       ## rospy.loginfo("TODO: update state when a new measurement has arrived using this function")
        return

    def run_kf(self):
        current_input = self.u
        current_measurement = self.phi
        if math.isnan(current_measurement) == False:
              self.measurement_update()
              self.predict()
              self.x = self.x + self.W*(self.phi - self.phip)
              self.xl = self.xl + [self.x]
        else:
              self.predict()
              self.xl = self.xl + [self.x]
        if self.x > 3.05:
              self.end = True
       ## rospy.loginfo("TODO: complete this function to update the state with current_input and current_measurement")  
        self.state_pub.publish(str(float(self.x)))
	


if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
        
    rospy.init_node('Lab4')
    try:
        h = 0.6 #y distance to tower
        d = 1.5 #x distance to tower (from origin)  
        
        x_0 = 0 #initial state position
        
        Q = 1 #process noise covariance
        R = 1 #measurement noise covariance
        P_0 = 1 #initial state covariance 
        kf = KalmanFilter(h, d, x_0, Q, R, P_0)
        kf.scan_sub = rospy.Subscriber('scan_angle', String, kf.scan_callback, queue_size=1)
        kf.cmd_sub = rospy.Subscriber('cmd_vel_noisy', Twist, kf.cmd_callback)
        rospy.sleep(1)
        rate = rospy.Rate(30)
        while (not rospy.is_shutdown()) and (not kf.end):
            kf.run_kf()  
            rate.sleep()
        x = np.array(kf.xl)
        P = np.array(kf.Pl)
        plt.plot(x)
        plt.show()
        plt.plot(P)
        plt.show()
            
    #except:
        #print(e)

    finally:
        rospy.loginfo("goodbye")

