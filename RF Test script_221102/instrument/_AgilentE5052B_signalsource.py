import time
import pyvisa as visa
import numpy as np


class Agilent_E5052B:
    medida = 'MHZ'

    def __init__(self):
        self.maxfreq = None
        self.instAgilent = None
        self.rm = None
        self.E5052B = None
        self.inicialFreq = None
        self.finalFreq = None
        self.centralFreq = None
        self.referenceLevel = None
        self.nPoints = None
        self.span = None
        self.marker1 = None
        self.marker2 = None
        self.marker3 = None
        self.marker4 = None
        self.marker5 = None
        # sel.nPoints = int(self.scope.query('SWE:POIN?'))

    def identity(self):
        info = self.E5052B.query('*IDN?')
        info = info.split(",")
        print("Fabricante: ", info[0])
        print("Model: ", info[1])
        print("Number of serie: ", info[2])
        print("Firmware: ", info[3])

    def spectrum_init(self, TCPIP):
        self.rm = visa.ResourceManager()
#        self.E5052B = self.rm.open_resource('TCPIP::192.168.190.32::INSTR')
        self.E5052B = self.rm.open_resource(TCPIP)

    def spectrum_config(self):
#        self.mode = self.E5052B.query(';TRIG:MODE?')
#        print(self.mode)
        self.E5052B.write(';TRIG:MODE PN1')
        time.sleep(0.5)
        self.E5052B.write(';CALC:PN1:TRAC:SPUR:POW 1')
        self.E5052B.write(';SENSe:PN1:AVERage:STAT 0')
        self.E5052B.write(';CALC:PN1:TRAC1:MARK1:STAT 1')
        self.E5052B.write(';CALC:PN1:TRAC1:MARK2:STAT 1')
        self.E5052B.write(';CALC:PN1:TRAC1:MARK3:STAT 1')
        self.E5052B.write(';CALC:PN1:TRAC1:FUNC:TYPE INT ')
        self.E5052B.write(';CALC:PN1:TRAC1:FUNC:DOM:X FRAN ')
        self.E5052B.write(';CALC:PN1:TRAC1:FUNC:DOM:Y FRAN ')
        self.E5052B.write(';SENS:PN1:FREQ:STAR 1000 ')
        self.E5052B.write(';SENS:PN1:FREQ:STOP 40000000')
        self.E5052B.write(';SENS:PN1:Correlation:COUNt 10')
        time.sleep(0.5)
#        self.stopfrq = self.E5052B.query(';SENS:PN1:FREQ:STOP?')
#        print(self.stopfrq)
        self.E5052B.write(';SENSe:PN1:AVERage:CLEar')
        time.sleep(2)

    def disconnect(self):
        self.E5052B.close()

    def getParamsSpectrum(self):
        print("Frecuencia central: ", self.centralFreq, "MHz")
        print("Frecuencia inicial: ", self.inicialFreq, "MHz")
        print("Frecuencia final: ", self.finalFreq, "MHz")
        print("Nivel de referencia: ", self.referenceLevel, "dBm")

    def setParamsSpectrum(self, inicialFreq, finalFreq, referenceLevel):
        self.inicialFreq = float(inicialFreq)
        self.finalFreq = float(finalFreq)
        self.referenceLevel = float(referenceLevel)
        self.centralFreq = (self.finalFreq + self.inicialFreq) / 2.0
        self.E5052B.write('FREQ:START ' + str(inicialFreq) + self.medida)
        self.E5052B.write('FREQ:STOP ' + str(finalFreq) + self.medida)
        self.E5052B.write('FREQ:CENT ' + str(self.centralFreq) + self.medida)
        self.E5052B.write('DISP:WIND:TRAC:Y:RLEV ' + str(referenceLevel))
        self.nPoints = int(self.E5052B.query('SWE:POIN?'))

    def updateMarker(self, Marker1, Marker2, Marker3, Marker4, Marker5):
        self.E5052B.write(';SENSe:PN1:AVERage:CLEar')
        time.sleep(0.8)
        if Marker1 is not None:
            self.marker1 = Marker1
            self.E5052B.write(';CALCulate:PN1:TRACe1:MARKer1:X ', self.marker1)
        if Marker2 is not None:
            self.marker2 = Marker2
            self.E5052B.write(';CALCulate:PN1:TRACe1:MARKer2:X ', self.marker2)
        if Marker3 is not None:
            self.marker3 = Marker3
            self.E5052B.write(';CALCulate:PN1:TRACe1:MARKer3:X ', self.marker3)
        if Marker4 is not None:
            self.marker4 = Marker4
            self.E5052B.write(';CALCulate:PN1:TRACe1:MARKer4:X ', self.marker4)
        if Marker5 is not None:
            self.marker5 = Marker5
            self.E5052B.write(';CALCulate:PN1:TRACe1:MARKer5:X ', self.marker5)

    def getMarkerdBcHz(self):
        BcHzTab = []*5
        self.marker1NF = self.marker2NF = self.marker3NF = self.marker4NF = self.marker5NF = 0
        if self.marker1 is not None:
            self.marker1NF = (round(float(self.E5052B.query(':CALCulate:PN1:TRACe1:MARKer1:Y? ')), 2))
        if self.marker2 is not None:
            self.marker2NF = (round(float(self.E5052B.query(':CALCulate:PN1:TRACe1:MARKer2:Y? ')), 2))
        if self.marker3 is not None:
            self.marker3NF = (round(float(self.E5052B.query(':CALCulate:PN1:TRACe1:MARKer3:Y? ')), 2))
        if self.marker4 is not None:
            self.marker4NF = (round(float(self.E5052B.query(':CALCulate:PN1:TRACe1:MARKer4:Y? ')), 2))
        if self.marker5 is not None:
            self.marker5NF = (round(float(self.E5052B.query(':CALCulate:PN1:TRACe1:MARKer5:Y? ')), 2))
            BcHzTab = [self.marker1NF, self.marker2NF, self.marker3NF, self.marker4NF, self.marker5NF]
        return BcHzTab

    def getDeg(self):
        readData = self.E5052B.query(':CALCulate:PN1:TRACe1:FUNCtion:INTegral:DATA?')
#        print(readData)
        temTab = str.split(readData, ',')
#        print(temTab)
        self.deg = round(float(temTab[3]), 3)
#        print(self.deg)
        return self.deg

    def getPowerDBM(self):
        readData = self.E5052B.query(':CALCulate:PN1:DATA:CARR? ')
        temTab = str.split(readData, ',')
        self.pwr = round(float(temTab[1]), 3)
        return self.pwr

    def getFreqkHz(self):
        readData = self.E5052B.query(':CALCulate:PN1:DATA:CARR? ')
        temTab = str.split(readData, ',')
        self.freq = int(round(float(temTab[0])/1000, 0))
        return self.freq
