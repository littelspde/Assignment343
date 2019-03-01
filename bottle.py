#!/usr/bin/env python3
# Little Josh
# An EV3 Python (library v2) solution to Exercise 3
# of the official Lego Robot Educator lessons that
# are part of the EV3 education software

# Group 10: Abinaya, Josh, Reuben, Vivian

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound

from time import sleep

from ev3dev2 import *

def main():
    # remove the following line and replace with your code

    btn = Button()  # we will use any button to stop script
    tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)

    sound = Sound()

    # Connect an EV3 color sensor to any sensor port.
    cl = ColorSensor()

    # Setup Touch Sensor
    ts = TouchSensor()

    while not btn.any():  # exit loop when any button pressed
        # if we are over the black line (weak reflection)

        if cl.reflected_light_intensity < 30:
            # medium turn right
            tank_pair.on(left_speed=40, right_speed=0)

        else:  # strong reflection (>=30) so over white surface
            # medium turn left
            tank_pair.on(left_speed=0, right_speed=40)

        if ts.is_pressed:
            sound.speak("Ouch, that hurt")
            tank_pair.on_for_rotations(left_speed=-20, right_speed=-40, rotations=1)
            sound.speak("I am okay")
            tank_pair.on_for_seconds(left_speed=50, right_speed=50, seconds=1.1)
            tank_pair.on_for_seconds(left_speed = 0, right_speed = 30, seconds = .9)

            while cl.reflected_light_intensity > 30:
                tank_pair.on(left_speed=25, right_speed = 25)
            tank_pair.on(left_speed=0, right_speed=0)
            sound.speak("Ta Da, I am a good boy")

        sleep(0.1)  # wait for 0.1 seconds

try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass
