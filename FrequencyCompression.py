# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 17:00:14 2019

@author: Maria Ausilia Napoli Spatafora
"""

import numpy as np
from scipy import signal
from matplotlib import pyplot as plt

class FrequencyCompression:
    
    def __init__ (self, low_cutoff, high_cutoff, ratio, CR, samplerate):
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.cutoff = low_cutoff
        self.ratio = ratio
        self.samplerate = samplerate
        self.CR = CR
        self.audio_fc = []
    
    #It calculates index in the fft array of a frequency          
    def indexFrequency (self, entry_fft, frequency):
        fftabs, freqs, fft = entry_fft
        index = (frequency/self.samplerate)*freqs.size
        #print("self.cutoff/self.samplerate -> ", self.cutoff/self.samplerate)
        #print("freqs.size -> ", freqs.size)
        #print("index -> ", index)
        return int(index)
    
    #It finds and calculates the index of the max output frequency - DEPRECATED
    def indexFOutMax (self, entry):
        indexCO = self.indexFrequency(entry)
        f_in_max = self.samplerate/2
        f_in = f_in_max ** self.ratio
        f_co = indexCO ** (1 - self.ratio)
        f_out_max = int(f_in * f_co)
        #print("indexCO -> ", indexCO)
        #print("f_in_max -> ", f_in_max)
        #print("f_in -> ", f_in)
        #print("f_co -> ", f_co)
        #print("f_out_max -> ", f_out_max)
        return f_out_max
    
    #It calculates the maximum output frequency: the returned value is the frequency and not the index in the fft array
    def fOutMax (self):
        f_in_max = self.samplerate/2
        f_in = f_in_max ** self.ratio
        f_co = self.cutoff ** (1 - self.ratio)
        f_out_max = int(f_in * f_co)
        return f_out_max
    
    #It compares two ways for calculating maximum output frequency - PRIVATE USE
    def compareFOutMax (self, entry):
        index = self.indexFOutMax(entry)
        freq = self.fOutMax()
        index_freq = (freq/self.samplerate)*entry[1].size
        print("index: ", index)
        print("index_freq: ", index_freq)
        print(index == index_freq)
        
    #It analyzes spectral content in order to activate the lower or the higher cutoff frequency
    def cutoffActivator (self, entry):
        fftabs, freqs, fftdata = entry
        threshold = self.indexFrequency(entry, 3500)
        low_content = sum(fftabs[0:threshold])
        high_content = sum(fftabs[threshold:])
        ratio = low_content/high_content
        if ratio > 1: #low > high --> higher cutoff (= minus compression)
            self.cutoff = self.high_cutoff
        else: #high >= low --> lower cutoff (= plus compression)
            self.cutoff = self.low_cutoff
        print("The activated cutoff frequency is: ", self.cutoff)
        print("Low content is: ", low_content)
        print("High content is: ", high_content)
   
    #It normalizes the fft values in order to increase their volume
    def stretching (self, fftdata, fftabs):
        maximum_data = np.max(fftabs)
        #print("maximum_data: ", maximum_data)
        maximum = ((2**16))-1
        normalization_factor = maximum/maximum_data
        for i in range(len(fftdata)):
            fftdata[i] *= normalization_factor
            fftabs[i] *= normalization_factor
        return fftdata, fftabs
  
    #It calculates the low pass Butterworth filter and plots it
    def lowPassFilter (self):
        f_out_max = self.fOutMax()
        b, a = signal.butter(3, f_out_max/(self.samplerate/2), btype = "low", analog = "False", output = "ba")
        w, h = signal.freqz(b, a)
        plt.plot(0.5*self.samplerate*w/np.pi, np.abs(h), "b")
        plt.axvline(f_out_max, color = "k")
        plt.xlim(0, 0.5*self.samplerate)
        plt.title("Lowpass Filter Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()
        return b, a #b=denominator coeff; a=numerator coeff
 
#Techniques:
        
    def example_1 (self, entry):
        fftabs, freqs, fftdata = entry
        self.cutoffActivator(entry)
        f_out_max = self.fOutMax()
        f_out_max = self.indexFrequency(entry, f_out_max)
        for i in range(f_out_max+1, fftdata.size):
            fftdata[i] = 0
            fftabs[i] = 0
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def example_2 (self, entry):
        fftabs, freqs, fftdata = entry
        self.cutoffActivator(entry)
        f_out_max = self.fOutMax()
        f_out_max = self.indexFrequency(entry, f_out_max)
        f_out_max_spec = freqs.size - f_out_max
        for i in range (f_out_max+1, f_out_max_spec):
            fftdata[i] = 0
            fftabs[i] = 0
        t =(fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def technique_1A (self, entry): #compression
        fftabs, freqs, fftdata = entry
        self.cutoffActivator(entry)
        f_out_max = self.fOutMax()
        f_out_max = self.indexFrequency(entry, f_out_max)
        indexCO = self.indexFrequency(entry, self.cutoff)
        difference = f_out_max - indexCO
        for i in range(indexCO, f_out_max+1):
            fftdata[indexCO - difference + i] += fftdata[i]
            fftabs[indexCO - difference +i] += fftabs[i]
        #Butterworth filter
        #b, a = self.lowPassFilter() #b=denominator coeff; a=numerator coeff
        #fftdata = signal.lfilter(b, a, fftdata)
        #fftabs = signal.lfilter(b, a, fftabs)
        #Ideal filter
        fftdata[f_out_max+1 : fftdata.size] = 0
        fftabs[f_out_max+1 : fftdata.size] = 0
        fftdata, fftabs = self.stretching(fftdata, fftabs)
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def technique_1B (self, entry): #compression
        fftabs, freqs, fftdata = entry
        self.cutoffActivator(entry)
        f_out_max = self.fOutMax()
        f_out_max = self.indexFrequency(entry, f_out_max)
        indexCO = self.indexFrequency(entry, self.cutoff)
        difference = f_out_max - indexCO
        for i in range(indexCO, f_out_max+1):
            fftdata[indexCO - difference + i] += fftdata[i]
            fftabs[indexCO - difference + i] += fftabs[i]
        f_out_max_spec = freqs.size - f_out_max
        indexCO_spec = freqs.size - indexCO
        difference_spec = indexCO_spec - f_out_max_spec
        for i in range(f_out_max_spec, indexCO_spec+1):
            fftdata[indexCO_spec + difference_spec - i] += fftdata[i]
            fftabs[indexCO_spec + difference_spec - i] += fftabs[i]
        #Butterworth filter
        b, a = self.lowPassFilter() #b=denominator coeff; a=numerator coeff
        fftdata = signal.lfilter(b, a, fftdata)
        fftabs = signal.lfilter(b, a, fftabs)
        #Ideal filter
        #fftdata[f_out_max+1 : f_out_max_spec] = 0
        #fftabs[f_out_max+1 : f_out_max_spec] = 0
        #fftdata, fftabs = self.stretching(fftdata, fftabs)
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def technique_2 (self, entry): #compression
        fftabs, freqs, fftdata = entry
        self.cutoffActivator(entry)
        f_out_max = self.fOutMax()
        f_out_max = self.indexFrequency(entry, f_out_max)
        indexCO = self.indexFrequency(entry, self.cutoff)
        difference = f_out_max - indexCO
        i = 0
        for j in range(f_out_max+1, int(freqs.size/2) +1):
            fftdata[indexCO + i] += fftdata[j]
            fftabs[indexCO + i] += fftabs[j]
            i = (i+1)%difference
        f_out_max_spec = freqs.size - f_out_max
        indexCO_spec = freqs.size - indexCO
        difference_spec = indexCO_spec - f_out_max_spec
        i = 0
        for j in range(int(freqs.size/2), f_out_max_spec):
            fftdata[f_out_max_spec + i] += fftdata[j]
            fftabs[f_out_max_spec + i] += fftabs[j]
            i = (i+1)%difference_spec
        #Butterworth filter
        b, a = self.lowPassFilter() #b=denominator coeff; a=numerator coeff
        fftdata = signal.lfilter(b, a, fftdata)
        fftabs = signal.lfilter(b, a, fftabs)
        #Ideal filter
        #fftdata[f_out_max+1 : f_out_max_spec] = 0
        #fftabs[f_out_max+1 : f_out_max_spec] = 0
        #fftdata, fftabs = self.stretching(fftdata, fftabs)
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def technique_a (self, entry): #transposition
        fftabs, freqs, fftdata = entry
        indexCO = self.indexFrequency(entry, self.cutoff)
        difference = int(freqs.size/2) - indexCO
        for i in range(indexCO, int(freqs.size/2)+1):
            fftdata[indexCO - difference + i] += fftdata[i]
            fftabs[indexCO - difference + i] += fftabs[i]
        indexCO_spec = freqs.size - indexCO
        difference_spec = indexCO_spec - int(freqs.size/2)
        for i in range(difference_spec):
            fftdata[indexCO_spec + i] += fftdata[int(freqs.size/2)+1 + i]
            fftabs[indexCO_spec + i] += fftabs[int(freqs.size/2)+1 + i]
        #Butterworth filter
        b, a = self.lowPassFilter() #b=denominator coeff; a=numerator coeff
        fftdata = signal.lfilter(b, a, fftdata)
        fftabs = signal.lfilter(b, a, fftabs)
        #Ideal filter
        #fftdata[indexCO : indexCO_spec] = 0
        #fftabs[indexCO : indexCO_spec] = 0
        #fftdata, fftabs = self.stretching(fftdata, fftabs)
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
            
