####
# - Main purpse is Obstical Avoiding by using LIDAR sensor  
# - Any object comes inside of scan Robot takes sharp turn
# - This code is going to publish on topic "cmd_vel" and
#    subscribe "/scan" topic
#
#  Written by Muhammad Luqman
#  ros2,FOXY
#  13/6/21
#
###
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoidingBot(Node):
    def __init__(self):
        super().__init__('Go_to_position_node') ## name of the node
        # publisher
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 40)
        #subscriber
        self.subscription=self.create_subscription(LaserScan,'/scan',self.get_scan_values,40)
        #periodic publisher call
        timer_period = 0.2;self.timer = self.create_timer(timer_period, self.send_cmd_vel)
        ## Initializing Global values
        ## given a value for VELOCITY
        self.linear_vel = 0.22 
        ## Making dictionary to divide the area of lase scan 
        self.regions={'right':[],'mid':[],'left':[]}
        ## creating a message object to fit new velocities and publish them
        self.velocity=Twist()


    ## Subscriber Callback function 
    def get_scan_values(self,scan_data):
        ## We have 360 data points and we are dividing them in 3 regions
        ## we say if there is something in the region get the smallest value
        self.regions = {
        'right':   int(min(min(scan_data.ranges[0:120])  , 100)),
        'mid':     int(min(min(scan_data.ranges[120:240]), 100)),
        'left':    int(min(min(scan_data.ranges[240:360]), 100)),
        }
        print(self.regions['left']," / ",self.regions['mid']," / ",self.regions['right'])

  
    ## Callback Publisher of velocities called every 0.2 seconds
    def send_cmd_vel(self):
        ## angular and linear velocities are set into object self.velcity
        ## setting the linear velocity to be fixed and robot will keep on moving
        self.velocity.linear.x=self.linear_vel
        ## cases to make the robot change its angular velocity
        if(self.regions['left'] > 4  and self.regions['mid'] > 4   and self.regions['right'] > 4 ):
            self.velocity.angular.z=0.0 # condition in which area is total clear
            print("forward")
        elif(self.regions['left'] > 4 and self.regions['mid'] > 4  and self.regions['right'] < 4 ):
            self.velocity.angular.z=1.57# object on right,taking  left 
            print("right")
        elif(self.regions['left'] < 4 and self.regions['mid'] > 4  and self.regions['right'] > 4 ):
            self.velocity.angular.z=-1.57 #object  on left, taking  right
            print("left")          
        elif(self.regions['left'] < 4 and self.regions['mid'] < 4  and self.regions['right'] < 4 ):
            self.velocity.angular.z=3.14# object ahead take full turn
            print("reverse")
        else:## lThis code is not completed ->  you have  to add more conditions  ot make it robust
            print("some other conditions are required to be programmed") 
       
        ## lets publish the complete velocity
        self.publisher.publish(self.velocity)

def main(args=None):
    rclpy.init(args=args)
    oab=ObstacleAvoidingBot()
    rclpy.spin(oab)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
