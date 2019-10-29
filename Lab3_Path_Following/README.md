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

```$roslaunch turtlebot3_bringup turtlebot3_robot.launch``` [TurtleBot]

```$roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch``` [TurtleBot]

```$rosrun sessionX lab3.py``` [Remote PC]

## Task 1: Bang-Bang Control
With no knowledge of control theory, bang-bang control is often the first method considered in stabilizing a system.  As the name implies, the intent is to observe the environment for the  actual  state  of  the  system  and  move  toward  the  desired  state  with  maximal  control commands. This is demonstrated in `publisher_node1()` of `lab3.py`.

## Task 2: Proportional Control
One of the most basic controllers is the proportional-gain controller. The intent of this controller is to observe the environment for the actual state of the system and move toward the desired state more smoothly than the bang-bang type. As the error increases, the control command has greater influence. This is demonstrated in `publisher_node2()` of `lab3.py`.

The value of k<sub>p</sub> can be determined in multiple ways. If a mathematical model of the plant is known, then a controller can be designed to stabilize it. Alternatively, when the plant model is not known, too complex or uncertain, an iterative approach to gain selection can be used. With an iterative approach, the proportional gain value is, at first, set very low and tested. It is then increased until the system becomes oscillatory. Half of this value of k<sub>p</sub> is usually used as the final gain as in accordance with the Ziegler-Nichols method.
