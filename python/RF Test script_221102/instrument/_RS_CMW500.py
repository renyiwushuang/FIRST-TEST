import pyvisa as visa
import time
import warnings
import string
import sys
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
    RETRY = 0
    # Test mode chose, will be writen in test case;
    TESTMODE = 'Receiver 1M'  # End with no space.
    PACKAGELEN = '200'
    # Setting param: PER_Search
    PER_SET = 30.8
    START_LEVEL = -112.0
    END_LEVEL = -60.0
    INIT_STATUS = 0
    SET_GAP = 0.2
    ACI_STEP = 1
    ACI_EMAGE_PW = -67
    ACI_LOSS = 8


global Configs
Configs = class_config()


class DTM_test_mode:
    LE1M = 1
    LE2M = 2
    LES2 = 3
    LES8 = 4

sleep_time=0.3

class RS_CMW500:
    def __init__(self):
        self.rm = None
        self.CMW500 = None
        self.testmode = None
        # open connection to power supply
    
    def cmd_send(self, cmd):
        res = 0
        self.CMW500.write(cmd)
        while(res==0):
            res = self.CMW500.query('*OPC?')
            time.sleep(0.03)

    def per_data_querry(self):
        is_running = 'RUN\n'
        nums = 0
        if( self.testmode==1 | self.testmode==2 ):
            query_timeout=200
        else:
            query_timeout = 1000
        while ( is_running!= 'RDY\n' ):
            is_running = self.CMW500.query('FETC:BLU:SIGN1:RXQ:PER:STAT? ')
            # print('querry data is ' + is_running)
            time.sleep(0.02)
            nums = nums + 1
            if( nums == query_timeout ):
                self.cmd_send(self=self, cmd='STOP:BLU:SIGN:RXQ:PER')
                time.sleep(0.1)
                self.cmd_send(self=self, cmd='INIT:BLU:SIGN:RXQ:PER')
                nums = 0


    def CMW500_connect(self, TCPIP):
        self.rm = visa.ResourceManager()
        self.CMW500 = self.rm.open_resource(TCPIP)
        self.CMW500.timeout = 25000

    def non_signaling_mode(self, test_mode=[DTM_test_mode]):
        print('Non_signaling mode ' + str(test_mode) + ' start.')
        self.testmode = test_mode
        self.cmd_send(self=self, cmd='ROUT:BLU:MEAS:SCEN:SAL RF1C,RX1')
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:MEAS:RFSettings:EATTenuation 22 ')
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:MEAS:RFSettings:ENPower 0')
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:MEAS:RFSettings:UMARgin 3')
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:MEAS:RFSettings:FREQuency 2402E+6')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:BTYP LE')
        if( test_mode == 1 ):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
        elif( test_mode == 2 ):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE2M')
        elif( test_mode == 3 ):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LELR')
        else:
            print('This test mode '+ str(test_mode) +' is wrong.')
            sys.exit()

    def non_signaling_set_freq(self, freqMHz):
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:MEAS:RFSettings:FREQuency ' +str(freqMHz) +'E+6')

    def non_signaling_get_data(self):
        #process data
        if ( self.testmode == 1 ):
            recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:MAX? ')

        elif( self.testmode == 2 ):
            recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:MAX? ')

        elif( self.testmode == 4 ):
            recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LELR:MAX? ')
        return recive_data

    def non_signaling_close(self):
        self.cmd_send(self=self, cmd='STOP:BLU:MEAS1:MEV')
        self.cmd_send(self=self, cmd='SOUR:BLU:SIGN:STAT 0')

    def mev_close(self):
        self.cmd_send(self=self, cmd='STOP:BLU:MEAS1:MEV')
        self.cmd_send(self=self, cmd='SOUR:BLU:SIGN:STAT 0')

    def stop_per(self):
        self.cmd_send(self=self, cmd='STOP:BLU:SIGN:RXQ:PER')
        self.cmd_send(self=self, cmd='SOUR:BLU:SIGN:STAT 0')

    def stop_mev(self):
        self.cmd_send(self=self, cmd='STOP:BLU:MEAS1:MEV')

    def offset_carrier_mode(self, test_mode=[DTM_test_mode]):
        """
        :param test_mode: This test case only support 1M/2M/S8 test.
        :return: None.
        """
        print('Offset_carrier mode ' + str(test_mode) + ' start.')
        self.testmode = test_mode
        self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
        self.cmd_send(self=self, cmd='CONF:BASE:FDC:RCL')
        self.cmd_send(self=self, cmd='ROUTe:BLU:SIGN1:SCENario:OTRX RF1C,RX1,RF1C,TX1')
        self.cmd_send(self=self, cmd='SYSTem:BASE:REF:FREQ:SOURce INTernal')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:EATT:OUTP '+ Configs.RFOUTPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:EATT:INP '+ Configs.RFINPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:LEVel '+ Configs.RFLEVEL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:ENPower '+ Configs.RFEXPECTEDPW)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:ARANging OFF')
        self.cmd_send(self=self, cmd='SOURce:BLU:SIGN1:STATe ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:BTYP LE')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:CHAN:DTMode 0')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LENergy 37')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LENergy ' + Configs.SIGNALTYPE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:HWINterface ' + Configs.HWINTERFACE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CPRotocol ' + Configs.HWPROTOCOL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:BAUDrate ' + Configs.RSBAUDRATE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:STOPbits S1 ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:PARity ' + Configs.PARITY)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:PROTocol ' + Configs.PROTOCOL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:ERESet ON ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:HOPP OFF')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:WHIT OFF')
        self.cmd_send(self=self, cmd="ROUT:BLU:MEAS1:SCEN:CSP 'Bluetooth Sig1'")
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:BTYPe LE')

        if (test_mode == 1):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN P11')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')
            self.cmd_send(self=self, cmd='TRIG:BLU:MEAS1:MEV:TOUT 1')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SCO:MOD 10')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:REP SING')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        elif (2 == test_mode):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE2M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M P11')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LE2M STAN')
            self.cmd_send(self=self, cmd='TRIG:BLU:MEAS1:MEV:TOUT 1')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SCO:MOD 10')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:REP SING')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        elif (test_mode == 4):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LELR')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:FEC:LEN:LRAN S8')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ALL1')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LRAN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
            self.cmd_send(self=self, cmd='TRIG:BLU:MEAS1:MEV:TOUT 1')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SCO:MOD 10')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:REP SING')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        else:
            print('Offset_carrier mode ' + str(test_mode) + ' is wrong.')
            sys.exit()

    def offset_carrier_channel(self, CH):
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:CHAN:DTM '+str(CH))
        self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')

    def offset_carrier_get_data(self):
        """
        :return: List data, S8(DF2_99; FRE_ACC; FRE_DRI; MAX_DRI; FRE_OFF), else(DF2_99; FRE_ACC; FRE_DRI; MAX_DRI; FRE_OFF; INI_FRE_DRI).
        """
        if ( self.testmode == 1 ):
            recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:MAX? ')
        elif( self.testmode == 2 ):
            recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:MAX? ')
        elif( self.testmode == 4 ):
            recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LRAN:MAX? ')
        print(recive_data)
        split_data = str.split(recive_data, ',')

        while( split_data[0] != '0' ):
            #Reset test
            self.stop_mev(self=self)
            self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')

            if (self.testmode == 1):
                recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:MAX? ')
            elif (self.testmode == 2):
                recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:MAX? ')
            elif (self.testmode == 4):
                recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LRAN:MAX? ')
            print(recive_data)
            split_data = str.split(recive_data, ',')

        if( self.testmode == 4 ):
            # print('Data_Fram is: DF2_99; FRE_ACC; FRE_DRI; MAX_DRI; FRE_OFF')
            result_data = [ float(split_data[2]),float(split_data[3]),float(split_data[4]),float(split_data[5]),float(split_data[10]), 0 ]
        else:
            # print('Data_Fram is: DF2_99; FRE_ACC; FRE_DRI; MAX_DRI; FRE_OFF; INI_FRE_DRI')
            result_data = [float(split_data[2]), float(split_data[3]), float(split_data[4]), float(split_data[5]),
                           float(split_data[14]),float(split_data[15])]
        return result_data

    def modulation_mode(self, test_mode=[DTM_test_mode]):
        """
        :param test_mode: This test case only support 1M/2M/S8 test.
        :return: None.
        """
        print('Modulation mode ' + str(test_mode) + ' start.')
        self.testmode = test_mode
        self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
        self.cmd_send(self=self, cmd='CONF:BASE:FDC:RCL')
        self.cmd_send(self=self, cmd='ROUTe:BLU:SIGN1:SCENario:OTRX RF1C,RX1,RF1C,TX1')
        self.cmd_send(self=self, cmd='SYSTem:BASE:REF:FREQ:SOURce INTernal')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:EATT:OUTP ' + Configs.RFOUTPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:EATT:INP ' + Configs.RFINPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:LEVel ' + Configs.RFLEVEL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:ENPower ' + Configs.RFEXPECTEDPW)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:ARANging OFF')
        self.cmd_send(self=self, cmd='SOURce:BLU:SIGN1:STATe ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:BTYP LE')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:CHAN:DTMode 0')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LENergy 37')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:HWINterface ' + Configs.HWINTERFACE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CPRotocol ' + Configs.HWPROTOCOL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:BAUDrate ' + Configs.RSBAUDRATE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:STOPbits S1 ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:PARity ' + Configs.PARITY)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:PROTocol ' + Configs.PROTOCOL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:ERESet ON ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:HOPP OFF')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:WHIT OFF')
        self.cmd_send(self=self, cmd="ROUT:BLU:MEAS1:SCEN:CSP 'Bluetooth Sig1'")
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:BTYPe LE')

        if (test_mode == 1):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')
            self.cmd_send(self=self, cmd='TRIG:BLU:MEAS1:MEV:TOUT 1')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SCO:MOD 10')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:REP SING')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:CHAN:DTM 0')
        elif (test_mode == 2):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE2M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LE2M STAN')
            self.cmd_send(self=self, cmd='TRIG:BLU:MEAS1:MEV:TOUT 1')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SCO:MOD 10')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:REP SING')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS:ISIG:DMOD MAN')
        elif (test_mode == 4):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LELR')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:FEC:LEN:LRAN S8')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LRAN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
            self.cmd_send(self=self, cmd='TRIG:BLU:MEAS1:MEV:TOUT 1')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SCO:MOD 10')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:REP SING')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS:ISIG:DMOD MAN')
        else:
            print('Modulation Characteristics mode ' + str(test_mode) + ' is wrong.')
            sys.exit()

    def modulation_channel(self, CH):
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:CHAN:DTM '+str(CH))

    def modulation_get_data(self):
        """
        :return: List data, S8(DF2_99; FRE_ACC; FRE_DRI; MAX_DRI; FRE_OFF), else(DF2_99; FRE_ACC; FRE_DRI; MAX_DRI; FRE_OFF; INI_FRE_DRI).
        """
        if ( self.testmode == 1 ):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN P44 ')
            self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
            recive_data1 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:AVER? ')
            time.sleep(0.1)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN P11 ')
            self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
            recive_data2 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:AVER? ')
        elif( self.testmode == 2 ):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M P44 ')
            self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
            recive_data1 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:AVER? ')
            time.sleep(0.1)
            self.stop_mev(self=self)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M P11 ')
            self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
            recive_data2 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:AVER? ')
        elif( self.testmode == 4 ):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ALL1 ')
            self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
            recive_data1 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LRAN:AVER? ')
            time.sleep(0.1)

            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ALL1 ')
            self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
            recive_data2 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LRAN:AVER? ')

        print(recive_data1)
        print(recive_data2)

        split_data1 = str.split( recive_data1, ',')
        split_data2 = str.split( recive_data2, ',')

        while ((split_data1[0] != '0')|(split_data2[0] != '0')):
            self.stop_mev(self=self)
            if (self.testmode == 1):
                self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN P44 ')
                self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
                recive_data1 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:AVER? ')
                self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN P11 ')
                self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
                recive_data2 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:AVER? ')
            elif (self.testmode == 2):
                self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M P44 ')
                self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
                recive_data1 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:AVER? ')
                self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M P11 ')
                self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
                recive_data2 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LE2M:AVER? ')
            elif (self.testmode == 4):
                self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ALL1 ')
                self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
                recive_data1 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LRAN:AVER? ')
                self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ALL1 ')
                self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
                recive_data2 = self.CMW500.query('FETC:BLU:MEAS1:MEV:MOD:LEN:LRAN:AVER? ')
            split_data1 = str.split(recive_data1, ',')
            split_data2 = str.split(recive_data2, ',')


        if( self.testmode != 4):
            #('Data_Fram is: DF1_AVG; DF2_99; DF2_AVG')
            result_data = [ float(split_data1[6]),float(split_data2[2]),float(split_data2[9])]
        else:
            #('Data_Fram is: DF1_AVG; DF1_99')
            result_data = [ float(split_data2[2]),float(split_data2[6]), 0]
        return result_data

    def per_search_mode(self, test_mode=[DTM_test_mode]):
        """
        :param test_mode: This test case only support 1M/2M/S8 test.
        :return: None.
        """
        print('Per_search mode ' + str(test_mode) + ' start.')
        self.testmode = test_mode
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:OPM RFT')
        self.cmd_send(self=self, cmd='CONF:BASE:FDC:RCL')
        self.cmd_send(self=self, cmd='ROUTe:BLU:SIGN1:SCENario:OTRX RF1C,RX1,RF1C,TX1')
        self.cmd_send(self=self, cmd='SYSTem:BASE:REF:FREQ:SOURce INTernal')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:EATT:OUTP '+ Configs.RFOUTPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:EATT:INP ' + Configs.RFINPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:LEVel ' + Configs.RFLEVEL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:ENPower ' + Configs.RFEXPECTEDPW)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:ARANging OFF')
        self.cmd_send(self=self, cmd='SOURce:BLU:SIGN1:STATe ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:BTYP LE')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:CHAN:DTMode 0')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LENergy 37')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:HWINterface ' + Configs.HWINTERFACE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CPRotocol ' + Configs.HWPROTOCOL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:BAUDrate ' + Configs.RSBAUDRATE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:STOPbits S1 ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:PARity ' + Configs.PARITY)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:PROTocol ' + Configs.PROTOCOL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:ERESet ON ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:HOPP OFF')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:WHIT OFF')
        self.cmd_send(self=self, cmd="ROUT:BLU:MEAS1:SCEN:CSP 'Bluetooth Sig1'")
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:BTYPe LE')

        if (test_mode == 1):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LENergy ' + Configs.SIGNALTYPE)
            # self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:DTX:MODE:LEN SPEC')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:DTX:MODF:LEN HDRF')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:LEV -70')
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RXQ:PACK:LEN ' + Configs.PACKAGELEN)
        elif (test_mode == 2):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PHY:LEN LE2M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:DTX:MODF:LEN:LE2M HDRF')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:LEV -70')
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LE2M STAN')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RXQ:PACK:LEN:LE2M ' + Configs.PACKAGELEN)
        elif (test_mode == 3):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PHY:LEN LELR')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:FEC:LEN:LRAN S2 ')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LRAN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:DTX:MODF:LEN:LRAN HDRF')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:LEV -70')
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RXQ:PACK:LEN:LRAN '+ Configs.PACKAGELEN)
        elif (test_mode == 4):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PHY:LEN LELR')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:FEC:LEN:LRAN S8')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LRAN ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LRAN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:DTX:MODF:LEN:LRAN HDRF')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:LEV -70')
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RXQ:PACK:LEN:LRAN ' + Configs.PACKAGELEN)
        else:
            print('This test mode ' + str(test_mode) + ' is wrong.')
            sys.exit()
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RXQ:TOUT 0')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RXQ:REP SING')
        self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')

    def per_search_channel(self, CH):
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:CHAN:DTM '+str(CH))

    def per_send_only(self, level):
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:LEV ' + str(level))
        self.cmd_send(self=self, cmd='INIT:BLU:SIGN:RXQ:PER ')
        self.per_data_querry(self=self)

    def per_search_get_data(self, Level):
        """
        :return: Error percentage.
        """
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:LEV '+ str(Level) )
        self.cmd_send(self=self, cmd='INIT:BLU:SIGN:RXQ:PER ')
        self.per_data_querry( self=self)
        if ( self.testmode == 1 ):
            recive_data = self.CMW500.query('FETC:BLU:SIGN1:RXQ:PER:LEN? ')
        elif( self.testmode == 2 ):
            recive_data = self.CMW500.query('FETC:BLU:SIGN1:RXQ:PER:LEN:LE2M? ')
        else:
            recive_data = self.CMW500.query('FETC:BLU:SIGN1:RXQ:PER:LEN:LRAN?')


        split_data = str.split(recive_data, ',')

        result = float(split_data[1])

        return result

    def per_search_test( self, Channel , mode ):
        '''
        :param Channel_range: test channel.
        :return:
        '''
        self.per_search_mode(self=self, test_mode=mode)
        Channel_range = Channel
        Accuracy = np.array(np.zeros(len(Channel_range)))
        for CH in Channel_range:
            print("Per test channel is:" + str(int(CH)))
            self.per_search_channel(self=self, CH=CH)
            new_start_level = Configs.START_LEVEL
            new_end_level = Configs.END_LEVEL
            CH_ACC = 0
            send_gap = new_end_level - new_start_level

            start_sign = 1
            end_sign = 1

            while (send_gap > Configs.SET_GAP):
                if (start_sign):
                    Accuracy_start = self.per_search_get_data(self=self, Level=new_start_level)
                if (end_sign):
                    Accuracy_end = self.per_search_get_data(self=self, Level=new_end_level)

                mid_level = round((new_start_level + new_end_level) / 2, 2)
                Accuracy_mid = self.per_search_get_data(self=self, Level=mid_level)

                if (Accuracy_mid >= 30.8)&Configs.RETRY:
                    Accuracy_mid = self.per_search_get_data(self=self, Level=mid_level)

                if (Accuracy_end <= Configs.PER_SET) & (Accuracy_mid <= Configs.PER_SET):
                    new_end_level = mid_level

                    Accuracy_end = Accuracy_mid
                    end_sign = 0
                    start_sign = 0
                    CH_ACC = new_end_level
                elif (Accuracy_end <= Configs.PER_SET) & (Accuracy_start <= Configs.PER_SET):
                    print(
                        "Channel " + str(
                            CH) + " test falt, begin PER: " + Accuracy_start + " and end PER: " + Accuracy_end)
                    CH_ACC = 0
                    break
                else:
                    new_start_level = mid_level
                    Accuracy_start = Accuracy_mid
                    end_sign = 0
                    start_sign = 0
                send_gap = new_end_level - new_start_level

            Accuracy[CH] = CH_ACC
        return Accuracy

    def inband_mode(self, test_mode=[DTM_test_mode]):
        """
        :param test_mode: This test case only support 1M/2M/S8 test.
        :return: None.
        """
        print('In-band emissions mode ' + str(test_mode) + ' start.')
        self.testmode = test_mode
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:OPM RFT ')
        self.cmd_send(self=self, cmd='CONF:BASE:FDC:RCL')
        self.cmd_send(self=self, cmd='ROUTe:BLU:SIGN1:SCENario:OTRX RF1C,RX1,RF1C,TX1')
        self.cmd_send(self=self, cmd='SYSTem:BASE:REF:FREQ:SOURce INTernal')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:EATT:OUTP ' + Configs.RFOUTPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:EATT:INP ' + Configs.RFINPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:LEVel ' + Configs.RFLEVEL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:ENPower ' + Configs.RFEXPECTEDPW)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:ARANging OFF')
        self.cmd_send(self=self, cmd='SOURce:BLU:SIGN1:STATe ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:BTYP LE')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFSettings:CHAN:DTMode 0')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LENergy 37')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:HWINterface ' + Configs.HWINTERFACE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CPRotocol ' + Configs.HWPROTOCOL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:BAUDrate ' + Configs.RSBAUDRATE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:STOPbits S1 ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:PARity ' + Configs.PARITY)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:PROTocol ' + Configs.PROTOCOL)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:COMSettings:ERESet ON ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:HOPP OFF')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:WHIT OFF')
        self.cmd_send(self=self, cmd="ROUT:BLU:MEAS1:SCEN:CSP 'Bluetooth Sig1'")
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:BTYPe LE')

        if (test_mode == 1):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE1M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LENergy ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy STAN')
            self.cmd_send(self=self, cmd='TRIG:BLU:MEAS1:MEV:TOUT 1')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SACP:LEN:MEAS:MODE CH40 ')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:REP SING')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SCO:SACP 10')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:SACP ON')
        elif (test_mode == 2):
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SACP:LEN:MEAS:MODE CH10')
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:CONNection:PHY:LEN LE2M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PATT:LEN:LE2M ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LE2M STAN')
            self.cmd_send(self=self, cmd='TRIG:BLU:MEAS1:MEV:TOUT 1')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SACP:LEN:LE2M:MEAS:MODE CH40')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:REP SING')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:SCO:SACP 10')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
            self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:SACP ON')
        else:
            print('In-band emissions mode ' + str(test_mode) + ' is wrong.')
            sys.exit()

    def inband_get_data(self,CH):
        """
        :return: List data, S8(DF2_99; FRE_ACC; FRE_DRI; MAX_DRI; FRE_OFF), else(DF2_99; FRE_ACC; FRE_DRI; MAX_DRI; FRE_OFF; INI_FRE_DRI).
        """
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RFS:CHAN:DTM ' + str(CH))
        self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
        time.sleep(5)
        recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:TRAC:SACP:PTX? ')

        split_data = str.split(recive_data, ',')
        
        while( split_data[0] != '0' ):
            self.stop_mev(self=self)
            time.sleep(sleep_time)
            self.cmd_send(self=self, cmd='INIT:BLU:MEAS1:MEV ')
            recive_data = self.CMW500.query('FETC:BLU:MEAS1:MEV:TRAC:SACP:PTX? ')
            print(recive_data)
            split_data = str.split(recive_data, ',')
        
        
        result_data = np.matrix(np.zeros(81).reshape(81, 1))
        for i in range(0, 81):
            result_data[i] = float(split_data[i + 1])
            # print(result_data[i])
        return result_data


    def hci_aci_mode(self, test_mode=[DTM_test_mode]):
        """
        :param test_mode: This test case only support 1M/2M/S8 test.
        :return: None.
        """
        print('ACI mode ' + str(test_mode) + ' start.')
        self.testmode = test_mode
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:OPM RFT')
        self.cmd_send(self=self, cmd='SOUR:BLU:SIGN:STAT 1')
        self.cmd_send(self=self, cmd='ROUTe:BLU:SIGN:SCENario:OTRX RF1C,RX1,RF1C,TX1')
        self.cmd_send(self=self, cmd='SYSTem:BASE:REF:FREQ:SOURce INTernal')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFSettings:EATT:OUTP '+ Configs.RFOUTPUT)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFSettings:EATT:INP ' + Configs.RFINPUT)
        # self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFSettings:LEVel ' + Configs.RFLEVEL)
        # self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFSettings:ENPower ' + Configs.RFEXPECTEDPW)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFSettings:ARANging OFF')
        # self.cmd_send(self=self, cmd='SOURce:BLU:SIGN:STATe ON')
        # self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:BTYP LE')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:HWINterface ' + Configs.HWINTERFACE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CPRotocol ' + Configs.HWPROTOCOL)
        # self.cmd_send(self=self, cmd='CONF:BLU:SIGN:COMSettings:BAUDrate ' + Configs.RSBAUDRATE)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:COMSettings:STOPbits S1 ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:COMSettings:PARity ' + Configs.PARITY)
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:COMSettings:PROTocol ' + Configs.PROTOCOL)
        # self.cmd_send(self=self, cmd='CONF:BLU:SIGN:COMSettings:ERESet ON ')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:ARAN ON')
        # self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:HOPP OFF')
        # self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:WHIT OFF')
        # self.cmd_send(self=self, cmd="ROUT:BLU:MEAS1:SCEN:CSP 'Bluetooth Sig1'")
        self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN:CONNection:BTYPe LE')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFSettings:CHAN:DTMode 0')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PLEN:LENergy 37')

        if (test_mode == 1):
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN:CONNection:PHY:LEN LE1M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PLEN:LEN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PATT:LENergy ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:CHAN:DTM 0')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:LEV -70')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RXQ:PACK:LEN ' + Configs.PACKAGELEN)
            postion = "'D:\Rohde-Schwarz\CMW\Data\waveform\ACI_M1_SPSM8.wv'"
        elif (test_mode == 2):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PHY:LEN LE2M')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PLEN:LEN:LE2M ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PATT:LEN:LE2M ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:CHAN:DTM 0')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:LEV -70')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RXQ:PACK:LEN:LE2M ' + Configs.PACKAGELEN)
            postion = "'D:\Rohde-Schwarz\CMW\Data\waveform\ACI_M2_SPSMX.wv'"
        elif (test_mode == 3):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PHY:LEN LELR')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:FEC:LEN:LRAN S2 ')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PATT:LEN:LRAN ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PLEN:LEN:LRAN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:CHAN:DTM 0')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:LEV -70')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RXQ:PACK:LEN:LRAN '+ Configs.PACKAGELEN)
            postion = "'D:\Rohde-Schwarz\CMW\Data\waveform\ACI_M1_SPSM8.wv'"
        elif (test_mode == 4):
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PHY:LEN LELR')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:ARAN ON')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:FEC:LEN:LRAN S8')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PATT:LEN:LRAN ' + Configs.SIGNALTYPE)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:CONN:PACK:PLEN:LEN:LRAN ' + Configs.SIGNALLEN)
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:CHAN:DTM 0')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:LEV -70')
            self.cmd_send(self=self, cmd='CONFigure:BLUetooth:SIGN1:RFSettings:DTX:MINDex:MODE:LENergy:LRAN STAN')
            self.cmd_send(self=self, cmd='CONF:BLU:SIGN1:RXQ:PACK:LEN:LRAN ' + Configs.PACKAGELEN)
            postion = "'D:\Rohde-Schwarz\CMW\Data\waveform\ACI_M1_SPSM8.wv'"
        else:
            print('This test mode ' + str(test_mode) + ' is wrong.')
            sys.exit()

        self.cmd_send(self=self, cmd='SOUR:GPRF:GEN1:STAT OFF')
        self.cmd_send(self=self, cmd='SOURce:GPRF:GEN1:RFSettings:FREQuency 0 MHz')
        self.cmd_send(self=self, cmd='ROUT:GPRF:GEN1:RFS:CONN RF3OUT')
        self.cmd_send(self=self, cmd='SOURCe:GPRF:GEN1:BBMode ARB')
        self.cmd_send(self=self, cmd='SOURCe:GPRF:GENerator1:ARB:FILE '+ postion)
        self.cmd_send(self=self, cmd='SOUR:GPRF:GEN1:STAT ON')
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RXQ:REP SING')
        # self.cmd_send(self=self, cmd='CONF:BLU:MEAS1:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')

    def hci_aci_channel(self, CH):
        self.cmd_send(self=self, cmd='CONF:BLU:SIGN:RFS:CHAN:DTM '+str(CH))

    def hci_aci_interferer_freq(self, freqMHz):
        self.cmd_send(self=self, cmd='SOURce:GPRF:GEN1:RFSettings:FREQuency ' + str(freqMHz)+' MHz')

    def hci_aci_interferer_level(self, level):
        self.cmd_send(self=self, cmd='SOUR:GPRF:GEN1:RFS:LEV ' + str(level))

    def hci_aci_get_data(self):
        self.cmd_send(self=self, cmd='INIT:BLU:SIGN:RXQ:PER ')
        self.per_data_querry(self=self)
        if (self.testmode == 1):
            recive_data = self.CMW500.query('FETC:BLU:SIGN:RXQ:PER:LEN? ') #1M OK
        elif (self.testmode == 2):
            recive_data = self.CMW500.query('FETC:BLU:SIGN:RXQ:PER:LEN:LE2M? ') #2M OK
        else:
            recive_data = self.CMW500.query('FETC:BLU:SIGN:RXQ:PER:LEN:LRAN? ')   #S8 OK  S2 OK

        split_data = str.split(recive_data, ',')

        result = float(split_data[1])

        return result

    def hci_aci_stop(self):
        self.cmd_send(self=self, cmd='STOP:BLU:SIGN:RXQ:PER ')
        self.cmd_send(self=self, cmd='SOUR:BLU:SIGN:STAT 0')
        self.cmd_send(self=self, cmd='SOUR:GPRF:GEN1:STAT OFF')

    def hci_aci_test( self,  CH ,test_mode=[DTM_test_mode]):
        Result_IntPwr1 = np.array(np.zeros(len(CH)))
        Result_IntPwr2 = np.array(np.zeros(len(CH)))
        Result_IntPwr3 = np.array(np.zeros(len(CH)))
        Result_IntPwr4 = np.array(np.zeros(len(CH)))
        Result_IntPwr5 = np.array(np.zeros(len(CH)))
        Result_IntPwr6 = np.array(np.zeros(len(CH)))
        Result_IntPwr7 = np.array(np.zeros(len(CH)))
        Result_IntPwr8 = np.array(np.zeros(len(CH)))
        Result_IntPwr9 = np.array(np.zeros(len(CH)))
        Result_IntPwr10 = np.array(np.zeros(len(CH)))
        Result_IntPwr11 = np.array(np.zeros(len(CH)))
        Result_IntPwr12 = np.array(np.zeros(len(CH)))
        Result_IntPwr13 = np.array(np.zeros(len(CH)))

        self.hci_aci_mode(self=self, test_mode=test_mode)
        Per = 0
        band_range = np.linspace(-6,6,13)
        IntPwr_range = [-40,-50,-70,-60,-65,-70,-70,-70,-70,-65,-60,-40,-30]
        for channel in range(len(CH)):
            self.hci_aci_channel(self=self, CH=CH[channel])
            freq = 2402 + CH[channel]*2
            temp_result = np.array(np.zeros(len(band_range)))
            for bd in band_range:
                IntPwr = IntPwr_range[int(bd)+6]
                if(test_mode==2):
                    freq_intpwr = freq + bd*2
                else:
                    freq_intpwr = freq + bd
                self.hci_aci_interferer_freq(self=self, freqMHz=freq_intpwr )
                while (30.8-Per)>0:
                    self.hci_aci_interferer_level(self=self, level=IntPwr )
                    Per = self.hci_aci_get_data(self=self)
                    IntPwr = IntPwr + Configs.ACI_STEP
                Per = 0
                IntPwr = IntPwr - Configs.ACI_STEP
                temp_result[int(bd+6)] = Configs.ACI_EMAGE_PW - IntPwr + Configs.ACI_LOSS
            #Total 13 value in each CH
            Result_IntPwr1[channel] = temp_result[0]
            Result_IntPwr2[channel] = temp_result[1]
            Result_IntPwr3[channel] = temp_result[2]
            Result_IntPwr4[channel] = temp_result[3]
            Result_IntPwr5[channel] = temp_result[4]
            Result_IntPwr6[channel] = temp_result[5]
            Result_IntPwr7[channel] = temp_result[6]
            Result_IntPwr8[channel] = temp_result[7]
            Result_IntPwr9[channel] = temp_result[8]
            Result_IntPwr10[channel] = temp_result[9]
            Result_IntPwr11[channel] = temp_result[10]
            Result_IntPwr12[channel] = temp_result[11]
            Result_IntPwr13[channel] = temp_result[12]

        Result = [Result_IntPwr1,Result_IntPwr2,Result_IntPwr3,Result_IntPwr4,Result_IntPwr5,Result_IntPwr6,
                  Result_IntPwr7,Result_IntPwr8,Result_IntPwr9,Result_IntPwr10,Result_IntPwr11,Result_IntPwr12,Result_IntPwr13]

        return Result

    def aci_data_querry(self):
        is_running = 'RUN\n'
        nums = 0
        if( self.testmode==1 | self.testmode==2 ):
            query_timeout=200
        else:
            query_timeout = 1000
        while ( is_running!= 'RDY\n' ):
            is_running = self.CMW500.query('FETC:BLU:SIGN:RXQ:PER:STAT? ')
            # print('querry data is ' + is_running)
            time.sleep(0.02)
            nums = nums + 1
            if( nums == query_timeout ):
                self.cmd_send(self=self, cmd='STOP:BLU:SIGN:RXQ:PER')
                time.sleep(0.1)
                self.cmd_send(self=self, cmd='INIT:BLU:SIGN:RXQ:PER')
                nums = 0



