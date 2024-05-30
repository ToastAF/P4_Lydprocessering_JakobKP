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


def plain_reverberator(input_wave, delay, filter_param):
    n_data = np.size(input_wave)
    output_wave = np.zeros(n_data)
    for n in np.arange(n_data):
        if n < delay:
            output_wave[n] = input_wave[n]
        else:
            output_wave[n] = input_wave[n] + filter_param * output_wave[n - delay]
    return output_wave


def plain_gain_from_reverb_time(reverb_time, plain_delay, sample_rate):
    n_delays = np.size(plain_delay)
    plain_gains = np.zeros(n_delays)
    for i in np.arange(n_delays):
        plain_gains[i] = 10**(-3*plain_delay[i]/(reverb_time*sample_rate))
    return plain_gains


def allpass_reverberator(input_wave, delay, ap_param):
    n_data = np.size(input_wave)
    output_wave = np.zeros(n_data)
    for n in np.arange(n_data):
        if n < delay:
            output_wave[n] = input_wave[n]
        else:
            output_wave[n] = ap_param * input_wave[n] + input_wave[n-delay] - ap_param * output_wave[n-delay]
    return output_wave


def schroeders_reverberator(input_wave, mixing_param, plain_delay, plain_gain, ap_delay, ap_param):
    n_data = np.size(input_wave)
    tmp_signal = np.zeros(n_data)

    n_plain_reverberators = np.size(plain_delay)
    for i in np.arange(n_plain_reverberators):
        tmp_signal = tmp_signal + mixing_param[i] * plain_reverberator(input_wave, plain_delay[i], plain_gain[i])

    n_ap_reverberators = np.size(ap_delay)
    for i in np.arange(n_ap_reverberators):
        tmp_signal = allpass_reverberator(tmp_signal, ap_delay[i], ap_param[i])
    return tmp_signal


def play_sound(freq, waveform):
    new_duration = reverb_slider.get() + duration
    wave = generate_sine_wave(freq, new_duration, sample_rate, waveform)

    reverb_time = reverb_slider.get() # This should get the rever time from the slider in the GUI
    if reverb_slider.get() != 0:
        mixing_param = np.array([0.3, 0.15, 0.35, 0.2])
        plain_delays = np.array([300, 500, 700, 900])
        ap_delays = np.array([200, 300])
        ap_params = np.array([-0.9, 0.9])

        plain_gains = plain_gain_from_reverb_time(reverb_time, plain_delays, sample_rate)

    #ir_length = int(np.floor(reverb_time * sample_rate)) # Impulse response length
    #impulse = np.r_[np.array([1]), np.zeros(ir_length-1)]
    #impulse_response = schroeppel_reverberator(impulse, mixing_param, plain_delays, plain_gains, ap_delays, ap_params)

        reverbed_wave = schroeders_reverberator(wave, mixing_param, plain_delays, plain_gains, ap_delays, ap_params)

        sd.play(reverbed_wave, sample_rate)
        sd.wait()
    elif reverb_slider.get() == 0:
        sd.play(wave, sample_rate)
        sd.wait()


root = tk.Tk()
root.geometry('300x400')
root.title("JakobSynth")

#Different frames to seperate things :)
top_frame = tk.Frame(root)
top_frame.pack(side="top")
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom")

#The sliders are in the top of the GUI
reverb_slider = tk.Scale(top_frame, from_=0, to=0.4, resolution=0.1, orient="horizontal", label="Reverb Time")
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
