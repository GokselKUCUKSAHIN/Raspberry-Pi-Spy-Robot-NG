from pynput import keyboard
import RPi.GPIO as GPIO
import os
import time

motorL1 = 26
motorL2 = 19
motorR1 = 13
motorR2 = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(motorL1,GPIO.OUT)
GPIO.setup(motorL2,GPIO.OUT)
GPIO.setup(motorR1,GPIO.OUT)
GPIO.setup(motorR2,GPIO.OUT)

lis =[motorL1,motorL2,motorR1,motorR2]


def updateCurr():
    global curNum
    curNum += 1
    print(curNum)
    
def takePicture(imgCount):
    cmd = "fswebcam -p YUYV -d /dev/video0 -r 640x480 --no-banner /home/pi/pycam/image"
    st = cmd + str(imgCount) + ".jpg"
    os.system(st)
    #curNum = imgCount + 1

def clearKey(index,arr):
    GPOI.output(arr[index],GPIO.LOW)
    
def clearLed(array):
    for i in array:
        GPIO.output(i,GPIO.LOW)
    return

def driveMotor(array,index):
    GPIO.output(array[index],GPIO.HIGH)
    return
        
def on_press(key):
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        if key.char == '0':
            GPIO.cleanup()
            e.set()
            quit()
        elif key.char == '3':
            takePicture(curNum)
            updateCurr()
    except AttributeError:
        #print('special key {0} pressed'.format(key))
        if format(key) == "Key.up":
            driveMotor(lis,1)
            driveMotor(lis,3)
        elif format(key) == "Key.left":
            driveMotor(lis,1)
            driveMotor(lis,2)
        elif format(key) == "Key.down":
            driveMotor(lis,0)
            driveMotor(lis,2)
        elif format(key) == "Key.right":
            driveMotor(lis,0)
            driveMotor(lis,3)
            
def on_release(key):
    #print('{0} released'.format(key))
    clearLed(lis)
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
