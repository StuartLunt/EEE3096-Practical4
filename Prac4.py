import RPi.GPIO as GPIO
import Adafruit_MCP3008, time, os, sys, spidev
from datetime import datetime, timedelta
from threading import Event

#Open SPI bus
spi=spidev.SpiDev()
spi.open(0,0)

#initialise variables
startTime = time.time()
period = 0.5
run = True
pause = Event()
timeArray=[]
timerArray=[]
potArray=[]
tempArray=[]
lightArray=[]

#Set up GPIO
GPIO.setmode(GPIO.BCM)

#Pin definitions
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
switch1 = 14
switch2 = 15
switch3 = 18
switch4 = 17

#GPIO setup
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch4, GPIO.IN, pull_up_down=GPIO.PUD_UP)



mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)
values=[0]*8

def reset(channel):
    os.system('clear')
    startTime = time.time()

def frequency(channel):
    if period == 0.5 :
        period=1
    elif period == 1:
        period = 2
    else:
        period = 0.5

def stop(channel):
    run = not run

def display(channel):
    dummy = 0
    #display last 5
    
def currentTime():
    return time.strftime("%H:%M:%S", time.localtime())

def timer():
    sec=seconds=time.time()-startTime
    return sec

def timerString():
    sec=timedelta(seconds=time.time()-startTime)
    d=datetime(1,1,1)+sec
    s=str(d.hour)+":"+str(d.minute)+":"+str(d.second)
    return s

#Event detection set up
GPIO.add_event_detect(switch1, GPIO.FALLING, callback=reset, bouncetime=200)
GPIO.add_event_detect(switch2, GPIO.FALLING, callback=frequency, bouncetime=200)
GPIO.add_event_detect(switch3, GPIO.FALLING, callback=stop, bouncetime=200)
GPIO.add_event_detect(switch4, GPIO.FALLING, callback=display, bouncetime=200)


while run:
    print(currentTime()+"\t"+timerString())
    pause.wait(period)