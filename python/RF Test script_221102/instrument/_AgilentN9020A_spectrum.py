import pyvisa as visa
from matplotlib import pyplot as plot


class Agilent_MXA_N9020A:
    medida = 'MHZ'

    def __init__(self):
        self.datosCapturados = None
        self.maxfreq = None
        self.instAgilent = None
        self.rm = None
        self.N9020A = None
        self.inicialFreq = None
        self.finalFreq = None
        self.centralFreq = None
        self.referenceLevel = None
        self.nPoints = None
        self.span = None

        # sel.nPoints = int(self.scope.query('SWE:POIN?'))

    def identity(self):
        info = self.N9020A.query('*IDN?')
        info = info.split(",")
        print("Fabricante: ", info[0])
        print("Model: ", info[1])
        print("Number of serie: ", info[2])
        print("Firmware: ", info[3])

    def spectrum_init(self, TCPIP):
        self.rm = visa.ResourceManager()
#        self.N9020A = self.rm.open_resource('TCPIP::169.254.74.249::INSTR')
        self.N9020A = self.rm.open_resource(TCPIP)

    def disconnect(self):
        self.N9020A.close()

    def setSpectrum(self):
        self.N9020A.write('INST SA')
        self.instAgilent = 'SA'

    def getInitialParamsAgilent(self):
        self.instAgilent = str(self.N9020A.query('INST?'))
        self.setSpectrum(self)
        self.inicialFreq = float(self.N9020A.query('FREQ:START?')) / 1e6
        self.finalFreq = float(self.N9020A.query('FREQ:STOP?')) / 1e6
        self.centralFreq = float(self.N9020A.query('FREQ:CENT?')) / 1e6
        self.referenceLevel = float(self.N9020A.query('DISP:WIND:TRAC:Y:RLEV?'))
        self.nPoints = int(self.N9020A.query('SWE:POIN?'))
        self.span = float(self.N9020A.query('FREQ:SPAN?')) / 1e6
        self.N9020A.write('INST ' + self.instAgilent)

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

        self.N9020A.write('FREQ:START ' + str(inicialFreq) + self.medida)
        self.N9020A.write('FREQ:STOP ' + str(finalFreq) + self.medida)
        self.N9020A.write('FREQ:CENT ' + str(self.centralFreq) + self.medida)
        self.N9020A.write('DISP:WIND:TRAC:Y:RLEV ' + str(referenceLevel))
        self.nPoints = int(self.N9020A.query('SWE:POIN?'))

    def setParamsSpectrumSpan(self, centralFreq, span, referenceLevel):
        self.setCentralFreqMHz(centralFreq)
        self.setSpanMHz(span)
        self.setReferenceLevelDBM(referenceLevel)
        self.nPoints = int(self.N9020A.query('SWE:POIN?'))

    def setSpanMHz(self, span):
        self.span = float(span)
        mitad = self.span / 2.0
        self.N9020A.write('FREQ:SPAN ' + str(span) + self.medida)

        self.inicialFreq = self.centralFreq - mitad
        self.N9020A.write('FREQ:START ' + str(self.inicialFreq) + self.medida)
        self.finalFreq = self.centralFreq + mitad
        self.N9020A.write('FREQ:STOP ' + str(self.finalFreq) + self.medida)

    def getSpanMHz(self):
        print("Span: ", self.span, " MHz")

    def setCentralFreqMHz(self, centralFreq):
        self.centralFreq = float(centralFreq)
        self.N9020A.write('FREQ:CENT ' + str(centralFreq) + self.medida)

    def getCentralFreqMHz(self):
        print("Frecuencia central: ", self.centralFreq, " MHz")

    def setInicialFreqMHz(self, inicialFreq):
        self.inicialFreq = float(inicialFreq)
        self.N9020A.write('FREQ:START ' + str(inicialFreq) + self.medida)
        self.centralFreq = (self.inicialFreq + self.finalFreq) / 2.0

    def getInicialFreqMHz(self):
        print("Frecuencia inicial: ", self.inicialFreq, " MHz")

    def setFinalFreqMHz(self, finalFreq):
        self.finalFreq = float(finalFreq)
        self.N9020A.write('FREQ:STOP ' + str(finalFreq) + self.medida)
        self.centralFreq = (self.inicialFreq + self.finalFreq) / 2.0

    def getFinalFreqMHz(self):
        print("Frecuencia final: ", self.finalFreq, " MHz")

    def setReferenceLevelDBM(self, referenceLevel):
        self.referenceLevel = float(referenceLevel)
        self.N9020A.write('DISP:WIND:TRAC:Y:RLEV ' + str(referenceLevel))

    def getReferenceLevelDBM(self):
        print("Nivel de referencia: ", self.referenceLevel, " dBm")

    def getNumPoints(self):
        puntos = int(self.N9020A.query('SWE:POIN?'))
        return puntos

    def setNumPoints(self, npoints):
        self.nPoints = int(npoints)
        self.N9020A.write('SWE:POIN ' + str(npoints))

    def getMaxFreqPower(self):
        self.N9020A.write('CALC:MARK:MAX')
        self.maxfreq = float(self.N9020A.query('CALC:MARK:X?')) / 1e6
        power = float(self.N9020A.query('CALC:MARK:Y?'))
        return power

    def getMaxPowerFreqMHz(self):
        self.N9020A.write('CALC:MARK:MAX')
        self.maxfreq = float(self.N9020A.query('CALC:MARK:X?')) / 1e6
        return self.maxfreq

    def getPowerDBM(self, freq):
        self.N9020A.write('CALC:MARK:X ' + str(freq) + self.medida)
        print("Potencia asociada a la frecuencia dada: ", self.N9020A.query('CALC:MARK:Y?'), " dBm")

    def plotInfoAgilent(self):
        puntos = self.getNumPoints()

        self.N9020A.write('FORM ASC')
        datos = self.N9020A.query(
            'TRAC? TRACE1')
        datosManipulables = datos.split(",")
        datosManipulables = [float(i) for i in datosManipulables]
        self.datosCapturados = datosManipulables.copy()

        freq = self.finalFreq - self.inicialFreq
        pointWidth = freq / float(puntos)
        frequencies = []
        count = 0
        while len(frequencies) != puntos:
            frequencies.append(self.inicialFreq + (pointWidth * count))
            count += 1

        plot.clf()
        plot.xlabel("Frequency (MHz)")
        plot.ylabel("Power (dBm)")
        plot.title("Output of Spectrum Analyzer")
        plot.grid()
        plot.plot(frequencies, datosManipulables)
        plot.savefig('./images/graphAgilent.png')
        plot.show()
