#__init__ JellyBeanci(c)

import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
import os
import bluetooth
import threading
from datetime import datetime
import time
from OLED.Screen import Pixel as Ekran
LED=12

GPIO.setmode(GPIO.BCM)     #programming the GPIO by BCM pin numbers. (like PIN40 as GPIO21)
GPIO.setwarnings(False)
GPIO.setup(LED,GPIO.OUT)  #initialize GPIO21 (LED) as an output Pin
GPIO.output(LED,GPIO.LOW)
GPIO.setup(17,GPIO.OUT)

curNum = 0

global dead
dead = False

motorL1 = 26
motorL2 = 19
motorR1 = 13
motorR2 = 6

GPIO.setup(motorL1,GPIO.OUT)
GPIO.setup(motorL2,GPIO.OUT)
GPIO.setup(motorR1,GPIO.OUT)
GPIO.setup(motorR2,GPIO.OUT)

lis =[motorL1,motorL2,motorR1,motorR2]

  
def takePicture():
    print("cam started")
    cDc = "mkdir /home/pi/roboCamDir/"
    os.system(cDc)
    var = getTime()
    cDc += var
    os.system(cDc)
    cmd = "fswebcam -p YUYV -d /dev/video0 -r 640x480 --no-banner /home/pi/roboCamDir/"
    cmd += var + "/image" + getTimeCam() + ".jpg"


    os.system(cmd)
    print("cam exit")
    #updateCurr()


def sinyalLed(e, t):
    global dead
    while not dead:
        #print(ledState)
        if ledState:
            print(curPos)
            if curPos == 1:
                GPIO.output(17,GPIO.HIGH)
                GPIO.output(12,GPIO.LOW)
            elif curPos == 2:
                GPIO.output(12,GPIO.HIGH)
                GPIO.output(17,GPIO.LOW)
            time.sleep(0.2)
            if curPos == 1:
                GPIO.output(17,GPIO.LOW)
            elif curPos == 2:
                GPIO.output(12,GPIO.LOW)
            time.sleep(0.2)
        else:
            try:
                GPIO.output(17,GPIO.LOW)
                GPIO.output(12,GPIO.LOW)
                time.sleep(0.3)
            except:
                pass
        
ledState = False
curPos = 0

e = threading.Event()
t = threading.Thread(name='non-block', target=sinyalLed, args=(e, 0.1))
t.start() # threading
try:
    Ekran.initScreen()
except:
    print("Ekran bulunamadi.")
def getTime():
    tm = datetime.now()
    return (str(tm.day)+str(tm.month)+str(tm.year))

def getTimeCam():
    tm = datetime.now()
    return (str(tm.second) +str(tm.minute)+str(tm.hour))

def getTimeDetail(sep):
    tm = datetime.now()
    return (str(tm.hour) + sep+str(tm.minute)+sep+str(tm.second))

def updateCurr():
    global curNum
    curNum += 1
    print(curNum)
  
def clearLed(array):
    for i in array:
        GPIO.output(i,GPIO.LOW)
    return

def driveMotor(array,index):
    GPIO.output(array[index],GPIO.HIGH)
    return

def updateState(pos):
    global ledState #for redefining global variables
    global curPos
    
    if pos == curPos:
        ledState = False
        curPos = 0
    elif pos != curPos:
        if ledState == False:
            ledState = True
        curPos = pos
        
server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
 
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
 
client_socket,address = server_socket.accept()
try:
    Ekran.oledBlue(True,["Connection from :", str(address)],getTimeDetail(' : '))
except:
    print("Ekran bulunamadi.")
while True:
    try:
        data = client_socket.recv(1024)
        print (data)
        if(str(data) == "b'u'"):
            driveMotor(lis,1)
            driveMotor(lis,3)
        if(str(data) == "b'l'"):
            driveMotor(lis,1)
            driveMotor(lis,2)
        if(str(data) == "b'd'"):
            driveMotor(lis,0)
            driveMotor(lis,2)
        if(str(data) == "b'r'"):
            driveMotor(lis,0)
            driveMotor(lis,3)
        if(str(data) == "b'0'"):
            clearLed(lis)
        if(str(data) == "b'ls'"):
            updateState(1)
        if(str(data) == "b'rs'"):
            updateState(2)
        if (str(data) == "b'a\\xc3\\xa7'"):
            GPIO.output(17,1)
        if (str(data) == "b'kapat'"):
            GPIO.output(17,0)
        if (str(data) == "b'cam'"):
            #takePicture()
            camera = threading.Thread(target=takePicture).start()

        if (str(data) == "b'Quit'"):  
            print ("Quit")
            
            break
        if(str(data) == "b'\\xc3\\xa7\\xc4\\xb1k\\xc4\\xb1\\xc5\\x9f yap\\xc4\\xb1yorum'"):
            print("Ama neden oyle dedin ki ?")
            print("Alindim, Gucendim :(")
            ledState = False
            dead = True
            break
    except:
        print("except ici")
        try:
            Ekran.oledBlue(False,["Disconnected !"],getTimeDetail(' : '))
        except:
            print("Ekran bulunamadi.")
        server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        server_socket.bind(("",port))
        server_socket.listen(1)
        client_socket,address = server_socket.accept()
        try:
            Ekran.oledBlue(True,["Connection from :", str(address)],getTimeDetail(' : '))
        except:
            print("Ekran bulunamadi.")

try:
    ledState = False
    time.sleep(0.4)
    GPIO.cleanup() #define
    client_socket.close()
    server_socket.close()
except:
    print("hata")
print("son")
