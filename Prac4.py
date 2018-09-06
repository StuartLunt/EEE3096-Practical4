import RPi.GPIO as GPIO
import Adafruit_MCP3008, time, os, sys

#Open SPI bus
spi=spidev.SpiDev()
spi.open(0,0)

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

#GPIO setup
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Event detection set up
GPIO.add_event_detect(switch1, GPIO.FALLING, callback=reset)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)
values=[0]*8



while True:
    for i in range(8):
    values[i] = mcp.read_adc(i)
time.sleep(0.5)
print(values)

