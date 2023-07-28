# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 21:42:42 2020

@author: 21524
"""

from pydub import AudioSegment

sound =AudioSegment.from_file('1.m4a' , format='m4a')
file_handle = sound.export('1.wav', format='wav')
