#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String

my_pi = 3.14159265
actual = 0
distance = 0

def callback(data):
    global actual
    actual = int(data.data)

def callback1(data):
    global distance
    rospy.loginfo(data)
    distance = float(data.data)

def publisher_node():
    r = rospy.Rate(30)
    publisher = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.linear.x = 0.1
    twist.angular.z = 0
    publisher.publish(twist)
    correction = 0
    desired = 320
    kp = 0.003
    i = 0
    address = [0.61,1.22,2.44,3.05]
    while distance < 3.1 and i < 4:
        error = desired - actual
        correction = kp*error
        twist.linear.x = 0.1
        twist.angular.z = correction
        publisher.publish(twist)
        if distance > address[i]: 
             twist.linear.x = 0
             twist.angular.z = 0
             publisher.publish(twist)
             i = i+1
             rospy.sleep(2)
        r.sleep()
    twist.linear.x = 0
    twist.angular.z = 0
    publisher.publish(twist)
    pass

def main():
    try:
        rospy.init_node('motor')
        rospy.Subscriber("color_mono", String, callback)
        rospy.Subscriber('state', String, callback1)
        publisher_node()
    except rospy.ROSInterruptException:
        pass
    

if __name__ == '__main__':
    main()
