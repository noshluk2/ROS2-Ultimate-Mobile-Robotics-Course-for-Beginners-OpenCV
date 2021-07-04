import rclpy
from rclpy.node import Node
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoidingBot(Node):
    def __init__(self):
        super().__init__('Go_to_position_node')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 40)
        self.subscription=self.create_subscription(LaserScan,'/scan',self.get_scan_values,40)
        timer_period = 0.2;self.timer = self.create_timer(timer_period, self.send_cmd_vel)
        ## Initializing Global values
        self.linear_vel = 0.22
        self.velocity=Twist()
        self.regions={'right':[],'mid':[],'left':[]}

    def get_scan_values(self,scan_data):
        self.regions = {
        'right':     min(min(scan_data.ranges[0:120])  , 100),
        'mid':      min(min(scan_data.ranges[120:240]), 100),
        'left':    min(min(scan_data.ranges[240:360]), 100),
        }
        ## testing defined regions
        # print("///////left     = ", self.regions['left']) 
        # print("///////mid      = ", self.regions['mid'])
        # print("///////right    = ", self.regions['right'])


    

    def send_cmd_vel(self):
        self.velocity.linear.x=self.linear_vel
        if(self.regions['left'] > 4  and self.regions['mid'] > 4   and self.regions['right'] > 4 ):
            self.velocity.angular.z=0.0 # condition in which area is total clear
            # print("1")
        elif(self.regions['left'] > 4 and self.regions['mid'] > 4  and self.regions['right'] < 4 ):
            self.velocity.angular.z=-0.4 # right,taking slight left 
            # print("2")
        elif(self.regions['left'] > 4  and self.regions['mid'] < 4   and self.regions['right'] > 4 ):
            self.velocity.angular.z=1.1 #mid , object in the middle
            # print("3")
        elif(self.regions['left'] > 4  and self.regions['mid'] < 4    and self.regions['right'] < 4 ):
            self.velocity.angular.z=-1.0 # mid and right
            # print("4")
        elif(self.regions['left'] < 4 and self.regions['mid'] > 4  and self.regions['right'] > 4 ):
            self.velocity.angular.z=0.4 #left, taking slight right
            # print("5")
        elif(self.regions['left'] < 4 and self.regions['mid'] > 4  and self.regions['right'] < 4 ):
            self.velocity.angular.z=0.0 #left,right, going straight 
            # print("6")
        elif(self.regions['left'] < 4 and self.regions['mid'] < 4  and self.regions['right'] > 4 ):
            self.velocity.angular.z=4.0 #left and mid , taking right turn
            # print("7")
        elif(self.regions['left'] < 4 and self.regions['mid'] < 4  and self.regions['right'] < 4 ):
            self.velocity.linear.x=0.0 #object ahead close
            # print("8")
        print(self.regions['left']," / ",self.regions['mid']," / ",self.regions['right'])
        self.publisher.publish(self.velocity)

def main(args=None):
    rclpy.init(args=args)
    oab=ObstacleAvoidingBot()
    rclpy.spin(oab)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
