#!/usr/bin/env bash

# This is a simple script that allows to read the motion sensor state
# It prints the current date if motion is detected

MOTION_PIN=11

/usr/local/bin/gpio export $MOTION_PIN in

while [[ true ]];do
    value=$(gpio -g read $MOTION_PIN)
    sleep 1
    #echo $value
    if [[ $value == 0 ]];then
        echo $(date +%s)
    fi
    
done

