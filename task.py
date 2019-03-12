#!/usr/bin/env python3
# Little Josh

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor

from time import sleep
from threading import Thread

tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
btn = Button()
s = Sound()
cl = ColorSensor()
us = UltrasonicSensor()

black_count = 0
grey_count = 0
counted = False

# Setting threshold for what relfected light can be determined as black and white
# Anything below b_thresh
b_thresh = 14
w_thresh = 45

# Increase the black_count and beeps
def count_black():

    global black_count
    global counted

    s.play_tone(frequency=500, duration=0.2, delay=0, volume=100,
                play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
    black_count += 1
    counted = True

# Checks if the light sensor is sensing black
def is_black():
    if cl.reflected_light_intensity < b_thresh:
        return True
    else:
        return False

#Checks if the light sensor is sensing white
def is_white():
    if cl.reflected_light_intensity > w_thresh:
        return True
    else:
        return False

#Checks if the light sensor is not sensing black or white
def is_grey():
    if not is_black() and not is_white():
        return True
    else:
        return False


# A method that drives the robot forward and makes calls to adjust() once it goes off the
# black and white tiles.
def drive(speed = 40):

    global black_count
    global grey_count

    #Boolean to determine whether or not it has counted a black square
    global counted

    # Drive forward
    tank_pair.on(left_speed=speed, right_speed=speed)

    # While it hasn't counted 15 tiles
    while black_count < 14:
        if is_black() and counted == False:
           count_black()
        elif is_white():
            counted = False
        else:
            grey_count += 1
            sleep(0.2)

        # If grey has been sensed three times (its on a grey tile)
        if grey_count >= 3:
            counted = False
            grey_count = 0
            adjust()
        if is_white() or is_black():
            grey_count = 0


# A method to bring the robot back onto the black and white tiles after it veers off course
def adjust():

    global black_count
    global counted

    adjust_val = 16.75

    #Boolean to determine it turned left to get back on the tiles
    turn_left = True

    while is_grey():

        turn_left=False
        tank_pair.on_for_degrees(left_speed = 15, right_speed = -15, degrees = adjust_val)
        sleep(0.2)
        if is_white() or is_black():
            if is_black() and counted == False:
                count_black()
            break
        turn_left = True
        adjust_val += 33.5

        tank_pair.on_for_degrees(left_speed=-15, right_speed=15, degrees=adjust_val)
        sleep(0.2)
        if is_white() or is_black():
            if is_black() and counted == False:
                count_black()
            break
        adjust_val += 33.5

    tank_pair.on_for_degrees(left_speed = 40, right_speed = 40, degrees = 140)

    #The following adjust_vals may need to be changed
    #If it turned left to get on the tiles, turn right to straighten up
    if turn_left:
        tank_pair.on_for_degrees(left_speed=30, right_speed=0, degrees= 16.75 + adjust_val)
    #If it turned right to get on the tiles, turn left to straighten up
    else:
        tank_pair.on_for_degrees(left_speed=0, right_speed=30, degrees= 16.75 + adjust_val)
    drive(speed = 40)

def main():
    drive(speed = 40)

    tank_pair.on_for_degrees(left_speed=15, right_speed=-15, degrees=167.5)
    sleep(2)

    sense_tower()


try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass

