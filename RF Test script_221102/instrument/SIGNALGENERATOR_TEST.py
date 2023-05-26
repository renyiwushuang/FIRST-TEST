import time
import _AgilentN5181A_signalgenerator

TCPIP = 'TCPIP::169.254.74.249::INSTR'

if __name__ == '__main__':

    SG = _AgilentN5181A_signalgenerator.Signalgenerator
    SG.instr_init(self=SG, TCPIP=TCPIP)
    SG.set_output_para(self=SG, FreqMHz=2402, PowerDBM=0)
    SG.instr_output_on(self=SG)
    time.sleep(60)
    SG.instr_output_off(self=SG)
    SG.close()




