# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 22:48:20 2019

@author: Maria Ausilia Napoli Spatafora
"""

import matplotlib.pyplot as plt

class Graphs:
    
    def __init__(self):
        pass
    
    #It plots the waveform
    def waveform(self, entry): #input read file
        plt.figure()
        plt.plot(entry[2])
        plt.title("Waveform: {}"\
                  .format(entry[0]))
        plt.show()
    
    #It plots the frequency spectrum aftet fft    
    def frequency_spectrum(self, entry_fft, entry_file): #input: fft and read audio
        plt.figure()
        plt.xlim([10, entry_file[1]/2.])
        plt.grid(True)
        plt.xlabel("Frequency (Hz)")
        plt.plot(entry_fft[1][:int(entry_fft[1].size/2.)], entry_fft[0][:int(entry_fft[1].size/2.)])
        plt.title("Frequency Spectrum: {}"\
                  .format(entry_file[0]))
        plt.show()

    #It plots the spectrogram
    def spectrogram(self, entry): #input: read file
        plt.figure()
        plt.specgram(entry[2], Fs = entry[1])
        plt.xlabel("Time")
        plt.ylabel("Frequency")
        plt.xlabel("Time")
        plt.ylabel("Frequency")
        plt.title("Spectrogram: {}"\
                  .format(entry[0]))
        plt.show()
