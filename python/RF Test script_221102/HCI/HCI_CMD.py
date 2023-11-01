import HCI_For_Serial

reg_val = 0x0
RegAddr = 0x40008000
if __name__ == "__main__":
    MXD2670 = HCI_For_Serial.HCI_Serial
    # MXD2670.refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port='COM3', bps=115200, timeout=2)
    print(MXD2670.HCI_ldo_rf_voltage(self=MXD2670, ldoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV))


    # reg read demo
    # for i in range(0x40008000, 0x400087FF+4, 4):
    #     reg_val = MXD2670.HCI_read_reg(self=MXD2670, reg_addr=i)
    #     print('0x{:08X}'.format(i), '->', '0x{:08X}'.format(reg_val))

    # reg write demo
    # reg_val = MXD2670.HCI_read_reg(self=MXD2670, reg_addr=RegAddr)
    # print('0x{:08X}'.format(RegAddr), '->', '0x{:08X}'.format(reg_val))
    # reg_val += 5
    # print('write val:0x{:08X}'.format(reg_val))
    # write_state = MXD2670.HCI_write_reg(self=MXD2670, reg_addr=RegAddr, write_val=reg_val)
    # print('write state:', write_state)
    # reg_val = MXD2670.HCI_read_reg(self=MXD2670, reg_addr=RegAddr)
    # print('0x{:08X}'.format(RegAddr), '->', '0x{:08X}'.format(reg_val))

    # hci reset demo
    # print(MXD2670.HCI_reset(self=MXD2670))
    # MXD2670.HCI_single_tone(self=MXD2670, freqMHz=2400, powerSel=1)

    # hci single tone frequency demo
    # for i in range(2100, 2900, 1):
    #     MXD2670.HCI_single_tone(self=MXD2670, freqMHz=i, powerSel=4)

    # print(MXD2670.HCI_single_tone(self=MXD2670, freqMHz=2440, powerSel=4))

    while 1:
        MXD2670.HCI_single_tone(self=MXD2670, freqMHz=2440, powerSel=4)
        MXD2670.HCI_single_tone(self=MXD2670, freqMHz=2441, powerSel=4)
        MXD2670.HCI_single_tone(self=MXD2670, freqMHz=2440, powerSel=4)
        MXD2670.HCI_single_tone(self=MXD2670, freqMHz=2439, powerSel=4)





