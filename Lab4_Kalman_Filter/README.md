# Kalman Filter

The objective of this exercise is to acquire hands-on experience with Kalman filtering for robot localization using the Turtlebot 3 Waffle Pi. In particular:

* To implement an extended Kalman filter for one-dimensional localization
* To test the filter on an idealized robotic mail-delivery task

The intended route for the robot consists of four addresses (and corresponding co-ordinates) as given in the table below.

| Address | Coordinates [cm] |
| :---: | :---: |
| 4 Bloor Street W | (61,0) |
| 8 Bloor Street W | (122,0) |
| 16 Bloor Street W | (244,0) |
| 20 Bloor Street W | (305,0) |

## Task 1: Line-Following Control
To begin, the line-following control (from Lab 3) is applied. This ensures that the robot can smoothly follow the designated line provided in the test course.

## Task 2: Unfiltered Localization 
The first demonstration is to localize the robot without the benefit of any filtering of sensor data. This will provide a baseline capability against which the benefits of Kalman filtering can be assessed. To accomplish this task, a starter code has been provided in `localizer.py`, which subscribes to the topic `/cmd_vel_noisy`. Using this velocity input, and `rospy`’s timing functions, a simple localization node is implemented which integrates the velocity over each discrete-time period to produce an estimate of the robot’s position. Note that `/cmd_vel_noisy` is the `/cmd_vel` topic with Gaussian noise added (due to the limited amount of space, odometry error does not significantly grow; the noise is added to simulate traveling overthe longer distances that a delivery robot would be required to traverse). To produce the simulated noise, run the node: 
```rosrun sessionX pub_noisy_vel.py```

## Task 3: Lidar Calibration
Before implementing the Kalman filter, the laser sensor (lidar) needs to be calibrated. A script has been provided that returns the bearing θ of the CN Tower. Running the node
```rosrun sessionX get_scan_angle.py```
publishes the angle to the topic `/scan_angle`. This script assumes that the laser-sensor reference frame is aligned with the robot’s reference frame. With real sensors, this is rarely the case. To calibrate the sensor, the robot is aligned with the CN Tower at a known angle and the measured bearing is checked. `get_scan_angle.py` is modified to account for the miscalibration of the laser sensor such that the node publishes the correct angle.

## Task 4: Extended Kalman Filter
The EKF is implemented in `lab4.py`, which fuses odometry measurements with the angular measurements of the Tower to localize the robot. The localization procedure is tested under the following conditions:

1. The localization procedure is demonstrated on the test course with *no* obstructions. The estimated position and the covariance are plotted over time.
2.  The localization procedure is demonstrated on the test course with obstructions. The estimated position and the covariance are plotted over time again. 

Bonus: An EKF should be sufficiently robust to deal with erroneous measurements and even missing measurements. The localization procedure is also tested with the robot starting from various erroneous initial positions.
