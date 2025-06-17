import tkinter as tk
from tkinter import filedialog
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.playback import play
import pygame
import mido
import os

# Initialize pygame mixer
pygame.mixer.init()
#kick = pygame.mixer.Sound("sounds/mixkit-pulsating-bass-transition-2295.wav")
#snare = pygame.mixer.Sound("sounds/mixkit-knocking-sub-bass-2300.wav")
#hihat = pygame.mixer.Sound("sounds/nice-bass-drum-sound-a-key-19-Ru1.wav")

# Constants
SAMPLE_RATE = 44100

# Load default drum samples
samples = {
    "Kick": "sounds/kick.wav",
    "Snare": "sounds/snare.wav",
    "HiHat": "sounds/hihat.wav"
}

# Play sample using pygame
def play_sample(sample_name):
    pygame.mixer.Sound(samples[sample_name]).play()

# Generate a sine wave
def generate_sine_wave(freq, duration=1.0, volume=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.sin(freq * t * 2 * np.pi)
    audio = wave * (volume * 32767)
    return audio.astype(np.int16)

# Play generated wave
def play_synth():
    wave = generate_sine_wave(freq_slider.get(), duration=1.0)
    sd.play(wave, SAMPLE_RATE)
    write("synth.wav", SAMPLE_RATE, wave)

# Record from microphone
def record_audio():
    duration = 3  # seconds
    recorded = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    write("recorded.wav", SAMPLE_RATE, recorded)
    print("Recording saved as recorded.wav")

# Save a simple beat
def export_beat():
    beat = AudioSegment.silent(duration=2000)  # 2-second silent base
    beat = beat.overlay(AudioSegment.from_wav(samples["Kick"]), position=0)
    beat = beat.overlay(AudioSegment.from_wav(samples["Snare"]), position=1000)
    beat.export("exported_beat.wav", format="wav")
    print("Beat exported as exported_beat.wav")

# Upload a new sample
def upload_sample(sample_type):
    file_path = filedialog.askopenfilename(
        title=f"Select a {sample_type} sample",
        filetypes=[("WAV files", "*.wav")]
    )
    if file_path:
        samples[sample_type] = file_path
        print(f"{sample_type} sample updated: {file_path}")

# GUI
root = tk.Tk()
root.title("Python Beat Maker")

# Buttons for samples
for name in samples:
    tk.Button(root, text=f"Play {name}", command=lambda n=name: play_sample(n)).pack()

# Synth controls
tk.Label(root, text="Synth Frequency (Hz)").pack()
freq_slider = tk.Scale(root, from_=100, to=1000, orient=tk.HORIZONTAL)
freq_slider.set(440)
freq_slider.pack()

tk.Button(root, text="Play Synth", command=play_synth).pack()
tk.Button(root, text="Record Audio", command=record_audio).pack()
tk.Button(root, text="Export Beat", command=export_beat).pack()

# Add upload buttons for each sample type
for name in samples:
    tk.Button(root, text=f"Upload {name}", command=lambda n=name: upload_sample(n)).pack()

# Run GUI
root.mainloop()
