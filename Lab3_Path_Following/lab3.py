#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String

actual = 0

def callback(data):
    global actual
    rospy.loginfo(data)
    actual = int(data.data)

def publisher_node1():
    r = rospy.Rate(20)
    publisher = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.linear.x = 0.1
    twist.angular.z = 0
    publisher.publish(twist)
    t0 = rospy.Time.now().to_sec()
    t = rospy.Time.now().to_sec() - t0
    correction = 0
    desired = 320
    while t<20:
        t = rospy.Time.now().to_sec() - t0
        error = desired - actual
        if error < 0:
            correction = -0.4
        elif error > 0:
            correction = 0.4
        else:
            correction = 0
        twist.linear.x = 0.1
        twist.angular.z = correction
        publisher.publish(twist)
        r.sleep()
    twist.linear.x = 0
    twist.angular.z = 0
    publisher.publish(twist)
    pass

def publisher_node2():
    r = rospy.Rate(20)
    publisher = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.linear.x = 0.1
    twist.angular.z = 0
    publisher.publish(twist)
    t0 = rospy.Time.now().to_sec()
    t = rospy.Time.now().to_sec() - t0
    correction = 0
    desired = 320
    kp = 0.0075
    while t<25:
        t = rospy.Time.now().to_sec() - t0
        error = desired - actual
        correction = kp*error
        twist.linear.x = 0.1
        twist.angular.z = correction
        publisher.publish(twist)
        r.sleep()
    twist.linear.x = 0
    twist.angular.z = 0
    publisher.publish(twist)
    pass

def publisher_node3():
    r = rospy.Rate(20)
    publisher = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.linear.x = 0.1
    twist.angular.z = 0
    publisher.publish(twist)
    t0 = rospy.Time.now().to_sec()
    t = rospy.Time.now().to_sec() - t0
    correction = 0
    desired = 320
    integral = 0
    ki = 0.00005
    kp = 0.0075
    while t<25:
        t = rospy.Time.now().to_sec() - t0
        error = desired - actual
        integral = integral + error
        correction = kp*error + ki*integral
        twist.linear.x = 0.1
        twist.angular.z = correction
        publisher.publish(twist)
        r.sleep()
    twist.linear.x = 0
    twist.angular.z = 0
    publisher.publish(twist)
    pass

def publisher_node4():
    r = rospy.Rate(20)
    publisher = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    twist=Twist()
    twist.linear.x = 0.1
    twist.angular.z = 0
    publisher.publish(twist)
    t0 = rospy.Time.now().to_sec()
    t = rospy.Time.now().to_sec() - t0
    correction = 0
    desired = 320
    integral = 0
    derivative = 0
    lasterror = 0
    kd = 0.0075
    ki = 0.00005
    kp = 0.0075
    while t<25:
        t = rospy.Time.now().to_sec() - t0
        error = desired - actual
        integral = integral + error
        derivative = error - lasterror 
        correction = kp*error + ki*integral + kd*derivative
        twist.linear.x = 0.1
        twist.angular.z = correction
        publisher.publish(twist)
        lasterror = error
        r.sleep()
    twist.linear.x = 0
    twist.angular.z = 0
    publisher.publish(twist)
    pass

def main():
    try:
        rospy.init_node('motor')
        rospy.Subscriber("color_mono", String, callback)
        publisher_node4()
    except rospy.ROSInterruptException:
        pass
    

if __name__ == '__main__':
    main()
