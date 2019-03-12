#!/usr/bin/env python3
# Little Josh

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import TouchSensor

from time import sleep
from threading import Thread

tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
btn = Button()
s = Sound()
cl = ColorSensor()
us = UltrasonicSensor()
touch = TouchSensor()

cl.mode = 'COL-REFLECT'
us.mode = 'US-DIST-CM'

black_count = 0
grey_count = 0
counted = False

# Setting threshold for what relfected light can be determined as black and white
# Anything below b_thresh is black, anything higher than w_thresh is white
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

#Calculate turns of less than 90 degrees
def turn(degrees = 0, spot = True, right = True):

    if spot == True:
        ninety = 167.5
    else:
        ninety = 350

    x = 90/degrees
    turn_val = ninety/x

    if spot:
        if right:
            tank_pair.on_for_degrees(left_speed = 15, right_speed = -15, degrees =turn_val)
        else:
            tank_pair.on_for_degrees(left_speed=-15, right_speed=15, degrees=turn_val)
    else:
        if right:
            tank_pair.on_for_degrees(left_speed=15, right_speed=-15, degrees=turn_val + 10)
        else:
            tank_pair.on_for_degrees(left_speed=-15, right_speed=15, degrees=turn_val + 10)


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
    while black_count < 15:
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

    adjust_val = 10

    #Boolean to determine it turned left to get back on the tiles
    turn_left = True

    while is_grey():

        turn_left=False
        turn(adjust_val, spot = True, right = True)
        sleep(0.2)
        if is_white() or is_black():
            if is_black() and counted == False:
                count_black()
            break
        turn_left = True
        adjust_val += 10

        turn(degrees = adjust_val, spot = True, right = True)
        sleep(0.2)
        if is_white() or is_black():
            if is_black() and counted == False:
                count_black()
            break
        adjust_val += 10

    tank_pair.on_for_degrees(left_speed = 40, right_speed = 40, degrees = 140)

    #The following adjust_vals may need to be changed/replaced
    #If it turned left to get on the tiles, turn right to straighten up
    if turn_left:
        turn(degrees = adjust_val, spot = False, right = True)
    #If it turned right to get on the tiles, turn left to straighten up
    else:
        turn(degrees = adjust_val, spot = False, right = False)
    drive(speed = 40)

def sense_tower():
    dist_mid = 0
    dist_right = 0
    dist_left = 0
    sense_num = 0

    # is_pressed needs updated to sensor name
    while True:
        # Ping tower, set dist_mid
        dist_mid = us.value()
        sleep(0.3)

        # Turn left, ping tower, set dist_left variable
        turn(degrees = 45, spot = True, right = False)
        dist_left = us.value()
        sleep(0.3)

        # Turn right, ping tower, set dist_right variable
        turn(degrees = 90, spot = True, right = True)
        dist_right = us.value()
        sleep(0.3)

        # Update sense_num
        sense_num += 1

        # Turn towards direction closest to tower
        if dist_mid < dist_left and dist_mid < dist_right:
            turn(degrees = 45, spot = True, right = False)
        elif dist_left < dist_right and dist_left < dist_mid:
            turn(degrees = 90, spot = True, right = False)

        # Drives 2 rotations/sense_num
        rot = 2
        tank_pair.on_for_rotations(left_speed=60, right_speed=60, rotations=rot)

        if touch.ispressed():
            break


    # While on the black square, push tower
    while is_black():
        tank_pair.on(left_speed=100, right_speed=100)

    # Play note once tower is off the black square
    s.play_tone(frequency=500, duration=0.2, delay=0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

def main():
    drive(speed = 40)

    turn(degrees = 90, spot = True, right = True)
    tank_pair.on_for_degrees(left_speed = 50, right_speed = 50, degrees = 3800)
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

