# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:30:28 2019

@author: Maria Ausilia Napoli Spatafora
"""

from AudioManaging import AudioManaging
from FourierTransform import FourierTransform
from Graphs import Graphs
from FrequencyCompression import FrequencyCompression

low_cutoff = 2500
high_cutoff = 6000
cutoff_lp = 10000 #or 8000
ratio = 0.5
CR = 2
samplerate = 44100
n = 6 #order LP butter filter
name = "Tone" #or "Xylo" #or "Audio" #or "Track" or #Music
number = 8 #or 6 #or 12 #or 6 #or 4
am = AudioManaging()
am_lp = AudioManaging() #low pass
am_ct = AudioManaging() #compression technique
am_hp = AudioManaging() #high pass
am_ctlp = AudioManaging() #before compression technique, after low pass
ft_lp = FourierTransform() #low pass
ft_ct = FourierTransform() #compression technique
ft_hp = FourierTransform() #high pass
ft_ctlp = FourierTransform() #before compression technique, after low pass 
gr = Graphs()
fc_lp = FrequencyCompression(low_cutoff, high_cutoff, ratio, CR, samplerate) #low pass
fc_ct = FrequencyCompression(low_cutoff, high_cutoff, ratio, CR, samplerate) #compression technique
fc_hp = FrequencyCompression(low_cutoff, high_cutoff, ratio, CR, samplerate) #high pass
fc_ctlp = FrequencyCompression(cutoff_lp, cutoff_lp, ratio, CR, samplerate) #before compression technique, after low pass

for i in range (1, number):
#1 - Take path
    path = "./records/testing/{:s}{:d}/{:s}{:d}.wav"\
                        .format(name, i, name, i)
#2 - Read wav file
    am.read_file(path)
#3a - Time to Frequency domain for low pass filter
    ft_lp.time_to_frequency(am.audio_file[i-1])
#4a - Applying low pass filter
    fc_lp.applyLPButter(ft_lp.audio_fft[i-1])
#5a - Frequency to Time domain for low pass filter
    ft_lp.frequency_to_time(fc_lp.audio_fc[i-1])
#6a - Save new wav file with low pass filter
    signal = am.convert_numpy(ft_lp.audio_ifft[i-1])
    am.save_file("testing/{}{}/{}lp".format(name, i,name), i, am.audio_file[i-1][1], signal.T)
#3b - Time to Frequency domain for compression technique
    ft_ct.time_to_frequency(am.audio_file[i-1])
#4b - Applying compression technique
    fc_ct.technique_a(ft_ct.audio_fft[i-1])
#5b - Frequency to Time domain for compression technique 
    ft_ct.frequency_to_time(fc_ct.audio_fc[i-1])
#6b - Save new wav file with compression technique
    signal = am.convert_numpy(ft_ct.audio_ifft[i-1])
    am.save_file("testing/{}{}/{}ct".format(name, i, name), i, am.audio_file[i-1][1], signal.T)
#3c - Time to Frequency domain for high pass filter
    ft_hp.time_to_frequency(am.audio_file[i-1])
#4c - Applying high pass filter
    fc_hp.applyHPButter(ft_hp.audio_fft[i-1])
#5c - Frequency to Time domain for high pass filter
    ft_hp.frequency_to_time(fc_hp.audio_fc[i-1])
#6c - Save new wav file with high pass filter
    signal = am.convert_numpy(ft_hp.audio_ifft[i-1])
    am.save_file("testing/{}{}/{}hp".format(name, i,name), i, am.audio_file[i-1][1], signal.T)    
#7 - Read new wav files
    am_lp.read_file("./records/testing/{:s}{:d}/{:s}lp_{:d}.wav"\
                        .format(name, i, name, i))
    am_ct.read_file("./records/testing/{:s}{:d}/{:s}ct_{:d}.wav"\
                        .format(name, i, name, i))
    am_hp.read_file("./records/testing/{:s}{:d}/{:s}hp_{:d}.wav"\
                        .format(name, i, name, i))
#8 - Apply low pass Butter filter in frequency domain, save and read new wav file
    ft_ctlp.time_to_frequency(am_ct.audio_file[i-1])
    fc_ctlp.applyLPButter(ft_ctlp.audio_fft[i-1])
    ft_ctlp.frequency_to_time(fc_ctlp.audio_fc[i-1])
    signal = am_ct.convert_numpy(ft_ctlp.audio_ifft[i-1])
    am_ct.save_file("testing/{}{}/{}ctlp".format(name, i, name), i, am_ct.audio_file[i-1][1], signal)
    am_ctlp.read_file("./records/testing/{:s}{:d}/{:s}ctlp_{:d}.wav"\
                        .format(name, i, name, i))
#9 - Plot and save waveform and spectrogram
    gr.waveform(am.audio_file[i-1])
    gr.waveform(am_lp.audio_file[i-1])
    gr.waveform(am_ct.audio_file[i-1])
    gr.waveform(am_ctlp.audio_file[i-1])
    gr.spectrogram(am.audio_file[i-1])
    gr.spectrogram(am_lp.audio_file[i-1])
    gr.spectrogram(am_ct.audio_file[i-1])
    gr.spectrogram(am_ctlp.audio_file[i-1])
    
