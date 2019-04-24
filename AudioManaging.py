# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:05:57 2019

@author: Maria Ausilia Napoli Spatafora
"""

from scipy.io import wavfile
import numpy as np
import subprocess as sp
import os
import platform

class AudioManaging:
    
    audio_file = [] #list of tuple(path, samplerate, data)
    audio_numpy = [] #list of tuple(signal) after ifft
    
    #It allows to read the file audio.wav from path
    def read_file(self, path):
        samplerate, data = wavfile.read(path)
        t = (path, samplerate, data)
        self.audio_file.append(t)
        
    #It allows to print some information about file audio    
    def print_metadata(self, entry):
        print("Path: {}"\
              .format(entry[0]))
        print("\tsamplerate: {}"\
              .format(entry[1]))
        print("\t#samples: {}"\
              .format(entry[2].shape))
        ttl = list(entry[2].shape) #to extract tuple's values as int first it converts into list
        shape = ttl.pop() #and then it is popped the single element of list
        print("\tduration: {} seconds"\
              .format(str(round(shape/entry[1]))))
    
    #It allows to convert the complex output of ifft to real numpy array    
    def convert_numpy(self, entry):
        signal = np.int16(entry.real)
        signal = np.asarray(signal, dtype = np.int16)
        return signal
    
    #It allows to save processed file audio with wav format
    def save_file(self, name, idx, samplerate, signal):
        wavfile.write("./records/{}_{}.wav"\
                      .format(name, idx), samplerate, signal)
    
    #It allows to join audio channels to only one
    def join_audio_channels(self, path, out = 0): #out = 1 for join channels of audio output
        idx = 0
        for s in path:
            if s.isdigit() == True:
                idx = s
                break
        if out == 0:
            name = "./records/sample_{}m.wav"\
                    .format(idx)
        else:
            name = "./records/output_{}m.wav"\
                    .format(idx)
        if platform.system() == "Linux":
            cmdffmpeg_L = "ffmpeg -y -i {} -ac 1 -f wav {}"\
                        .format(path, name)
            os.system(cmdffmpeg_L)
        elif platform.system() == "Windows":
            cmdffmpeg_W = "./ffmpeg/bin/ffmpeg -y -i {} -ac 1 -f wav {}"\
                        .format(path, name)
            sp.call(cmdffmpeg_W)
        return name
    
    def resampling(self, path):
        idx = 0
        for s in path:
            if s.isdigit() == True:
                idx = s
                break
        name = "./records/sample_{}ms.wav"\
                .format(idx)
        if platform.system() == "Linux":
            cmdffmpeg_L = "ffmpeg -i {} -ar 16000 -f wav {}"\
                        .format(path, name)
            os.system(cmdffmpeg_L)
        elif platform.system() == "Windows":
            cmdffmpeg_W = "./ffmpeg/bin/ffmpeg -i {} -ar 16000 -f wav {}"\
                        .format(path, name)
            sp.call(cmdffmpeg_W)
        return name
              
