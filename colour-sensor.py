#!/usr/bin/env python3
# Little Josh   

from ev3dev2.button import Button
from ev3dev2.sensor.lego import ColorSensor

from time import sleep


def main():
    # remove the following line and replace with your code

    btn = Button() # we will use any button to stop script
    cl = ColorSensor()
    cl.mode = 'COL-COLOR'

    while not btn.any():  # exit loop when any button pressed
        print("Colour reading:")
        print(cl.value())

        sleep(1)  # wait for 0.1 seconds

try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass
