def sense_tower():
    dist_mid = 0
    dist_right = 0
    dist_left = 0
    sense_num = 0

    #is_pressed needs updated to sensor name
    while not is_pressed:
        # Ping tower, set dist_mid
        dist_mid = distance_centimeters_ping()
        sleep(0.3)

        # Turn left, ping tower, set dist_left variable
        tank_pair.on_for_degrees(left_speed=15, right_speed=-15, degrees=83.75)
        dist_left = distance_centimeters_ping
        sleep(0.3)

        # Turn right, ping tower, set dist_right variable
        tank_pair.on_for_degrees(left_speed=-15, right_speed=15, degrees=167.5)
        dist_right = distance_centimeters_ping
        sleep(0.3)

        #Update sense_num
        sense_num += 1

        # Turn towards direction closest to tower
        if dist_mid < dist_left and dist_mid < dist_right:
            tank_pair.on_for_degrees(left_speed=15, right_speed=-15, degrees=83.75)
        elif dist_left < dist_right and dist_left < dist_mid:
            tank_pair.on_for_degrees(left_speed=15, right_speed=-15, degrees=167.5)

        # Drives 2 rotations/sense_num
        rot = 2/sense_num
        tank_pair.on_for_rotations(left_speed=30, right_speed=30, rotations=rot )

    #While on the black square, push tower
    while is_black():
        tank_pair.on(left_speed=70, right_speed=70)

    #Play note once tower is off the black square
    s.play_tone(frequency=500, duration=0.2, delay=0, volume=100, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)