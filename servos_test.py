from adafruit_servokit import ServoKit
import time
myKit= ServoKit(channels=16)
while True:
    for i in range(0,180,1):
        myKit.servo[0].angle=i
        myKit.servo[1].angle=i
        time.sleep(.01)
    for i in range(180,0,-1):
        myKit.servo[0].angle=i
        myKit.servo[1].angle=i
        time.sleep(.01)