#
import rospy
import numpy as np

#
from math import pi
from math import atan2
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry, OccupancyGrid, Path
from geometry_msgs.msg import Twist, Pose2D, Point, PoseStamped

#Publish and Subscribe // Some topic was subscribed into the function
pub1 = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)


#Global variables
xo = 0
theta = 0
r = []
cur_val = -1 #current value for turtlebot3's state control
cur_sta = 0 #current state of turtlebot3

state = {   #states of turtlebot3 #state structure
    0: 'D', # Go Ahead
    1: 'TurnL', # Turn Left
    # 2: 'TurnR',
    # 3: 'N', #Stop and check collision
    # 4: 'NL', #Check then turn left to escape collision
    # 5: 'NR', #Check then turn right to escape collision
}

section = {
    'zero':0, #Angle 0
    'nine':0, #Angle 90
    'twos':0, #Angle 270
    'onee':0, #Angle 180
}

# Callback function for command function
def callback(msg):
    global xo
    global theta

    xo = msg.pose.pose.position.x 
    rot = msg.pose.pose.orientation
    (roll,pitch, theta) = euler_from_quaternion([rot.x, rot.y, rot.z, rot.w])

def callback1(msg):
    global r
    r = msg.ranges
    
rospy.Subscriber("/odom", Odometry, callback)
rospy.Subscriber("/scan", LaserScan, callback1)
#Command
#vel_msg = Twist()


#Command functions
def change(num_sta): #choice of current state in the state structure
    global cur_sta
    if num_sta is not cur_sta:
        cur_sta = num_sta

def Goahead(): #Go straight ahead
    vel_msg = Twist()
    vel_msg.linear.x = 0.1
    vel_msg.angular.z = 0
    return vel_msg

def CheckCol():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    return vel_msg

def TurnL():
    rate = rospy.Rate(10)

    
    vel_msg = Twist()
    if len(r):
        rangeAhead = r[0]
        
        if (rangeAhead < 0.26):
            yawInit = theta
            yawCurr = theta
            while (abs(yawCurr - yawInit) < pi/2):
                rospy.logerr('TURNINGGGGGG') #DEBUG
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0.1
                yawCurr = theta
                pub1.publish(vel_msg)
                rate.sleep()
    return vel_msg

    # vel_msg = Twist()
    # rospy.logerr('DEBUG')
    # vel_msg.linear.x = 0
    # vel_msg.angular.z = 0.1
    # return vel_msg
    
def TurnR():
    rate = rospy.Rate(10)

    vel_msg = Twist()
    if len(r):
        rangeAhead = r[0]
        
        if (rangeAhead < 0.3):
            yawInit = theta
            yawCurr = theta
            while (abs(yawCurr - yawInit) < pi/2):

                vel_msg.linear.x = 0
                vel_msg.angular.z = -0.1
                yawCurr = theta
                pub1.publish(vel_msg)
                rate.sleep()
    return vel_msg

def CheckColL(): #Turn left when detect wall
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0.15
    return vel_msg

def CheckColR(): #Turn right when detect wall
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.angular.z = -0.15
    return vel_msg
    
#Callback functions


def callback2(msg):
    global section

    range = np.array(msg.ranges)
    section = {
        'zero':min(range[0:30]) and min(range[340:359]),
        'nine':min(range[85:95]),
        'twos':min(range[265:275]),
        'onee':min(range[175:185]),
    }
    Algorithm()
    
    
#Algorithm of control
def Algorithm():
    global cur_val  
    min = 0.26
    rospy.loginfo("Direction {f}".format(f=cur_val))
    
    if section['zero'] > min :  
        change(0)
        
    elif cur_val == -1: #Find direction for robot
        if section['zero'] > min:
            change(0)
            cur_val = 0
        elif section['zero'] < min:
            change(1)
            cur_val = 1          
        else:
            rospy.loginfo('Next Value')
    else:
        rospy.loginfo('Good Initial') #Just for DEBUG
        cur_val  = 1
        
    if cur_val == 0: # Go ahead
        rospy.logerr('GOING')
        if section['zero'] < min:
            change(1)            
        
    if cur_val == 1: # Turn left
        rospy.loginfo('TURNING LEFT')
        if section['zero'] > min:
            change(0)
        if section['zero'] < min:
            change(1)
            cur_val = -1

    #FUTURE WORK
    # if cur_val == 2: # Right
    #     rospy.logerr('SAI RIGHT') #DEBUG
    #     if section['zero'] < min:
    #         change(4)
    #     elif section['twos'] < min:
    #         change(1)
    #     else:
    #         change(0)       
    
    # if cur_val == 3: # Check collision
    #     rospy.logerr('SAI CHECK') #DEBUG
    #     if section['zero'] > min and section['nine'] > min and section['twos'] > min and section ['onee'] > min:
    #         change(0)
    #     else:
    #         cur_val = -1   
             
    # if cur_val == 4: # Check collision then turn L
    #     rospy.logerr('SAI CHECK L') #DEBUG
    #     if section['zero'] > min and section['nine'] > min and section['twos'] > min and section ['onee'] > min:
    #         change(0)
    #     else:
    #         change(0)     
                
    # if cur_val == 5: # Check collision then turn R
    #     rospy.logerr('SAI CHECK R') #DEBUG
    #     if section['zero'] > min and section['nine'] > min and section['twos'] > min and section ['onee'] > min:
    #         change(0)
    #     else:
    #         change(0)               
    
  
#Main
def main():
    rospy.init_node('SLAM')
    rospy.loginfo("Press Ctrl + C to terminate")
    rospy.Subscriber('/scan', LaserScan, callback2)
    while not rospy.is_shutdown():
        vel_msg = Twist()
        if cur_sta == 0:
            vel_msg = Goahead()
        elif cur_sta == 1:
            vel_msg = TurnL()
        # elif cur_sta == 2:
        #     vel_msg = TurnR()
        # elif cur_sta == 3:
        #     vel_msg == CheckCol()
        # elif cur_sta == 4:
        #     vel_msg = CheckColL()
        # elif cur_sta == 5:
        #     vel_msg == CheckColR()         
        else:
            rospy.logerr('NO STATE DETECT')
            break
        pub1.publish(vel_msg)
    rospy.spin()
    
if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Action terminated.")