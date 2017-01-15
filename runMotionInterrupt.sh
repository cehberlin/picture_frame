#!/usr/bin/env bash

# This is a simple startup script for the motionInterrupt daemon
# The script should be started after the screensaver is turned on

nohup python /home/xbian/scripts/motionInterrupt.py &>/home/xbian/runMotionInterrupt.log &