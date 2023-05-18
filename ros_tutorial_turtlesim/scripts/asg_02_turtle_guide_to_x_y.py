#!usr/bin/env python
 
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, pi
import time

current_pose = Pose()

def current_position_callback(data):
  global current_pose
  current_pose.x = data.x
  current_pose.y = data.y
  current_pose.theta = data.theta
  
def calculate_error(goal_pose, current_pose):
  error = Pose()
  error.x = goal_pose.x - current_pose.x
  error.y = goal_pose.y - current_pose.y
  error.theta = calculate_angle_b(error.y, error.x) - current_pose.theta
  return error
    
def calculate_angle_b(y_error, x_error):
  return (atan2(y_error, x_error) + 2 * pi) % (2 * pi)
  

rospy.init_node("turtle_guide_to_xy")
publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
current_position_subscriber = rospy.Subscriber("/turtle1/pose", Pose, current_position_callback)

rospy.set_param("x_target", float(input("Enter X: "))) 
rospy.set_param("y_target", float(input("Enter Y: ")))
rospy.set_param("threshold", 0.01)

rospy.loginfo("Moving to X: %s , Y: %s", str(rospy.get_param("x_target")), str(rospy.get_param("y_target")))

while not rospy.is_shutdown():
  # Set target coordinates
  goal_pose = Pose()
  goal_pose.x = rospy.get_param("x_target")
  goal_pose.y = rospy.get_param("y_target")
  threshold = rospy.get_param("threshold")
  
  velocity_msg = Twist()
  
  error = calculate_error(goal_pose, current_pose)
  distance = sqrt(pow(error.x, 2) + pow(error.y, 2))
  
  while abs(distance) >= threshold:
    error = calculate_error(goal_pose, current_pose)
    distance = sqrt(pow(error.x, 2) + pow(error.y, 2))
    
    rospy.logdebug("Current position X: %s , Y: %s", str(current_pose.x), str(current_pose.y))
  
    # applying constant rotation speed in the direction of the error.theta
    if abs(error.theta) > pi:
      if error.theta > 0:
        error.theta = error.theta - 2 * pi
      else:
        error.theta = error.theta + 2 * pi
    
    velocity_msg.angular.z = 1.5 * error.theta 
    
    publisher.publish(velocity_msg)
    time.sleep(0.5)
    velocity_msg.linear.x = 0.5 * distance
    
    publisher.publish(velocity_msg)
  
  rospy.loginfo("Target reached, Current position X: %s , Y: %s", str(current_pose.x), str(current_pose.y)) 
  break
   
time.sleep(0.1)
velocity_msg.angular.z = 0
velocity_msg.linear.x = 0
publisher.publish(velocity_msg)
  
rospy.spin()
    
    
