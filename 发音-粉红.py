import time

import numpy as np
import sounddevice as sd


SAMPLE_RATE = 44100
CHANNELS = 1
VOLUME = 0.4
BUFFER_DURATION = 10


def generate_pink_noise(duration, sr, channels):
    num_samples = duration * sr
    white = np.random.randn(num_samples)
    X = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(num_samples, d=1/sr)
    freqs[0] = 1
    X = X / np.sqrt(freqs)
    pink = np.fft.irfft(X)
    pink = pink / np.max(np.abs(pink))
    pink = np.tile(pink.reshape(-1, 1), (1, channels))
    return pink

PINK_BUFFER = generate_pink_noise(BUFFER_DURATION, SAMPLE_RATE, CHANNELS)
BUFFER_LENGTH = len(PINK_BUFFER)
current_idx = 0

def audio_callback(outdata, frames, time_info, status):
    global current_idx

    end_idx = current_idx + frames
    if end_idx < BUFFER_LENGTH:
        noise = PINK_BUFFER[current_idx:end_idx]
        current_idx = end_idx
    else:
        remain = BUFFER_LENGTH - current_idx
        noise = np.empty((frames, CHANNELS))
        noise[:remain] = PINK_BUFFER[current_idx:]
        noise[remain:] = PINK_BUFFER[:frames - remain]
        current_idx = frames - remain

    outdata[:] = noise * VOLUME

def main():
    with sd.OutputStream(samplerate=SAMPLE_RATE,
                         channels=CHANNELS,
                         callback=audio_callback):
        while True:
            time.sleep(0.1)


if __name__ == "__main__":
    main()
