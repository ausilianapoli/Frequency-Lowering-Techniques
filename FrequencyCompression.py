# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 17:00:14 2019

@author: Maria Ausilia Napoli Spatafora
"""
import numpy as np

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
        #print("-> ", self.cutoff/self.samplerate)
        #print("-> ", freqs.size)
        #print("-> ", index)
        return int(index)
    
    def technique_1 (self, entry):
      indexCO = self.indexCutoff(entry)
      i = indexCO
      fftabs, freqs, fftdata = entry
      while i <= fftdata.size/2:
          fftdata[int(i*self.ratio)] += fftdata[i]
          i+=1
      n_fftdata = fftdata[:indexCO]
      n_freqs = freqs[:indexCO]
      n_fftabs = abs(n_fftdata)
      t = (n_fftabs, n_freqs, n_fftdata)
      self.audio_fc.append(t)
      
    def technique_2 (self, entry):
      indexCO = self.indexCutoff(entry)
      fftabs, freqs, fftdata = entry
      for i in range(indexCO, int(fftdata.size/2)):
          fftdata[i] = 0
      n_fftdata = fftdata[:indexCO]
      n_freqs = freqs[:indexCO]
      n_fftabs = abs(n_fftdata)
      t = (n_fftabs, n_freqs, n_fftdata)
      self.audio_fc.append(t)
      
    def technique_3 (self, entry):
        indexCO = self.indexCutoff(entry)
        fftabs, freqs, fftdata = entry
        f_in_max = self.samplerate/2
        f_in = f_in_max ** self.ratio #it is an index
        f_co = indexCO ** (1-self.ratio) #it is an index
        f_out_max = int(f_in * f_co)
        print("f_out_max: ", f_out_max)
        print("fftdata.size: ", fftdata.size)
        n_fftdata = fftdata[:f_out_max]
        n_freqs = freqs[:f_out_max]
        n_fftabs = abs(n_fftdata)
        #print("?? ", n_fftdata.size == fftdata.size)
        t = (n_fftabs, n_freqs, n_fftdata)
        self.audio_fc.append(t)
        
    def technique_4A (self, entry):
        indexCO = self.indexCutoff(entry)
        fftabs, freqs, fftdata = entry
        f_in_max = self.samplerate/2
        f_in = f_in_max ** self.ratio #it is an index
        f_co = indexCO ** (1-self.ratio) #it is an index
        f_out_max = int(f_in * f_co)
        data_to_comprime = fftdata[f_out_max:]
        #print(f_out_max)
        #print(fftdata.size/2)
        #print(data_to_comprime)
        #print(fftdata[f_out_max:])
        n_size = int(data_to_comprime.size/self.CR)
        for i in range(n_size, data_to_comprime.size):
            data_to_comprime[(i-n_size)%n_size] += (data_to_comprime[i]/self.CR)
        print("fftdata.shape: ", fftdata.shape)
        print("data_to_comprimre.shape: ", data_to_comprime.shape)
        n_fftdata = np.append(fftdata[f_out_max:], data_to_comprime)
        n_size = f_out_max + data_to_comprime.size
        n_freqs = freqs[:n_size]
        n_fftabs = abs(n_fftdata[:n_size])
        print("n_fftdata.shape: ", n_fftdata.shape)
        t = (n_fftabs, n_freqs, n_fftdata)
        self.audio_fc.append(t)
        
    def technique_4B (self, entry):
        indexCO = self.indexCutoff(entry)
        fftabs, freqs, fftdata = entry
        f_in_max = self.samplerate/2
        f_in = f_in_max ** self.ratio #it is an index
        f_co = indexCO ** (1-self.ratio) #it is an index
        f_out_max = int(f_in * f_co)
        data_to_comprime = fftdata[f_out_max:]
        #print(f_out_max)
        #print(fftdata.size/2)
        #print(data_to_comprime)
        #print(fftdata[f_out_max:])
        n_size = int(data_to_comprime.size/self.CR)
        for i in range(n_size, data_to_comprime.size):
            data_to_comprime[(i-n_size)%n_size] += (data_to_comprime[i]/self.CR)
        print("fftdata.shape: ", fftdata.shape)
        print("data_to_comprimre.shape: ", data_to_comprime.shape)
        n_fftdata = np.vstack((fftdata[f_out_max:], data_to_comprime))
        n_size = f_out_max + data_to_comprime.size
        n_freqs = freqs[:n_size]
        n_fftabs = abs(n_fftdata[:n_size])
        print("n_fftdata.shape: ", n_fftdata.shape)
        t = (n_fftabs, n_freqs, n_fftdata)
        self.audio_fc.append(t)

        
            
 
        
            