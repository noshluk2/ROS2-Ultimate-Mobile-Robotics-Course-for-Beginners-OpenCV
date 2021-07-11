import cv2
import numpy 
import os
cap = cv2.VideoCapture('/home/luqman/Desktop/output.avi')
while(cap.isOpened()):
    ret, frame = cap.read()
    light_orange = numpy.array([ 100,100,100])
    dark_orange = numpy.array([200,200,200])
    mask = cv2.inRange(frame, light_orange,dark_orange)
    canny= cv2.Canny(mask,40,10)
    r1=150;c1=0
    img = canny[r1:r1+240,c1:c1+640]
    # # for specific row,column pair  find 255 value in it
    # # for j in range (479):
    # #     for i in range(639):
    # #         if(img[j,i] != 0):
    # #             print(j,i)

    # ## to find location of row selected 
    # for i in range (639):
    #     img[160,i]=255

    ## general solution to find boundaries and mid point to keep in mid
    edge=[]
    for i in range (639):
        if(img[160,i]==255):
            edge.append(i)
    # print(edge)

    ### extracting only two points ## for later as 2 points near to each other 
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
    mid_area=(edge[1]-edge[0])
    mid_point= +edge[0] + (mid_area/2)
    img[160,int(mid_point)]=255
    ### control system to keep the mid point in middle frame
    frame_mid = 639/2
    error=frame_mid-mid_point 

    if(error > 0):## go left
        action="Go Right"
    else :
        action="Go Left"



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



    # # print("error",error)
    # # print("frame_mid",frame_mid)
    # # print("mid_point",mid_point)
    



    cv2.imshow('output image',f_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()