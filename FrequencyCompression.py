# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 17:00:14 2019

@author: Maria Ausilia Napoli Spatafora
"""

import numpy as np
from scipy import signal

class FrequencyCompression:
    
    def __init__ (self, cutoff, ratio, CR, samplerate):
        self.cutoff = cutoff
        self.ratio = ratio
        self.samplerate = samplerate
        self.CR = CR
        self.audio_fc = []
               
    def indexFrequency (self, entry_fft, frequency):
        fftabs, freqs, fft = entry_fft
        index = (frequency/self.samplerate)*freqs.size
        #print("self.cutoff/self.samplerate -> ", self.cutoff/self.samplerate)
        #print("freqs.size -> ", freqs.size)
        #print("index -> ", index)
        return int(index)
    
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
    
    def fOutMax (self):
        f_in_max = self.samplerate/2
        f_in = f_in_max ** self.ratio
        f_co = self.cutoff ** (1 - self.ratio)
        f_out_max = int(f_in * f_co)
        return f_out_max
    
    def compareFOutMax (self, entry):
        index = self.indexFOutMax(entry)
        freq = self.fOutMax()
        index_freq = (freq/self.samplerate)*entry[1].size
        print("index: ", index)
        print("index_freq: ", index_freq)
        print(index == index_freq)
    
    def stretching (self, fftdata, fftabs):
        maximum_data = np.max(fftabs)
        #print("maximum_data: ", maximum_data)
        maximum = ((2**16))-1
        normalization_factor = maximum/maximum_data
        for i in range(len(fftdata)):
            fftdata[i] *= normalization_factor
            fftabs[i] *= normalization_factor
        return fftdata, fftabs
    
    def lowPassFilter (self):
        f_out_max = self.fOutMax()
        b, a = signal.butter(3, f_out_max/(self.samplerate/2), btype = "low", analog = "False", output = "ba")
        return b, a #b=denominator coeff; a=numerator coeff
        
    def example_1 (self, entry):
        fftabs, freqs, fftdata = entry
        f_out_max = self.fOutMax()
        f_out_max = self.indexFrequency(entry, f_out_max)
        for i in range(f_out_max+1, fftdata.size):
            fftdata[i] = 0
            fftabs[i] = 0
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def example_2 (self, entry):
        fftabs, freqs, fftdata = entry
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
            fftabs[f_out_max_spec + i] += fftdata[j]
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
        
            
