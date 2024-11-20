#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 10:23:40 2022

@author: ritikakhot
"""

#Hall Effect lab Thermocouple Voltage against heater temperature
#log(n) vs 1/T plot
import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('i_will_scream.csv',delimiter=',',skip_header=1)

#~~~~~~~~~~~~~~~~~~~~Plotting Information~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig = plt.figure(figsize=(11,7))
ax = fig.add_subplot(111)


y = data[:,0]
y_errs = data[:,1]
x=data[:,2]
x_errs = data[:,3]
#NOTE TO USER: ADJUST LABELS TO REQUIREMENTS

initial_fit_poly= np.polyfit( x, y, 1)
mc_tuple = initial_fit_poly
m = mc_tuple[0]
c = mc_tuple[1]
m_round = round(mc_tuple[0],4)
c_round = round(mc_tuple[1],4)
print(m)
x_polyfit = np.linspace(0.0025,0.007,100000)
y_expected = np.polyval(initial_fit_poly, x_polyfit)

plt.xlabel('1/T /$K^{-1}$')
plt.ylabel('log(n$T^{-3/2}$)')
plt.title('Log(n$T^{-3/2}$) against 1/T')

#plt.xlim(xmin=0.0002,xmax=0.007)
#plt.ylim(ymin=48,ymax=60)

gradient_error = abs(m*np.sqrt((y_errs/y)**2 + (x_errs/x)**2))
print(gradient_error)


# Summing the individual uncertainties on gradient
sum=0
for i in range(0,len(gradient_error)):
    sum = sum + 1/(gradient_error[i])**2
print(sum)

gradient_uncert_final = np.sqrt(1/sum)
print(m,'+/-', gradient_uncert_final)

strline_label = 'log(n$T^{-3/2}$)= ' + str(m_round) +' $1/T$ + ' + str(c_round)
ax.errorbar(x, y, xerr=x_errs, yerr=y_errs, fmt='o')
#ax.margins(0.05)
ax.scatter(x,y,linestyle='None',color='blue',label="Raw data")
ax.plot(x_polyfit,y_expected,linestyle ='solid',color ='orange',label=strline_label)
ax.legend()

plt.savefig('log(nT^1.5)_line_zoom_5_final.png',dpi=300)
plt.show()