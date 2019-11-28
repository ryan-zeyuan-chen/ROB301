#!/usr/bin/env python

import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import matplotlib.pyplot as plt
import numpy as np
import re
import sys, select, os

my_pi = 3.14159265

if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

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

class BayesLoc:
    def __init__(self):
	#Subscribers
	self.colour_sub = rospy.Subscriber('mean_img_rgb', String, self.measurement_callback)
	self.line_idx_sub = rospy.Subscriber('line_idx', String, self.line_callback)
	self.cmd_pub= rospy.Publisher('cmd_vel', Twist, queue_size=1)
	#Color mapping and line changing
	self.color_map = color_map
	self.measured_rgb = np.array([0,0,0]) # updated with the measurement_callback
	self.line_idx = 0 # updated with the line_callback with the index of the detected black line.
	#Publishers
	self.state_pub = rospy.Publisher('state', String, queue_size = 1)
	self.color_pub = rospy.Publisher('color', String, queue_size = 1)
	#prior
	self.predict = [0.0]*12
	#posterior
	self.current = [1.0/12]*12
        self.initial = [1.0/12]*12
        self.u = 1
	# Predicted Address
        self.add = 0 #Predicted Address
        self.conf = 0.0 #Estimation confidence
        self.update = np.zeros((12,12)) #State Probability
        self.cnt = 0 #Counter of office
        self.goal = [4,6,8] #Targeted offices
	# P Control
	self.kp = 0.002
        self.r = rospy.Rate(20)
	self.desired = 320
	self.x = 0.03
	self.twist = Twist()
        
    
    def measurement_callback(self, msg):
	rgb = msg.data.replace('r:','').replace('b:','').replace('g:','').replace(' ','')
	r,g,b = rgb.split(',')
	r,g,b=(float(r), float(g),float(b))
	self.measured_rgb = np.array([r,g,b])

    def line_callback(self, data):
        index = int(data.data)
        self.line_idx = index
    
    def control(self):
        correction = 0
        error = self.desired - self.line_idx
        correction = self.kp*error
        #print('Error =', error, 'Corr =', correction)
        self.twist.linear.x = self.x
        self.twist.angular.z = correction
        self.cmd_pub.publish(self.twist)    
        #self.r.sleep()
        pass
    
    def forward(self):
        self.twist.linear.x = self.x
        self.twist.angular.z = 0
        self.cmd_pub.publish(self.twist)    
        self.r.sleep()
        pass

    def turn(self):
        self.twist.linear.x = 0
        self.twist.angular.z = 0.2
        self.cmd_pub.publish(self.twist)
        time = my_pi/4/0.1
        rospy.sleep(time)
        self.twist.linear.x = 0
        self.twist.angular.z = 0
        self.cmd_pub.publish(self.twist)
        rospy.sleep(1)
        self.twist.linear.x = 0
        self.twist.angular.z = -0.2
        self.cmd_pub.publish(self.twist)
        time = my_pi/4/0.1
        rospy.sleep(time)
        pass

    def state_predict(self, u):
        self.predict=[0.0]*12
        for i in range(len(self.current)):
            if u == 1:
                self.predict[(i-1)%12] += self.current[i]*0.05
                self.predict[i%12] += self.current[i]*0.10
                self.predict[(i+1)%12]+=self.current[i]*0.85
            elif u == 0:
                self.predict[(i-1)%12] += self.current[i]*0.05
                self.predict[i%12] += self.current[i]*0.90
                self.predict[(i+1)%12]+=self.current[i]*0.05
            elif u == -1:
                self.predict[(i-1)%12] += self.current[i]*0.85
                self.predict[i%12] += self.current[i]*0.10
                self.predict[(i+1)%12]+=self.current[i]*0.05
            else:
                print('ERR: invalid input')
                #raise err

    def normalize(self, l):
        norm = 0
        for i in range(len(l)):
            norm += l[i]
        for i in range(len(l)):
            l[i] = l[i]/norm
        return l
                
    def state_update(self, col):
        # Nothing = 0, Blue = 1, Green = 2, Yellow = 3, Orange = 4
        color_code = 'Nothing'
        # Check the office map in lab
        b_add = [4,8,9]
        g_add = [0,2,5]
        y_add = [3,7,11]
        o_add = [1,6,10]
        
        if col == 1: # Blue
            color_code = 'Blue'
            for i in b_add:
                self.current[i] = self.predict[i]*0.60
            for i in g_add:
                self.current[i] = self.predict[i]*0.20
            for i in y_add:
                self.current[i] = self.predict[i]*0.05
            for i in o_add:
                self.current[i] = self.predict[i]*0.05
        
        elif col == 2: # Green
            color_code = 'Green'
            for i in b_add:
                self.current[i] = self.predict[i]*0.20
            for i in g_add:
                self.current[i] = self.predict[i]*0.60
            for i in y_add:
                self.current[i] = self.predict[i]*0.05
            for i in o_add:
                self.current[i] = self.predict[i]*0.05
                
        elif col == 3: # Yellow
            color_code = 'Yellow'
            for i in b_add:
                self.current[i] = self.predict[i]*0.05
            for i in g_add:
                self.current[i] = self.predict[i]*0.05
            for i in y_add:
                self.current[i] = self.predict[i]*0.65
            for i in o_add:
                self.current[i] = self.predict[i]*0.20
        
        elif col == 4: #Orange
            color_code = 'Orange'
            for i in b_add:
                self.current[i] = self.predict[i]*0.05
            for i in g_add:
                self.current[i] = self.predict[i]*0.05
            for i in y_add:
                self.current[i] = self.predict[i]*0.15
            for i in o_add:
                self.current[i] = self.predict[i]*0.60
                
        elif col == 0: #Nothing
            for i in b_add:
                self.current[i] = self.predict[i]*0.10
            for i in g_add:
                self.current[i] = self.predict[i]*0.10
            for i in y_add:
                self.current[i] = self.predict[i]*0.10
            for i in o_add:
                self.current[i] = self.predict[i]*0.10
        else:
            print('ERR: invalid color code', col)
        
#         print(color_code)
        self.current = self.normalize(self.current) #Normalization
        #all_guess = []
        best_guess = max(self.current)
        best_location = self.current.index(best_guess)
        return best_location, best_guess

    def get_color(self, rgb):
        color = 0
        # Blue
        if rgb[0] < 60 and rgb[1] < 170 and rgb[1] > 50 and rgb[2] > 155:
            color = 1
        # Orange
        elif rgb[0] > 215 and rgb[1] < 165 and rgb[1] > 15 and rgb[2] < 5:
            color = 4
        # Yellow
        elif rgb[0] > 180 and rgb[1] > 140 and rgb[2] < 5:
            color = 3
        # Green
        elif rgb[0] < 180 and rgb[1] > 140 and rgb[2] < 5:
            color = 2
        return color
	
    def run(self):
        self.color = self.get_color(self.measured_rgb)
        #print(self.color)
        #return
        if self.color == 0: #Nothing
            self.control()
        else:
            self.forward()
            rospy.sleep(0.5)
            self.color = self.get_color(self.measured_rgb)
            if self.color == 0:
                self.control()
            else:
                self.state_predict(self.u)
                self.add, self.conf = self.state_update(self.color)
                self.update[self.cnt] = np.array(self.current)
                print(self.add, self.color, self.conf)
                self.cnt += 1
                if self.add in self.goal and self.conf > 0.5:
                    self.forward()
                    rospy.sleep(4.5)
                    self.turn()
                    self.forward()
                    rospy.sleep(4.5)
                else:
                    self.forward()
                    rospy.sleep(9)
            

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
      
    color_map = [0,1,2,3] ### A sample map with 4 colours in a row
                 
    rospy.init_node('bayes_loc')
    BL=BayesLoc()
    rospy.sleep(0.5)
    rate_main = rospy.Rate(20)
    
    ### Initialize your PID controller here ( to merge with the bayes_loc node )
    t0 = rospy.Time.now().to_sec()
    t = rospy.Time.now().to_sec() - t0
    try:
        while t<400:
            t = rospy.Time.now().to_sec() - t0
            key = getKey()
            if (key == '\x03'): #1.22:bayesian.curPos >= 1.6 or
                rospy.loginfo('Finished!')
                break
            BL.run()
            rospy.loginfo("Measurement: {}".format(BL.measured_rgb))
            #rospy.loginfo("Line index: {}".format(BL.line_idx))
            rate_main.sleep()
                
#    except Exception as e:
#        print("comm failed:{}".format(e))

    finally:

            ### Stop the robot when code ends
        cmd_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        cmd_publisher.publish(twist)
        # Plot
        x = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
        y = BL.update
        plt.subplot(6,1,1)
        plt.bar(x,BL.initial)
        plt.subplot(6,1,2)
        plt.bar(x,y[0])
        plt.subplot(6,1,3)
        plt.bar(x,y[1])
        plt.subplot(6,1,4)
        plt.bar(x,y[2])
        plt.subplot(6,1,5)
        plt.bar(x,y[3])
        plt.subplot(6,1,6) 
        plt.bar(x,y[4])
        plt.show()

        plt.subplot(6,1,1)
        plt.bar(x,y[5])
        plt.subplot(6,1,2)
        plt.bar(x,y[6])
        plt.subplot(6,1,3)
        plt.bar(x,y[7])
        plt.subplot(6,1,4)
        plt.bar(x,y[8])
        plt.subplot(6,1,5)
        plt.bar(x,y[9])
        plt.subplot(6,1,6)
        plt.bar(x,y[10])
        plt.show()

        plt.bar(x,y[11])
        plt.show()


