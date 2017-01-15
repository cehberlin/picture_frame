#!/usr/bin/env bash

# This script terminates the motion interrupt daemon
# It should be started after the screensaver is turned off

pkill -f motionInterrupt.py
