'''
To install dependencies on Mac OS X run the following commands:
    sudo brew install portaudio
    sudo pip install --allow-external pyaudio --allow-unverified pyaudio pyaudio

 DTMF
                1209 Hz 1336 Hz 1477 Hz 1633 Hz
        697 Hz  1       2       3       A
        770 Hz  4       5       6       B
        852 Hz  7       8       9       C
        941 Hz  *       0       #       D

2015
Noah Spurrier noah@noah.org

http://www.noah.org/wiki/tones ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
Modified: 
2021
Markus (GNU/Fox)

'''

import math
import numpy
import pyaudio
import sys
import time

class DTMF:
    def __init__(self, length=0.40,ratio=0.25,  rate=44100):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=1, rate=44100, output=1)
        self.length = length
        self.rate = rate
        self.ratio = ratio

        self.silence = numpy.zeros(int(self.length/2)*self.rate).astype(numpy.float32).tobytes()
    #enddef


    def dial(self, number):
        self.play_dtmf_tone(number)
    #enddef

    def sine_wave(self, frequency, length, rate):
        length = int(length * rate)
        factor = float(frequency) * (math.pi * 2) / rate
        return numpy.sin(numpy.arange(length) * factor)
    #enddef

    def sine_sine_wave(self, f1, f2, length, rate):
        s1=self.sine_wave(f1,length,rate)
        s2=self.sine_wave(f2,length,rate)
        ss=s1+s2
        sa=numpy.divide(ss, 2.0)
        return sa
    #enddef

    def play_dtmf_tone(self, digits):
        dtmf_freqs = {'1': (1209,697), '2': (1336, 697), '3': (1477, 697), 'A': (1633, 697),
                    '4': (1209,770), '5': (1336, 770), '6': (1477, 770), 'B': (1633, 770),
                    '7': (1209,852), '8': (1336, 852), '9': (1477, 852), 'C': (1633, 852),
                    '*': (1209,941), '0': (1336, 941), '#': (1477, 941), 'D': (1633, 941)}
        dtmf_digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#', 'A', 'B', 'C', 'D']
        if type(digits) is not type(''):
            digits=str(digits)[0]
        digits = ''.join ([dd for dd in digits if dd in dtmf_digits])


        for digit in digits:
            digit=digit.upper()
            frames = []
            frames.append([0]*int((self.length*self.ratio)*self.rate))
            frames.append(self.sine_sine_wave(dtmf_freqs[digit][0], dtmf_freqs[digit][1], self.length, self.rate))
            ##frames.append([0]*int((self.length/2)*self.rate))
            chunk = numpy.concatenate(frames) * 0.6

            free = self.stream.get_write_available()
            print(f"free 0: {free}")

            self.stream.write(chunk.astype(numpy.float32).tobytes())
        #endfor
    #enddef

    def __del__(self):
        self.stream.close()
        self.p.terminate()
    #enddef
#endclass

