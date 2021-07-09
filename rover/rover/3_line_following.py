## This code is going to publish on topic "cmd_vel" and subscribe "/scan" topic
#  Written by Muhammad Luqman
# 8/6/21
from scipy import interpolate as inter
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time

class follow_wall_bot(Node):
    def __init__(self):
        super().__init__('Go_to_position_node') ## name of the node
        # publisher
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        #subscriber
        self.subscription=self.create_subscription(LaserScan,'/scan',self.get_scan_values,40)
        #periodic publisher call
        timer_period = 0.2;self.timer = self.create_timer(timer_period, self.send_cmd_vel)
        ## Initializing Global values
        self.linear_vel = 0.2 ## given a value
        self.velocity=Twist()
        self.region_1=0;self.region_2=0;self.region_3=0
        self.error=0
        self.case=""

    def get_scan_values(self,scan_data):
        ## We have 360 data points so we divide them in 3 region
        ## we say if there is something in the region get the smallest value
        
        self.region_1= min(min(scan_data.ranges[0:20])   , 100 )
        self.region_2= min(min(scan_data.ranges[20:40])  , 100 )
        self.region_3= min(min(scan_data.ranges[40:60])  , 100 )

        #print(self.region['left']," / ",self.region['mid']," / ",self.region['right'])
        # print(round(self.region_3,3)," / ",round(self.region_2,3)," / ",round(self.region_1,3),
        #         "/",round(self.error,3),"/",round(self.velocity.angular.z,3))
        
        print(round(self.region_3,3) ,"/",round(self.region_2,3),"/",round(self.region_1,3),"/",self.velocity.angular.z,"/",self.case )

    
    def cases(self,case_num):
        if(case_num ==1):
            self.case="Find the wall" ## go straight and find the wall
            self.velocity.linear.x=0.2
            self.velocity.angular.z=0.0
        elif(case_num==2):
            self.case="Following the wall"
            self.proporitonal_control()


        elif(case_num==3):
            self.case="Wall is ending , goint to take a turn"
            self.velocity.linear.x= self.linear_vel
            time.sleep(1500)
            self.velocity.angular.z=1.57
        elif(case_num==4):
            self.case="Wall is skipped"
            self.velocity.linear.x=0.4
            self.velocity.angular.z=0.0
            time.sleep(1000)
        elif(case_num==5):
            self.case="Straight Motion"
            self.velocity.linear.x=0.2

        else:
            self.case="Case Not programmed"
            
    def proporitonal_control(self):
        self.error = 1.2 - self.region_1
        if(self.error < -1.57):
            self.error = 1.57
        self.velocity.linear.x= self.linear_vel
        self.velocity.angular.z=(self.error)

    def send_cmd_vel(self):
        if(self.region_1<4): ## last ray block is on the wall
            self.case="basic"
            self.proporitonal_control()
            if(self.region_3 > 4 and self.region_2 > 4):## turning coming ahead
                self.case="TURN"
                self.velocity.linear.x= 0.4
                self.velocity.angular.z=-1.57
        

           
        self.publisher.publish(self.velocity)

def main(args=None):
    rclpy.init(args=args)
    oab=follow_wall_bot()
    rclpy.spin(oab)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
