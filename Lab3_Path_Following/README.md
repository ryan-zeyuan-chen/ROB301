# Path Following

The objective of this exercise is to introduce the foundational concepts of control theory and its practical use in mobile robotics using the Turtlebot 3 Waffle Pi. In particular:

* To implement a controller to execute path following in stages with
  1. a bang-bang controller
  2. a P controller 
  3. a PI controller 
  4. a PID controller
* To design and test a controller to follow a closed-circuit race course.

The following commands should be run in separate terminal windows sequentially to properly start the ROS program:
```$roscore``` [Remote PC]
`$roslaunch turtlebot3_bringup turtlebot3_robot.launch` [TurtleBot]
`$roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch` [TurtleBot]
`$rosrun sessionX lab3.py` [Remote PC]
