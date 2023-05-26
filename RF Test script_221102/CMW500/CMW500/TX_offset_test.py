"""
This project is used for TX module test in CMW500.
@author: zhou chen
@First Vision: 2022/9/29

Support case:
    1M/s : Carrier frequency offset and drift, In-band emissions, Modulation Characteristics, Outputpower
    2M/s : Carrier frequency offset and drift, In-band emissions, Modulation Characteristics
    long-range : Carrier frequency offset and drift(S=8), Modulation Characteristics(S=8)
"""


import socket
import time
import string
import numpy as np
from main import class_config

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(( '192.168.190.63', 5025 ))


class tx_general_config:
    TESTMODE = 'CFOD1M'
    SIGNALLEN = '37'
    
class stcfod:
    FRE_ACC = 0
    FRE_OFF = 999
    FRE_DRI = 999
    MAX_DRI = 999
    INI_FRE_DRI = 999
    DF2_99 = 999
    
class result_cfod:
    FRE_ACC = np.matrix(np.zeros(40).reshape(40,1))
    FRE_OFF = np.matrix(np.zeros(40).reshape(40,1))
    FRE_DRI = np.matrix(np.zeros(40).reshape(40,1))
    MAX_DRI = np.matrix(np.zeros(40).reshape(40,1))
    INI_FRE_DRI = np.matrix(np.zeros(40).reshape(40,1))
    DF2_99 = np.matrix(np.zeros(40).reshape(40,1))      # %99 △F2

global Tx_config, Configs
Tx_config = tx_general_config()
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
    



def tx_cfod1m_config():
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN P11')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Tx_config.SIGNALLEN)
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')
    
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:MOD 10')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')

def tx_cfod2m_config():
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE2M')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M P11')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Tx_config.SIGNALLEN)
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LE2M STAN')
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:MOD 10')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')    
    
def tx_cfods8_config():
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LELR')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:FEC:LEN:LRAN S8')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ALL1')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LRAN ' + Tx_config.SIGNALLEN)
    cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
    cmd_send('TRIG:BLU:MEAS1:MEV:TOUT 1')
    cmd_send('CONF:BLU:MEAS1:MEV:SCO:MOD 10')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send('CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')    
    

def cfod1m_read():
    #is_running = b'RUN\n'
    # while (is_running.decode('utf-8') != 'RDY') :
    #     socket_send('FETCh:BLUetooth1:MEASurementMEValuation:STATe?')
    #     is_running = conn.recv(1024)
    #     if (is_running.decode('utf-8') == 'RDY\n'):
    #         break
    time.sleep(0.1)
    if ( Tx_config.TESTMODE == 'CFOD1M' ):
        socket_send('FETC:BLU:MEAS1:MEV:MOD:LEN:MAX? ')    #P584
    elif ( Tx_config.TESTMODE == 'CFOD2M' ):
        socket_send('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:MAX? ')
    elif( Tx_config.TESTMODE == 'CFODS8' ):
        socket_send('FETC:BLU:MEAS1:MEV:MOD:LEN:LRAN:MAX? ')
    temp_data = conn.recv(1024)
    print(temp_data.decode())
    return temp_data

def cfod1m_test():
    socket_send('INIT:BLU:MEAS1:MEV ' )
    test_per = cfod1m_read()
    split_data = str.split( test_per.decode('utf-8'), ',')
    rst_data = stcfod()
    if( Tx_config.TESTMODE == 'CFODS8' ):
        rst_data.DF2_99 = float(split_data[2])
        rst_data.FRE_ACC = float(split_data[3])
        rst_data.FRE_DRI = float(split_data[4])
        rst_data.MAX_DRI = float(split_data[5])
        rst_data.FRE_OFF = float(split_data[10])
        rst_data.INI_FRE_DRI = 0
    else:
        rst_data.DF2_99 = float(split_data[2])
        rst_data.FRE_ACC = float(split_data[3])
        rst_data.FRE_DRI = float(split_data[4])
        rst_data.MAX_DRI = float(split_data[5])
        rst_data.FRE_OFF = float(split_data[14])
        rst_data.INI_FRE_DRI = float(split_data[15])
 #   print(str(split_data[0]) + '  ' + str(split_data[1]) + '  ' + str(split_data[2])+ '  ' + str(split_data[3])+ '  ' + str(split_data[4]) )
    return rst_data




def Tx_test(mode):
    
    if( mode == '1M' ):
        Tx_config.TESTMODE = 'CFOD1M'
    elif( mode == '2M' ):
        Tx_config.TESTMODE = 'CFOD2M'
    elif( mode == 'S8'):
        Tx_config.TESTMODE = 'CFODS8'
    
    config_init()
    
    Result = result_cfod()
    
    if( Tx_config.TESTMODE == 'CFOD1M' ):
        tx_cfod1m_config()
    elif( Tx_config.TESTMODE == 'CFOD2M' ):
        tx_cfod2m_config()
    elif( Tx_config.TESTMODE == 'CFODS8' ):
        tx_cfods8_config()

    #Set Channel  -- 需要时可重写
    Channel_range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
                     10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                     20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 
                     30, 31, 32, 33, 34, 35, 36, 37, 38, 39)
    
    for CH in Channel_range:
        print("test channel is:" + str(int(CH)))
        temp_res = stcfod()
        cmd_send('CONF:BLU:SIGN1:RFS:CHAN:DTM '+str(CH))
        temp_res = cfod1m_test()
        Result.FRE_ACC[CH] = temp_res.FRE_ACC
        Result.FRE_OFF[CH] = temp_res.FRE_OFF
        Result.FRE_DRI[CH] = temp_res.FRE_DRI
        Result.MAX_DRI[CH] = temp_res.MAX_DRI
        Result.INI_FRE_DRI[CH] = temp_res.INI_FRE_DRI
        Result.DF2_99[CH] = temp_res.DF2_99
        
    socket_send('STOP:BLU:MEAS1:MEV' )
    return Result




if __name__ == "__main__":
    
    
    Configs.PACKAGELEN = '50'
    
    RST_CFOD1M = result_cfod()
    RST_CFOD2M = result_cfod()
    RST_CFODS8 = result_cfod()
    RST_CFOD1M = Tx_test('1M')
    
    
    ACC=RST_CFOD1M.FRE_ACC
    DRI = RST_CFOD1M.FRE_DRI
    MAX_DRI = RST_CFOD1M.MAX_DRI
    DF2_99 = RST_CFOD1M.DF2_99
    FRE_OFF = RST_CFOD1M.FRE_OFF
    INI_FRE_DRI = RST_CFOD1M.INI_FRE_DRI
    
    RST_CFOD2M = Tx_test('2M')
    ACC2 = RST_CFOD2M.FRE_ACC
    DRI2 = RST_CFOD2M.FRE_DRI
    MAX_DRI2 = RST_CFOD2M.MAX_DRI
    DF2_992 = RST_CFOD2M.DF2_99
    FRE_OFF2 = RST_CFOD2M.FRE_OFF
    INI_FRE_DRI2 = RST_CFOD2M.INI_FRE_DRI
    
    RST_CFODS8 = Tx_test('S8')
    ACCS8 = RST_CFODS8.FRE_ACC
    DRIS8 = RST_CFODS8.FRE_DRI
    MAX_DRIS8 = RST_CFODS8.MAX_DRI
    DF2_99S8 = RST_CFODS8.DF2_99
    FRE_OFFS8 = RST_CFODS8.FRE_OFF
    
    INI_FRE_DRIS8 = RST_CFODS8.INI_FRE_DRI
