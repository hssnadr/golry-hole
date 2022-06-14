import os
import time
import vlc

# PLAYER
vlc_player = vlc.Instance('--es-fps=15')
# vlc_player = vlc.Instance()
audio_player = vlc_player.media_player_new()
audio_volume = 125

# AUDIO OUTPUT
devices = []
mods = audio_player.audio_output_device_enum()
print("----------------------------")
print("VLC PLAYER - AUDIO DEVICES")
print("Available audio devices:")
if mods:
    mod = mods
    while mod:
        mod = mod.contents
        devices.append(mod.device)
        print("-", len(devices), ":", mod.device)
        mod = mod.next
vlc.libvlc_audio_output_device_list_release(mods) # frees the list of available audio output devices (cf. doc)
audio_output = devices[0]
print("Audio output set to:", audio_output)
print("----------------------------")

def play_golryjoke(golry_file_):
    global audio_player
    # path_ = os.path.join(path_files, golry_file_)
    print("Start playing", golry_file_)
    media_ = vlc.Media(golry_file_)
    # media_ = vlc.Media("/home/pi/Music/LookLikeKill_07_Intro.wav")
    audio_player.set_media(media_)
    audio_player.audio_set_volume(audio_volume)
    audio_player.audio_output_device_set(None, audio_output)
    audio_player.play()

def stop():
    audio_player.stop()

def is_playing() -> bool:
    return audio_player.is_playing()