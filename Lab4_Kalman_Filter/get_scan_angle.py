#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String

import matplotlib.pyplot as plt
import math
import numpy as np

def get_scan():
        scan = rospy.wait_for_message('scan', LaserScan)
       
        scan_filter = []
        for val in scan.ranges:
            if val == 0:
                scan_filter.append(30)
            else:
                scan_filter.append(val)


        in_range = np.array(scan_filter[0:180]) #only use the scan where y>=0 
        angles = np.array(range(0,180))*np.pi/180
        y_range = np.copy(in_range)*np.sin(np.copy(angles)) #computes the y-distance to each measurement
        x_range = np.copy(in_range)*np.cos(np.copy(angles)) # computes the x distance
        
        angles = np.where(np.logical_and(np.logical_and(y_range <=0.7,y_range>=0.5)==1, in_range < 3, np.abs(x_range) < 1.6)) #filter out measurements to ignore obstacles, people, or other detections, and anything over 3 m away

        median_angle = np.median(angles)
	print(median_angle)

    	return median_angle + 2

def main():
    rospy.init_node('get_scan_angle')
    scan_pub = rospy.Publisher('scan_angle', String, queue_size=1)
    rate = rospy.Rate(30)
    try:
    	while not rospy.is_shutdown():
        	ind = get_scan()
        	scan_pub.publish(str(ind))
		rate.sleep()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
