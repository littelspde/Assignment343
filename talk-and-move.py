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

    count = 0

    sound = Sound()

    def play_count():
        prev = 0
        while True:
            if count > prev:
                sound.play_tone(frequency = 500, duration = 1, delay = 0, volume = 100,
                                play_type = Sound.PLAY_NO_WAIT_FOR_COMPLETE)
                prev = count

    t  = Thread(target = play_count)
    t.setDaemon(True)
    t.start()


    while not btn.any():  # exit loop when any button pressed

       tank_pair.on_for_rotations(left_speed=30, right_speed=30, rotations=2)
       tank_pair.on_for_rotations(left_speed=0, right_speed=50, rotations=2)

       count = count + 1
       sleep(0.1)  # wait for 0.1 seconds

try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass
