import cv2
print(cv2.__version__)
import numpy as np
from adafruit_servokit import ServoKit
kit= ServoKit(channels=16)

pan=90
tilt=90
kit.servo[0].angle=pan
kit.servo[1].angle=tilt

def nothing(x):
    pass
 
cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',1320,0)
 
cv2.createTrackbar('hueLower', 'Trackbars',50,179,nothing)
cv2.createTrackbar('hueUpper', 'Trackbars',100,179,nothing)
 
cv2.createTrackbar('hue2Lower', 'Trackbars',50,179,nothing)
cv2.createTrackbar('hue2Upper', 'Trackbars',0,179,nothing)
 
cv2.createTrackbar('satLow', 'Trackbars',100,255,nothing)
cv2.createTrackbar('satHigh', 'Trackbars',255,255,nothing)
cv2.createTrackbar('valLow','Trackbars',100,255,nothing)
cv2.createTrackbar('valHigh','Trackbars',255,255,nothing)
 
 
dispW=640
dispH=480
flip=0
#Uncomment These next Two Line for Pi Camera
#camSet='nvarguscamerasrc sensor_id=1 !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam=cv2.VideoCapture(2)
#width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
#height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
width=640
height=480
print('width :',width,'height :',height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cam.read()
    #frame=cv2.imread('smarties.png')
    
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 
    hueLow=cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'Trackbars')
 
    hue2Low=cv2.getTrackbarPos('hue2Lower', 'Trackbars')
    hue2Up=cv2.getTrackbarPos('hue2Upper', 'Trackbars')
 
    Ls=cv2.getTrackbarPos('satLow', 'Trackbars')
    Us=cv2.getTrackbarPos('satHigh', 'Trackbars')
 
    Lv=cv2.getTrackbarPos('valLow', 'Trackbars')
    Uv=cv2.getTrackbarPos('valHigh', 'Trackbars')
 
    l_b=np.array([hueLow,Ls,Lv])
    u_b=np.array([hueUp,Us,Uv])
 
    l_b2=np.array([hue2Low,Ls,Lv])
    u_b2=np.array([hue2Up,Us,Uv])
 
    FGmask=cv2.inRange(hsv,l_b,u_b)
    FGmask2=cv2.inRange(hsv,l_b2,u_b2)
    FGmaskComp=cv2.add(FGmask,FGmask2)
    cv2.imshow('FGmaskComp',FGmaskComp)
    cv2.moveWindow('FGmaskComp',0,530)

    contours,hierachy=cv2.findContours(FGmaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
        if area>=50:
            #cv2.drawContours(frame,[cnt],0,(255,0,0),3)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
            objX=x+w/2
            objY=y+h/2
            errorPan=objX-width/2
            errorTilt=objY-height/2

            if abs(errorPan)>15:
                pan=pan-errorPan/40
            if abs(errorTilt)>15:
                tilt=tilt-errorTilt/40
            
            
            if pan>180:
                pan=180
                print("Pan Is Out of Range ,180")
            if pan<0:
                pan=0
                print("Pan Is Out of Range ,0")
            if tilt>180:
                tilt=180
                print("Tilt Is Out of Range ,180")
            if tilt<0:
                tilt=0
                print("Tilt Is Out of Range ,0")
            kit.servo[0].angle=pan
            kit.servo[1].angle=tilt
            break

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
 

 
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()