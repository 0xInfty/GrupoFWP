# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:09:13 2018

@author: Usuario
"""

import numpy as np
import math as mth
       
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
        return (mean, mth.sqrt(variance))
    
    else:
        return (np.mean(X), np.std(X))


#%%

def error_value(X, nc=0, units='',
                scale=True, lscale=False, rnum=False, fprec=True):

    ans = '%.' + str(nc-1) + 'e'
    ans = ans % X[1]
    ans = ans.split("e")
    
    orderr = int(ans[1])
    err = ans[0]

    ans2 = '%15e' % X[0]
    ans2 = ans2.split("e")
    
    ordnum = int(ans2[1])
    num = float(ans2[0])
    
    if -9<=ordnum<12 and scale==True:
        pref=['n', r'$\mu$', 'm','','k','M','G']
        escala=[-9,-6,-3,0,3,6,9,12]
        for i in range(7):
            if lscale==False:
                if escala[i]<=ordnum<escala[i+1]:
                    pref=pref[i]
                    escala=escala[i]
                    break
            else:
                if escala[i]-1<=ordnum<escala[i+1]-1:
                    pref=pref[i]
                    escala=escala[i]
                    break
        ans=True
    else:
        escala=ordnum
        pref=''
        ans=False

    if orderr<escala:
        if nc-orderr+escala-1>=0:
            ans3 = '%.' + str(nc-orderr+escala-1) + 'f'
            err = ans3 % ( float(err)*10**(orderr-escala) )
            num = ans3 % ( num*10**(ordnum-escala) )
        else:
            err = float(err)*10**(orderr-escala)
            num = float(num)*10**(ordnum-escala)
    else:
        ans3 = '%.' + str(nc-1) + 'f'
        err = ans3 % ( float(err)*10**(orderr-escala) )
        num = ans3 % ( float(num)*10**(ordnum-escala) )
                
    if ans==False and ordnum!=0:
        leg = r'(%s$\pm$%s)$10^{%i}$%s%s' % (num,err,escala,pref,units)
    else:
        leg = r'(%s$\pm$%s)%s%s' % (num,err,pref,units)
    
    if rnum==True:
        print(leg)
        if fprec==True:
            return X
        else:
            return ( float(num)*10**escala, float(err)*10**escala )
    else:
        return leg

#%%

def Ajuste_Polyfit(X,Y,dY=0,\
                tit='Ajuste lineal Polyfit', ylab='nan', xlab='nan', \
                yft='nan', xft='nan', dim='nan', \
                xaxlim='nan', yaxlim='nan', \
                text='nan', textp='up', \
                leg='nan', legp = 'best', mbp='nan', \
                ajunits = ('',''), ajnc=2, ajrnc=3, ajscale=(False,False), \
                ernum=(False,20), \
                fname='nan', ftype='png', \
                showfig=True, savefigure=False, savetext=False, figinforme=True, \
                gdir='C:\\Users\\Usuario\\Documents\\Git\\Privado'):  

    # ¿Cómo hago Rsq si tengo pesos?
    
    from numpy import ndarray, polyfit#, corrcoef
    from math import sqrt
    from GAux import Ajuste_2D, Ajuste_Ponderado_2D
    from FAux import Rsq

    if type(dY)==int:
        W = None
        mod = 'Ajuste lineal'
    elif type(dY)!=ndarray:
        print("¡Error! dY debe ser numpy.ndarray.")
        return
    else:
        W = abs(1/dY)
        mod = 'Ajuste lineal ponderado'
        
    Data = polyfit(X,Y,1,cov=True,w=W)
    
    m = ( Data[0][0], sqrt(Data[1][0,0]) )
    b = ( Data[0][1], sqrt(Data[1][1,1]) )
    rsq = Rsq(X,Y,m,b)
    #rsq = ( corrcoef(X, Y)[0,1] )**2

    if m[0]>=0:
        legp = 'lower right'
        mbp = (.02,.9)
    else:
        legp = 'upper right'
        mbp = (.02,.03)
    
    if showfig==True:
        if mod == 'Ajuste lineal':
            Ajuste_2D(Y=Y, X=X, m=m, b=b, rsq=rsq,  \
                tit=tit, ylab=ylab, xlab=xlab, \
                yft=yft, xft=xft, dim=dim, \
                xaxlim=xaxlim, yaxlim=yaxlim, \
                text=text, textp=textp, \
                leg='nan', legp=legp, mbp=mbp, \
                lstyle='', lmarksize=6, lwidth=1.0, lmark='.', lcolor='b', \
                ajline = '-r', ajunits = ajunits, ajnc=ajnc, ajrnc=ajrnc, ajscale=ajscale, \
                fname=fname, ftype=ftype, \
                savefigure=savefigure, savetext=savetext, figinforme=figinforme, \
                gdir=gdir)
        else:
            Ajuste_Ponderado_2D(Y=Y,X=X,dY=dY,m=m,b=b,rsq=rsq,\
                tit=tit, ylab=ylab, xlab=xlab, \
                yft=yft, xft=xft, dim=dim, \
                xaxlim=xaxlim, yaxlim=yaxlim, \
                text=text, textp=textp, \
                leg='nan', legp=legp, mbp=mbp, \
                lstyle='', lmarksize=6, lwidth=1.0, lmark='.', lcolor='b', \
                ercolor='black', ernum=ernum, \
                ajline = '-r', ajunits = ajunits, ajnc=ajnc, ajrnc=ajrnc, ajscale=ajscale, \
                fname=fname, ftype=ftype, \
                savefigure=savefigure, savetext=savetext, figinforme=figinforme, \
                gdir=gdir)

    return m, b, rsq

#%%

#def Rsq(X,Y):
#
#	from math import sqrt
#
#	n = len(X)
#
#	r = n*(sum(X*Y))-sum(X)*sum(Y)
#	r = r/sqrt( (n*sum(X**2)-sum(X)**2)*(n*sum(Y**2)-sum(Y)**2) )
#
#	return r**2

def Rsq(X,Y,m,b):
# Solía ser Rsq_2
    
    print("¡Ojo! El rsq no tiene en cuenta los pesos.")
    
    from numpy import mean

    try:
        m = m[0]
    except:
        m = m
    
    try:
        b = b[0]
    except:
        b = b

    SSreg = sum( (Y - m*X - b)**2 )
    SStot = sum( (Y - mean(Y))**2 )
    rsq = 1 - SSreg/SStot
    
    # Con los pesos W=1/dY ¿multiplico W*(blah)**2 o hago (W*Y-blah)**2?

    return rsq
