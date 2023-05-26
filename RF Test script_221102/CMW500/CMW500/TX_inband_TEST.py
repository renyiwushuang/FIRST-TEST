"""
This project is used for TX module test in CMW500.
@author: zhou chen
@First Vision: 2022/9/29

Support case:
    1M/s : In-band emissions
    2M/s : In-band emissions
"""
import socket
import time
import string
import numpy as np
from main import class_config

class stinband:
    LEVEL = np.matrix(np.zeros(81).reshape(81,1))

class result_inband:
    CH_LEVEL = np.matrix(np.zeros(81*40).reshape(81,40))

class result2_inband:
    CH_LEVEL = np.matrix(np.zeros(81*40).reshape(81,40))

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(( '192.168.190.63', 5025 ))

global  Configs
#Tx_config = tx_general_config()
Configs = class_config()

def socket_send(sendmsg):
    sendmsg = sendmsg+' ;\r\n'
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
    
 #   cmd_send('CONF:BLU:SIGN:OPM RFT')
  
 #   cmd_send('CONF:BASE:FDC:RCL')
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
    cmd_send('CONF:BLU:SIGN1:HWINterface ' + Configs.HWINTERFACE)
    cmd_send('CONF:BLU:SIGN1:CPRotocol ' + Configs.HWPROTOCOL)
    cmd_send('CONF:BLU:SIGN1:COMSettings:PORT:COMPort '+ Configs.RFCOM)
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
    Configs.INIT_STATUS = 1
    
def inband1m_config():
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LENergy ' + Configs.SIGNALTYPE)
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN) 
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')  
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SACP:LEN:MEAS:MODE CH40 ')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:SACP 10')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:SACP ON')
    
def inband2m_config():
    cmd_send('CONF:BLU:MEAS1:MEV:SACP:LEN:MEAS:MODE CH10 ')
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE2M')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M ' + Configs.SIGNALTYPE)
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN) 
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LE2M STAN')  
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SACP:LEN:LE2M:MEAS:MODE CH40')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:SACP 10')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:SACP ON')
    
    
def inband_read():
    #is_running = b'RUN\n'
    # while (is_running.decode('utf-8') != 'RDY') :
    #     socket_send('FETCh:BLUetooth1:MEASurementMEValuation:STATe?')
    #     is_running = conn.recv(1024)
    #     if (is_running.decode('utf-8') == 'RDY\n'):
    #         break
    time.sleep(1)

    socket_send('FETC:BLU:MEAS1:MEV:TRAC:SACP:PTX? ')    #P625  LE 1M PHY or LE 2M PHY.
    
    temp_data = conn.recv(2048)
    time.sleep(0.1)
    print(temp_data.decode())
    return temp_data

def inband_test():
    socket_send('INIT:BLU:MEAS1:MEV ' )
    test_per = inband_read()
    split_data = str.split( test_per.decode('utf-8'), ',')
    rst_data = np.matrix(np.zeros(81).reshape(81,1))
    for i in range(0,81):
        rst_data[i] = float(split_data[i+1])
        print(rst_data[i])
        print(i)
    
    return rst_data    
    
    
    
    
    
    
def inband_test_main(mode):
    if( mode == '1M' ):
        Configs.TESTMODE = 'INBAND1M'
    elif( mode == '2M' ):
        Configs.TESTMODE = 'INBAND2M'
    
    if( Configs.INIT_STATUS == 0):
        config_init()
    
    if( Configs.TESTMODE == 'INBAND1M' ):
        inband1m_config()
    elif( Configs.TESTMODE == 'INBAND2M' ):
        inband2m_config()  
        print("2M config")

    # Channel_range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
    #                  10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
    #                  20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
    #                  30, 31, 32, 33, 34, 35, 36, 37, 38, 39)                #  
    
    Channel_range =(1, 25, 37 )
    
    Result = result_inband()
    
    for CH in Channel_range:
        print("test channel is:" + str(int(CH)))
        cmd_send('CONF:BLU:SIGN1:RFS:CHAN:DTM '+str(CH))
        temp_res = inband_test()
        print(temp_res.size)
        Result.CH_LEVEL[0:,CH] = temp_res
        
    socket_send('STOP:BLU:MEAS1:MEV' )
    # cmd_send('CONF:BLU:SIGN1:RFS:ARAN OFF')
    return Result    
    
    
if __name__ == "__main__":
    
    INBAND1M = result_inband()

    INBAND1M = inband_test_main('1M')
    
    band1 = INBAND1M.CH_LEVEL[0:,37]
    
    # INBAND2M = result2_inband()

    # INBAND2M = inband_test_main('2M')  
    # band2 = INBAND2M.CH_LEVEL[0:,37]
    
    
    
    
    
    
    
    