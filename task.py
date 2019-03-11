#!/usr/bin/env python3
# Little Josh

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor

from time import sleep
from threading import Thread

tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
btn = Button()
s = Sound()
cl = ColorSensor()
black_count = 0
counted = False
grey_count = 0

def drive(speed = 40):
    global black_count
    global counted
    global grey_count
    tank_pair.on(left_speed=speed, right_speed=speed)
    while black_count < 15:
        if cl.reflected_light_intensity < 12 and counted == False:
            s.play_tone(frequency=500, duration=0.2, delay=0, volume=100,
                            play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            black_count += 1
            counted = True
        elif cl.reflected_light_intensity > 45:
            counted = False
        else:
            grey_count += 1
            sleep(0.2)
        if grey_count >= 3:
            counted = False
            grey_count = 0
            adjust()
        if cl.reflected_light_intensity > 49 or cl.reflected_light_intensity < 12:
            grey_count = 0


def adjust():
    adjust_val = 16.75
    turn_left = True
    while cl.reflected_light_intensity > 12 and cl.reflected_light_intensity < 45:
        turn_left=False
        tank_pair.on_for_degrees(left_speed = 15, right_speed = -15, degrees = adjust_val)
        sleep(0.2)
        if cl.reflected_light_intensity > 49 or cl.reflected_light_intensity < 12:
            break
        turn_left = True
        adjust_val += 33.5
        tank_pair.on_for_degrees(left_speed=-15, right_speed=15, degrees=adjust_val)
        sleep(0.2)
        if cl.reflected_light_intensity > 49 or cl.reflected_light_intensity < 12:
            break
        adjust_val += 33.5
    tank_pair.on_for_degrees(left_speed = 40, right_speed = 40, degrees = 80)
    # the follow adjuct_vals should potentiall be (180-adjust_val) or (90-adjust_val)
    if turn_left:
        tank_pair.on_for_degrees(left_speed=30, right_speed=0, degrees=adjust_val)
    else:
        tank_pair.on_for_degrees(left_speed=0, right_speed=30, degrees=adjust_val)
    drive(speed = 40)


def main():
    drive(speed = 40)
try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass

