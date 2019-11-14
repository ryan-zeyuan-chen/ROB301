#!/usr/bin/env python

import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import numpy as np
import re
import sys, select, os
if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

actual = 0
distance = 0

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

class PIDcontrol:

    def __init__(self):
        self.x = 0.05
        self.publisher = rospy.Publisher('cmd_vel',Twist,queue_size=1)
        self.r = rospy.Rate(20)
        self.twist=Twist()
        self.desired = 320
        self.kp = 0.0015
        self.ki = 0.00005
        self.kd = 0.0015
        self.integral = 0
        self.lasterror = 0
        self.twist.linear.x = self.x
        self.twist.angular.z = 0
        self.publisher.publish(self.twist)  

    def run(self):
        correction = 0
        error = self.desired - BL.line_idx
        self.integral = self.integral + error
        derivative = error - self.lasterror 
        correction = self.kp*error
        self.twist.linear.x = self.x
        self.twist.angular.z = correction
        self.publisher.publish(self.twist)    
        self.lasterror = error
        self.r.sleep()
        pass

    def forward(self):
        self.twist.linear.x = self.x
        self.twist.angular.z = 0
        self.publisher.publish(self.twist)    
        self.r.sleep()
        pass

class BayesLoc:

    def __init__(self, color_map):
        self.colour_sub = rospy.Subscriber('mean_img_rgb', String, self.measurement_callback)
        self.line_idx_sub = rospy.Subscriber('line_idx', String, self.line_callback)
        self.cmd_pub= rospy.Publisher('cmd_vel', Twist, queue_size=1)

        self.color_map = color_map
        self.measured_rgb = np.array([0,0,0]) # updated with the measurement_callback
        self.line_idx = 0 # updated with the line_callback with the index of the detected black line.

 
    def measurement_callback(self, msg):
        rgb = msg.data.replace('r:','').replace('b:','').replace('g:','').replace(' ','')
        r,g,b = rgb.split(',')
        r,g,b=(float(r), float(g),float(b))
        self.measured_rgb = np.array([r,g,b])
        
    def line_callback(self, data):
        index = int(data.data)
        self.line_idx = index

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
      
    color_map = [0,1,2,3] ### A sample map with 4 colours in a row
                 
    rospy.init_node('bayes_loc')
    BL=BayesLoc(color_map)
    rospy.sleep(0.5)
    
    ### Initialize your PID controller here ( to merge with the bayes_loc node )
    #PID = PIDcontrol()
    t0 = rospy.Time.now().to_sec()
    t = rospy.Time.now().to_sec() - t0
    try:
        while t<40:
            t = rospy.Time.now().to_sec() - t0
            key = getKey()
            if (key == '\x03'): #1.22:bayesian.curPos >= 1.6 or
                rospy.loginfo('Finished!')
                break
            #if max(BL.measured_rgb) > 175:
                #PID.forward()
            #else:
                #PID.run()
            rospy.loginfo("Measurement: {}".format(BL.measured_rgb))
            rospy.loginfo("Line index: {}".format(BL.line_idx))
                
#    except Exception as e:
#        print("comm failed:{}".format(e))

    finally:

            ### Stop the robot when code ends
        cmd_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        cmd_publisher.publish(twist)





