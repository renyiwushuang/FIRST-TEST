import socket
import math
import time
import string
import numpy as np


class class_config:
    RFOUTPUT = '22.0'
    RFINPUT = '22.0'
    RFLEVEL = '-40.0'
    RFEXPECTEDPW = '10.0'
    RSCOM = 'COM2'
    RSBAUDRATE = 'B115K'
    PROTOCOL = 'NONE'
    SIGNALTYPE = 'PRBS9'
    SIGNALLEN = '37'
    HWINTERFACE = 'RS232'
    HWPROTOCOL = 'HCI'
    RFCOM = '0'
    PARITY = 'NONE'

# Test mode chose, can be  Receiver 1M ; Receiver 2M ;
    TESTMODE = 'Receiver 1M'  # End with no space.
    PACKAGELEN = '200'
    # setting param
    PER_SET = 30.8
    START_LEVEL = -116.0
    END_LEVEL = -50.0


global Configs
Configs = class_config()
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('192.168.190.63', 5025))
# 本地测试使用
#conn.connect(( '192.168.28.239', 5077 ))

##################################### TCP/IP communication###################################


def socket_send(sendmsg):
    sendmsg = sendmsg+'\r\n'
    conn.send(sendmsg.encode())


def cmd_send(send):
    socket_send(send)
    is_running = b'0\n'
    while (1):
        socket_send('*OPC? ')
        is_running = conn.recv(1024)
        if (is_running.decode('utf-8') == '1\n'):
            break
        time.sleep(0.05)


def config_init():

    cmd_send('CONF:BLU:SIGN:OPM RFT')

    cmd_send('CONF:BASE:FDC:RCL')
    # Signal config
    cmd_send('ROUTe:BLU:SIGN1:SCENario:OTRX RF1C,RX1,RF1C,TX1')
    cmd_send('SYSTem:BASE:REF:FREQ:SOURce INTernal')
    cmd_send('CONF:BLU:SIGN1:RFSettings:EATT:OUTP ' + Configs.RFOUTPUT)
    cmd_send('CONF:BLU:SIGN1:RFSettings:EATT:INP ' + Configs.RFINPUT)
    cmd_send('CONF:BLU:SIGN1:RFSettings:LEVel ' + Configs.RFLEVEL)
    cmd_send('CONF:BLU:SIGN1:RFSettings:ENPower ' + Configs.RFEXPECTEDPW)
    cmd_send('CONF:BLU:SIGN1:RFSettings:ARANging OFF')
    cmd_send('SOURce:BLU:SIGN1:STATe ON')

    cmd_send('CONF:BLU:SIGN1:CONN:BTYP LE')
    cmd_send('CONF:BLU:SIGN1:RFSettings:CHAN:DTMode 0')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LENergy 37')
    cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LENergy ' + Configs.SIGNALTYPE)
    cmd_send('CONF:BLU:SIGN1:HWINterface ' + Configs.HWINTERFACE)
    cmd_send('CONF:BLU:SIGN1:CPRotocol ' + Configs.HWPROTOCOL)
#    socket_send('CONF:BLU:SIGN1:COMSettings:PORT:COMPort '+ Configs.RFCOM)
    cmd_send('CONF:BLU:SIGN1:COMSettings:BAUDrate ' + Configs.RSBAUDRATE)

    cmd_send('CONF:BLU:SIGN1:COMSettings:STOPbits S1 ')
    cmd_send('CONF:BLU:SIGN1:COMSettings:PARity ' + Configs.PARITY)
    cmd_send('CONF:BLU:SIGN1:COMSettings:PROTocol ' + Configs.PROTOCOL)
    cmd_send('CONF:BLU:SIGN1:COMSettings:ERESet ON')
    cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
#  Init reciever 1M test case

    cmd_send('CONF:BLU:SIGN1:RFS:HOPP OFF')
    cmd_send('CONF:BLU:SIGN1:CONN:WHIT OFF')
    cmd_send("ROUT:BLU:MEAS1:SCEN:CSP 'Bluetooth Sig1'")
    cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:BTYPe LE')

    if (Configs.TESTMODE == 'Receiver 1M'):
        cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN)
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LENergy ' + Configs.SIGNALTYPE)
        #socket_send('CONF:BLU:SIGN1:RFS:DTX:MODE:LEN SPEC')
        cmd_send('CONF:BLU:SIGN1:RFS:DTX:MODF:LEN HDRF')
        cmd_send('CONF:BLU:SIGN1:RFS:LEV -70')
        cmd_send('CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')
        cmd_send('CONF:BLU:SIGN1:RXQ:PACK:LEN ' + Configs.PACKAGELEN)
    elif (Configs.TESTMODE == 'Receiver 2M'):
        cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE2M')
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M ' + Configs.SIGNALTYPE)
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN)
        cmd_send('CONF:BLU:SIGN1:RFS:LEV -70')
        cmd_send('CONF:BLU:SIGN1:RFS:DTX:MODF:LEN:LE2M HDRF')
        cmd_send(
            'CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LE2M STAN')
        cmd_send('CONF:BLU:SIGN1:RXQ:PACK:LEN:LE2M ' + Configs.PACKAGELEN)
    elif (Configs.TESTMODE == 'Receiver S2'):
        cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LELR')
        cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
        cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:FEC:LEN:LRAN S2')
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ' + Configs.SIGNALTYPE)
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LRAN ' + Configs.SIGNALLEN)
        cmd_send('CONF:BLU:SIGN1:RFS:LEV -70')
        cmd_send('CONF:BLU:SIGN1:RFS:DTX:MODF:LEN:LRAN HDRF')
        cmd_send(
            'CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
        cmd_send('CONF:BLU:SIGN1:RXQ:PACK:LEN:LRAN ' + Configs.PACKAGELEN)
    elif(Configs.TESTMODE == 'Receiver S8'):
        cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LELR')
        cmd_send('CONF:BLU:SIGN1:RFS:ARAN ON')
        cmd_send('CONFigure:BLUetooth:SIGN1:CONNection:FEC:LEN:LRAN S8')
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ' + Configs.SIGNALTYPE)
        cmd_send('CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LRAN ' + Configs.SIGNALLEN)
        cmd_send('CONF:BLU:SIGN1:RFS:LEV -70')
        cmd_send('CONF:BLU:SIGN1:RFS:DTX:MODF:LEN:LRAN HDRF')
        cmd_send(
            'CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
        cmd_send('CONF:BLU:SIGN1:RXQ:PACK:LEN:LRAN ' + Configs.PACKAGELEN)

    cmd_send('CONF:BLU:SIGN1:RXQ:TOUT 0')
    cmd_send('CONF:BLU:MEAS1:MEV:REP SING')
    cmd_send(
        'CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')


################################################Function TEST###################################################
def level_read():
    is_running = b'RUN\n'
    while (is_running.decode('utf-8') != 'RDY'):
        socket_send('FETC:BLU:SIGN1:RXQ:PER:STAT? ')
        is_running = conn.recv(1024)
        if (is_running.decode('utf-8') == 'RDY\n'):
            break
        time.sleep(0.05)
    if (Configs.TESTMODE == 'Receiver 1M'):
        socket_send('FETC:BLU:SIGN1:RXQ:PER:LEN? ')
    elif (Configs.TESTMODE == 'Receiver 2M'):
        socket_send('FETC:BLU:SIGN1:RXQ:PER:LEN:LE2M? ')
    else:
        socket_send('FETC:BLU:SIGN1:RXQ:PER:LEN:LRAN? ')
    temp_data = conn.recv(1024)
    split_data = str.split(temp_data.decode('utf-8'), ',')
    test = float(split_data[1])
    print(test)
    return test


def level_test(test_level):
    print("and test level is: " + str(test_level) + "\n")
    socket_send('CONF:BLU:SIGN:RFS:LEV ' + str(test_level))
    socket_send('INIT:BLU:SIGN:RXQ:PER ')
    test_per = level_read()
    return test_per


def RXM_sens_test(mode):
    print("mod is" + mode)
    if(mode == '1M'):
        Configs.TESTMODE = 'Receiver 1M'
    elif (mode == '2M'):
        Configs.TESTMODE = 'Receiver 2M'
    elif(mode == 'S2'):
        Configs.TESTMODE = 'Receiver S2'
    elif(mode == 'S8'):
        Configs.TESTMODE = 'Receiver S8'

    start_level = Configs.START_LEVEL
    end_level = Configs.END_LEVEL

    config_init()

    print("start to test.")

    time.sleep(2)

    Accuracy = np.matrix(np.zeros(40).reshape(40, 1))

    # Set Channel  -- 需要时可重写
    Channel_range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                     10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                     20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                     30, 31, 32, 33, 34, 35, 36, 37, 38, 39)

    for CH in Channel_range:
        print("test channel is:" + str(int(CH)))
        socket_send('CONF:BLU:SIGN:RFS:CHAN:DTM '+str(CH))
        new_start_level = start_level
        new_end_level = end_level
        CH_ACC = 0
        send_gap = new_end_level - new_start_level

        start_sign = 1
        end_sign = 1
        pass_sign = 0

        while (send_gap > 0.1):
            if (start_sign):
                Accuracy_start = level_test(new_start_level)
            if(end_sign):
                Accuracy_end = level_test(new_end_level)

            mid_level = round((new_start_level+new_end_level)/2, 2)
            Accuracy_mid = level_test(mid_level)

            if Accuracy_mid >= 30.8:
                mid_level = round((new_start_level+new_end_level)/2, 2)
                Accuracy_mid = level_test(mid_level)

            if (Accuracy_end <= Configs.PER_SET) & (Accuracy_mid <= Configs.PER_SET):
                new_end_level = mid_level
                Accuracy_end = Accuracy_mid
                pass_sign = 1
                end_sign = 0
                start_sign = 0
                CH_ACC = new_end_level
            elif (Accuracy_end <= Configs.PER_SET) & (Accuracy_start <= Configs.PER_SET):
                print("Channel "+str(CH)+" test falt, begin PER: " +
                      Accuracy_start + " and end PER: " + Accuracy_end)
                CH_ACC = 0
                break
            else:
                new_start_level = mid_level
                Accuracy_start = Accuracy_mid
                pass_sign = 0
                end_sign = 0
                start_sign = 0

            if(pass_sign):
                send_gap = new_end_level - new_start_level

        Accuracy[CH] = CH_ACC

    socket_send('SOUR:BLU:SIGN:STAT 0')
    print("Test end.")

    return Accuracy


# def RXS_sens_test(mode):
#     if(mode == 'S2'):
#         Configs.TESTMODE ='Receiver S2'
#     elif(mode == 'S8'):
#         Configs.TESTMODE ='Receiver S8'

#     config_init()
#     print(mode+"start to test.")
#     time.sleep(1)
#     RX_S_Accuracy = np.matrix(np.zeros(40).reshape(40,1))

class class_per_acc:
    Rx_1M = np.matrix(np.zeros(40).reshape(40, 1))
    Rx_2M = np.matrix(np.zeros(40).reshape(40, 1))
    Rx_S2 = np.matrix(np.zeros(40).reshape(40, 1))
    Rx_S8 = np.matrix(np.zeros(40).reshape(40, 1))
    pass


if __name__ == "__main__":

   # PER_search_Accuracy = np.matrix(np.zeros(40).reshape(40,4))
    PER_search_Accuracy = class_per_acc()

    PER_search_Accuracy.Rx_1M = RXM_sens_test('1M')
    PER_search_Accuracy.Rx_2M = RXM_sens_test('2M')
    PER_search_Accuracy.Rx_S2 = RXM_sens_test('S2')
    PER_search_Accuracy.Rx_S8 = RXM_sens_test('S8')

    conn.close()
