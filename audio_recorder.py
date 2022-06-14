import pyaudio
import wave

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 5 # seconds to record


class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio() # create pyaudio instantiation
        
        print("----------------------------")
        print("AUDIO RECORDER - AUDIO DEVICES")
        for ii in range(self.audio.get_device_count()):
            print(ii, '-', self.audio.get_device_info_by_index(ii).get('name'))
        self.dev_index = 1 # device index found by p.get_device_info_by_index(ii)
        print("Set to: ", self.audio.get_device_info_by_index(self.dev_index).get('name'))
        print("----------------------------")

        # path_files = os.path.join(os.path.dirname(__file__), '_files')
        # file_ = random.choice(os.listdir(path_files))
        # self.file_name = '_files/test1.wav' # name of .wav file

        self.is_recording = False

    def __del__(self):
        self.audio.terminate()
    
    def is_recording(self) -> bool:
        return self.is_recording
    
    def record(self):
        # create pyaudio stream
        stream = self.audio.open(format = form_1,rate = samp_rate,channels = chans, \
                            input_device_index = self.dev_index,input = True, \
                            frames_per_buffer=chunk)
        print("recording")
        self.frames = []

        # loop through stream and append audio chunks to frame array
        self.is_recording = True
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            data = stream.read(chunk, exception_on_overflow = False)
            self.frames.append(data)
        
        self.is_recording = False
        print("finished recording")

        # stop the stream, close it, and terminate the pyaudio instantiation
        stream.stop_stream()
        stream.close()

    def save_audio(self, file_name_):
        # save the audio frames as .wav file
        wavefile = wave.open(file_name_,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(self.audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(self.frames))
        wavefile.close()
        print("Saved" + file_name_)