# 41014_SLAMTurtlebot
	READ ME FOR CODE ONLY
_____________________________________________________________________________
# Currently Implemented on Turtlebot:
- Follow the right side wall and maneuver from straight ahead wall with a simple algorithm
- Update the subscribed data (current odometry, LiDAR scans) from ROS and assign to global variables
- Process LiDAR reading to determine wall avoiding logic 
- Build structure for code and internal commands for specific Turtlebot's action
- Block function built for update and no need to rebuild
- Complete basic Mapping of a customised floor plan constructed in Gazebo

# To Do (Future Work):
- Escape from Collision
- Complete exit from Collision and return to Go Ahead
- Can get through a small hole because SLAM detect is noisy
- Deal with real problem when real LIDAR is interfered by material	
- Detect the chosen target/position
_____________________________________________________________________________|
# How to apply the code

	1. Prerequisites 
	- Before starting ROS, make sure the IP address is up to date
	- Command:
		+ $ ifconfig (Find the assigned IP address)
		+ $ nano ~/.bashrc (Open and update ROS IP)
		+ $ source ~/.bashrc (Source the bashrc)
	
	2. Start ROS
	- Command:
		+ $ roscore


	3. Start Gazebo	
	- Command 
		+ $ roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
	- Manual input the mapp
		+File MAP A2
		
	4. Start RVIZ (SLAM)
	- Command:
		+ $ roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping
		or
		+ $ roslaunch turtlebot3_slam turtlebot3_slam.launch
	5. Running CODE in the IDE platform (VScode)
		Ctrl + C when Mapping is completed

	6. Save Map
	-Command:
		+ $ rosrun map_server map_saver -f ~/map

	7. Turn off the RVIZ SLAM and start RVIZ NAVI
	-Command:
		+ $ roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml

_____________________________________________________________________________	
# Individual Contributions

Actually, we have worked together and we all understand the code, algorithm, structure...
so individual work is quite  hard to determine. But basiclly, Khanh worked on calibration
the most, Nam focused on the  flow of data and Trung tried to build the structure. 

Then, 
	DIEN TRANG KHANH 30%,
	NAM VU 35%,
	TRUNG LE 35% 
for the coding only.

_____________________________________________________________________________	
# Progress Reports (CODE ONLY);

13/10/22 ALL TEAMS

- Divide code for simulation and real Demo
	- CODE for simulation: DONE
	- CODE for real Demo: Working....
- Find shortest path code (not the priority then using RVIZ packages)
- Delete Update nav_msgs.msg/ Path

.............................................................................
12/10/22
Nam Vu and Trung Le
- testing code and debug
- Update nav_msgs.msg/ Path
- Update logger and loginfor
- 

Trang Khanh Dien
- Do Calibration for Laser Scan
.............................................................................
5/10/22 
- Working on the Algorithms
	CODE LOGIC:
		ALGORITHM
				UPDATE CURRENT CHOICE
					CHOICE
					RETURN NEXT STATE
					RESET DATA
.............................................................................
4/10/22 TRANG KHANH DIEN
- Update Callback
	Callback for Laser
		Returns the range value of LiDAR
	Callback for Odometry
		Returns the value of global x and yaw

4/10/22 TRUNG LE
- Add rate sleep to the command
- When Turtlebot3 rotates, LaserScan is still active and interrupts rotation
- Update code:
	If (abs(current yaw - initial yaw) < pi/2)
		#Done turn
		rate.sleep()
	
4/10/22 NAM VU
- Updated orientation commands
- Rebuild flow code:

	Main: STATE (1 -> 6)
		CALLBACK()
			ALGORITHM
				UPDATE CURRENT CHOICE
					CHOICE
					RETURN NEXT STATE
		EACH STATE: DO 1 COMMAND
		
.............................................................................
21/9/22 TRUNG LE
- Update Structure for code
	Structure 1: State
	{
		Go Ahead
		Turn Left
		Turn Right
		Check Collision
		Go Ahead while turn left
		Go Ahead while turn right
	}
- Each State will be executed with different sets of commands, avoiding duplicate orders

- Updated Structure for laser data
	Structure 2: Laser
	{
		Angle 0
		Angle from 30 to 60
		...
	}

.............................................................................
20/9/22 TRANG KHANH DIEN
- Build minimun range for Lidar, want to use PID control so lidar will be
projected at angles of 30-60 for right and 300-330 for left.
- Update, no using PID
- Subscribe to LaserScan can scan data in 1 area
	min range [30:60] (Wall Follow)
	min range [0:15] && [345:359] (Ahead)

.............................................................................
16/9/22: NAM VU
- Update functions to use
	+Function (Move or Turn or Check)
		Declare global variable
		linear 
		angular
		return globle variable 

- Test the Functions. The functione
	inear = 1
		angular = 0
	current_choice = 2 (Turn)
		linear = 0
		angular = 1 (-1)  

.............................................................................
11/9/22: TRUNG LE
- Use Rosmsg and Rostopic to identify topics suitable for programming.
Select topic /cmd_vel (Twist()) as the main topic for moving the robot.
- Logic Code:
	+ Go Ahead (Pub in linear.x) and current distance (Sub in Odemetry)
		if current distance < distance (min distrance with wall) 
			Turn Left

11/9/22: TRANG KHANH DIEN
- Identify other Topics to subscribe to:
	+ sensor_msgs/LaserScan
	+ nav_msgs/Odometry
	+ Math
	+ Transformation

- Instead of determining the distance by a certain value, 
we can determine it by subscribing to the data in LaserScan.
- Logic Code: 
	+ If LaserScan < minimum variables
		Turn
	
.............................................................................
10/9/22: NAM VU
1. 
- Install packages (Gazebo, SLAM, Turtlebot3 Empty World,...) to prepare the code.

2. 
- The target will only be SLAM using 2D-lidar so the turtlebot will only need to be controlled by X, Y and YAW.

- Turtlebot does not have the ability to move along the Y axis, so there will only be X and YAW(THETA)

- Now the function will revolve around the forward and rotate commands.

- Like learning Mx2, send commands from the computer to the turtlebot to control it.
The commands will be divided into functions: Go straight, Turn Left, Turn Right, Check Wall.

- Update function: Escape Collision

- Logic code:
	Fing Wall -> Rotate to the Wall -> Approach the Wall -> Rotate Paralel -> Follow Wall
		if Wall -> Rotate left



