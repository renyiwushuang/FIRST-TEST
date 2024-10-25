# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 17:00:04 2024

@author: E002012
"""

import pandas as pd
import matplotlib.pyplot as plt

FT_rawfile = 'F:\python code\FIRST-TEST\python\MXD\FT20241023\[20241017]MXD2710EN45CDS_V2FT.xls'
raw_data = pd.ExcelFile(FT_rawfile)
raw_data_STDF = pd.read_excel(raw_data, sheet_name=raw_data.sheet_names.index('_00_STDF01'))
raw_data_STDF_PASS = raw_data_STDF[raw_data_STDF['Unnamed: 1']=='1:Pass']

## Yield 
pass_rate = raw_data_STDF_PASS.shape[0]/raw_data_STDF.shape[0]
print('Yield=', pass_rate)


plt.close('all')
## good product parameter distribution

### LDO_VACT_1V3
data_LDO_VACT_1V3 = raw_data_STDF['6002:V_LDO ACT_1V3'][4:].dropna()

fig, ax_LDO_VACT_1V3 = plt.subplots(1, 2)
ax_LDO_VACT_1V3[0].plot(data_LDO_VACT_1V3, 'r', label='V_LDO ACT_1V3', marker='o')
ax_LDO_VACT_1V3[0].grid()
ax_LDO_VACT_1V3[0].set_title('V_LDO ACT_1V3 line chart')

ax_LDO_VACT_1V3[1].hist(data_LDO_VACT_1V3, bins=20)
ax_LDO_VACT_1V3[1].grid()
ax_LDO_VACT_1V3[1].set_title('V_LDO ACT_1V3 histograms')

### RC32K 
data_RC32K = raw_data_STDF['8009:Clock_Result_32k'][4:].dropna()

fig, ax_RC32K = plt.subplots(1, 2)
ax_RC32K[0].plot(data_RC32K, 'r', label='RC32K', marker='o')
ax_RC32K[0].grid()
ax_RC32K[0].set_title('RC32K line chart')

ax_RC32K[1].hist(data_RC32K, bins=20)
ax_RC32K[1].grid()
ax_RC32K[1].set_title('RC32K histograms')

### RC16M
data_RC16M = raw_data_STDF['8013:Clock_Result_16M'][4:].dropna()

fig, ax_RC16M = plt.subplots(1, 2)
ax_RC16M[0].plot(data_RC16M, 'r', label='RC16M', marker='o')
ax_RC16M[0].grid()
ax_RC16M[0].set_title('RC16M line chart')

ax_RC16M[1].hist(data_RC16M, bins=20)
ax_RC16M[1].grid()
ax_RC16M[1].set_title('RC16M histograms')

### I_VDDR_RST
data_I_VDDR_RST = raw_data_STDF['4007:I_VDDR_RST'][4:].dropna()

fig, ax_I_VDDR_RST = plt.subplots(1, 2)
ax_I_VDDR_RST[0].plot(data_I_VDDR_RST, 'r', label='I_VDDR_RST', marker='o')
ax_I_VDDR_RST[0].grid()
ax_I_VDDR_RST[0].set_title('I_VDDR_RST line chart')

ax_I_VDDR_RST[1].hist(data_I_VDDR_RST, bins=20)
ax_I_VDDR_RST[1].grid()
ax_I_VDDR_RST[1].set_title('I_VDDR_RST histograms')

### I_VIO_RST
data_I_VIO_RST = raw_data_STDF['4008:I_VIO_RST'][4:].dropna()

fig, ax_I_VIO_RST = plt.subplots(1, 2)
ax_I_VIO_RST[0].plot(data_I_VIO_RST, 'r', label='I_VIO_RST', marker='o')
ax_I_VIO_RST[0].grid()
ax_I_VIO_RST[0].set_title('I_VIO_RST line chart')

ax_I_VIO_RST[1].hist(data_I_VIO_RST, bins=20)
ax_I_VIO_RST[1].grid()
ax_I_VIO_RST[1].set_title('I_VIO_RST histograms')

### I_VDDR_WORK
data_I_VDDR_WORK = raw_data_STDF['4009:I_VDDR_WORK'][4:].dropna()

fig, ax_I_VDDR_WORK = plt.subplots(1, 2)
ax_I_VDDR_WORK[0].plot(data_I_VDDR_WORK, 'r', label='I_VDDR_WORK', marker='o')
ax_I_VDDR_WORK[0].grid()
ax_I_VDDR_WORK[0].set_title('I_VDDR_WORK line chart')

ax_I_VDDR_WORK[1].hist(data_I_VDDR_WORK, bins=20)
ax_I_VDDR_WORK[1].grid()
ax_I_VDDR_WORK[1].set_title('I_VDDR_WORK histograms')

### I_TX_-18dBm
data_I_TX_n18dBm = raw_data_STDF['16013:I_TX_-18dBm'][4:].dropna()

fig, ax_I_TX_n18dBm = plt.subplots(1, 2)
ax_I_TX_n18dBm[0].plot(data_I_TX_n18dBm, 'r', label='I_TX_-18dBm', marker='o')
ax_I_TX_n18dBm[0].grid()
ax_I_TX_n18dBm[0].set_title('I_TX_-18dBm line chart')

ax_I_TX_n18dBm[1].hist(data_I_TX_n18dBm, bins=20)
ax_I_TX_n18dBm[1].grid()
ax_I_TX_n18dBm[1].set_title('I_TX_-18dBm histograms')

### I_TX_5dBm
data_I_TX_5dBm = raw_data_STDF['16014:I_TX_5dBm'][4:].dropna()

fig, ax_I_TX_5dBm = plt.subplots(1, 2)
ax_I_TX_5dBm[0].plot(data_I_TX_5dBm, 'r', label='I_TX_5dBm', marker='o')
ax_I_TX_5dBm[0].grid()
ax_I_TX_5dBm[0].set_title('I_TX_5dBm line chart')

ax_I_TX_5dBm[1].hist(data_I_TX_5dBm, bins=20)
ax_I_TX_5dBm[1].grid()
ax_I_TX_5dBm[1].set_title('I_TX_5dBm histograms')

### VDDRCL_LIMIT30
data_VDDRCL_LIMIT30 = raw_data_STDF['18005:VDDRCL_LIMIT30'][4:].dropna()

fig, ax_VDDRCL_LIMIT30 = plt.subplots(1, 2)
ax_VDDRCL_LIMIT30[0].plot(data_VDDRCL_LIMIT30, 'r', label='VDDRCL_LIMIT30', marker='o')
ax_VDDRCL_LIMIT30[0].grid()
ax_VDDRCL_LIMIT30[0].set_title('VDDRCL_LIMIT30 line chart')

ax_VDDRCL_LIMIT30[1].hist(data_VDDRCL_LIMIT30, bins=20)
ax_VDDRCL_LIMIT30[1].grid()
ax_VDDRCL_LIMIT30[1].set_title('VDDRCL_LIMIT30 histograms')

