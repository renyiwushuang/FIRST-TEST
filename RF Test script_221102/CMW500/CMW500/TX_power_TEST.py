"""
This project is used for TX module test in CMW500.
@author: zhou chen
@First Vision: 2022/9/29

Support case:
    Output power test.
"""

import socket
import time
import string
import numpy as np
from main import class_config

class stpower:
    BURST_OUT = 0
    NORM_PW = 0
    PEAK_PW = 0
    LEAK_PW = 999
    PEAK_MIN_AVG = 0

class result_power:
    BURST_OUT = np.matrix(np.zeros(40).reshape(40,1))
    NORM_PW = np.matrix(np.zeros(40).reshape(40,1))
    PEAK_PW = np.matrix(np.zeros(40).reshape(40,1))
    LEAK_PW = np.matrix(np.zeros(40).reshape(40,1))
    PEAK_MIN_AVG = np.matrix(np.zeros(40).reshape(40,1))


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(( '192.168.190.63', 5025 ))

global  Configs
#Tx_config = tx_general_config()
Configs = class_config()

def socket_send(sendmsg):
    sendmsg = sendmsg+'\r\n'
    conn.send( sendmsg.encode() )

def cmd_send(send):
    socket_send(send)
    is_running = b'0\n'
    while (1) :
        socket_send('*OPC? ')
        is_running = conn.recv(1024)
        if (is_running.decode('utf-8') == '1\n'):
            break
        time.sleep(0.05)
        

def config_init():
    
    cmd_send('CONF:BLU:SIGN:OPM RFT')
    
    cmd_send('CONF:BASE:FDC:RCL')
    #Signal config
    cmd_send('ROUTe:BLU:SIGN1:SCENario:OTRX RF1C,RX1,RF1C,TX1')
    cmd_send('SYSTem:BASE:REF:FREQ:SOURce INTernal')
    cmd_send('CONF:BLU:SIGN1:RFSettings:EATT:OUTP '+ Configs.RFOUTPUT)
    cmd_send('CONF:BLU:SIGN1:RFSettings:EATT:INP '+ Configs.RFINPUT)
    cmd_send('CONF:BLU:SIGN1:RFSettings:LEVel '+ Configs.RFLEVEL)
    cmd_send('CONF:BLU:SIGN1:RFSettings:ENPower '+ Configs.RFEXPECTEDPW)
    cmd_send('CONF:BLU:SIGN1:RFSettings:ARANging OFF')
    cmd_send('SOURce:BLU:SIGN1:STATe ON')
    
    cmd_send('CONF:BLU:SIGN1:CONN:BTYP LE')
    cmd_send('CONF:BLU:SIGN1:RFSettings:CHAN:DTMode 0')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LENergy 37')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LENergy ' + Configs.SIGNALTYPE)
    cmd_send('CONF:BLU:SIGN1:HWINterface ' + Configs.HWINTERFACE)
    cmd_send('CONF:BLU:SIGN1:CPRotocol ' + Configs.HWPROTOCOL)
    cmd_send('CONF:BLU:SIGN1:COMSettings:BAUDrate ' + Configs.RSBAUDRATE)
    cmd_send('CONF:BLU:SIGN1:COMSettings:STOPbits S1 ')
    cmd_send('CONF:BLU:SIGN1:COMSettings:PARity ' + Configs.PARITY)
    cmd_send('CONF:BLU:SIGN1:COMSettings:PROTocol ' + Configs.PROTOCOL)
    cmd_send('CONF:BLU:SIGN1:COMSettings:ERESet ON')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONF:BLU:SIGN1:RFS:HOPP OFF')
    cmd_send('CONF:BLU:SIGN1:CONN:WHIT OFF')

    cmd_send("ROUT:BLU:MEAS1:SCEN:CSP 'Bluetooth Sig1'")
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:BTYPe LE')
    
    
def power1m_config():
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONF:BLU:MEAS1:ISIG:PATT:LEN OTH')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN)    
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')    
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:PVT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,ON,OFF,OFF,OFF,OFF')    


def power_read():
    #is_running = b'RUN\n'
    # while (is_running.decode('utf-8') != 'RDY') :
    #     socket_send('FETCh:BLUetooth1:MEASurementMEValuation:STATe?')
    #     is_running = conn.recv(1024)
    #     if (is_running.decode('utf-8') == 'RDY\n'):
    #         break
    time.sleep(0.1)
    if ( Configs.TESTMODE == 'POWER1M' ):
        socket_send('FETC:BLU:MEAS1:MEV:PVT:LEN:AVER? ')    #P563
    temp_data = conn.recv(1024)
    print(temp_data.decode())
    return temp_data

def power1m_test():
    socket_send('INIT:BLU:MEAS1:MEV ' )
    test_per = power_read()
    split_data = str.split( test_per.decode('utf-8'), ',')
    rst_data = stpower()
    if( Configs.TESTMODE == 'POWER1M' ):
        rst_data.BURST_OUT = float(split_data[1])
        rst_data.NORM_PW = float(split_data[2])
        rst_data.PEAK_PW = float(split_data[3])
        rst_data.LEAK_PW = float(split_data[4])
        rst_data.PEAK_MIN_AVG = float(split_data[5])
    return rst_data






def power_test_main(mode):
    if( mode == '1M' ):
        Configs.TESTMODE = 'POWER1M'
        
    config_init()
    Result = result_power()
    
    if( Configs.TESTMODE == 'POWER1M' ):
        power1m_config()

    Channel_range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
                     10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                     20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
                     30, 31, 32, 33, 34, 35, 36, 37, 38, 39)
    
    for CH in Channel_range:
        print("test channel is:" + str(int(CH)))
        temp_res = stpower()
        cmd_send('CONF:BLU:SIGN1:RFS:CHAN:DTM '+str(CH))
        temp_res = power1m_test()
        Result.BURST_OUT[CH] = temp_res.BURST_OUT
        Result.NORM_PW[CH] = temp_res.NORM_PW
        Result.PEAK_PW[CH] = temp_res.PEAK_PW
        Result.LEAK_PW[CH] = temp_res.LEAK_PW
        Result.PEAK_MIN_AVG[CH] = temp_res.PEAK_MIN_AVG
        
#    socket_send('STOP:BLU:MEAS1:MEV' )
    return Result

if __name__ == "__main__":
    
    RST_POWER = result_power()
    
    RST_POWER = power_test_main('1M')
    
    BURST_OUT = RST_POWER.BURST_OUT
    NORM_PW = RST_POWER.NORM_PW
    PEAK_PW = RST_POWER.PEAK_PW
    LEAK_PW = RST_POWER.LEAK_PW
    PEAK_MIN_AVG = RST_POWER.PEAK_MIN_AVG







