#!/usr/bin/env python3
# Little Josh

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor

from time import sleep
from threading import Thread

def main()

    btn = Button()
    sen = ColorSensor()
    tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
    sound = Sound()

    white_count = 0

    def play_count():
        prev = 0
        while True:
            if white_count > prev:
                sound.play_tone(frequency=500, duration=1, delay=0, volume=100,
                                play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
                prev = white_count

    def white_search():
        if sen.reflected_light_intensity > 15:
            white_count++
            sleep(0.5)


    t = Thread(target = play_count())
    t.setDaemon(True)
    t.start()

    t2 = Thread(target = white_search())
    t.setDaemon(True)
    t.start()


    while white_count < 2:
        tank_pair.on(left_speed = 30, right_speed = 30)


try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass

