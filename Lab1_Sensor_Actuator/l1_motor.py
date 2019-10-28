#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String


def publisher_node():
    r = rospy.Rate(10)
    cmd_pub = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.linear.x=0.25
    twist.angular.z=0

    t0 = rospy.Time.now().to_sec()
    distance = 0
    while (distance < 1.25):
	cmd_pub.publish(twist)
	t1 = rospy.Time.now().to_sec()
	distance = 0.25*(t1-t0)
	r.sleep()
    #msg = Float()
    #msg.data = distance
    #rospy.loginfo(msg.data)
    #cmd_pub.publish(msg)
    twist.linear.x = 0
    cmd_pub.publish(twist)

    t0 = rospy.Time.now().to_sec()
    twist.angular.z=0.3
    angle = 0
    while (angle < 7):
	cmd_pub.publish(twist)
	t1 = rospy.Time.now().to_sec()
	angle = 0.3*(t1-t0)
	r.sleep()
    #msg.data = angle
    #rospy.loginfo(msg.data)
    #cmd_pub.publish(msg)
    twist.angular.z = 0
    cmd_pub.publish(twist)
    pass


def main():
    try:
        rospy.init_node('motor')
        publisher_node()
    except rospy.ROSInterruptException:
        pass
    

if __name__ == '__main__':
    main()
