from oled.device import sh1106
from oled.render import canvas
from PIL import ImageDraw, Image,ImageFont
import time
fontSize = 12
font = ImageFont.truetype('/home/pi/fonts/redalert.ttf', fontSize)
#font = ImageFont.load_default()
device= "null"
try:
    device = sh1106(port=1, address=0x3C)
except:
    print("Ekran Bulunamadi!")

bon = "/home/pi/Desktop/Robot/OLED/img/bluetooth/on.png"
boff = "/home/pi/Desktop/Robot/OLED/img/bluetooth/off.png"
banner = "/home/pi/Desktop/Robot/OLED/img/banner/banner.png"
class Pixel:
    def initScreen():
        try:
            if(device != "null"):
                img = Image.open(banner).convert('1')
                with canvas(device) as draw:
                    draw.bitmap((0,0),img,fill=1)
        except:
            print("Banner Error")
                    
    def printScreen(lines):
        try:
            if(device != "null"):
                x = 32
                img = Image.open(imgloc).convert('1')
                with canvas(device) as draw:
                    for line in lines:
                        draw.bitmap((0,0),img,fill=1)
                        draw.text((2,x), line, font=font, fill=255)
                        x += fontSize
        except:
            print("printScreen Error")
            
    def oledBlue(state,lines,time):
        try:
            if(device != "null"):
                x = 32
                if state == True:
                    img = Image.open(bon).convert('1')
                else:
                    img = Image.open(boff).convert('1')
                with canvas(device) as draw:
                    draw.bitmap((0,0),img,fill=1)
                    draw.text((35,10), time, font=font, fill=255)
                    for line in lines:
                        draw.text((2,x), line, font=font, fill=255)
                        x += fontSize
        except:
            print("oledBlue Error")
            
    def clearScreen(state):
        try:
            color = 0
            if state:
                color = 255
            if(device != "null"):
                with canvas(device) as draw:
                    draw.rectangle((0,0,128,64),outline=color,fill=color)
        except:
            print("clearScreen Error")
        
