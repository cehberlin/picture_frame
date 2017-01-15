#!/usr/bin/python

# Requires kernel module bcm2835_gpiomem and udev rule /etc/udev/rules.d/20-gpio.rules
#SUBSYSTEM=="bcm2835-gpiomem", KERNEL=="gpiomem", GROUP="gpio", MODE="0660"
#SUBSYSTEM=="gpio", KERNEL=="gpiochip*", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys/class/gpio/export /sys/class/gpio/unexport ; chmod 220 /sys/class/gpio/export /sys/class/gpio/unexport'"
#SUBSYSTEM=="gpio", KERNEL=="gpio*", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys%p/active_low /sys%p/direction /sys%p/edge /sys%p/value ; chmod 660 /sys%p/active_low /sys%p/direction /sys%p/edge /sys%p/value'"
#further information: https://sourceforge.net/p/raspberry-gpio-python/tickets/115/ and http://wiringpi.com/wiringpi-update-to-2-29/
from __future__ import division
from __future__ import with_statement
import RPi.GPIO as GPIO
import time
import os, sys
import threading

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='motionInterrupt.log', level=logging.DEBUG)


###Configuration
LCD_POWER_PIN=8
MOTION_PIN=11
LCD_POWER_DETECT_PIN = 24
TIME_UNTIL_TURN_OFF_MIN= 15 # time of no detected motion until the screen is turned off
CHECK_FOR_TURN_OFF_SEC = 30 # sleep time between test for turning off the display


###Global variables

#LCD state
lcd_on = True
#Lock to synchronize switching
lock_switch = threading.Lock()

###Functions

def init():
    global lcd_on
    global last_motion_time

    lcd_on = True

    # SoC als Pinreferenz waehlen
    GPIO.setmode(GPIO.BCM)  

    GPIO.setwarnings(False)

    # Pin 24 vom SoC als Input deklarieren und Pull-Down Widerstand aktivieren
    GPIO.setup(MOTION_PIN, GPIO.IN)

    GPIO.setup(LCD_POWER_PIN, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.setup(LCD_POWER_DETECT_PIN, GPIO.IN)

    last_motion_time = time.time()
    
    # Interrupt Event hinzufuegen. Pin 24, auf steigende Flanke reagieren und ISR "Interrupt" deklarieren
    GPIO.add_event_detect(MOTION_PIN, GPIO.FALLING, callback = motion_interrupt, bouncetime = 200)

    logging.info('Configuration: Turning off after %s min, checking time difference each %s s', TIME_UNTIL_TURN_OFF_MIN, CHECK_FOR_TURN_OFF_SEC)

    logging.info('Finished init()')

# ISR
def motion_interrupt(channel):
    # Access global variables
    global last_motion_time
    global lcd_on
    
    last_motion_time = time.time()

    logging.debug("Motion detected")
    #XXX may wait until we received several measures (filtering)
    
    if not lcd_on:
        logging.info("LCD is turned on again")
        switch_to_lcd_state(1)
        lcd_on = True


def get_lcd_state():
    # returns 0 if display is off (LED=off) and 1 if display is on (LED=on)
    return GPIO.input(LCD_POWER_DETECT_PIN)

def switch_to_lcd_state(target_state):
    """
    Switch the lcd to the given target state
    Keep trying until target state is achieved
    :param target_state: target state of the lcd 0=off 1=on
    """
    global lock_switch
    with lock_switch:
        while get_lcd_state() != target_state:
            press_lcd_power_key()
            time.sleep(1)

# Press Power key of LCD display
def press_lcd_power_key():
    GPIO.output(LCD_POWER_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(LCD_POWER_PIN, GPIO.HIGH)
    #print("power button pressed")
    
def check_idle_time_turn_off():
    global lcd_on
    now = time.time() 
    diff_min = (now - last_motion_time) / 60

    logging.debug("Current time diff: %s", diff_min)

    if diff_min >= TIME_UNTIL_TURN_OFF_MIN and lcd_on == True:
        logging.info("Idle time exeeded, LCD is turned off")
        switch_to_lcd_state(0)
        lcd_on = False

def main_loop():
    init()
    # endless loop
    while True:
        time.sleep(CHECK_FOR_TURN_OFF_SEC)
        check_idle_time_turn_off()
    
###Main programm    
if __name__ == '__main__':
    #alternative without process
    #main_loop()

    # start check in an own process
    fpid = os.fork()
    if fpid==0:
      # Running as daemon now. PID is fpid
      logging.debug("Daemon process started")
      main_loop()

    exit() #exit first start process