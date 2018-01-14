# picture_frame
A collection of scripts that help to turn a Raspberry PI with xbian into a smart picture frame. They are used in conjuction with the built-in Kodi screensaver and the extension [service.xbmc.callbacks2](https://github.com/KenV99/service.xbmc.callbacks2) to trigger the scripts.

* shutdown_button.py: Daemon script enabling raspy shutdown from button press
* motionInterrupt.py: Daemon that turns the screen on/off depending on a passive IR motion sensor and a timeout.
   * runMotionInterrupt.sh: Bash script for starting above daemon if the Kodi screensafer is turned on
   * stopMotionInterrupt.sh: Bash script for stopping above daemon if the Kodi screensafer is turned on
   * configureMotionPins.sh: Setup script, which can be used during start-up to configure the GPIOs
* pressPowerLCD.sh: Bash script that allows to turn/off the screen
   * configurePressPowerLCD.sh: Setup script, which can be used during start-up to configure the GPIOs 

# Pin configuration

SoC is Pin reference

LCD_POWER_PIN=8
LCD_POWER_DETECT_PIN=24
MotionPin=11
