# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 18:57:08 2023

@author: Asus
"""

import numpy as np
import pandas as pd
from tabulate import tabulate
from scipy.optimize import curve_fit

Psun=0.1     #0.1W/cm2
Acel=12.5*12.5
celulas=['1','2','3','4']

def r(m,x,b):
    return m*x+b

def f(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

for x in range(len(celulas)):
    
    data1={'Célula':[],'par de contactos':[],'Potência máxima (W)':[],'Eficiência (%)':[],'Fill factor, FF (%)':[],'Rsh (ohm)':[],'Rs (ohm)':[]}
    data2={'V max power (V)':[],'I max power (A)':[],'V open circuit (V)':[],'I short circuit (A)':[]}
    Il1=0   
    Rs1=0
    Rsh1=0
    
    n=[0,1,2,3,4,5,6,7,8]
    cel=[celulas[x]]*9
    cont1=['1','1','1','2','2','2','3','3','3']
    cont2=['1','2','3','1','2','3','1','2','3']
    
    for i in n:
        t='c'+cel[i]+'t'+cont1[i]+cont2[i]+'.txt'
        dt=pd.read_csv(t)
        V=np.array(dt["Voltage (V)"])
        I=np.array(dt[" Current (A)"])
        P=np.array(dt[' Power (W)'])
        
        data1['Célula'].append(cel[i])
        data1['par de contactos'].append(cont1[i]+' e '+cont2[i])
        pm=P.max()
        data1['Potência máxima (W)'].append(pm)
        ef=round((pm/(Psun*Acel))*100,2)
        data1['Eficiência (%)'].append(ef)
        ip=np.where(P==pm)
        vmpi=V[ip]
        vmp=str(vmpi)[1:-1]
        data2['V max power (V)'].append(vmp)
        impi=I[ip]
        imp=str(impi)[1:-1]
        data2['I max power (A)'].append(imp)
        voc=V.max()
        data2['V open circuit (V)'].append(voc)
        isc=I.max()
        data2['I short circuit (A)'].append(isc)
        FF=(((float(vmp))*(float(imp)))/(voc*isc))*100
        data1['Fill factor, FF (%)'].append(round(FF,2))
        Vshi=f(V,0)
        Vshf=f(V,1.5)
        Vsh=V[Vshi:Vshf]
        Ish=I[Vshi:Vshf]
        popt, pcov=curve_fit(r,Vsh,Ish)
        m=popt[0]
        b=popt[1]
        Rsh2=round(-1/m,2)
        Rsh1=Rsh1+Rsh2
        data1['Rsh (ohm)'].append(Rsh2)
        Vsi=f(V,3)
        Vs=V[Vsi:]
        Is=I[Vsi:]
        popt, pcov=curve_fit(r,Vs,Is)
        m=popt[0]
        b=popt[1]
        Rs2=round(-1/m,4)
        Rs1=Rs1+Rs2
        data1['Rs (ohm)'].append(Rs2)
        Il2=((Rsh2+Rs2)/Rsh2)*isc
        Il1=Il1+Il2

    
    df1=pd.DataFrame(data1)
    df2=pd.DataFrame(data2)
    Il=Il1/(len(n))
    Rsh=Rsh1/(len(n))
    Rs=Rs1/(len(n))
    
    print(tabulate(df1, showindex=False, headers=df1.columns, tablefmt="pretty", stralign='decimal'))
    print(tabulate(df2, showindex=False, headers=df2.columns, tablefmt="pretty", stralign='decimal'))
    print('Il célula',celulas[x],' = ',Il)
    print('Rsh célula',celulas[x],' = ',Rsh)
    print('Rs célula',celulas[x],' = ',Rs)
    print()
