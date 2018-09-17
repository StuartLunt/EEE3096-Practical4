#!/usr/bin/python
import RPi.GPIO as GPIO
import Adafruit_MCP3008, time, os, sys, spidev
from datetime import datetime, timedelta
from threading import Event

#Open SPI bus
spi=spidev.SpiDev()
spi.open(0,0)

#initialise variables
global startTime
startTime=time.time()
global period
period = 0.5
global run
run = True
pause = Event()
pot = 0
temp = 0
light = 0
global timeArray, timerArray, potArray, tempArray, lightArray
timeArray=[0,0,0,0,0,0]
timerArray=[0,0,0,0,0,0]
potArray=[0,0,0,0,0,0]
tempArray=[0,0,0,0,0,0]
lightArray=[0,0,0,0,0,0]
GPIO.setwarnings(False)
print("Time \t     Timer \t  Pot \t  Temp \t Light")

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

#Main function
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)
values=[0]*8

def reset(channel):
    global startTime
    os.system('clear')
    startTime = time.time()

def frequency(channel):
    global period
    if period == 0.5:
        period=1
    elif period == 1:
        period = 2
    else:
        period = 0.5

def stop(channel):
    global run, timeArray, timerArray, potArray, tempArray, lightArray, period
    run = not run
    for j in range(0,5):
        for i in range(8):
            values[i] = mcp.read_adc(i)
        pot = pot_reading(values[0])
        temp = temp_convert(values[1])
        light = light_convert(values[2])
        
        timeArray[j]=currentTime()
        timerArray[j]=timerString()
        potArray[j]=pot
        tempArray[j]=temp
        lightArray[j]=light
        time.sleep(period)
        

def display(channel):
    print("Time \t     Timer \t  Pot \t  Temp \t Light")
    for i in range(0,5):
        print("{0:10} {1:6} {2:5}V, {3:4}C, {4:4}%".format(timeArray[i], timerArray[i], potArray[i], tempArray[i], lightArray[i]))
    
def currentTime():
    return time.strftime("%H:%M:%S", time.localtime())

def timer():
    sec=time.time()-startTime
    return sec

def timerString():
    global startTime
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
    V = a*3.3/1023  # ADC outputs values between 0 and 1023 so this converts ADC value to a voltage
    
    return round(V,1)

# Temperature Sesing
def temp_convert(a):
    Vo = a *3.3/1023 # ADC outputs values between 0 and 1023 so this converts ADC value to a voltage
    Ta = (Vo-0.5)/0.01 # Ambient temperature formula
    
    return round(Ta)

# Light Sesing
def light_convert(a):
    # The max value read by the ADC when a cellphone light was shone on it was 800 
    # The minimum value read by the ADC was zero when the LDR was put in complete darkness
    if a >= 800:
        percent = 100
    else:
        percent = a*(1/8) # Approximating light percentage by a straight line
    
    return round(percent)

while True:
    while run:
        for i in range(8):
            values[i] = mcp.read_adc(i)
        pot = pot_reading(values[0])
        temp = temp_convert(values[1])
        light = light_convert(values[2])
        
        print("{0:10} {1:6} {2:5}V, {3:4}C, {4:4}%".format(currentTime(), timerString(), pot,temp,light))

        time.sleep(period)
