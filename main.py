import os
import random
import time
import keyboard
import threading

import sensor_hcsr04 as hc

# MAIN
# dirname = os.path.dirname(__file__)
path_files = os.path.join(os.path.dirname(__file__), '_files')
running = False

# SENSOR
dist_sensor = None
pin_trig = 23
pin_echo = 24
dist_threshold = 30

def keyboard_interact():
    global running
    while running:
        if keyboard.read_key() == "esc":
            print("ESC was pressed. quitting...")
            quit()

def quit():
    global running
    global dist_sensor
    del dist_sensor
    running = False
    print('Quit program...')

if __name__ == '__main__':
    try:
        print("Enter the Golry Hole")
        
        # Main
        running = True
        dist_sensor = hc.HCSR04(pin_trig, pin_echo)

        # Keyboard
        try:
            keyboard_thread = threading.Thread(
                target=keyboard_interact, daemon=True)
            keyboard_thread.start()
        except:
            print("Error: unable to start keyboard thread")

        print("Ok let's go")
        print(random.choice(os.listdir(path_files)))
        while running:
            print(random.choice(os.listdir(path_files)))
            # dist_sensor.update()
            # print(dist_sensor.get_distance())
            time.sleep(0.5)

        print("MAIN IS OVER")

    except KeyboardInterrupt:
        quit()