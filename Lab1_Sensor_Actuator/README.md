# Sensor & Actuator Programming

The objective of this laboratory exercise is to familiarize with the equipment and software that will be used for all labs and the project in ROB301. In particular:
* To learn about the robot’s hardware and its suite of sensors
* To learn how to write ROS programs to command the robot, i.e., 
  * How to write a simple Python ROS node
  * How to upload to the Waffle Pi
  * How to acquire data from the sensors
  * How to drive the actuators
  
The following commands should be run in separate terminal windows sequentially to properly start the ROS program:
```$roscore``` [Remote PC]

```$roslaunch turtlebot3_bringup turtlebot3_robot.launch``` [TurtleBot]

## Task 1: Publish to 'cmd_vel' 
The goal of this task is to command the wheel to go forward 1 m, then rotate 360◦and then stop. This is demonstrated in `l1_motor.py`.

## Task 2: Subscribe to 'odom'
The goal of this task is to retrieve the current pose of the robot. This is demonstrated in `l1_odometry.py`.
