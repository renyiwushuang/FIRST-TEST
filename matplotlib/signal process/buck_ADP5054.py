# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:25:39 2023

@author: E002012
"""
import numpy as np
import matplotlib.pyplot as plt
############ condition ##################
Vin = 12 #input voltage unit:V
Vout = 3.9 #output voltage unit:V
Vref = 0.8 #reference voltage unit:V
Fsw = 6e5 # switch frequency unit:Hz
I_load = 2# load current unit:A
Delta_I = 0.3*I_load # ripple current unit:A
D = Vout / Vin # duty cycle
K_uv = 2 
K_ov = 2 
Delta_V_uv = 0.05*Vout
Delta_V_ov = 0.05*Vout
V_ripple = 1e-2
I_step = 2
########### inductor results ################
L = ((Vin - Vout) * D) / (Delta_I * Fsw) # inductor value unit:uH
I_peak = I_load + (Delta_I / 2) # peak current unit:A
I_rms = np.sqrt(I_load**2 + (Delta_I**2 / 12)) # rms current unit:A
print('\033[1;31m select inductor parameter \033[0m')
print('\033[1;35m L = \033[0m', L, '\033[1;35mI_peak = \033[0m', I_peak, '\033[1;35mI_rms = \033[0m', I_rms)

########### capacitor results #############
C_uv = (K_uv*I_step**2*L) / (2*(Vin - Vout)*Delta_V_uv)
C_ov = (K_ov*I_step**2*L) / ((Vout + Delta_V_ov)**2 - Vout**2)
C_ripple = Delta_I / (8 * Fsw * V_ripple)
R_esr = V_ripple / Delta_I
I_cout_rms = Delta_I / np.sqrt(12)
I_cin_rms = I_load * np.sqrt(D * (1-D))
print('\033[1;31m select capacitor parameter \033[0m')
print('\033[1;34m C_uv = \033[0m', C_uv, '\033[1;34m C_ov = \033[0m', C_ov, '\033[1;34m C_ripple = \033[0m', C_ripple, '\033[1;34m R_esr = \033[0m', R_esr, '\033[1;34m I_cout_rms = \033[0m', I_cout_rms, '\033[1;34m I_cin_rms = \033[0m', I_cin_rms)

########### FB resistor for output voltage ###########
R_bot = 2.32e4
R_top = (Vout - Vref) * R_bot / Vref
R_rt = ((14822 / (Fsw / 1e3))**1.081) * 1e3
print('\033[1;31m resistor choose \033[0m')
print('\033[1;36m R_bot = \033[0m', R_bot, '\033[1;36m R_top = \033[0m', R_top, '\033[1;36m R_rt = \033[0m', R_rt)

######## COMPENSATION NETWORK ###########
f_cross = Fsw/10
A_vi = 20# CH1&2 = 20  CH3&4 =6.66
gm = 4.7e-4
R_c_esr = 1e-3
R_load = Vout / I_load
C_out = 6.6e-5#max(C_ov, C_ripple, C_uv)
R_c = (2 * np.pi * Vout * C_out * f_cross) / (gm * 0.8 * A_vi)
C_c = (R_load + R_c_esr) * C_out / R_c

C_cp = 0 * R_c_esr * C_out / R_c

print('\033[1;31m resistor choose \033[0m')
print('\033[1;32m R_c = \033[0m', R_c, '\033[1;32m C_c = \033[0m', C_c, '\033[1;32m C_cp = \033[0m', C_cp)


################# H(s) bode figure ##############
freq = np.arange(1e3, 1e7, 1e3)
s = 2j * np.pi * freq
G_vd = A_vi * R_load * (1 + R_c_esr * C_out * s) / (1 + (R_c_esr + R_load) * C_out * s)
H_s =G_vd * (R_bot / (R_bot + R_top)) * (-gm / (C_c + C_cp)) * ((1 + R_c * C_c * s) / (s * (1 + s * R_c * C_c * C_cp / (C_c + C_cp)))) 
mag_dB = 20 * np.log10(np.abs(H_s))
phase_deg = np.angle(H_s, deg=True)

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.semilogx(freq, mag_dB)
ax1.set_title('Bode Plot - Magnitude')
ax1.set_ylabel('Magnitude(dB)')
ax1.set_xlabel('Frequency(Hz)')


ax2.semilogx(freq, phase_deg)
ax2.set_title('Bode Plot - Phase')
ax2.set_ylabel('Phase(deg)')
ax2.set_xlabel('Frequency(Hz)')

plt.show()