# golry-hole
 
Add _files/ folder to fill with audio files

## requirements
pip install python-vlc
pip install PyAudio
sudo pip install python-osc

Neopixel
sudo pip install rpi_ws281x adafruit-circuitpython-neopixel
sudo pip install rpi_ws281x adafruit-circuitpython-neoxel
Turn off audio on pin 18:
sudo nano /boot/config.txt
change: dtparam=audio=on
to: dtparam=audio=off
then reboot

need to run: sudo apt-get install python3-pyaudio 
to fix 'ImportError: libportaudio.so.2: cannot open shared object file: No such file or directory'

## Enhance audio
see: https://raspberrypi.stackexchange.com/questions/106827/how-to-increase-mic-input-volume