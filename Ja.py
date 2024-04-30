import sounddevice as sd
import tkinter as tk
import numpy as np
import soundfile as sf
import librosa


class Synthesizer:
    sample_rate = 44100
    frequency = 0
    duration = 1

    def __init__(self, master):
        self.master = master
        master.title("Synthesizer")

        self.frequency_slider = tk.Scale(master, from_=10, to=1000, orient="horizontal", label="Frequency")
        self.frequency_slider.pack()

        self.waveform_menu = tk.OptionMenu(master, tk.StringVar(), "Sine", "Square", "Triangle")
        self.waveform_menu.pack()

        self.play_button = tk.Button(master, text="Play", command=self.play_audio)
        self.play_button.pack()

    def play_audio(self, wave, s_rate):
        #sd.play(wave, s_rate)
        #sd.wait()
        print('Playing sound...')


def generate_sine_wave(freq, dur, s_rate):
    t = np.linspace(0, dur * s_rate, endpoint=False)
    wave = np.sin(2 * np.pi * freq * t / s_rate)
    return wave


def play_sound(wave, s_rate):
    sd.play(wave, s_rate)
    sd.wait()


sound = generate_sine_wave(440, 1, 44100)
sf.write('temp_sound.wav', sound, 44100)
y_audio, sr_audio = librosa.load('temp_sound.wav', sr=None)
play_sound(y_audio, sr_audio)

root = tk.Tk()
root.geometry('200x200')
app = Synthesizer(root)
root.mainloop()
