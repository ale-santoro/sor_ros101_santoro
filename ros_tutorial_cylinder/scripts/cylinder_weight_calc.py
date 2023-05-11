#!usr/bin/env python
import rospy
from std_msgs.msg import Float64
from ros_tutorial_cylinder.msg import Cylinder

density = 0
volume = 0

density_found = False
volume_found = False

def cylinder_callback(data):
  global volume
  global volume_found
  msg = data
  volume = msg.volume
  volume_found = True
  
  
def density_callback(data):
  global density
  global density_found
  density = data.data
  density_found = True


def calculate_weight():
  if density_found and volume_found:
    weight = volume * density
    publisher.publish(weight)
    
    
rospy.init_node("cylinder_weight_calc")
cylinder_subscriber = rospy.Subscriber("/cylinder", Cylinder, cylinder_callback)
density_subscriber = rospy.Subscriber("/density", Float64, density_callback)
publisher = rospy.Publisher("/weight", Float64, queue_size=10)

while not rospy.is_shutdown():
  calculate_weight()
  rospy.sleep(0.1)
