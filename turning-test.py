#!/usr/bin/env python3
# Little Josh
# An EV3 Python (library v2) solution to Exercise 3
# of the official Lego Robot Educator lessons that
# are part of the EV3 education software

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.button import Button
from ev3dev2.sound import Sound

from time import sleep
from threading import Thread


def main():
    # remove the following line and replace with your code

    btn = Button()  # we will use any button to stop script
    tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
    s = Sound()

    while not btn.any():

        """s.speak("Turning 90 degrees, 350 degrees")
        tank_pair.on_for_degrees(left_speed = 30, right_speed = 0, degrees = 350)
        sleep(3)"""

        sleep(3)
        s.speak("Now turning on the spot")
        sleep(3)

        s.speak("Turning 90 degrees, 167.5 degrees")
        tank_pair.on_for_degrees(left_speed=15, right_speed=-15, degrees=167.5)
        sleep(2)

        adjust = 16.75
        count = 1
        while True:
            tank_pair.on_for_degrees(left_speed = 15, right_speed = -15, degrees = adjust)
            count += 1
            sleep(2)
            adjust = 16.75 * count
            tank_pair.on_for_degrees(left_speed=-15, right_speed=15, degrees=adjust)
            count += 1
            sleep(2)
            adjust = 16.75 * count




    sleep(5)



try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass

