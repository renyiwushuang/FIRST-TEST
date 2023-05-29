import time
import serial
import serial.tools.list_ports


from retrying import retry


class TxPaModeDef:
    LP_mode = 3
    VMD_mode = 1


class TxPowerDef:
    TX_NEG20_DBM = 0
    TX_NEG5_DBM = 1
    TX_0_DBM = 2
    TX_5_DBM = 3
    TX_7_DBM = 4
    TX_10_DBM = 5


class TxGainTabIdxDef:
    TX_GAIN_0 = 0
    TX_GAIN_1 = 1
    TX_GAIN_2 = 2
    TX_GAIN_3 = 3
    TX_GAIN_4 = 4
    TX_GAIN_5 = 5


class VcoPowerDef:
    LDO_VCO_850mV = 0
    LDO_VCO_900mV = 1
    LDO_VCO_950mV = 2
    LDO_VCO_1000mV = 3
    LDO_VCO_1050mV = 4
    LDO_VCO_1100mV = 5
    LDO_VCO_1150mV = 6
    LDO_VCO_1200mV = 7


# reg 40008814[7:5]
class VcoVppDef:
    VCO_VPP_350mV = 0
    VCO_VPP_400mV = 1
    VCO_VPP_450mV = 2
    VCO_VPP_500mV = 3
    VCO_VPP_550mV = 4
    VCO_VPP_600mV = 5
    VCO_VPP_650mV = 6
    VCO_VPP_700mV = 7


class LdoActDef:
    LDO_ACT_1300mV = 0
    LDO_ACT_1250mV = 1
    LDO_ACT_1200mV = 2
    LDO_ACT_1150mV = 3
    LDO_ACT_1100mV = 4
    LDO_ACT_1050mV = 5
    LDO_ACT_1000mV = 6
    LDO_ACT_950mV = 7


class LdoRfDef:
    LDO_RF_850mV = 0
    LDO_RF_900mV = 1
    LDO_RF_950mV = 2
    LDO_RF_1000mV = 3
    LDO_RF_1050mV = 4
    LDO_RF_1100mV = 5
    LDO_RF_1150mV = 6
    LDO_RF_1200mV = 7


class RfTestModeDef:
    LE1M = 1
    LE2M = 2
    LES2 = 4
    LES8 = 3


class PayloadTypeDef:
    PRBS9 = 0
    HALF10 = 1
    MIX10 = 2
    PRBS15 = 3
    ALL1 = 4
    ALL0 = 5
    HALF01 = 6
    MIX01 = 7

# Reg 0x40009010 [2:0]


class RegAcgModeDef:
    AUTO = 0
    GAIN0 = 1
    GAIN1 = 3
    GAIN2 = 5


class UCI_Serial:
    def __init__(self):
        self.ser = None
        self.send_num = 0
        self.receive_num = 0
        self.port = ''
        self.bps = 115200
        self.timeout = 0
        self.serIsOpen = False

    def UCI_serial_port_refresh(self):
        # 查询可用的串口
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            print("No used com!")
        else:
            for i in range(0, len(plist)):
                plist_0 = list(plist[i])
                print(plist_0[0])

    def UCI_port_init(self, port, bps, timeout):
        self.port = port
        self.bps = bps
        self.timeout = timeout

    def UCI_read_reg(self, reg_addr):
        reg_val = 0xFFFFFFFF
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        # print(reg_addr.to_bytes(4, 'big'))
        reg_addr_data = bytearray(4)
        # for i in range(0, 4):
        #     reg_addr_data[i] = reg_addr.to_bytes(4, 'little')[i]
        # # print(reg_addr_data.hex())

        # if self.ser.isOpen():
        #     # print("serial open success")
        #     self.serIsOpen = True
        #     # print(ser.name)
        # else:
        #     print("serial open fail")
        # cmdorg = bytes.fromhex('01 C2 FC 04')
        # cmd = bytearray(8)
        # for i in range(0, 4):
        #     cmd[i] = cmdorg[i]
        # for i in range(0, 4):
        #     cmd[i + 4] = reg_addr_data[i]
        # # print(cmd.hex())

        try:
            self.ser.write(cmd)
            # print("<- " + cmd.hex())
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.02)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                # print(num)
                rcvdata = self.ser.read(num)
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)

                index = rcvdata.find(0xfc) + 1
                reg_val = rcvdata[index] + (rcvdata[index + 1] << 8) + (rcvdata[index + 2] << 16) + (
                    rcvdata[index + 3] << 32)
            else:
                print('serial receive fail!')
        except:
            reg_val = 0xFFFFFFFF
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        return reg_val

    def HCI_write_reg(self, reg_addr, write_val):
        ret = False
        reg_val = 0xFFFFFFFF
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        # print(reg_addr.to_bytes(4, 'big'))
        reg_addr_data = bytearray(4)
        for i in range(0, 4):
            reg_addr_data[i] = reg_addr.to_bytes(4, 'little')[i]
        # print(reg_addr_data.hex())

        write_val_data = bytearray(4)
        for i in range(0, 4):
            write_val_data[i] = write_val.to_bytes(4, 'little')[i]
        # print(write_val_data.hex())

        if self.ser.isOpen():
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 C3 FC 08')
        cmd = bytearray(12)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        for i in range(0, 4):
            cmd[i + 4] = reg_addr_data[i]
        for i in range(0, 4):
            cmd[i + 8] = write_val_data[i]
        # print(cmd.hex())

        try:
            self.ser.write(cmd)
            # print("<- " + cmd.hex())
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.02)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                index = rcvdata.find(0xfc) + 1
                reg_val = rcvdata[index] + (rcvdata[index + 1] << 8) + (rcvdata[index + 2] << 16) + (
                    rcvdata[index + 3] << 32)
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if reg_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_rf_reset(self):
        ret = False
        evt_val = 0xFF
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        if self.ser.isOpen():
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 03 0C 00')
        cmd = bytearray(4)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                index = rcvdata.find(0x0C) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_pa_power_rfio_cap(self, power_mode, RfioCapacitor):
        # power_mode 0 == Lp 0dBm ， power_mode 1 == VMD 10dBm
        Reg_addr = 0x4000882c
        if (power_mode == 0):
            Reg_bit_shift = 3
        else:
            Reg_bit_shift = 8
        Reg_bit_set = RfioCapacitor
        Reg_Mask = 0x31 << Reg_bit_shift  # [7:5]
        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        print('0x{:08X}'.format(Reg_addr), '->', '0x{:08X}'.format(Now_Reg))
        Now_Reg &= ~(Reg_Mask)
        # print('0x{:08X}'.format(Now_Reg))
        Now_Reg |= ((Reg_bit_set << Reg_bit_shift) & Reg_Mask)
        # print('0x{:08X}'.format(Now_Reg))
        self.HCI_write_reg(self, reg_addr=Reg_addr, write_val=Now_Reg)
        Read_reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        print('0x{:08X}'.format(Read_reg))

    @retry(tries=2)
    def HCI_single_tone(self, freqMHz, powerSel=[TxPowerDef]):
        ret = False
        evt_val = 0xFF
        freq_h = freqMHz >> 8
        freq_l = freqMHz & 0x00ff
        # print(freq_h)
        # print(freq_l)
        self.ser = serial.Serial(self.port, self.bps, timeout=0.1)
        if self.ser.isOpen():
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 36 20 03')
        cmd = bytearray(7)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = freq_l
        cmd[5] = freq_h
        cmd[6] = powerSel
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.02)
        try:
            num = self.ser.inWaiting()
            # print(num)
            if num > 0:
                rcvdata = self.ser.read(num)
                # print(rcvdata.hex())
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0x36) + 2
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail! 1')

        self.ser.close()
        time.sleep(0.05)
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_vco_ldo_voltage(self, powerSel=[VcoPowerDef]):
        ret = False
        evt_val = 0xFF
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        if self.ser.isOpen():
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 F4 FC 01')
        cmd = bytearray(5)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = powerSel
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0xFC) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_vco_vpp_voltage(self, VcoVppVal=[VcoVppDef]):
        Reg_addr = 0x40008814
        Reg_bit_shift = 5
        Reg_bit_set = VcoVppVal
        Reg_Mask = 0x7 << 5  # [7:5]
        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        # print('The reg val is: ' + Now_Reg.hex())
        print('0x{:08X}'.format(Reg_addr), '->', '0x{:08X}'.format(Now_Reg))

        Now_Reg &= ~(Reg_Mask)
        print('0x{:08X}'.format(Now_Reg))
        Now_Reg |= ((Reg_bit_set << Reg_bit_shift) & Reg_Mask)
        print('0x{:08X}'.format(Now_Reg))
        self.HCI_write_reg(self, reg_addr=Reg_addr, write_val=Now_Reg)
        Read_reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        print('0x{:08X}'.format(Read_reg))
        # print('The reg val is set: ' + str(bin(Read_reg)))

    # @retry(tries=2)
    def HCI_ldo_act_voltage(self, ldoAct=[LdoActDef]):
        ret = False
        evt_val = 0xFF
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        if self.ser.isOpen():
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 F5 FC 01')
        cmd = bytearray(5)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = ldoAct
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0xFC) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    # @retry(tries=3)
    def HCI_ldo_rf_voltage(self, ldoRf=[LdoRfDef]):
        ret = False
        evt_val = 0xFF
        if self.ser.isOpen() is False:
            time.sleep(0.1)
            self.ser = serial.Serial(self.port, self.bps, timeout=2)
            self.serIsOpen = True
        cmdorg = bytes.fromhex('01 F3 FC 01')
        cmd = bytearray(5)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = ldoRf
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0xFC) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    # @retry(tries=5)
    def HCI_tx_pa_acw_config(self, AcwVal, TxGainSel=[TxGainTabIdxDef]):
        ret = False
        evt_val = 0xFF
        if AcwVal > 255:
            AcwVal = 255
        if self.ser.isOpen() is False:
            self.ser = serial.Serial(self.port, self.bps, timeout=3)
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial still open!!")
        cmdorg = bytes.fromhex('01 F2 FC 02')
        cmd = bytearray(6)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = TxGainSel
        cmd[5] = AcwVal
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0xFC) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_tx_pa_h2_config(self, H2Val):  # H2Val range is 0~0x1e
        ret = False
        evt_val = 0xFF
        if H2Val > 15:
            AcwVal = 15
        if self.ser.isOpen() is False:
            self.ser = serial.Serial(self.port, self.bps, timeout=3)
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial still open!!")
        cmdorg = bytes.fromhex('01 F9 FC 01')
        cmd = bytearray(5)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = H2Val
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0xFC) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_otw_debug_modgain(self, OTW_VAL):
        ret = False
        evt_val = 0xFF
        if OTW_VAL > 255:
            OTW_VAL = 255
        # if self.ser.isOpen() is False:
        #     self.ser = serial.Serial(self.port, self.bps, timeout=2)
        #     print("serial open success")
        #     self.serIsOpen = True
        #     # print(ser.name)
        # else:
        #     print("serial still open!!")

        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        cmdorg = bytes.fromhex('01 FB FC 01')
        cmd = bytearray(5)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = OTW_VAL
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0xFC) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_rf_tx_test(self, channel, payloadtype=[PayloadTypeDef], test_mode=[RfTestModeDef]):
        # self.HCI_rf_reset(self=self)
        ret = False
        evt_val = 0xFF
        # print(channel)
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        if self.ser.isOpen():
            self.serIsOpen = True
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 34 20 04')
        cmd = bytearray(8)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = channel
        cmd[5] = 0x25
        cmd[6] = payloadtype
        if(test_mode == RfTestModeDef.LE1M):
            cmd[7] = 1
        elif(test_mode == RfTestModeDef.LE2M):
            cmd[7] = 2
        elif(test_mode == RfTestModeDef.LES8):
            cmd[7] = 3
        elif (test_mode == RfTestModeDef.LES2):
            cmd[7] = 4
        print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                print(rcvdata.hex())
                index = rcvdata.find(0x20) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')
        self.ser.close()
        time.sleep(0.05)
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_rf_tx_end(self):
        ret = False
        # print(channel)
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        if self.ser.isOpen():
            self.serIsOpen = True
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 1F 20 00')
        cmd = bytearray(4)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                print(rcvdata.hex())
                index = rcvdata.find(0x20) + 3
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        time.sleep(0.05)
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_rf_rx_test(self, channel, test_mode=[RfTestModeDef]):
        self.HCI_rf_reset(self=self)
        ret = False
        evt_val = 0xFF
        # print(channel)
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        if self.ser.isOpen():
            self.serIsOpen = True
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 33 20 02')
        cmd = bytearray(6)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = channel
        if(test_mode == RfTestModeDef.LE1M):
            cmd[5] = 1
        elif(test_mode == RfTestModeDef.LE2M):
            cmd[5] = 2
        elif(test_mode == RfTestModeDef.LES8):
            cmd[5] = 3
        elif (test_mode == RfTestModeDef.LES2):
            cmd[5] = 4
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                # print(rcvdata.hex())
                index = rcvdata.find(0x20) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        time.sleep(0.05)
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_rf_tx_end(self):
        ret = False
        evt_val = 0xFF
        # print(channel)
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        if self.ser.isOpen():
            self.serIsOpen = True
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 1F 20 00')
        cmd = bytearray(4)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                print(rcvdata.hex())
                index = rcvdata.find(0x20) + 3
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        time.sleep(0.05)
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    def HCI_rf_rx_end(self):
        ret = False
        # print(channel)
        self.ser = serial.Serial(self.port, self.bps, timeout=2)
        if self.ser.isOpen():
            self.serIsOpen = True
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 1F 20 00')
        cmd = bytearray(4)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        packnum = 0
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                # print(rcvdata.hex())
                index = rcvdata.find(0x20) + 1
                packnum = (rcvdata[rcvdata.find(0x20) + 2]
                           ) | rcvdata[(rcvdata.find(0x20) + 3)] << 8
                # packnum = ( 12 << 16 ) | rcvdata[(rcvdata.find(0x20) + 3)]
                print(packnum)
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        time.sleep(0.05)
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
            return packnum
        else:
            ret = False
            return ret

    def HCI_get_modgain_cail_val(self, freqMHz):
        modgain = 0x0
        freq_h = freqMHz >> 8
        freq_l = freqMHz & 0x00ff
        # print(freq_h)
        # print(freq_l)
        self.ser = serial.Serial(self.port, self.bps, timeout=0.1)
        if self.ser.isOpen():
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 FA FC 01')
        cmd = bytearray(6)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = freq_l
        cmd[5] = freq_h
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.02)
        try:
            num = self.ser.inWaiting()
            # print(num)
            if num > 0:
                rcvdata = self.ser.read(num)
                # print(rcvdata.hex())
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0xFC) + 1
                modgain = rcvdata[index]
                modgain |= (rcvdata[index + 1] << 8)
                modgain |= (rcvdata[index + 2] << 16)
                modgain |= (rcvdata[index + 3] << 32)
                # print(modgain)
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail! 1')

        self.ser.close()
        time.sleep(0.05)
        self.serIsOpen = False
        return modgain

    def HCI_set_dcxo_loadcap_val(self, loadCap):
        extval = 55
        loadCap_h = loadCap >> 8
        loadCap_l = loadCap & 0x00ff
        print(loadCap_h)
        print(loadCap_l)
        self.ser = serial.Serial(self.port, self.bps, timeout=0.05)
        if self.ser.isOpen():
            # print("serial open success")
            self.serIsOpen = True
            # print(ser.name)
        else:
            print("serial open fail")
        cmdorg = bytes.fromhex('01 FC FC 02')
        cmd = bytearray(6)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = loadCap_l
        cmd[5] = loadCap_h
        print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.02)
        try:
            num = self.ser.inWaiting()
            # print(num)
            if num > 0:
                rcvdata = self.ser.read(num)
                # print(rcvdata.hex())
                # out_s = ''
                # for i in range(0, len(rcvdata)):
                #     out_s = out_s + '{:02X}'.format(rcvdata[i]) + ' '
                # print(out_s)
                index = rcvdata.find(0xFC) + 1
                extval = rcvdata[index]
                # print(modgain)
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail! 1')

        self.ser.close()
        time.sleep(0.05)
        self.serIsOpen = False
        if extval == 0:
            return True
        else:
            return False

    def HCI_reg_acg_mode(self, AcgMode=[RegAcgModeDef]):
        Reg_addr = 0x40009010
        Reg_bit_shift = 0
        Reg_bit_set = AcgMode
        Reg_Mask = 0x7  # [7:5]
        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        # print('The reg val is: ' + Now_Reg.hex())
        print('0x{:08X}'.format(Reg_addr), '->', '0x{:08X}'.format(Now_Reg))

        Now_Reg &= ~(Reg_Mask)
        print('0x{:08X}'.format(Now_Reg))
        Now_Reg |= ((Reg_bit_set << Reg_bit_shift) & Reg_Mask)
        print('0x{:08X}'.format(Now_Reg))
        self.HCI_write_reg(self, reg_addr=Reg_addr, write_val=Now_Reg)
        Read_reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        print('0x{:08X}'.format(Read_reg))

    def HCI_rssi_read(self):
        Reg_addr = 0x4000a010
        Rssi_Mask = 0x3FFF  # [13:0]
        Acg_Mask = 0x3 << 14

        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        Rssi = Now_Reg & Rssi_Mask
        # print('0x{:08X}'.format(Reg_addr), '->', '0x{:08X}'.format(Rssi))
        Acg_Level = (Now_Reg & Acg_Mask) >> 14
        if(Acg_Level >= 4):
            Acg_Level = 0
        # print('0x{:08X}'.format(Acg_Level))
        result = [Rssi, Acg_Level]
        return result

    def HCI_rssi_read_dbm(self):
        Reg_addr = 0x4000a024
        Rssi_Mask = 0xFF  # [13:0]

        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        Rssi = Now_Reg & Rssi_Mask
        if (Rssi > 127):
            Rssi = ~Rssi & 0x7F
            Rssi = Rssi+0x1
            Rssi = -Rssi
        return Rssi

    def HCI_rssi_agc0_read(self):
        Reg_addr = 0x40009048
        Rssi_Mask = 0xFF  # [13:0]

        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        Rssi = Now_Reg & Rssi_Mask
        # if (Rssi>127):
        #     Rssi = ~Rssi&0x7F
        #     Rssi = Rssi+0x1
        #     Rssi = -Rssi
        return Rssi

    def HCI_rssi_agc1_read(self):
        Reg_addr = 0x4000904c
        Rssi_Mask = 0xFF  # [13:0]

        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        Rssi = Now_Reg & Rssi_Mask
        # if (Rssi>127):
        #     Rssi = ~Rssi&0x7F
        #     Rssi = Rssi+0x1
        #     Rssi = -Rssi
        return Rssi

    def HCI_rssi_agc2_read(self):
        Reg_addr = 0x40009050
        Rssi_Mask = 0xFF  # [13:0]

        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        Rssi = Now_Reg & Rssi_Mask
        # if (Rssi>127):
        #     Rssi = ~Rssi&0x7F
        #     Rssi = Rssi+0x1
        #     Rssi = -Rssi
        return Rssi

    def HCI_power_ant_sub_val_read(self):
        Reg_addr = 0x40009054
        Rssi_Mask = 0xFF  # [13:0]

        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        Rssi = Now_Reg & Rssi_Mask
        # if (Rssi>127):
        #     Rssi = ~Rssi&0x7F
        #     Rssi = Rssi+0x1
        #     Rssi = -Rssi
        return Rssi

    def HCI_power_ant_sub_val_read(self):
        Reg_addr = 0x40009054
        Rssi_Mask = 0xFF  # [13:0]

        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        Rssi = Now_Reg & Rssi_Mask
        # if (Rssi>127):
        #     Rssi = ~Rssi&0x7F
        #     Rssi = Rssi+0x1
        #     Rssi = -Rssi
        return Rssi

    def HCI_rssi_2_bit_read(self):
        Reg_addr = 0x4000902c
        Rssi_Mask = 0x1  # [13:0]

        Now_Reg = self.HCI_read_reg(self, reg_addr=Reg_addr)
        Rssi = Now_Reg & Rssi_Mask
        # if (Rssi>127):
        #     Rssi = ~Rssi&0x7F
        #     Rssi = Rssi+0x1
        #     Rssi = -Rssi
        return Rssi

    def HCI_dcdc_config(self, H2Val):  # H2Val range is 0~0x1e
        ret = False
        evt_val = 0xFF
        # if H2Val > 1:
        #     AcwVal = 1
        self.ser = serial.Serial(self.port, self.bps, timeout=3)
        cmdorg = bytes.fromhex('01 F6 FC 01')
        cmd = bytearray(5)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = H2Val
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                print(rcvdata.hex())
                index = rcvdata.find(0xFC) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret

    # H2Val range is 0~0x1e
    def HCI_pa_mode_config(self, Pa_mode=[TxPaModeDef]):
        ret = False
        evt_val = 0xFF
        self.ser = serial.Serial(self.port, self.bps, timeout=3)
        cmdorg = bytes.fromhex('01 F8 FC 01')
        cmd = bytearray(5)
        for i in range(0, 4):
            cmd[i] = cmdorg[i]
        cmd[4] = Pa_mode
        # print(cmd.hex())
        try:
            self.ser.write(cmd)
        except:
            print("serial sent fail!")
        # print("serial sent success")
        time.sleep(0.05)
        try:
            num = self.ser.inWaiting()
            if num > 0:
                rcvdata = self.ser.read(num)
                print(rcvdata.hex())
                index = rcvdata.find(0xFC) + 1
                evt_val = rcvdata[index]
            else:
                print('serial receive fail!')
        except:
            print('serial receive fail!')

        self.ser.close()
        self.serIsOpen = False
        if evt_val == 0x0:
            ret = True
        else:
            ret = False
        return ret


if __name__ == "__main__":
    print("hello world")
    MXD2670 = HCI_Serial
    # MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port='COM3', bps=115200, timeout=0.5)
    # print(MXD2670.HCI_vco_ldo_voltage(self=MXD2670, powerSel=VcoPowerDef.LDO_VCO_900mV))
    # MXD2670.HCI_reset(self=MXD2670)

    MXD2670.HCI_single_tone(self=MXD2670, freqMHz=2440,
                            powerSel=TxPowerDef.TX_10_DBM)
    MXD2670.HCI_set_dcxo_loadcap_val(self=MXD2670, loadCap=95)

    # MXD2670.HCI_otw_debug_modgain(self=MXD2670, OTW_VAL=0)

    # print(MXD2670.HCI_get_modgain_cail_val(self=MXD2670, freqMHz=2438))

    # for i in range(LdoActDef.LDO_ACT_1300mV, LdoActDef.LDO_ACT_950mV + 1):
    #     print(i)
    #     print(MXD2670.HCI_ldo_act_voltage(self=MXD2670, ldoAct=i))
    #     time.sleep(1)

    # for i in range(0, 255):
    #     print(MXD2670.HCI_tx_pa_acw_config(self=MXD2670, AcwVal=i, TxGainSel=TxGainTabIdxDef.TX_GAIN_5))

    # ok_count = 0
    # ng_count = 0
    # while 1:
    #     ser = serial.Serial("COM3", 115200, timeout=2)
    #     if ser.isOpen():
    #         # print("serial open success")
    #         # print(ser.name)
    #         print('')
    #     else:
    #         print("serial open fail")
    #     cmdorg = bytes.fromhex('01 C2 FC 04 00 80 00 40')
    #     cmd = bytearray(8)
    #     for i in range(0, 8):
    #         cmd[i] = cmdorg[i]
    #
    #     try:
    #         ser.write(cmd)
    #         print("<- " + cmd.hex())
    #     except:
    #         print("serial sent fail!")
    #     # print("serial sent success")
    #
    #     time.sleep(0.01)
    #
    #     try:
    #         num = ser.inWaiting()
    #         if num > 0:
    #             data = ser.read(num)
    #             print("-> " + data.hex())
    #         if num != 12:
    #             print('serial receive count fail!', num)
    #             ng_count += 1
    #     except:
    #         ser.close()
    #         ser = None
    #         print('serial receive fail!')
    #
    #     ser.close()
    #
    #     ok_count += 1
    #     print("[ok count]", ok_count)
    #     print("[ng count]", ng_count)
