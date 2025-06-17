import tkinter as tk
from tkinter import filedialog
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.playback import play
import pygame
import os
import time

# Initialize pygame mixer
pygame.mixer.init()

SAMPLE_RATE = 44100

samples = {
    "Kick": "sounds/kick.wav",
    "Snare": "sounds/snare.wav",
    "HiHat": "sounds/hihat.wav"
}

def play_sample(sample_name):
    pygame.mixer.Sound(samples[sample_name]).play()

def generate_sine_wave(freq, duration=1.0, volume=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.sin(freq * t * 2 * np.pi)
    audio = wave * (volume * 32767)
    return audio.astype(np.int16)

def play_synth():
    wave = generate_sine_wave(freq_slider.get(), duration=1.0)
    sd.play(wave, SAMPLE_RATE)
    write("synth.wav", SAMPLE_RATE, wave)

def record_audio():
    duration = 3  # seconds
    recorded = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    write("recorded.wav", SAMPLE_RATE, recorded)
    print("Recording saved as recorded.wav")

def export_beat():
    beat = AudioSegment.silent(duration=2000)  # 2-second silent base
    beat = beat.overlay(AudioSegment.from_wav(samples["Kick"]), position=0)
    beat = beat.overlay(AudioSegment.from_wav(samples["Snare"]), position=1000)
    beat.export("exported_beat.wav", format="wav")
    print("Beat exported as exported_beat.wav")

def upload_sample(sample_type):
    file_path = filedialog.askopenfilename(
        title=f"Select a {sample_type} sample",
        filetypes=[("WAV files", "*.wav")]
    )
    if file_path:
        samples[sample_type] = file_path
        print(f"{sample_type} sample updated: {file_path}")

# --- Step Sequencer Logic ---
NUM_STEPS = 16
instruments = list(samples.keys())
sequence = [[0 for _ in range(NUM_STEPS)] for _ in instruments]

def toggle_cell(row, col):
    sequence[row][col] = 1 - sequence[row][col]
    btn = grid_buttons[row][col]
    btn.config(bg="green" if sequence[row][col] else "white")

def play_sequence():
    bpm = bpm_slider.get()
    interval = 60 / bpm / 4  # 16 steps per bar (4 beats)
    for step in range(NUM_STEPS):
        for row, inst in enumerate(instruments):
            if sequence[row][step]:
                play_sample(inst)
        root.update()
        time.sleep(interval)

# --- GUI ---
root = tk.Tk()
root.title("Python Beat Maker")

# Step Sequencer Grid
tk.Label(root, text="Step Sequencer").pack()
grid_frame = tk.Frame(root)
grid_frame.pack()

grid_buttons = []
for row, inst in enumerate(instruments):
    tk.Label(grid_frame, text=inst).grid(row=row, column=0)
    row_buttons = []
    for col in range(NUM_STEPS):
        btn = tk.Button(grid_frame, width=2, bg="white",
                        command=lambda r=row, c=col: toggle_cell(r, c))
        btn.grid(row=row, column=col+1)
        row_buttons.append(btn)
    grid_buttons.append(row_buttons)

tk.Button(root, text="Play Sequence", command=play_sequence).pack(pady=5)

bpm_slider = tk.Scale(root, from_=60, to=180, orient=tk.HORIZONTAL, label="BPM")
bpm_slider.set(120)
bpm_slider.pack()

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

root.mainloop()

