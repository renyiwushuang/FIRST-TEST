# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:55:07 2024

@author: E002012
"""

import pandas as pd
import matplotlib.pyplot as plt



post_file = 'F:\python code\FIRST-TEST\python\MXD\MXD2710EN34CDA_HTOL20240806\summary.xlsx'


# processing post data
post_data = pd.ExcelFile(post_file)
post_data_PMU = pd.read_excel(post_file, sheet_name=post_data.sheet_names.index('007_PMU_RF_MEASURING'))
post_data_TX = pd.read_excel(post_file, sheet_name=post_data.sheet_names.index('018_RF_TX'))
post_data_RX = pd.read_excel(post_file, sheet_name=post_data.sheet_names.index('019_RF_RX'))






plt.close('all')
# PMU
# draw 3R
fig_3R, ax_3R = plt.subplots()
ax_3R.plot(post_data_PMU['ID'], post_data_PMU['3R'], 'r', label='post', marker='o')
ax_3R.set_title('PMU 3R Current')
# plt.legend()
plt.savefig('20240806_PMU_3R_CURRENT', dpi=300)
# draw START
fig_start, ax_start = plt.subplots()
ax_start.plot(post_data_PMU['ID'], post_data_PMU['启动'], 'r', label='post', marker='o')
ax_start.set_title('PMU Start Current')
# plt.legend()
plt.savefig('20240806_PMU_Start_Current', dpi=300)

# draw TX TONE
fig_TX, ax_TX = plt.subplots()
ax_TX.plot(post_data_PMU['ID'], post_data_PMU['TX单音'], 'r', label='post', marker='o')
ax_TX.set_title('PMU TX Current')
# plt.legend()
plt.savefig('20240806_PMU_TX_Current', dpi=300)
# draw UWB CLK
fig_UWB, ax_UWB = plt.subplots()
ax_UWB.plot(post_data_PMU['ID'], post_data_PMU['UWB_CLK'], 'r', label='post', marker='o')
ax_UWB.set_title('PMU UWB_CLK Current')
plt.legend()
plt.savefig('20240806_PMU_UWB_Current', dpi=300)


# TX
# draw TX POWER
fig_TXpower, ax_TXpower = plt.subplots()
ax_TXpower.plot(post_data_TX['board_id'], post_data_TX['Data_Power'], 'r', label='post', marker='o')
ax_TXpower.set_title('RF_TX_POWER')
plt.legend()
plt.savefig('20240806_RFTX_POWER', dpi=300)

# RX
# draw TX POWER
fig_PER, ax_PER = plt.subplots()
ax_PER.plot(post_data_RX['board id'], post_data_RX['rx sensitivity'], 'r', label='post', marker='o')
ax_PER.set_title('RF_RX_PER')
plt.legend()
plt.savefig('20240806_RFRX_PER', dpi=300)