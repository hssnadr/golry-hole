import pyaudio
import wave

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 3 # seconds to record


class AudioRecorder:
    def __init__(self):
        # for ii in range(pyaudio.PyAudio.get_device_count()):
        #     print('')
        #     print('--------------------------')
        #     print(ii, '-', pyaudio.PyAudio.get_device_info_by_index(ii).get('name'))
        self.dev_index = 1 # device index found by p.get_device_info_by_index(ii)

        # path_files = os.path.join(os.path.dirname(__file__), '_files')
        # file_ = random.choice(os.listdir(path_files))
        self.file_name = '_files/test1.wav' # name of .wav file

        self.audio = pyaudio.PyAudio() # create pyaudio instantiation

    def record(self):
        # create pyaudio stream
        self.stream = self.audio.open(format = form_1,rate = samp_rate,channels = chans, \
                            input_device_index = self.dev_index,input = True, \
                            frames_per_buffer=chunk)
        print("recording")
        self.frames = []

        # loop through stream and append audio chunks to frame array
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            data = self.stream.read(chunk, exception_on_overflow = False)
            self.frames.append(data)
        
        print("finished recording")

        # stop the stream, close it, and terminate the pyaudio instantiation
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_audio(self):
        # save the audio frames as .wav file
        wavefile = wave.open(self.file_name,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(self.audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(self.frames))
        wavefile.close()