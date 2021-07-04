
# import rospy
# import math
# from sensor_msgs.msg import LaserScan
# from geometry_msgs.msg import Twist

# LINEAR_VEL = 0.22
# STOP_DISTANCE = 0.2
# LIDAR_ERROR = 0.05
# SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR

# class Obstacle():
#     def __init__(self):
#         self._cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
#         self.obstacle()
        
#     def get_scan(self):
#         scan = rospy.wait_for_message('scan', LaserScan)
#         scan_filter = []
       
#         samples = len(scan.ranges)  # The number of samples is defined in 
#                                     # turtlebot3_<model>.gazebo.xacro file,
#                                     # the default is 360.
#         samples_view = 1            # 1 <= samples_view <= samples
        
#         if samples_view > samples:
#             samples_view = samples

#         if samples_view is 1:
#             scan_filter.append(scan.ranges[0])

#         else:
#             left_lidar_samples_ranges = -(samples_view//2 + samples_view % 2)
#             right_lidar_samples_ranges = samples_view//2
            
#             left_lidar_samples = scan.ranges[left_lidar_samples_ranges:]
#             right_lidar_samples = scan.ranges[:right_lidar_samples_ranges]
#             scan_filter.extend(left_lidar_samples + right_lidar_samples)

#         for i in range(samples_view):
#             if scan_filter[i] == float('Inf'):
#                 scan_filter[i] = 3.5
#             elif math.isnan(scan_filter[i]):
#                 scan_filter[i] = 0
        
#         return scan_filter

#     def obstacle(self):
#         twist = Twist()
#         turtlebot_moving = True

#         while not rospy.is_shutdown():
#             lidar_distances = self.get_scan()
#             min_distance = min(lidar_distances)

#             if min_distance < SAFE_STOP_DISTANCE:
#                 if turtlebot_moving:
#                     twist.linear.x = 0.0
#                     twist.angular.z = 0.0
#                     self._cmd_pub.publish(twist)
#                     turtlebot_moving = False
#                     rospy.loginfo('Stop!')
#             else:
#                 twist.linear.x = LINEAR_VEL
#                 twist.angular.z = 0.0
#                 self._cmd_pub.publish(twist)
#                 turtlebot_moving = True
#                 rospy.loginfo('Distance of the obstacle : %f', min_distance)

# def main():
#     rospy.init_node('turtlebot3_obstacle')
#     try:
#         obstacle = Obstacle()
#     except rospy.ROSInterruptException:
#         pass

# if __name__ == '__main__':
#     main()