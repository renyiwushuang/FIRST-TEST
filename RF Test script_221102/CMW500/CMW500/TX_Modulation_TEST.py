"""
This project is used for TX module test in CMW500.
@author: zhou chen
@First Vision: 2022/9/29

Support case:
    1M/s : Modulation Characteristics
    2M/s : Modulation Characteristics
    long-range : Modulation Characteristics(S=8)
"""

import socket
import time
import string
import numpy as np
from main import class_config




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
    Configs.INIT_STATUS = 1
    
def mc1m_config():
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN) 
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')  
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:MOD 10')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
    
def mc2m_config():
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE2M')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN)
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LE2M STAN')
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:MOD 10')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')  
    
def mcs8_config():
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LELR')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:FEC:LEN:LRAN S8')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN)
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:MOD 10')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')    
    
    
    
    
    
#data read for LE uncoded PHY (LE 1M PHY, LE 2M PHY)
def mc_read():
    #is_running = b'RUN\n'
    # while (is_running.decode('utf-8') != 'RDY') :
    #     socket_send('FETCh:BLUetooth1:MEASurementMEValuation:STATe?')
    #     is_running = conn.recv(1024)
    #     if (is_running.decode('utf-8') == 'RDY\n'):
    #         break
    time.sleep(0.1)
    if( Configs.TESTMODE == 'MCS8' ):
        socket_send('FETC:BLU:MEAS1:MEV:MOD:LEN:LRAN:AVER? ') 
    elif( Configs.TESTMODE == 'MC2M'):
        socket_send('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:AVER? ')    #P625  LE 1M PHY or LE 2M PHY.
    elif( Configs.TESTMODE == 'MC1M'):
        socket_send('FETC:BLU:MEAS1:MEV:MOD:LEN:AVER? ')    #P625  LE 1M PHY or LE 2M PHY.
    temp_data = conn.recv(1024)
    print(temp_data.decode())
    return temp_data

def mc_test():
    if( Configs.TESTMODE == 'MCS8'):
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ALL1 ')
        socket_send('INIT:BLU:MEAS1:MEV ' )
        test_per1 = mc_read()
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ALL1 ')
        socket_send('INIT:BLU:MEAS1:MEV ' )
        test_per1 = mc_read()        
    elif( Configs.TESTMODE == 'MC2M'):
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M P44 ')
        socket_send('INIT:BLU:MEAS1:MEV ' )
        test_per1 = mc_read()
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M P11 ')
        socket_send('INIT:BLU:MEAS1:MEV ' )   
        test_per2 = mc_read()
    elif( Configs.TESTMODE == 'MC1M' ):
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN P44 ')
        socket_send('INIT:BLU:MEAS1:MEV ' )
        test_per1 = mc_read()
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN P11 ')
        socket_send('INIT:BLU:MEAS1:MEV ' )   
        test_per2 = mc_read()
    # split_data = str.split( test_per.decode('utf-8'), ',')
    # rst_data = stinband()
    # for i in range(0,40):
    #     rst_data.LEVEL[i] = float(split_data[i+1])
    return 1        




    
    
def mc_test_main(mode):
    if( mode == '1M' ):
        Configs.TESTMODE = 'MC1M'
    elif( mode == '2M' ):
        Configs.TESTMODE = 'MC2M'
    elif( mode == 'S8' ):
        Configs.TESTMODE = 'MCS8'
        
    if( Configs.INIT_STATUS == 0):
        config_init()
    
    if( Configs.TESTMODE == 'MC1M' ):
        mc1m_config()
    elif( Configs.TESTMODE == 'MC2M' ):
        mc2m_config()
    elif( Configs.TESTMODE == 'MCS8' ):
        mcs8_config()
    #    inband2m_config()       

    Channel_range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
                     10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                     20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
                     30, 31, 32, 33, 34, 35, 36, 37, 38, 39)
    
#    Result = result_inband()
    
    for CH in Channel_range:
        print("test channel is:" + str(int(CH)))
#        temp_res = stinband()
        cmd_send('CONF:BLU:SIGN1:RFS:CHAN:DTM '+str(CH))
        temp_res = mc_test()
#        Result.CH_LEVEL[CH,0:] = temp_res
        
    socket_send('STOP:BLU:MEAS1:MEV' )
    return 1        
    





if __name__ == "__main__":
    
    mc_test_main('1M')
    
    # mc_test_main('2M')
    
    # mc_test_main('S8')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    