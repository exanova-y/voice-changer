import pyaudio
import numpy as np
from scipy.signal import resample
import time

# capture input
chunk = 1024
audio_format = pyaudio.paInt16 # from negative 2^16 to +ve int 16 
num_channels = 1 # mono. the number of independent audio signals
sampling_rate = 44100 # sampling rate
pitch_shift = 0.8
virtual_audio_cable_index = None

def get_audio_input():
    data = np.frombuffer(input_stream.read(chunk), dtype=np.int16)
    return data

def simple_pitch_shift(data, shift):
    # each second becomes 1.5? or whatever value shift is?
    # changes the pitch by altering playback speed
    indices = np.round(np.arange(0, len(data), shift)) # use round since np.arange might not be stable
    indices = indices[indices < len(data)].astype(int) # only return indices smaller than the length of data
    return data[indices]

# write audio data to output stream
def play_output(data):
    output_stream.write(data.astype(np.int16).tobytes())

 
def find_virtual_audio_cable():
    for i in range(p.get_device_count()):
        device = p.get_device_info_by_index(i)
        print(f"Index {i}: {device['name'].encode('utf-8', 'ignore').decode('utf-8')}")
        if "Virtual Audio Cable" in device['name']:
            virtual_audio_cable_index = i
            print(i)            
            break
    if virtual_audio_cable_index is None:
        print("there is no VCA, maybe you wanna install it first")

p = pyaudio.PyAudio() # initializes audio library
# input instance
input_stream = p.open(format = audio_format, channels=num_channels, rate=sampling_rate, input=True, frames_per_buffer=chunk)

# output instance
output_stream = p.open(format=audio_format,channels=num_channels,rate=sampling_rate, output=True, output_device_index=virtual_audio_cable_index, frames_per_buffer=chunk)
find_virtual_audio_cable()

print("listening...")
try:
    while True:
        input_data = get_audio_input()
        output_data = simple_pitch_shift(input_data, pitch_shift)
        output_stream.write(output_data.astype(np.int16).tobytes())

except KeyboardInterrupt:
    print("exiting loop")

input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()