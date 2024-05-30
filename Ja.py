import sounddevice as sd
import tkinter as tk
from tkinter import ttk
import numpy as np

#Frequencies for the different notes
frequency_a = 440 # A
frequency_a_sharp = 466.2 # A#
frequency_b = 493.9 # B
frequency_c = 523.3 # C
frequency_c_sharp = 554.4 # C#
frequency_d = 587.3 # D
frequency_d_sharp = 622.3 # D#
frequency_e = 659.3 # E

sample_rate = 44100
duration = 0.5 # The sounds should last a small amount of time


def generate_sine_wave(freq, dur, s_rate, waveform):
    if waveform == "Sine":
        t = np.linspace(0, dur, int(s_rate * dur), endpoint=False)
        wave = np.sin(2 * np.pi * freq * t) # Sine wave
        return wave
    elif waveform == "Square":
        t = np.linspace(0, dur, int(s_rate * dur), endpoint=False)
        wave = np.sign(np.sin(2 * np.pi * freq * t)) # Square wave
        return wave


def apply_reverb(wave, reverb_amount):
    delay = int(sample_rate * 0.02)
    reverb_wave = np.copy(wave)
    for i in range(delay, len(wave)):
        reverb_wave[i] += reverb_amount * reverb_wave[i - delay]
    reverb_wave = reverb_wave / (1 + reverb_amount)
    return reverb_wave


def play_sound(freq, waveform):
    wave = generate_sine_wave(freq, duration, sample_rate, waveform)

    reverb = reverb_slider.get() / 100
    if reverb > 0:
        wave = apply_reverb(wave, reverb)

    sd.play(wave, sample_rate)
    sd.wait()


root = tk.Tk()
root.geometry('800x400')
root.title("JakobSynth")

#Different frames to seperate things :)
top_frame = tk.Frame(root)
top_frame.pack(side="top")
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom")

#The sliders are in the top of the GUI
reverb_slider = tk.Scale(top_frame, from_=0, to=100, orient="horizontal", label="Reverb")
reverb_slider.pack()

strings = tk.StringVar()
waveform_menu = ttk.Combobox(top_frame, width=15, textvariable=strings)
waveform_menu['values'] = ("Sine", "Square")
waveform_menu.pack(pady=5)

#The buttons are in the bottom of the GUI
key1_button = tk.Button(bottom_frame, text="Play A", command=lambda: play_sound(frequency_a, strings.get()))
key1_button.pack(pady=5)
key2_button = tk.Button(bottom_frame, text="Play A#", command=lambda: play_sound(frequency_a_sharp, strings.get()))
key2_button.pack(pady=5)
key3_button = tk.Button(bottom_frame, text="Play B", command=lambda: play_sound(frequency_b, strings.get()))
key3_button.pack(pady=5)
key4_button = tk.Button(bottom_frame, text="Play C", command=lambda: play_sound(frequency_c, strings.get()))
key4_button.pack(pady=5)
key5_button = tk.Button(bottom_frame, text="Play C#", command=lambda: play_sound(frequency_c_sharp, strings.get()))
key5_button.pack(pady=5)
key6_button = tk.Button(bottom_frame, text="Play D", command=lambda: play_sound(frequency_d, strings.get()))
key6_button.pack(pady=5)
key7_button = tk.Button(bottom_frame, text="Play D#", command=lambda: play_sound(frequency_d_sharp, strings.get()))
key7_button.pack(pady=5)
key8_button = tk.Button(bottom_frame, text="Play E", command=lambda: play_sound(frequency_e, strings.get()))
key8_button.pack(pady=5)


waveform_menu.current(0)
root.mainloop()
