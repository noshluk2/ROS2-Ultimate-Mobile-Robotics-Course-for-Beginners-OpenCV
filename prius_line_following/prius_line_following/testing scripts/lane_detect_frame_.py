####
# - Main purpse is Process A single frame to extract
#   line and frame mid points using image processing techniques
# - This scripts is Simple opencv Python based no ROS involved 
#
#  Written by Muhammad Luqman
#  ros2,FOXY
#  13/6/21
#
###

import cv2
import numpy 

## Reading the image
image = cv2.imread('/home/luqman/Desktop/image.png')
    ##### Segmentation
## Defining the color Upper bound and Lower bound limits to extract 
light_line = numpy.array([ 100,100,100])
dark_line = numpy.array([200,200,200])
mask = cv2.inRange(image, light_line,dark_line)

    ##### Boundaries Extraction
## applying the canny edge dector function
canny= cv2.Canny(mask,40,10)
## Cropping the image
r1=150;c1=0
img = canny[r1:r1+240,c1:c1+640]



   ##### Finding Line  Mid point
## Visually finding the perfect Row to fix for mid points
## by setting all values to be light
edge=[]
for i in range (639):
    if(img[160,i]==255):
        edge.append(i)
print(edge)

## We only need two points # one from left line # second from right line 
# When values are 4
if(len(edge)==4):
    edge[0]=edge[0]
    edge[1]=edge[2]
## When Values are 3 and if they are 2 we donot need to process them
## If the values of pixels is greater then 5 then they are adjecent to eachother
if(len(edge)==3):
    for i in range(len(edge)):
        if(edge[1]-edge[0] > 5): ## meaning idx(0) and idx(1) are ok [193, 506, 507 ]
            edge[0]=edge[0]
            edge[1]=edge[1]
        else:#[193, 194, 507 ]
            edge[0]=edge[0]
            edge[1]=edge[2]
## Apllying a white pixel to final line mid point found
mid_area=(edge[1]-edge[0])
mid_point= +edge[0] + (mid_area/2)
img[160,int(mid_point)]=255



    ##### Finding Frame Mid point
frame_mid = 639/2


    ##### Controlling the car process
## Although it is not applying velocites yet but we will print things on the
# Screen to see the output
error=frame_mid-mid_point 

if(error < 0):## go left
    action="Go Right"
else :
    action="Go Left"



## More apparent mid frame pixel by setting upper and lower pixels to be white 
img[160,int(frame_mid)]=255
img[159,int(frame_mid)]=255
img[161,int(frame_mid)]=255
## Writing on the Frame as output for better understanding
f_image = cv2.putText(img, action, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,), 2, cv2.LINE_AA)



print("Error",error,"  /  Frame_mid",frame_mid,"  /  Mid_point",mid_point)
   



cv2.imshow('output image',f_image)


cv2.waitKey(0)
cv2.destroyAllWindows()