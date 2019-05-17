# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 19:19:19 2019

@author: Maria Ausilia Napoli Spatafora
"""

from AudioManaging import AudioManaging
from FourierTransform import FourierTransform
from Graphs import Graphs
from FrequencyCompression import FrequencyCompression

def test_AudioManaging_1(first=1): #first=1 for initial operations on input; first=0 for last operation on output
    a = AudioManaging()
    if first == 1:
        for i in range (1, 6):
            path = a.join_audio_channels("./records/sample_{:d}n.wav"\
                        .format(i))
            path = a.resampling(path)
            a.read_file(path)
        for i in range(0, 5):
            entry = a.audio_file[i]
            a.print_metadata(entry)
    else:
       for i in range (1, 6):
           path = a.join_audio_channels("./records/output_{:d}.wav"\
                        .format(i), 1)
           a.read_file(path) 
    return a.audio_file
    
def test_AudioManaging_2(list_ifft, list_file): #last operation on files
    a = AudioManaging()
    for i in range(len(list_ifft)):
        signal = a.convert_numpy(list_ifft[i])
        a.save_file("output", i+1, list_file[i][1], signal)
    
def test_FourierTransform_1(list_file): #from time to frequency space
    f = FourierTransform()
    for i in range (len(list_file)):
        f.time_to_frequency(list_file[i])
    return f.audio_fft
    
def test_FourierTransform_2(list_fft): #from frequency to time space
    f = FourierTransform()
    for i in range(len(list_fft)):
        f.frequency_to_time(list_fft[i])
    return f.audio_ifft

def test_Graphs_1(list_file, list_fft): #for input
    g = Graphs()
    for i in range(len(list_file)):
        g.waveform(list_file[i])
        g.frequency_spectrum(list_fft[i], list_file[i])
        g.spectrogram(list_file[i])
        
def test_Graphs_2(list_file_out): #for output
    g = Graphs()
    for i in range(len(list_file_out)):
        g.waveform(list_file_out[i])
        g.spectrogram(list_file_out[i])

def test_FrequencyCompression(list_fft, ratio, CR, samplerate):
    fc = FrequencyCompression(low_cutoff, high_cutoff, ratio, CR, samplerate)
    for i in range(len(list_fft)):
        fc.technique_f(list_fft[i])
    return fc.audio_fc
    
#---- MAIN ----

low_cutoff = 4000
high_cutoff = 6000
ratio = 0.5
CR = 2
samplerate = 16000

list_file = test_AudioManaging_1()
list_fft = test_FourierTransform_1(list_file)
test_Graphs_1(list_file, list_fft)
list_fc = test_FrequencyCompression(list_fft, ratio, CR, samplerate)
list_ifft = test_FourierTransform_2(list_fc)
test_AudioManaging_2(list_ifft, list_file)
list_file_out = test_AudioManaging_1(0)
test_Graphs_2(list_file_out)
