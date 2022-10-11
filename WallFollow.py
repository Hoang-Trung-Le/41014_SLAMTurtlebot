#!/usr/bin/env python

import imp
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

def move():
    rospy.init_node('robot', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    print("Move")
    speed = input("Input speed:")
    distance = input("Type distance:")
    isForward = input("Forward?: ")

    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    while not rospy.is_shutdown():

        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        while(current_distance < distance):

            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_distance = speed*(t1-t0)

        vel_msg.linear.x = 0
        velocity_publisher.publish(vel_msg)
        print('vel-published | lin_x =',vel_msg.linear.x,'| ang_z =',vel_msg.angular.z)

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass