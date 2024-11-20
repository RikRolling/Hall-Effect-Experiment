#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:06:46 2022

@author: ritikakhot
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



#Hall Effect Callibration Voltage against Temperature for Temperature monitor

data = np.genfromtxt('Voltage_temp_callaboration.csv', delimiter=',', skip_header=1)
V_data = data[:, 0]
T_data = data[:, 1]

fig = plt.figure(figsize=(9,7))

ax = fig.add_subplot(111)
ax.scatter(V_data,T_data,linestyle='None',color='blue',label='Raw data')