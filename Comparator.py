# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:30:28 2019

@author: Maria Ausilia Napoli Spatafora
"""

from AudioManaging import AudioManaging
from FourierTransform import FourierTransform
from Graphs import Graphs
from FrequencyCompression import FrequencyCompression

cutoff = 4000
ratio = 0.5
CR = 2
samplerate = 44100
name = "Audio"
number = 12
am = AudioManaging()
am_lp = AudioManaging() #low pass
am_ct = AudioManaging() #compression technique
ft_lp = FourierTransform() #low pass
ft_ct = FourierTransform() #compression technique
gr = Graphs()
fc_lp = FrequencyCompression(cutoff, ratio, CR, samplerate) #low pass
fc_ct = FrequencyCompression(cutoff, ratio, CR, samplerate) #compression technique

for i in range (1, number):
#1 - Take path
    path = "./records/testing/{:s}{:d}/{:s}{:d}.wav"\
                        .format(name, i, name, i)
#2 - Read wav file
    am.read_file(path)
#3a - Time to Frequency domain for low pass filter
    ft_lp.time_to_frequency(am.audio_file[i-1])
#4a - Applying low pass filter
    fc_lp.example_2(ft_lp.audio_fft[i-1])
#5a - Frequency to Time domain for low pass filter
    ft_lp.frequency_to_time(fc_lp.audio_fc[i-1])
#6a - Save new wav file with low pass filter
    signal = am.convert_numpy(ft_lp.audio_ifft[i-1])
    am.save_file("testing/Audio{}/{}lp".format(i,name), i, am.audio_file[i-1][1], signal.T)
#3a - Time to Frequency domain for compression technique
    ft_ct.time_to_frequency(am.audio_file[i-1])
#4b - Applying compression technique
    fc_ct.technique_2(ft_ct.audio_fft[i-1])
#5b - Frequency to Time domain for compression technique 
    ft_ct.frequency_to_time(fc_ct.audio_fc[i-1])
#6b - Save new wav file with compression technique
    signal = am.convert_numpy(ft_ct.audio_ifft[i-1])
    am.save_file("testing/Audio{}/{}ct".format(i, name), i, am.audio_file[i-1][1], signal.T)  
#7 - Print metadata and read new wav files
    #am.print_metadata(path)
    am_lp.read_file("./records/testing/{:s}{:d}/{:s}lp_{:d}.wav"\
                        .format(name, i, name, i))
    am_ct.read_file("./records/testing/{:s}{:d}/{:s}ct_{:d}.wav"\
                        .format(name, i, name, i))
#8 - Plot waveform and spectrogram
    gr.waveform(am.audio_file[i-1])
    gr.waveform(am_lp.audio_file[i-1])
    gr.waveform(am_ct.audio_file[i-1])
    gr.spectrogram(am.audio_file[i-1])
    gr.spectrogram(am_lp.audio_file[i-1])
    gr.spectrogram(am_ct.audio_file[i-1])
    
