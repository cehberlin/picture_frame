#! /usr/bin/env python
# This script lists on a button event in order to shutdown the system.
# Install: 1) Make script executable and add it to /etc/rc.local
import os
import RPi.GPIO as GPIO
import sys
import signal
import time

# GPIO3 (pin 5) set up as input. 
SHUTDOWN_PIN = 3 

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def shutdown_button(channel):
    print('shuting down')
    GPIO.cleanup(SHUTDOWN_PIN)
    GPIO.setup(SHUTDOWN_PIN, GPIO.OUT)
    GPIO.output(SHUTDOWN_PIN, GPIO.HIGH)
    # shut down the rpi
    os.system("/sbin/shutdown -h now")  

signal.signal(signal.SIGINT, signal_handler)
GPIO.setmode(GPIO.BCM)

#It is pulled up to stop false signals
GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(SHUTDOWN_PIN, GPIO.FALLING, callback = shutdown_button, bouncetime = 250)  
 
try:
    while True:
         time.sleep(10)       
        
except:
    GPIO.cleanup()
