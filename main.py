import os
import random
import time
import keyboard
import threading
import vlc

import sensor_hcsr04 as hc

# MAIN
path_files = os.path.join(os.path.dirname(__file__), '_files')
running = False
timerVTrig0 = 0
delayVTrig = 0.1 # seconds

# VLC
audio_volume = 125

# SENSOR
dist_sensor = None
pin_trig = 23
pin_echo = 24
dist_threshold = 10

# PLAYER
# vlc_player = vlc.Instance('--es-fps=15')
vlc_player = vlc.Instance()
audio_player = vlc_player.media_player_new()

# AUDIO OUTPUT
devices = []
mods = audio_player.audio_output_device_enum()
print("Available audio devices:")
if mods:
    mod = mods
    while mod:
        mod = mod.contents
        devices.append(mod.device)
        print("-", len(devices), ":", mod.device)
        mod = mod.next
vlc.libvlc_audio_output_device_list_release(mods) # frees the list of available audio output devices (cf. doc)
audio_output = devices[1]
print("Audio output set to:", audio_output)

def play_golryjoke(golry_file_):
    global audio_player
    path_ = os.path.join(path_files, golry_file_)
    print("Start playing", path_)
    media_ = vlc.Media(path_)
    audio_player.set_media(media_)
    audio_player.audio_set_volume(audio_volume)
    audio_player.audio_output_device_set(None, audio_output)
    audio_player.play()

def keyboard_interact():
    global running
    while running:
        if keyboard.read_key() == "a":
            file_ = random.choice(os.listdir(path_files))
            play_golryjoke(file_)

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
        while running:
            dist_sensor.update()

            if time.time() - timerVTrig0 > delayVTrig :
                timerVTrig0 = time.time()
                print(dist_sensor.get_distance())
                print("Is media playing ?", audio_player.is_playing(), "!!!")
                if dist_sensor.get_distance() < dist_threshold and audio_player.is_playing() == False:
                    print("go")
                    file_ = random.choice(os.listdir(path_files))
                    play_golryjoke(file_)
                    print("----------------------------")

        print("MAIN IS OVER")

    except KeyboardInterrupt:
        quit()