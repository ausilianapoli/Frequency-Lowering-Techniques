# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 17:00:14 2019

@author: Maria Ausilia Napoli Spatafora
"""

class FrequencyCompression:
    
    def __init__ (self, cutoff, ratio, CR, samplerate):
        self.cutoff = cutoff
        self.ratio = ratio
        self.samplerate = samplerate
        self.CR = CR
        self.audio_fc = []
               
    def indexCutoff (self, entry_fft):
        fftabs, freqs, fft = entry_fft
        index = (self.cutoff/self.samplerate)*freqs.size
        #print("self.cutoff/self.samplerate -> ", self.cutoff/self.samplerate)
        #print("freqs.size -> ", freqs.size)
        #print("index -> ", index)
        return int(index)
    
    def indexFOutMax (self, entry):
        indexCO = self.indexCutoff(entry)
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
        
    def example_1 (self, entry):
        fftabs, freqs, fftdata = entry
        f_out_max = self.indexFOutMax(entry)
        for i in range(f_out_max+1, fftdata.size):
            fftdata[i] = 0
            fftabs[i] = 0
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def example_2 (self, entry):
        fftabs, freqs, fftdata = entry
        f_out_max = self.indexFOutMax(entry)
        f_out_max_spec = freqs.size - f_out_max
        for i in range (f_out_max+1, f_out_max_spec):
            fftdata[i] = 0
            fftabs[i] = 0
        t =(fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def technique_1A (self, entry):
        fftabs, freqs, fftdata = entry
        f_out_max = self.indexFOutMax(entry)
        indexCO = self.indexCutoff(entry)
        difference = f_out_max - indexCO
        for i in range(indexCO, f_out_max+1):
            fftdata[indexCO - difference + i] += fftdata[i]
            fftabs[indexCO - difference +i] += fftabs[i]
        for i in range(f_out_max + 1, fftdata.size):
            fftdata[i] = 0
            fftabs[i] = 0
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def technique_1B (self, entry):
        fftabs, freqs, fftdata = entry
        f_out_max = self.indexFOutMax(entry)
        indexCO = self.indexCutoff(entry)
        difference = f_out_max - indexCO
        for i in range(indexCO, f_out_max+1):
            fftdata[indexCO - difference + i] += fftdata[i]
            fftabs[indexCO - difference + i] += fftabs[i]
        f_out_max_spec = freqs.size - f_out_max
        indexCO_spec = freqs.size - indexCO
        difference_spec = indexCO_spec - f_out_max_spec
        for i in range(f_out_max_spec, indexCO_spec+1):
            fftdata[indexCO_spec + difference_spec +i] += fftdata[i]
            fftabs[indexCO_spec + difference_spec +i] += fftabs[i]
        for i in range(f_out_max+1, f_out_max_spec):
            fftdata[i] = 0
            fftabs[i] = 0
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
        
    def technique_2 (self, entry):
        fftabs, freqs, fftdata = entry
        f_out_max = self.indexFOutMax(entry)
        indexCO = self.indexCutoff(entry)
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
        for i in range(f_out_max+1, f_out_max_spec):
            fftdata[i] = 0
            fftabs[i] = 0
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
 
        
            
