# -*- coding: utf-8 -*-


import speech_recognition as sr
file = '1.wav'
r = sr.Recognizer()
with sr.AudioFile(file) as source:
    audio = r.record(source)
try:
    content = r.recognize_sphinx(audio, language='zh-CN')
    print(content)
except sr.RequestError as e:
    print(e)
    
