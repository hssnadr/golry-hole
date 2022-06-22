import os
import time
import random
import RPi.GPIO as GPIO

import gpio_button as btn
import audio_recorder as rec
import sensor_hcsr04 as hc
import golry_player as player

# MAIN
running = False
path_folder = os.path.join(os.path.dirname(__file__), '_files')
def get_file_path(file_name_):
    return os.path.join(path_folder, file_name_)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# TEST
GPIO.setup(25,GPIO.OUT) # to remove

# --------------------------------------------------------
# BUTTON
button = btn.Button(17)

# SENSOR
timer_trigsens_0 = 0
delay_sens = 0.1 # seconds
dist_threshold_in = 10
dist_threshold_out = 50
timer_out_0 = -1
delay_out = 1.0 # second
pin_trig = 23
pin_echo = 24
dist_sensor = hc.HCSR04(pin_trig, pin_echo)

# AUDIO RECORDER
recorder = rec.AudioRecorder()
def save_record(file_name_):
    global recorder
    path_file_ = get_file_path(file_name_)
    # recorder.start()
    recorder.save_audio(path_file_  + ".wav")

def quit():
    global running
    global button
    global dist_sensor
    global recorder
    del button
    del dist_sensor
    del recorder
    running = False
    print('Quit program...')
    GPIO.cleanup()

# --------------------------------------------------------
if __name__ == '__main__':
    try:
        # START PROGRAMM
        print("Enter the Golry Hole")
        running = True
        while running:
            if not recorder.is_recording():
                # BUTTON RECORDER
                button.update()
                if button.get_bang():
                    # file_rec_ = "vocal_" + time.strftime("%Y%m%d_%H%M%S")
                    # start_record(file_rec_)
                    recorder.start() # start recording

                # SENSITIVE PLAYER
                dist_sensor.update()
                if time.time() - timer_trigsens_0 > delay_sens :
                    timer_trigsens_0 = time.time()
                    # print(dist_sensor.get_distance())
                    # print("Is media playing ?", player.is_playing(), "!!!")
                    
                    # Start listening
                    if dist_sensor.get_distance() < dist_threshold_in and player.is_playing() == False:
                        if len(os.listdir(path_folder)) > 0:
                            file_ = random.choice(os.listdir(path_folder))
                            file_path_ = get_file_path(file_)
                            player.play_golryjoke(file_path_)
                            time.sleep(1)
                            print("----------------------------")
                    
                    # Stop listening
                    if dist_sensor.get_distance() > dist_threshold_out and player.is_playing() == True:
                        if timer_out_0 == -1:
                            print("start stop")
                            timer_out_0 = time.time()
                        else :
                            if time.time() - timer_out_0  > delay_out:
                                print("stop!!!!")
                                player.stop()

                    if dist_sensor.get_distance() < dist_threshold_out:
                        timer_out_0 = -1
                # Reset stop timer
                if player.is_playing() == False:
                    timer_out_0 = -1

                time.sleep(0.1)
            
            else :
                recorder.update()

                # print("ta gueule")
                # print("ta gueule")
                # print("ta gueule")
                # print("ta gueule")
                # print("ta gueule")
                # print("ta gueule")
                # print("ta gueule")
                # GPIO.output(25, True)
                # GPIO.output(25, False)
                # GPIO.output(25, True)
                # GPIO.output(25, False)
                # GPIO.output(25, True)
                # GPIO.output(25, False)
                # GPIO.output(25, True)
                # GPIO.output(25, False)
                # GPIO.output(25, True)
                # GPIO.output(25, False)
                # GPIO.output(25, True)
                # GPIO.output(25, False)
                
                if recorder.ellapsed_record() > 25.0:
                    recorder.stop()
                    file_name_ = "vocal_" + time.strftime("%Y%m%d_%H%M%S")
                    save_record(file_name_)

    except KeyboardInterrupt:
        quit()