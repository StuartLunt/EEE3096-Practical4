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
pot = 0
temp = 0
light = 0
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
    print("Time \t Timer \t Pot \t Temp \t Light")
    for i in range(0,5):
        print("{t} \t {tmr} \t {pot} V \t {tmp} C \t {ldr} %".format(t=timeArray[i], tmr=timeArray[i], pot=potArray[i], tmp=tempArray[i], ldr=lightArray[i]))
    
def currentTime():
    return time.strftime("%H:%M:%S", time.localtime())

def timer():
    sec=time.time()-startTime
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


# Potentiometer Voltage
def pot_reading(a):
    V = a*3.3/1023
    return V

# Temperature Sesing
def temp_convert(a):
    Vo = a *3.3/1023
    Ta = (Vo-0.5)/0.01
    return Ta

# Light Sesing
def light_convert(a):
    #max = 800
    #min = 0
    percent = a*(1/8)
    return percent


while True:
    for i in range(8):
        values[i] = mcp.read_adc(i)
    time.sleep(period)
    pot = pot_reading(values[0])
    temp = temp_convert(values[1])
    light = light_convert(values[2])
    
while run:
    for i in range(0,4):
        timeArray[i+1]=timeArray[i]
        timerArray[i+1]=timerArray[i]
        potArray[i+1]=potArray[i]
        tempArray[i+1]=tempArray[i]
        lightArray[i+1]=lightArray[i]
    timeArray[0]=currentTime()
    timerArray[0]=timerString()
    potArray[0]=pot
    tempArray[0]=temp
    lightArray[0]=light
    time.sleep(period)