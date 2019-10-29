# Pose-to-Pose Control

The objective of this laboratory exercise is to study feedforward or open-loop pose-to-posemotion control of the robot. In particular:

* To study pose-to-pose control using a straight-line path
* To study pose-to-pose control using waypoints with straight-line segments
* To study pose-to-pose control using curved paths

For the purposes of this lab, the robot can be modeled as an “unicycle,” whose pose is given by three degrees of freedom: x, y and θ, as measured in a global reference frame. In short, **x** = [x y θ] with x, y in units of cm and θ in degrees. 

## Task 1: Pose-to-Pose Locomotion Using a Straight-Line Path
To demonstrate the basics of locomotion, the robot is commanded to move from a start pose **x**<sub>Start</sub> to a goal pose **x**<sub>Goal</sub>, with **x**<sub>Start</sub> = [0 0 0] and **x**<sub>Goal</sub> = [200 50 135]. The most direct way is to plan a straight-line path from the start to the goal and have the robot follow it.

## Task 2: Pose-to-Pose Locomotion Via Waypoints
In this demonstration, the robot is moved through a square path, defined by waypoints A, B, C, back to its original pose. That is, let **x**<sub>Start</sub> = [0 0 0], **x**<sub>A</sub> = [100 0 90], **x**<sub>B</sub> = [100 100 180], **x**<sub>C</sub> = [0 100 270] and **x**<sub>Goal</sub> = **x**<sub>Start</sub>. 

## Task 3: Pose-to-Pose Locomotion Along a Curved Path
Unfortunately, some robots may not be capable of pivoting on the spot. In this case, it would be necessary to design a curved path for the robot tofollow. Assuming that the minimum turning radius for the robot is 25 cm, design a paththat will take it from start to goal as given in Task 1. This task is demonstrated in `lab2.py`. 
