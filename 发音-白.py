import time

import numpy as np
import sounddevice as sd


SAMPLE_RATE = 44100
CHANNELS = 1
VOLUME = 0.2


def audio_callback(outdata, frames, time_info, status):
    noise = np.random.uniform(low=-1.0, high=1.0, size=(frames, CHANNELS)) * VOLUME
    outdata[:] = noise


def main():
    with sd.OutputStream(samplerate=SAMPLE_RATE, 
                            channels=CHANNELS, 
                            callback=audio_callback):
        while True:
            time.sleep(0.1)
                

if __name__ == "__main__":
    main()
