# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 17:00:14 2019

@author: Maria Ausilia Napoli Spatafora
"""

import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
import math

class FrequencyLowering:
    
    octave = 20000
    
    def __init__ (self, low_cutoff, high_cutoff, ratio, CR, samplerate):
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.cutoff = high_cutoff
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
    
    #COMPRESSION - It calculates the maximum output frequency: the returned value is the frequency and not the index in the fft array
    def fOutMax (self):
        f_in_max = self.samplerate/2
        f_in = f_in_max ** self.ratio
        f_co = self.cutoff ** (1 - self.ratio)
        f_out_max = int(f_in * f_co)
        return f_out_max
    
    #COMPRESSION - It analyzes spectral content in order to activate the lower or the higher cutoff frequency
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
   
    #It calculates the constant to normalize the fft values in order to increase their volume
    def normalizationConstant (self, pre_signal, post_signal): #pre_signal before frequency manipulation; post_signal after frequency manipulation
         return pre_signal/post_signal
  
    #It calculates the Low Pass Butterworth based on its mathematic formula (it's used in frequency domain)
    def butterLPFilter (self, entry, n = 1): #n is order filter
        fftabs, freqs, fftdata = entry
        mask = np.zeros(fftabs.size) #it will be my filter
        indexCutoff = self.indexFrequency(entry, self.cutoff)
        for i in range(len(mask)):
            mask[i] = 1/(1 + (i/indexCutoff)**(2*n))
            #mask[len(mask) - 1 - i] =  mask[i]
        plt.figure()
        plt.axvline(self.cutoff, color = "k")
        plt.xlim(0, self.samplerate)
        plt.title("Low Pass Butterworth Order " + str(n) + " Frequency Response")
        plt.grid()
        plt.plot(mask)
        plt.show()
        return mask
    
    #It calculates the High Pass Butterworth based on its mathematic formula (it's used in frequency domain)
    def butterHPFilter (self, entry, n = 1): #n is order filter
        fftabs, freqs, fftdata = entry
        mask = np.zeros(fftabs.size) #it will be my filter
        indexCutoff = self.indexFrequency(entry, self.cutoff)
        for i in range(int(len(mask)/2)):
            mask[i] = 1 - 1/(1 + (i/indexCutoff)**(2*n))
            mask[len(mask) - 1 - i] =  mask[i]
        plt.figure()
        plt.axvline(self.cutoff, color = "k")
        plt.xlim(0, self.samplerate)
        plt.title("High Pass Butterworth Order " + str(n) + " Frequency Response")
        plt.grid()
        plt.plot(mask)
        plt.show()
        return mask
    
    #It calculates the High Pass Gaussian based on its mathematic formula (it's used in frequency domain)
    def gaussianHPFilter(self, entry):
        fftabs, freqs, fftdata = entry
        mask = np.zeros(fftabs.size) #it will be my filter
        indexCutoff = self.indexFrequency(entry, self.cutoff)
        for i in range(int(len(mask)/2)):
            mask[i] = 1 - math.exp(-(i**2)/(2*(indexCutoff**2)))
            mask[len(mask) - 1 - i] =  mask[i]
        plt.figure()
        plt.axvline(self.cutoff, color = "k")
        plt.xlim(0, self.samplerate)
        plt.title("High Pass Gaussian Filter Frequency Response")
        plt.grid()
        plt.plot(mask)
        plt.show()
        return mask
    
    def idealLPFilter(self, entry):
        fftabs, freqs, fftdata = entry
        indexCutoff = self.indexFrequency(entry, self.cutoff)
        mask = np.zeros(fftabs.size) #it will be my filter
        mask[:indexCutoff] = 1
        spec_indexCutoff = freqs.size - indexCutoff
        mask[spec_indexCutoff:] = 1
        return mask
    
    #It applys butterHPFilter simply (it's used in Comparator.py)
    def applyHPButter(self, entry, n = 1):
        fftabs, freqs, fftdata = entry
        mask = self.butterHPFilter(entry, n)
        fftdata *= mask
        fftabs *= mask
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
     
    #It applys butterLPFilter simply (it's used in Comparator.py)
    def applyLPButter (self, entry, n=1):
        fftabs, freqs, fftdata = entry
        mask = self.butterLPFilter(entry, n)
        fftdata *= mask
        fftabs *= mask
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
    
    #COMPOSITION - It creates the list of the indeces of every region for composition techniques (minimal region)
    def createRegion (self, entry):
        list_region = []
        #1 region
        inf_dst = self.indexFrequency(entry, 1587) #inferior extreme of destination region (lower)
        sup_dst = self.indexFrequency(entry, 2429) #superior extreme of destination region (lower)
        inf_src = self.indexFrequency(entry, 3940) #inferior extreme of source region (higher)
        sup_src = self.indexFrequency(entry, 6985) #superior extreme of source region (higher)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        #2 region
        inf_dst = self.indexFrequency(entry, 1763)
        sup_dst = self.indexFrequency(entry, 2522)
        inf_src = self.indexFrequency(entry, 4116)
        sup_src = self.indexFrequency(entry, 7228)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        #3 region
        inf_dst = self.indexFrequency(entry, 1957)
        sup_dst = self.indexFrequency(entry, 2790)
        inf_src = self.indexFrequency(entry, 4310)
        sup_src = self.indexFrequency(entry, 7496)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        #4 region
        inf_dst = self.indexFrequency(entry, 2169)
        sup_dst = self.indexFrequency(entry, 3083)
        inf_src = self.indexFrequency(entry, 4522)
        sup_src = self.indexFrequency(entry, 7789)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        return list_region
    
    #COMPOSITION - It creates the list of the indeces of every region for composition techniques until 10KHz
    def createRegionExtended (self, entry):
        list_region = self.createRegion(entry)
        #5 region
        inf_dst = self.indexFrequency(entry, 2402)
        sup_dst = self.indexFrequency(entry, 3405)
        inf_src = self.indexFrequency(entry, 4755)
        sup_src = self.indexFrequency(entry, 8111)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        #6 region
        inf_dst = self.indexFrequency(entry, 2658)
        sup_dst = self.indexFrequency(entry, 3758)
        inf_src = self.indexFrequency(entry, 5011)
        sup_src = self.indexFrequency(entry, 8664)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        #7 region
        inf_dst = self.indexFrequency(entry, 2938)
        sup_dst = self.indexFrequency(entry, 4145)
        inf_src = self.indexFrequency(entry, 5291)
        sup_src = self.indexFrequency(entry, 8851)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        #8 region
        inf_dst = self.indexFrequency(entry, 3246)
        sup_dst = self.indexFrequency(entry, 4570)
        inf_src = self.indexFrequency(entry, 5599)
        sup_src = self.indexFrequency(entry, 9276)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        #9 region
        inf_dst = self.indexFrequency(entry, 3583)
        sup_dst = self.indexFrequency(entry, 5036)
        inf_src = self.indexFrequency(entry, 5806)
        sup_src = self.indexFrequency(entry, 9480)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        #10 region
        inf_dst = self.indexFrequency(entry, 3954)
        sup_dst = self.indexFrequency(entry, 5547)
        inf_src = self.indexFrequency(entry, 5954)
        sup_src = self.indexFrequency(entry, 9547)
        t = (inf_dst, sup_dst, inf_src, sup_src)
        list_region.append(t)
        return list_region
 
#Techniques:
        
    #COMPRESSION      
    def technique_1A (self, entry): #TH: no 1
        fftabs, freqs, fftdata = entry
        sum_pre_signal = sum(fftabs)
        self.cutoffActivator(entry)
        f_out_max = self.fOutMax()
        f_out_max = self.indexFrequency(entry, f_out_max)
        indexCO = self.indexFrequency(entry, self.cutoff)
        difference = f_out_max - indexCO
        for i in range(indexCO, f_out_max+1):
            fftdata[indexCO - difference + i] += fftdata[i]
            fftabs[indexCO - difference +i] += fftabs[i]
        #Ideal filter
        #fftdata[f_out_max+1 : fftdata.size] = 0
        #fftabs[f_out_max+1 : fftdata.size] = 0
        #fftdata, fftabs = self.stretching(fftdata, fftabs)
        #My Butterworth filter
        mask = self.butterLPFilter(entry)
        fftdata *= mask
        fftabs *= mask
        sum_post_signal = sum(fftabs)
        k = self.normalizationConstant(sum_pre_signal, sum_post_signal)
        fftdata *= k
        fftabs *= k
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
    
    #COMPRESSION
    def technique_1B (self, entry):
        fftabs, freqs, fftdata = entry
        sum_pre_signal = sum(fftabs)
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
        mask = self.butterLPFilter(entry)
        fftdata *= mask
        fftabs *= mask
        sum_post_signal = sum(fftabs)
        k = self.normalizationConstant(sum_pre_signal, sum_post_signal)
        fftdata *= k
        fftabs *= k
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
    
	#COMPRESSION     
    def technique_2 (self, entry): #TH: no 2
        fftabs, freqs, fftdata = entry
        sum_pre_signal = sum(fftabs)
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
        #Specular actions
        fftdata[int(freqs.size/2):] = 0
        fftabs [int(freqs.size/2):] = 0
        fftdata *= 2
        fftabs *= 2
        #My Butterworth filter
        n = 3
        mask = self.butterLPFilter(entry, n)
        fftdata *= mask
        fftabs *= mask
        sum_post_signal = sum(fftabs)
        k = self.normalizationConstant(sum_pre_signal, sum_post_signal)
        fftdata *= k
        fftabs *= k
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
       
	#TRANSPOSITION 
    def technique_a (self, entry): #TH no 3
        fftabs, freqs, fftdata = entry
        sum_pre_signal = sum(fftabs)
        indexCO = self.indexFrequency(entry, self.cutoff)
        nyquist = 220500 #parameter dependent to samplerate: it is tailored for pure tones
        reduced_fftabs = fftabs[indexCO:nyquist]
        peak_frequency = np.where(reduced_fftabs == max(reduced_fftabs)) #peak_frequency is the index of maximum frequency!
        peak_frequency = int(peak_frequency[0][0]) + indexCO
        target_octave = peak_frequency - self.octave
        self.cutoff = ((peak_frequency - self.octave/2)/freqs.size)*self.samplerate
        for i in range(self.octave):
            fftdata[target_octave - int(self.octave/2) + i ] += (fftdata[peak_frequency - int(self.octave/2) + i]*self.ratio)
            fftabs[target_octave - int(self.octave/2) + i ] += (fftabs[peak_frequency - int(self.octave/2) + i]*self.ratio)
        #Specular actions
        fftdata[int(freqs.size/2):] = 0
        fftabs [int(freqs.size/2):] = 0
        fftdata *= 2
        fftabs *= 2
        #low pass filter
        mask = self.idealLPFilter(entry)
        fftdata *= mask
        fftabs *= mask
        self.cutoff = self.high_cutoff #reset of cutoff to default value
        sum_post_signal = sum(fftabs)
        k = self.normalizationConstant(sum_pre_signal, sum_post_signal)
        fftdata *= k
        fftabs *= k
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
      
	#COMPOSITION  
    def technique_b (self, entry): #composition without cutoff and limited bandwidth to 8 KHz #TH no 4
        list_region = self.createRegion(entry)
        fftabs, freqs, fftdata = entry
        #sum_pre_signal = sum(fftabs)
        for i in range (0, 4):
            inf_dst, sup_dst, inf_src, sup_src = list_region[i]
            j = inf_dst
            for k in range (inf_src, sup_src+1):
                fftabs[j] += fftabs[k]
                fftdata[j] += fftdata[k]
                #specular
                fftabs[freqs.size - j] += fftabs[freqs.size - k]
                fftdata[freqs.size - j] += fftdata[freqs.size - k]
                j+=1
                if j > sup_dst:
                    j = inf_dst
        #sum_post_signal = sum(fftabs)
        #k = self.normalizationConstant(sum_pre_signal, sum_post_signal)
        #fftdata *= k
        #fftabs *= k
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)

	#COMPOSITION       
    def technique_c (self, entry): #composition without cutoff but bandwidth of 10 KHz #TH no 4
        list_region = self.createRegionExtended(entry)
        fftabs, freqs, fftdata = entry
        for i in range (0, 10):
            inf_dst, sup_dst, inf_src, sup_src = list_region[i]
            j = inf_dst
            for k in range (inf_src, sup_src+1):
                fftabs[j] += fftabs[k]
                fftdata[j] += fftdata[k]
                #specular
                fftabs[freqs.size - j] += fftabs[freqs.size - k]
                fftdata[freqs.size - j] += fftdata[freqs.size - k]
                j+=1
                if j > sup_dst:
                    j = inf_dst
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
  
	#COMPOSITION      
    def technique_d (self, entry): #composition with cutoff, 8 KHz and unchanged destination regions #TH no 5
        list_region = self.createRegion(entry)
        fftabs, freqs, fftdata = entry
        cutoff = self.indexFrequency(entry, self.cutoff)
        for i in range (0, 4):
            inf_dst, sup_dst, inf_src, sup_src = list_region[i]
            j = inf_dst
            if cutoff > inf_src:
                inf_src = cutoff
            for k in range (inf_src, sup_src+1):
                fftabs[j] += fftabs[k]
                fftdata[j] += fftdata[k]
                #specular
                fftabs[freqs.size - j] += fftabs[freqs.size - k]
                fftdata[freqs.size - j] += fftdata[freqs.size - k]
                j+=1
                if j > sup_dst:
                    j = inf_dst
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
     
	#COMPOSITION   
    def technique_e (self, entry): #composition with cutoff, 8 KHz and narrow destination regions #TH no 6
        list_region = self.createRegion(entry)
        fftabs, freqs, fftdata = entry
        cutoff = self.indexFrequency(entry, self.cutoff)
        for i in range (0, 4):
            inf_dst, sup_dst, inf_src, sup_src = list_region[i]
            j = inf_dst
            narrow_sup_dst = ((sup_dst - inf_dst)/(cutoff - inf_src))*(sup_src - inf_src) #it's proportion between regions' dimensions
            if cutoff > inf_src:
                inf_src = cutoff
            for k in range (inf_src, sup_src+1):
                fftabs[j] += fftabs[k]
                fftdata[j] += fftdata[k]
                #specular
                fftabs[freqs.size - j] += fftabs[freqs.size - k]
                fftdata[freqs.size - j] += fftdata[freqs.size - k]
                j+=1
                if j > narrow_sup_dst:
                    j = inf_dst
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)

	#COMPOSITION      
    def technique_f (self, entry): #composition with cutoff, 10 Khz and unchanged destination regions #TH no 5
        list_region = self.createRegionExtended(entry)
        fftabs, freqs, fftdata = entry
        #sum_pre_signal = sum(fftabs)
        cutoff = self.indexFrequency(entry, self.cutoff)
        for i in range (0, 10):
            inf_dst, sup_dst, inf_src, sup_src = list_region[i]
            j = inf_dst
            if cutoff > inf_src:
                inf_src = cutoff
            for k in range (inf_src, sup_src+1):
                fftabs[j] += fftabs[k]
                fftdata[j] += fftdata[k]
                j+=1
                if j >= sup_dst:
                    j = inf_dst
        #Specular actions
        fftdata[int(freqs.size/2):] = 0
        fftabs[int(freqs.size/2):] = 0
        fftdata *= 2
        fftabs *= 2
        #sum_post_signal = sum(fftabs)
        #k = self.normalizationConstant(sum_pre_signal, sum_post_signal)
        #fftdata *= k
        #fftabs *= k
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t)
  
	#COMPOSITION      
    def technique_g (self, entry): #composition with cutoff, 10 KHz and narrow destination regions #TH no 6
        list_region = self.createRegionExtended(entry)
        fftabs, freqs, fftdata = entry
        cutoff = self.indexFrequency(entry, self.cutoff)
        for i in range (0, 10):
            inf_dst, sup_dst, inf_src, sup_src = list_region[i]
            j = inf_dst
            narrow_sup_dst = ((sup_dst - inf_dst)/(cutoff - inf_src))*(sup_src - inf_src) #it's proportion between regions' dimensions
            if cutoff > inf_src:
                inf_src = cutoff
            for k in range (inf_src, sup_src+1):
                fftabs[j] += fftabs[k]
                fftdata[j] += fftdata[k]
                #specular
                fftabs[freqs.size - j] += fftabs[freqs.size - k]
                fftdata[freqs.size - j] += fftdata[freqs.size - k]
                j+=1
                if j > narrow_sup_dst:
                    j = inf_dst
        t = (fftabs, freqs, fftdata)
        self.audio_fc.append(t) 
            
