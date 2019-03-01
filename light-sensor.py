#!/usr/bin/env python3
# Little Josh
# An EV3 Python (library v2) solution to Exercise 3
# of the official Lego Robot Educator lessons that
# are part of the EV3 education software

from ev3dev2.button import Button
from ev3dev2.sensor.lego import ColorSensor

from time import sleep


def main():
    # remove the following line and replace with your code

    btn = Button() # we will use any button to stop script
    cl = ColorSensor()


    while not btn.any():  # exit loop when any button pressed
        print(cl.value())

        sleep(0.1)  # wait for 0.1 seconds

try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass
