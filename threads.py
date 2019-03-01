#!/ usr/ bin / env python3
from ev3dev2 . sensor . lego import TouchSensor
from ev3dev2 . led import Leds
from ev3dev2 . button import Button
from ev3dev2 . sound import Sound
from time import sleep
from threading import Thread

# Will use touch sensor
ts = TouchSensor ()
sound = Sound ()

# Function that plays a tone
def playtone ():
    for j in range (0 , 20): # Do twenty times .
        sound . tone (1000 , 200) # 1000 Hz for 0.2 s
        sleep (0.5)

t = Thread(target = playtone) # Create a thread that will execute the playtone function
t. setDaemon(True) # Make the thread a deamon ( will stop when main program stops )
t. start() # Run the thread
btn = Button() # will use buttons
leds = Leds()

while not btn . backspace :
    if ts . value () == 0: # while button is not pressed
        leds . set_color ('LEFT ', 'RED ')
        sleep (0.1) # do nothing other than wait
    elif ts . value () == 1: # while button is pressed
        leds . set_color ('LEFT', 'GREEN ')
        sleep (0.1) # do nothing other than wait


sound.beep ()
leds.all_off ()