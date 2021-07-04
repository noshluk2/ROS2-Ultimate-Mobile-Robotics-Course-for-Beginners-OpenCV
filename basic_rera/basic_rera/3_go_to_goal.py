import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist , Point
from math import pow, atan2, sqrt
import numpy as np
import math
bot_x = 0.0
bot_y = 0.0 
bot_theta = 0.0

def get_turtlesim_pose(data):
    global bot_x
    global bot_y
    global bot_theta
    bot_x = data.pose.pose.position.x
    bot_y = data.pose.pose.position.y
    rot_q = data.pose.pose.orientation
    (roll, pitch, bot_theta) = euler_from_quaternion(rot_q)

    

def send_turtlesim_cmd_vel():
    global  pub , desired_pose , bot_x, bot_y ,bot_theta
    distance_to_goal = sqrt(pow((desired_pose.x - bot_x), 2) +  pow((desired_pose.y - bot_y), 2))
    angle_to_goal    = atan2(desired_pose.y - bot_y, desired_pose.x - bot_x)
    angle_to_turn    = angle_to_goal - bot_theta
    new_vel= Twist()
    new_vel.linear.x = distance_to_goal
    new_vel.angular.z= angle_to_turn
    print("angle to goal = ",angle_to_goal )
    print("angle_to_turn = ",angle_to_turn )
    print("Theta = ",bot_theta )
    if (distance_to_goal>=0.5): # as it will never converge and overshoot
        pub.publish(new_vel)

 
def euler_from_quaternion(quaternion):
    """
    Converts quaternion (w in last place) to euler roll, pitch, yaw
    quaternion = [x, y, z, w]
    Bellow should be replaced when porting for ROS 2 Python tf_conversions is done.
    """
    x = quaternion.x
    y = quaternion.y
    z = quaternion.z
    w = quaternion.w

    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    sinp = 2 * (w * y - z * x)
    pitch = np.arcsin(sinp)

    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


def main(args=None):
    rclpy.init(args=args)
    global node, pub , desired_pose
    node = Node('Go_to_position_node')
    node.create_subscription(Odometry,'/odom',get_turtlesim_pose,10)
    desired_pose=Point()
    desired_pose.x = 3.1
    desired_pose.y = 3.1
    pub=node.create_publisher(Twist,'/cmd_vel',10)
    node.create_timer(0.5, send_turtlesim_cmd_vel)

    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
