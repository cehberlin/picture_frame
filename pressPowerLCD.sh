#!/bin/bash
# This scripts allows to control the power button of the lcd screen
# Run it from /etc/rc.local

# Global PIN configuration
LCD_POWER_PIN=8
LCD_POWER_DETECT_PIN=24

#Shortcut definition
function gpio(){
    /usr/local/bin/gpio $@
}

#Functions configures/exports output pins only if necessary
function configure_output(){
    local pin=$1
    local direction=$2
    local configstate=`gpio exports | grep ".$pin.*$direction" | wc -l`

    #only update port configuration if not already set
    if [ $configstate -eq 0 ];then
        echo "setting pin: $pin to $direction"
        gpio export $pin $direction
        sleep 1 # wait for a short time after configuration change
    fi
}

configure_output $LCD_POWER_PIN out
configure_output $LCD_POWER_DETECT_PIN in

#init to off
lcd_state=0

function get_lcd_state() {
# returns 0 if display is off (LED=off) and 1 if display is on (LED=on)
    lcd_state=`gpio -g read $LCD_POWER_DETECT_PIN`
}

function switch_to_state(){
    while : ; do
        if [ $lcd_state -eq $1 ];then
            break
        else
            #turn on again if display is still reporting off
            #toggle imitates button press
            gpio -g write $LCD_POWER_PIN 1
            gpio -g write $LCD_POWER_PIN 0
            sleep 1 #wait a moment
            get_lcd_state
        fi
    done
}

get_lcd_state

echo "Current state: $lcd_state"

if [ $# -eq 0 ];then
    #calculate inverted state from current state
    target_lcd_state=$(( ($lcd_state +1) % 2  ))
elif [ "$1" = "on" ];then
    target_lcd_state=1
elif [ "$1" = "off" ];then
     target_lcd_state=0
else
    echo "Wrong command, use no argument for toggling, 'on' or 'off'"
    exit
fi

echo "Target state: $target_lcd_state"

switch_to_state $target_lcd_state

