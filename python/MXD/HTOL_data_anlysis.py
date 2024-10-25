# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:55:07 2024

@author: E002012
"""

import pandas as pd
import matplotlib.pyplot as plt


pre_file = 'F:\python code\FIRST-TEST\python\MXD\HTOL20240527\summary.xlsx'
post_file = 'F:\python code\FIRST-TEST\python\MXD\HTOL0723\summary.xlsx'


# processing post data
post_data = pd.ExcelFile(post_file)
post_data_PMU = pd.read_excel(post_file, sheet_name=post_data.sheet_names.index('007_PMU_RF_MEASURING'))
post_data_TX = pd.read_excel(post_file, sheet_name=post_data.sheet_names.index('018_RF_TX'))
post_data_RX = pd.read_excel(post_file, sheet_name=post_data.sheet_names.index('019_RF_RX'))


# processing pre data
pre_data = pd.ExcelFile(pre_file)
pre_data_PMU = pd.read_excel(pre_file, sheet_name=pre_data.sheet_names.index('007_PMU_RF_MEASURING'))
pre_data_PMU = pre_data_PMU[pre_data_PMU['ID'].isin(post_data_PMU['ID'].tolist())]
pre_data_TX = pd.read_excel(pre_file, sheet_name='018_RF_TX')
pre_data_TX = pre_data_TX[pre_data_TX['board_id'].isin(post_data_PMU['ID'].tolist())]
pre_data_RX = pd.read_excel(pre_file, sheet_name='019_RF_RX')
pre_data_RX = pre_data_RX[pre_data_RX['board id'].isin(post_data_PMU['ID'].tolist())]

# merge data
merge_data_PMU = pd.merge(post_data_PMU, pre_data_PMU, on='ID')
merge_data_TX = pd.merge(post_data_TX, pre_data_TX, left_on='board_id' ,right_on='board_id')
merge_data_RX = pd.merge(post_data_RX, pre_data_RX, left_on='board id' ,right_on='board id')
merge_data_RX = merge_data_RX[merge_data_RX['rx sensitivity_y']!='FAIL']

plt.close('all')
# PMU
# draw 3R
fig_3R, ax_3R = plt.subplots()
ax_3R.plot(merge_data_PMU['ID'], merge_data_PMU['3R_x'], 'r', label='post', marker='o')
ax_3R.plot(merge_data_PMU['ID'], merge_data_PMU['3R_y'], 'b', label='pre', marker='o')
ax_3R.set_title('PMU 3R Current')
# plt.legend()
plt.savefig('MAY-JLUY_PMU_3R_CURRENT', dpi=300)
# draw START
fig_start, ax_start = plt.subplots()
ax_start.plot(merge_data_PMU['ID'], merge_data_PMU['启动_x'], 'r', label='post', marker='o')
ax_start.plot(merge_data_PMU['ID'], merge_data_PMU['启动_y'], 'b', label='pre', marker='o')
ax_start.set_title('PMU Start Current')
# plt.legend()
plt.savefig('MAY-JLUY_PMU_Start_Current', dpi=300)

# draw TX TONE
fig_TX, ax_TX = plt.subplots()
ax_TX.plot(merge_data_PMU['ID'], merge_data_PMU['TX单音_x'], 'r', label='post', marker='o')
ax_TX.plot(merge_data_PMU['ID'], merge_data_PMU['TX单音_y'], 'b', label='pre', marker='o')
ax_TX.set_title('PMU TX Current')
# plt.legend()
plt.savefig('MAY-JLUY_PMU_TX_Current', dpi=300)
# draw UWB CLK
fig_UWB, ax_UWB = plt.subplots()
ax_UWB.plot(merge_data_PMU['ID'], merge_data_PMU['UWB_CLK_x'], 'r', label='post', marker='o')
ax_UWB.plot(merge_data_PMU['ID'], merge_data_PMU['UWB_CLK_y'], 'b', label='pre', marker='o')
ax_UWB.set_title('PMU UWB_CLK Current')
plt.legend()
plt.savefig('MAY-JLUY_PMU_UWB_Current', dpi=300)


# TX
# draw TX POWER
fig_TXpower, ax_TXpower = plt.subplots()
ax_TXpower.plot(merge_data_TX['board_id'], merge_data_TX['Data_Power_x'], 'r', label='post', marker='o')
ax_TXpower.plot(merge_data_TX['board_id'], merge_data_TX['Data_Power_y'], 'b', label='pre', marker='o')
ax_TXpower.set_title('RF_TX_POWER')
plt.legend()
plt.savefig('MAY-JLUY_RFTX_POWER', dpi=300)

# RX
# draw TX POWER
fig_PER, ax_PER = plt.subplots()
ax_PER.plot(merge_data_RX['board id'], merge_data_RX['rx sensitivity_x'], 'r', label='post', marker='o')
ax_PER.plot(merge_data_RX['board id'], merge_data_RX['rx sensitivity_y'], 'b', label='pre', marker='o')
ax_PER.set_title('RF_RX_PER')
plt.legend()
plt.savefig('MAY-JLUY_RFRX_PER', dpi=300)