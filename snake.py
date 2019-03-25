#!/usr/bin/env python3
# Little Josh (aka LJ)



from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import TouchSensor

from time import sleep

# Creating instances of sensor classes
tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
btn = Button()
s = Sound()
cl = ColorSensor()
us = UltrasonicSensor()
touch = TouchSensor()

# Setting default sensor modes
cl.mode = 'COL-REFLECT'
us.mode = 'US-DIST-CM'

# Initialising global variables
black_count = 0
grey_count = 0
counted = False

# Setting threshold for what reflected light can be determined as black and white
# Anything below b_thresh is black, anything higher than w_thresh is white
b_thresh = 15
w_thresh = 49

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

#Calculate turns of less than 180 degrees
def turn(degrees = 0.0, spot = True, right = True, forward = True):

    if degrees <= 0:
        return

    if spot:
        one_eighty = 335
    else:
        one_eighty = 700

    x = 180/degrees
    turn_val = one_eighty/x

    spot_speed = 15
    forward_speed = 30 if forward else -30

    if spot:
        if right:
            tank_pair.on_for_degrees(left_speed = spot_speed, right_speed = -spot_speed, degrees = turn_val)
        else:
            tank_pair.on_for_degrees(left_speed = -spot_speed, right_speed = spot_speed, degrees = turn_val)
    else:
        if right:
            tank_pair.on_for_degrees(left_speed = forward_speed, right_speed = 0, degrees = turn_val)
        else:
            tank_pair.on_for_degrees(left_speed = 0, right_speed = forward_speed, degrees = turn_val)


# A method to calibrate the white threshold (w_thresh) and black threshold (b_thresh) based off
# the ambient light on the black starting tile. Do not run on any tiles, only the starting 'S' square
def calibrate():

    global b_thresh, w_thresh

    cl.mode = 'COL-AMBIENT'
    amb = cl.value()

    if amb > 8:
        w_thresh = 50

    cl.mode = 'COL-REFLECT'
    sleep(1)


def start():

    g_count = 0
    seen = False

    tank_pair.on(left_speed = 20, right_speed = 20)

    # Drive until you have seen a non-black tile, followed by a black tile, followed by another non-black
    while g_count < 2:

        if not is_black() and not seen:
            g_count += 1
            seen = True

        elif is_black():
            if seen:
                count_black()
            seen = False

    # Turn 90 degrees to line up with tiles
    turn(degrees = 90, spot = False, right = False, forward = False)

    sleep(0.5)





# A method that drives the robot forward and makes calls to adjust() once it goes off the
# black and white tiles.
def drive(l_speed, r_speed):

    global black_count, grey_count, b_thresh, w_thresh

    #Boolean to determine whether or not it has counted a black square
    global counted

    # Drive forward
    tank_pair.on(left_speed=l_speed, right_speed=r_speed)

    # While it hasn't counted 15 tiles
    while black_count < 15:
        if is_black() and counted == False:
           count_black()
        elif is_white():
            counted = False
        else:
            # grey_count += 1
            # sleep(0.1)
            temp = l_speed
            l_speed = r_speed
            r_speed = temp
            tank_pair.off()
            drive(l_speed, r_speed)

        # If grey has been sensed three times (its on a grey tile)
        # if grey_count >= 1:
        #     counted = False
        #     grey_count = 0
        #     # adjust()
        #     temp = l_speed
        #     l_speed = r_speed
        #     r_speed = temp
        #     tank_pair.off()
        #     drive(l_speed, r_speed)
        # if is_white() or is_black():
        #     grey_count = 0


# A method to bring the robot back onto the black and white tiles after it veers off course
def adjust():

    global black_count
    global counted

    adjust_val = 10
    a_count = 0
    back_up = False

    # Boolean to determine it turned left to get back on the tiles
    turn_left = True

    # Until you find a black or white tile, scan by turning left and right, increasing angle of turn by
    # 10 degrees each time.
    while is_grey():

        turn_left=False
        turn(adjust_val, spot = True, right = True)
        a_count += 1
        sleep(0.2)
        if is_white() or is_black():
            if is_black() and counted == False:
                count_black()
            break
        adjust_val += 10


        turn_left = True
        a_count += 1
        turn(degrees = adjust_val, spot = True, right = False)
        a_count += 1
        sleep(0.2)
        if is_white() or is_black():
            if is_black() and counted == False:
                count_black()
            break
        adjust_val += 10

    # Drive onto the black/white tile that was found
    tank_pair.on_for_degrees(left_speed = 40, right_speed = 40, degrees = 160)

    #If it turned left to get on the tiles, turn right to straighten up
    if turn_left:
        turn(degrees = (adjust_val/2) - 5, spot = False, right = True)
    #If it turned right to get on the tiles, turn left to straighten up
    else:
        turn(degrees = (adjust_val/2), spot = False, right = False)

    #Call back to drive
    drive(speed = 40)


# Makes 3 scans for the tower and drive in the direction of the shortest distance found to object
def sense_tower():


    dist_mid = 0
    dist_right = 0
    dist_left = 0

    sense_num = 0


    while not touch.is_pressed:


        # Ping tower, set dist_mid
        dist_mid = us.value()
        sleep(0.3)

        # Turn left, ping tower, set dist_left variable
        turn(degrees= 45, spot=True, right=False)
        dist_left = us.value()
        sleep(0.3)

        # Turn right, ping tower, set dist_right variable
        turn(degrees= 90, spot=True, right=True)
        dist_right = us.value()
        sleep(0.3)

        sense_num += 1

        # Turn toward shortest distance registered
        if dist_mid < dist_left and dist_mid < dist_right:
            turn(degrees = 45, spot = True, right = False)
        elif dist_left < dist_right and dist_left < dist_mid:
            turn(degrees = 90, spot = True, right = False)

        # After a few scans, drive less between checks to improve accuracy
        if sense_num <= 3:
            rot = 2
        elif 3 < sense_num < 5:
            rot = 1
        else:
            rot = 0.7
        tank_pair.on_for_rotations(left_speed=50, right_speed=50, rotations=rot)

    #Tower found

    tank_pair.on_for_degrees(left_speed = -10, right_speed = -10, degrees = 70)

    while True:
        tank_pair.on(left_speed=70, right_speed=70)
        sleep(1)
        if is_grey():
            break

    tank_pair.off()
    sleep(1)

    s.play_song((
        ('D4', 'e3'),
        ('D4', 'e3'),
        ('D4', 'e3'),
        ('G4', 'h'),
        ('D5', 'h')
    ))

# Main method that makes calls to the functions for each part of the task
def main():

    calibrate()

    start()

    drive(35, 25)

    turn(degrees = 90, spot = True, right = True)

    tank_pair.on_for_degrees(left_speed = 50, right_speed = 50, degrees = 3600)
    sleep(1)

    sense_tower()


try:
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while True:
        pass

