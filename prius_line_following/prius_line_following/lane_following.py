import cv2
import numpy 
import rclpy
from rclpy.node import Node 
from cv_bridge import CvBridge 
from sensor_msgs.msg import Image 

class lane_detection_and_following(Node):
    def __init__(self):
        super().__init__('Lane_follower')
        self.subscriber = self.create_subscription(Image,'/camera/image_raw',self.process_data,10)
        self.bridge = CvBridge() # converting ros images to opencv data

    def process_data(self, data): 
        frame = self.bridge.imgmsg_to_cv2(data) # performing conversion
        light_line = numpy.array([ 100,100,100])
        dark_line = numpy.array([200,200,200])
        mask = cv2.inRange(frame, light_line,dark_line)
        canny= cv2.Canny(mask,40,10)
        r1=150;c1=0
        img = canny[r1:r1+240,c1:c1+640]

        edge=[]
        for i in range (639):
            if(img[160,i]==255):
                edge.append(i)
    
        if(len(edge)==4):
            edge[0]=edge[0]
            edge[1]=edge[2]
                    
        if(len(edge)==3):
            for i in range(len(edge)):
                if(edge[1]-edge[0] > 5): ## meaning idx(0) and idx(1) are ok [193, 506, 507 ]
                    edge[0]=edge[0]
                    edge[1]=edge[1]
                else:#[193, 194, 507 ]
                    edge[0]=edge[0]
                    edge[1]=edge[2]

        # ### finding mid point as a reference
        if(len(edge) < 2):
            edge=[240,440]

        mid_area=(edge[1]-edge[0])
        mid_point= +edge[0] + (mid_area/2)
        img[160,int(mid_point)]=255
        ### control system to keep the mid point in middle frame
        frame_mid = 639/2
        error=frame_mid-mid_point 

        if(error > 0):## go left
            action="Go Left"
        else :
            action="Go Right"



        # ## clear mid frame pixel
        img[160,int(frame_mid)]=255
        img[159,int(frame_mid)]=255
        img[161,int(frame_mid)]=255

        coordinates = (100,100)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255,0,255)
        thickness = 2
        f_image = cv2.putText(img, action, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)




        cv2.imshow('output image',f_image)
        cv2.waitKey(1)
        

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(args=None):
  rclpy.init(args=args)
  image_subscriber = lane_detection_and_following()
  rclpy.spin(image_subscriber)
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()