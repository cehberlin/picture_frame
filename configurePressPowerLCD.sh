#!/bin/bash
# This script is for configuration of the LCD power control pins during system startup

LCD_POWER_PIN=8
LCD_POWER_DETECT_PIN=24

#configure
/usr/local/bin/gpio export $LCD_POWER_PIN out
/usr/local/bin/gpio export $LCD_POWER_DETECT_PIN in

while : ; do
    # returns 0 if display is off (LED=off) and 1 if display is on (LED=on)
    lcd_state=`/usr/local/bin/gpio -g read $LCD_POWER_DETECT_PIN`
    sleep 1 #wait a moment
    if [ $lcd_state -eq 1 ];then
        break
    else
        #turn on again if display is still reporting off
        /usr/local/bin/gpio -g write $LCD_POWER_PIN 1
        /usr/local/bin/gpio -g write $LCD_POWER_PIN 0
    fi
done




