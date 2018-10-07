# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:09:13 2018

@author: Vall
"""

import fwp_format as fmt
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
       
#%%

def mean(X, dX=None):
    """Returns average or weighted average and standard deviation.
    
    If dX is given, it returns weighted average (weight=1/dX**2) of 
    data. If not, it returns common average.

    Parameters
    ----------
    X : list, np.array
        Data.
    dX=None : list, np.array
        Data's error.
    
    Returns
    -------
    (mean, std): tuple
        This tuple contains data's mean and standard deviation. If dX is 
        given, it returns weighted values (weight=1/dX**2).
    
    Raises
    ------
    "The X data is not np.array-like" : TypeError
        If X can't be easily converted to numpy array.
    "The dX data is not np.array-like" : TypeError
        If dX can't be easily converted to numpy array.
    "The dX array's length should match X's" : IndexError
        If dX's length doesn't match X's.
    
    """
    
    
    if not isinstance(X, np.ndarray):
        try:
            X = np.array(X)
        except:
            raise TypeError("The X data is not np.array like")

    if dX is not None:
        if not isinstance(dX, np.ndarray):
            try:
                dX = np.array(dX)
            except:
                raise TypeError("The dX data is not np.array like")
        if len(dX) != len(X):
            raise IndexError("The dX array's length should match X's")

        mean = np.average(X, weights=1/dX**2)
        variance = np.average((X-mean)**2, weights=1/dX**2)
        return (mean, sqrt(variance))
    
    else:
        return (np.mean(X), np.std(X))

#%%

def linear_fit(X, Y, dY=None, showplot=True,
               plot_some_errors=(False, 20), **kwargs):
    """Applies linear fit and returns m, b and Rsq. Can also plot it.
    
    By default, it applies minimum-square linear fit. If dY is 
    specified, it applies weighted minimum-square linear fit.
    
    Parameters
    ----------
    X : np.array, list
        Independent X data to fit.
    Y : np-array, list
        Dependent Y data to fit.
    dY : np-array, list
        Dependent Y data's associated error.
    shoplot : bool
        Says whether to plot or not.
    plot_some_errors : tuple (bool, int)
        Says wehther to plot only some error bars (bool) and specifies 
        the number of error bars to plot.
    
    Returns
    -------
    (m, dm) : tuple (float, float)
        Linear fit's slope: value and associated error.
    (b, db) : tuple (float, float)
        Linear fit's intercept: value and associated error.
    rsq : float
        Linear fit's R Square Coefficient.
    
    Other Parameters
    ----------------
    txt_position : tuple (horizontal, vertical), optional
        Indicates the parameters' text position. Each of its values 
        should be a number (distance in points measured on figure). 
        But vertical value can also be 'up' or 'down'.
    mb_units : tuple (m_units, b_units), optional
        Indicates the parameter's units. Each of its values should be a 
        string.
    mb_error_digits : tuple (m_error_digits, b_error_digits), optional
        Indicates the number of digits to print in the parameters' 
        associated error. Default is 3 for slope 'm' and 2 for intercept 
        'b'.
    mb_string_scale : tuple (m_string_scale, b_string_scale), optional
        Indicates whether to apply string prefix's scale to printed 
        parameters. Each of its values should be a bool; i.e.: 'True' 
        means 'm=1230.03 V' with 'dm = 10.32 V' would be printed as 
        'm = (1.230 + 0.010) V'. Default is '(False, False)'.
    rsq_decimal_digits : int, optional.
        Indicates the number of digits to print in the Rsq. Default: 3.
        
    Warnings
    --------
    The returned Rsq doesn't take dY weights into account.
    
    """

    # ¿Cómo hago Rsq si tengo pesos?
    
    if dY is None:
        W = None
    else:
        W = 1/dY**2
                
    fit_data = np.polyfit(X,Y,1,cov=True,w=W)
    
    m = fit_data[0][0]
    dm = sqrt(fit_data[1][0,0])
    b = fit_data[0][1]
    db = sqrt(fit_data[1][1,1])
    rsq = 1 - sum( (Y - m*X - b)**2 )/sum( (Y - np.mean(Y))**2 )

    try:
        kwargs['txt_position']
    except KeyError:
        if m > 1:
            aux = 'up'
        else:
            aux = 'down'
        kwargs['txt_position'][0] = .02

    if showplot:

        plt.figure()
        if dY is None:
            plt.plot(X, Y, 'b.', zorder=0)
        else:
            if plot_some_errors[0] == False:
                plt.errorbar(X, Y, yerr=dY, linestyle='b', marker='.',
                             ecolor='b', elinewidth=1.5, zorder=0)
            else:
                plt.errorbar(X, Y, yerr=dY, linestyle='-', marker='.',
                             color='b', ecolor='b', elinewidth=1.5,
                             errorevery=len(Y)/plot_some_errors[1], 
                             zorder=0)
        plt.plot(X, m*X+b, 'r-', zorder=100)
        
        plt.legend(["Ajuste lineal ponderado","Datos"])
        
        kwargs_list = ['txt_position', 'mb_units', 'mb_string_scale', 
                       'mb_error_digits', 'rsq_decimal_digits']
        kwargs_default = [(.02, aux), ('', ''), (False, False), 
                          (3, 2), 3]
        for key, value in zip(kwargs_list, kwargs_default):
            try:
                kwargs[key]
            except KeyError:
                kwargs[key] = value
        
        if kwargs['text_position'][1] == 'up':
            vertical = [.9, .82, .76]
        elif kwargs['text_position'][1] == 'down':
            vertical = [.05, .13, .21]
        else:
            if kwargs['text_position'][1] <= .08:
                fact = .08
            else:
                fact = -.08
            vertical = [kwargs['txt_position']+fact*i for i in range(2)]
        
        plt.annotate('m={}'.format(fmt.error_value(
                        m, 
                        dm,
                        errordigits=kwargs['mb_error_digits'][0],
                        units=kwargs['mb_units'][0],
                        string_scale=kwargs['mb_string_scale'][0],
                        one_point_scale=True)),
                    (kwargs['text_position'][0], vertical[0]),
                    xycoords='axes fraction')
        plt.annotate('b={}'.format(fmt.error_value(
                        b, 
                        db,
                        errordigits=kwargs['mb_error_digits'][1],
                        units=kwargs['mb_units'][1],
                        string_scale=kwargs['mb_string_scale'][1],
                        one_point_scale=True)),
                    (kwargs['text_position'][0], vertical[1]),
                    xycoords='axes fraction')
        rsqft = r'$R^2$={:.' + str(kwargs['rsq_decimal_digits']) + 'f}'
        plt.annotate(rsqft.format(rsq),
                    (kwargs['text_position'][0], vertical[2]),
                    xycoords='axes fraction')
        
        fmt.plot_style()
        plt.show()

    return (m, dm), (b, db), rsq

