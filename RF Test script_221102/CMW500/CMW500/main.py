# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 17:07:21 2022

@author: E001643
"""

global Configs


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
    
#Test mode chose, can be  Receiver 1M ; Receiver 2M ;
    TESTMODE = 'Receiver 1M'   #End with no space.
    PACKAGELEN = '200'
    #setting param
    PER_SET = 30.8
    START_LEVEL = -100.0
    END_LEVEL = -50.0
    
    INIT_STATUS = 0