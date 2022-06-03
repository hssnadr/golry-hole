
import pyaudio
import wave
import sys

CHUNK = 1024

# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

# wf = wave.open(sys.argv[1], 'rb')
wf = wave.open("/home/pi/Music/TrackAudio.wav", 'rb')


p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()

# import wave
# obj = wave.open('/home/pi/Music/TrackAudio.wav','r')
# print( "Number of channels",obj.getnchannels())
# print ( "Sample width",obj.getsampwidth())
# print ( "Frame rate.",obj.getframerate())
# print ("Number of frames",obj.getnframes())
# print ( "parameters:",obj.getparams())
# obj.close()