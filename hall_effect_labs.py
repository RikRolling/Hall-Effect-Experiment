# Third year lab - Hall Effect in Indium Antimonide
# Author: Ritika Khot, October 2022

# 2D plot of experimental data, with line of best fit on same plot
#Need to add error bars to plot when possible!!!

import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit


#Reading in data file
data = np.genfromtxt('96K_B0.5_COMP.txt', delimiter=',', skip_header=1)

#Separting data file into required variables


def straight_line_model(X,m,c):


    return m*X + c

def gradient_cubic(a,b,c,x):

    return 3*a*x**2 + 2*b*x + c


#Combining x and y data
def array_combined(array_1, array_2):
    """
    Parameters
    ----------
    array_1 : array of floats
        Data from FILE_NUMBER_1.
    array_2 : array of floats
        Data from FILE_NUMBER_2.

    Returns
    -------
    combined_array : array of floats
        Combined data from FILE_NUMBER_1 and FILE_NUMBER_2.
    """

    combined_array = np.vstack((array_1, array_2))

    return combined_array


#Removing Outliers from data

def removing_outliers(xy_values):
    """
    Parameters
    ----------
    combined_data : array


    Returns
    -------
    array

    combined_data

        Data outside of +/- 3*sigma level are removed

    """

    mean = np.mean(xy_values[:, 1])
    sigma = np.std(xy_values[:, 1])
    xy_values = xy_values[(xy_values[:, 1] > mean - 3*sigma)*\
                                  (xy_values[:, 1] < mean+3*sigma)]

    return xy_values


#NOTE TO USER: PLACEMENT OF DATA MAY DIFFER FROM FILE TO FILE
# NOTE TO USER: FOR COMPUTER DATA USE X_ERROR_COMP
#I_data = np.array(data[:,5])
I_comp = np.array(data[:,2])
#I_error = np.array(data[:,7])
I_error_comp = [0.000005]*7

#B_data = np.array(data[:,12])
B_comp = np.array(data[:,8])
#B_error = np.array(data[:,13])
B_error_comp = [0.000005]*7

#V_sample_data = data[:,9]
V_comp = data[:,3]
#V_error = data[:,11]
V_error_comp = [0.00005]*7

#V_hall_data = data[:,1]
V_hall_comp = data[:,1]
#V_hall_error = data[:,3]
V_hall_error_comp = [0.00005]*7

#IxB_data = I_data*B_data
IxB_data_comp = I_comp*B_comp
#IxB_error = abs((IxB_data)*np.sqrt((I_error/I_data)**2 + (B_error/B_data)**2))
IxB_error_comp = abs(IxB_data_comp)*np.sqrt((I_error_comp/I_comp)**2 + (B_error_comp/B_comp)**2)

heater_temp_comp = data[:,5]
temp_sum=0
for i in range(0,len(heater_temp_comp)):
    temp_sum = temp_sum + heater_temp_comp[i]

average_temp = temp_sum/len(heater_temp_comp)
print("Average Heater Temperature = ", average_temp,"+/- 0.0000005")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Curve Fit~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#NOTE TO USER: CHANGE X AND Y FOR "initial_fit" TO REQUIREMENTS
#initial_fit = curve_fit(straight_line_model,IxB_data_comp,V_hall_comp,p0=[1,-0.1],maxfev=2000000000)
initial_fit_poly, cov = np.polyfit( I_comp, V_comp, 1, cov=True)
#initial_fit_new = np.polynomial.polynomial.Polynomial.fit(I_comp,V_comp,1)
#print(initial_fit_new)

#FOR STRAIGHT LINE FIT
mc_tuple = initial_fit_poly
m = mc_tuple[0]
c = mc_tuple[1]
print(np.sqrt(np.diag(cov)))
#FOR CUBIC FIT
#a = mc_tuple[0]
#b = mc_tuple[1]
#c_cubic = mc_tuple[2]
#d = mc_tuple[3]
#Rounding m and c to 2dp - easier to read on graph
m_round = round(mc_tuple[0],4)
c_round = round(mc_tuple[1],4)
#a_round = round(mc_tuple[0],2)
#b_round = round(mc_tuple[1],2)
#c_cubic_round = round(mc_tuple[2],2)
#d_round = round(mc_tuple[3],2)
#~~~~~~~~~~~~~~~~~Gradient Uncertainty~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gradient_error_comp = abs(m*np.sqrt((V_error_comp/V_comp)**2 + (I_error_comp/I_comp)**2))
#gradient_error_man = abs(m*np.sqrt((V_hall_error/V_hall_data)**2 + (IxB_error/IxB_data)**2))

# Summing the individual uncertainties on gradient
sum=0
for i in range(0,len(gradient_error_comp)):
    sum = sum + 1/(gradient_error_comp[i])**2
print(sum)

average_gradient_errors = np.sqrt(1/sum)
print("error on gradient = ", average_gradient_errors)
#~~~~~~~~~~~~~~~Data inputs for plot~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#NOTE TO USER: CHANGE X_DATA AND Y_DATA BASED ON REQUIREMENTS
x_data = I_comp
y_data = V_comp

x = np.linspace(-0.065,0.09,100000)
y_expected = np.polyval(initial_fit_poly, x)

#~~~~~~~~~~~~~~~~~Getting "Full Accuracy" of LOBF~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#actual_equation_str = 'Y =' + str(m) +'X + ' + str(c)

#print(actual_equation_str)

#~~~~~~~~~~~~~~~~~~~~Removed Outliers data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#combined_data = array_combined(x_data, y_data)
#new_array = removing_outliers(combined_data)

#X_DATA = new_array[:, 0]
#Y_DATA = new_array[:, 1]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~Finding Gradient for each point on cubic~~~~~~~~~~~~~~
#gradient = []

#for i in x_data:

    #gradient = np.append(gradient, gradient_cubic(a,b,c_cubic,i))

#print("Left column: x_data, Right column: Gradient of tangent")
#x_gradient_array = np.vstack([x_data,gradient])
#print(np.vstack([x_data,gradient]))

#gradient_errors = gradient*IxB_error_comp*




#~~~~~~~~~~~~~~~~~~~~Plotting Information~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig = plt.figure(figsize=(9,7))
ax = fig.add_subplot(111)
#NOTE TO USER: ADJUST LABELS TO REQUIREMENTS

#curvefit_label = '$V_S$= ' + str(a_round) +' $I^3$ + ' + str(b_round) + ' $I^2$ +' + str(c_cubic_round) + ' $I$ + ' + str(d_round)
strline_label = '$V_S$= ' + str(m_round) +' $I$ + ' + str(c_round)
plt.xlabel('I/A')
plt.ylabel('$V_S$/V')
plt.title('Sample Voltage against Current for B=0.5T and T=96K')

#NOTE TO USER: "plt.xlim" RESTRICTS WHICH DATA POINTS ARE PLOTTED
#plt.xlim(xmin=-1,xmax=1)
#plt.ylim(ymin=-2,ymax=1.5)

ax.errorbar(x_data, y_data, xerr=IxB_error_comp, yerr=V_hall_error_comp, fmt='o')
#NOTE TO USER: "ax.plot" = CURVEFIT, "ax.scatter" = DATA FROM FILE

ax.scatter(x_data,y_data,linestyle='None',color='blue',label='Raw data')
ax.plot(x,y_expected,linestyle ='solid',color ='orange',label=strline_label)
ax.legend()

plt.savefig('96K_B0.5_COMP_IV.png',dpi=300)
plt.show()


