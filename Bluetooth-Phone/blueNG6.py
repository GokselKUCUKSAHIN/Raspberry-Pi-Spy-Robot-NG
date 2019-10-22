#__init__ JellyBeanci(c) a.k.a Göksel KÜÇÜKŞAHİN

#Library Block
import RPi.GPIO as GPIO #gpio lib
import os #lx5terminal
import bluetooth #custom bt lib
import threading #multi thread lib
from datetime import datetime #datetime lib
import time #time and timer
from OLED.Screen import Pixel as Ekran #Jellybeanci OLED lib

#Function Block

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

def signalLED():
    global dead
    global curPos
    flag = True
    while not dead:
        if ledState:
            #print('ledState =', ledState, curPos)
            if curPos == 1:
                GPIO.output(LeftLED,GPIO.HIGH)
                GPIO.output(RightLED,GPIO.LOW)
            elif curPos == 2:
                GPIO.output(RightLED,GPIO.HIGH)
                GPIO.output(LeftLED,GPIO.LOW)
            time.sleep(0.2)
            if curPos == 1:
                GPIO.output(LeftLED,GPIO.LOW)
            elif curPos == 2:
                GPIO.output(RightLED,GPIO.LOW)
            time.sleep(0.2)
            flag = True
        else:
            #print('x ledState =',ledState,curPos)
            if curPos == 0 and flag:
                #print("low")
                try:
                    GPIO.output(LeftLED,GPIO.LOW)
                    GPIO.output(RightLED,GPIO.LOW)
                except:
                    pass
                flag = False
                time.sleep(0.3)
            else:
                time.sleep(0.3)

def initScr():
    try:
        Ekran.initScreen()
    except:
        print("Ekran bulunamadi.")
        
def getTime():
    tm = datetime.now()
    return (str(tm.day)+'_'+str(tm.month)+'_'+str(tm.year))

def getTimeCam():
    tm = datetime.now()
    return (str(tm.second)+'_'+str(tm.minute)+'_'+str(tm.hour))

def getTimeDetail(sep):
    tm = datetime.now()
    return (str(tm.hour) + sep+str(tm.minute)+sep+str(tm.second))

def updateCurr():
    global curNum
    curNum += 1
    print(curNum)
  
def clearMotor(array):
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

def distance():
    global dead
    global dist
    while not dead:
        GPIO.output(triggerPin, True)
        # set trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(triggerPin, False)
        StartTime = time.time()
        StopTime = time.time()
        # save StartTime
        while GPIO.input(echoPin) == 0:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(echoPin) == 1:
            StopTime = time.time()
        DeltaTime = StopTime - StartTime
        dist = (DeltaTime * 34300) / 2
        print ("Mesafe = %.1f cm" % dist) #uncomment after before use
        time.sleep(1)

def voiceControl():
    for i in Command:
        if i == "b'ileri git'":
            print("ileri")
            driveMotor(motorArray, 1)
            driveMotor(motorArray, 3)
            time.sleep(0.5)
            clearMotor(motorArray)
            time.sleep(0.1)
        elif i == "b'geri git'":
            print("geri")
            driveMotor(motorArray, 0)
            driveMotor(motorArray, 2)
            time.sleep(0.5)
            clearMotor(motorArray)
            time.sleep(0.1)
        elif i == "b'sola d\\xc3\\xb6n'":
            print("sol")
            driveMotor(motorArray, 1)
            driveMotor(motorArray, 2)
            time.sleep(0.46)
            clearMotor(motorArray)
            time.sleep(0.1)
        elif i == "b'sa\\xc4\\x9fa d\\xc3\\xb6n'":
            print("sag")
            driveMotor(motorArray, 0)
            driveMotor(motorArray, 3)
            time.sleep(0.46)
            clearMotor(motorArray)
            time.sleep(0.1)
def BluetoothConnect():
    global server_socket
    global port
    global client_socket
    global address
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_socket.bind(("", port))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    
def BluetoothDisconnect():
    global cliend_socket
    global server_socket
    client_socket.close()
    server_socket.close()
    
#GLOBAL Block

GPIO.setmode(GPIO.BCM) #BCM not BOARD
GPIO.setwarnings(False) #For get rid of anoying warnings

curNum = 0

#Signal pins
LeftLED = 12
RightLED = 17
ledState = False #signal state var
curPos = 0 #signal position var

GPIO.setup(LeftLED,GPIO.OUT)
GPIO.setup(RightLED,GPIO.OUT)

global dead
dead = False

global dist
dist = 0
#HcSr04 pins
triggerPin = 25
echoPin = 21
#set trigger Output, echo Input
GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)


#motor pins
motorL1 = 26
motorL2 = 19
motorR1 = 13
motorR2 = 6

#set motor pins as Output 
GPIO.setup(motorL1,GPIO.OUT)
GPIO.setup(motorL2,GPIO.OUT)
GPIO.setup(motorR1,GPIO.OUT)
GPIO.setup(motorR2,GPIO.OUT)

motorArray = [motorL1, motorL2, motorR1, motorR2] #motorPin Array
global listen
listen = False
Command = []
sinyal = threading.Thread(target=signalLED)
tdist = threading.Thread(target=distance)

if __name__ == '__main__':
    print('Baslatılıyor 3sn')
    for i in range(3,0,-1):
        print(i,'saniye kaldi')
        time.sleep(1)
    print('Bitti')
    sinyal.start() # threading
    initScr() # initialize Screen
    try:
        BluetoothConnect()
        tdist.start()
        try:
            Ekran.oledBlue(True, ["Connection from :", str(address)], getTimeDetail(' : '))
        except:
            print("Ekran bulunamadi. hata 0x0A1")
        while True:
            try:
                data = client_socket.recv(1024)
                if listen == False:
                    print (data)
                    if (str(data) == "b'u'"):
                        driveMotor(motorArray, 1)
                        driveMotor(motorArray, 3)
                    if (str(data) == "b'l'"):
                        driveMotor(motorArray, 1)
                        driveMotor(motorArray, 2)
                    if (str(data) == "b'd'"):
                        driveMotor(motorArray, 0)
                        driveMotor(motorArray, 2)
                    if (str(data) == "b'r'"):
                        driveMotor(motorArray, 0)
                        driveMotor(motorArray, 3)
                    if (str(data) == "b'0'"):
                        clearMotor(motorArray)
                    if (str(data) == "b'ls'"):
                        updateState(1)
                    if (str(data) == "b'rs'"):
                        updateState(2)
                    if (str(data) == "b'a\\xc3\\xa7'"):
                        GPIO.output(17, 1)
                    if (str(data) == "b'kapat'"):
                        GPIO.output(17, 0)
                    if (str(data) == "b'cam'"):
                        camera = threading.Thread(target=takePicture).start()
                    #Exiting From Loop
                    if (str(data) == "b'Quit'"):
                        print ("Quit")
                        ledState = False
                        dead = True
                        break
                    if (str(data) == "b'\\xc3\\xa7\\xc4\\xb1k\\xc4\\xb1\\xc5\\x9f yap\\xc4\\xb1yorum'"):
                        print("Ama neden oyle dedin ki ?")
                        print("Alindim, Gucendim :(") #xd
                        ledState = False
                        dead = True
                        break
                    if(str(data) == "b'select'"):
                        listen = True
                        Command.clear()
                else:
                    print("Listening!!!")
                    if(str(data) == "b'tamam'"):
                        print("OK cikiliyor")
                        listen = False
                        for i in Command:
                            print(i)
                        voiceControl()
                    else:
                         Command.append(str(data))
                         print(str(data))
            except:
                try:
                    Ekran.oledBlue(False, ["Disconnected !"], getTimeDetail(' : '))
                except:
                    print("Ekran bulunamadi. hata 0xA2")
                BluetoothConnect()
                try:
                    Ekran.oledBlue(True, ["Connection from :", str(address)], getTimeDetail(' : '))
                except:
                    print("Ekran bulunamadi. hata 0xA3")
        try:
            ledState = False
            time.sleep(0.5)
            GPIO.cleanup()  # define
            BluetoothDisconnect()
        except:
            print("hata 0xB3")
    except KeyboardInterrupt:
        ledState = False
        time.sleep(0.5)
        Ekran.clearScreen(False) #false siyah
        GPIO.cleanup()  # define
        BluetoothDisconnect()
try:
    Ekran.clearScreen(False) #false siyah
except:
    print("Ekran bulunamadi")
print("End Of the Line")
