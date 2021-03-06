# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 22:22:18 2019

@author: Maria Ausilia Napoli Spatafora
"""

from scipy.fftpack import fft, fftfreq, ifft

class FourierTransform:
    
    def __init__(self):    
        self.audio_fft = []
        self.audio_ifft = []
    
    #It allows to convert time domain data into frequency domain data
    def time_to_frequency(self, entry): #input: read file
        datafft = fft(entry[2])
        fftabs = abs(datafft)
        ttl = list(entry[2].shape) #to extract tuple's values as int first it converts into list
        shape = ttl.pop() #and then it is popped the single element of list
        freqs = fftfreq(shape, 1./entry[1])
        #print("freqs: ", freqs)
        #print("freq 4000: ", freqs[4000])
        t = (fftabs, freqs, datafft)
        self.audio_fft.append(t)
     
    #It allows to convert frequency domain data into time domain data
    def frequency_to_time(self, entry): #input: transformate file
        signal = ifft(entry[2])
        t = (signal)
        self.audio_ifft.append(t)