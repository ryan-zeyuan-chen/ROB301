#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String

my_pi = 3.14159265

def curve(s,l,a):
    r = rospy.Rate(10)
    cmd_pub = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.linear.x=s[0]
    twist.linear.y=s[1]
    twist.linear.z=s[2]
    twist.angular.x= s[2]/a
    twist.angular.y= s[1]/a
    twist.angular.z= s[0]/a
    t0 = rospy.Time.now().to_sec()
    distance = 0
    while (distance < l):
	    cmd_pub.publish(twist)
	    t1 = rospy.Time.now().to_sec()
	    distance = s[0]/a*(t1-t0)
	    r.sleep()
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0
    cmd_pub.publish(twist)
    pass

def straight(s,l):
    r = rospy.Rate(10)
    cmd_pub = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.linear.x=s[0]
    twist.linear.y=s[1]
    twist.linear.z=s[2]
    t0 = rospy.Time.now().to_sec()
    distance = 0
    while (distance < l):
	    cmd_pub.publish(twist)
	    t1 = rospy.Time.now().to_sec()
	    distance = s[0]*(t1-t0)
	    r.sleep()
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0
    cmd_pub.publish(twist)
    pass

def rotate(s,l):
    r = rospy.Rate(10)
    cmd_pub = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.angular.x= s[0]
    twist.angular.y= s[1]
    twist.angular.z= s[2]
    t0 = rospy.Time.now().to_sec()
    angle = 0
    while (angle < l):
	    cmd_pub.publish(twist)
	    t1 = rospy.Time.now().to_sec()
	    angle = s[2]*(t1-t0)
	    r.sleep()
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0
    cmd_pub.publish(twist)
    pass

def publisher_node():
    curve([0.2,0,0],my_pi*19/480+0.1,0.25)
    straight([0.2,0,0],2)
    curve([0.2,0,0],my_pi*379/480,0.25)
    pass


def main():
    try:
        rospy.init_node('motor')
        publisher_node()
    except rospy.ROSInterruptException:
        pass
    

if __name__ == '__main__':
    main()
