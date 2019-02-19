# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:05:57 2019

@author: Maria Ausilia Napoli Spatafora
"""

from scipy.io import wavfile
import numpy as np

class AudioManaging:
    
    audio_file = [] #list of tuple(path, samplerate, data)
    audio_numpy = [] #list of tuple(signal) after ifft
    
    def read_file(self, path):
        samplerate, data = wavfile.read(path)
        t = (path, samplerate, data)
        self.audio_file.append(t)
        
    def print_metadata(self, entry):
        print("Path: {}"\
              .format(entry[0]))
        print("\tsamplerate: {}"\
              .format(entry[1]))
        print("\t#samples: {}"\
              .format(entry[2].shape))
        shape, channels = entry[2].shape #to extract only shape and discard number of channels
        print("\tlength: {} seconds"\
              .format(str(round(shape/entry[1]))))
        
    def convert_numpy(self, entry):
        signal = np.int16(entry.real)
        signal = np.asarray(signal, dtype = np.int16)
        return signal
        
    def save_file(self, idx, samplerate, signal):
        wavfile.write("./records/output_{}.wav"\
                      .format(idx), samplerate, signal)
              
