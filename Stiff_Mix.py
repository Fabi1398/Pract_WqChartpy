# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 16:18:59 2022

@author: Fabi
"""

import os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
from pylab import *
from funciones import *
from variables import *


def plot(df, 
         unit='mg/L', 
         figname='Stiff diagram', 
         figformat='jpg'):
    """Plot the Stiff diagram. 
    Parameters
    ----------
    df : class:`pandas.DataFrame`
        Geochemical data to draw Gibbs diagram.
    unit : class:`string`
        The unit used in df. Currently only mg/L is supported. 
    figname : class:`string`
        A path or file name when saving the figure.
    figformat : class:`string`
        The file format, e.g. 'png', 'pdf', 'svg'
    """
    # Determine if the provided unit is allowed
    ALLOWED_UNITS = ['mg/L', 'meq/L']
    if unit not in ALLOWED_UNITS:
        raise RuntimeError("""
        Currently only mg/L and meq/L are supported.
        Convert the unit manually if needed.""")
        
    # Convert unit if needed
    if unit == 'mg/L':
        iones_Weight = {'Ca':40.078, 'Mg':24.305, 'Na':22.9898, 'K':39.0983, 'HCO3':61.0171, 'Cl':35.4527, 'SO4':96.0636}
        iones_Charge = {'Ca':2.0, 'Mg':2.0, 'Na':1.0, 'K':1.0, 'HCO3':-1.0, 'Cl':-1.0, 'SO4':-2.0}
        
        tmpdf = df[['Ca', 'Mg', 'Na', 'K', 'HCO3', 'Cl', 'SO4']]
        dat = tmpdf.values
        
        meqL = (dat / abs(iones_Weight)) * (abs(iones_Charge))
        
        
    elif unit == 'meq/L':
        meqL = df[['Ca', 'Mg', 'Na', 'K', 'HCO3', 'Cl', 'SO4']].values
    
    else:
        raise RuntimeError("""
        Currently only mg/L and meq/L are supported.
        Convert the unit if needed.""")
   
    cat_max = np.max(np.array(((meqL[:, 2] + meqL[:, 3]), meqL[:, 0], meqL[:, 1])))
    an_max = np.max(meqL[:, 4:])
    
    
    
#equivalen weight colum
    df = df[['Ca', 'Mg', 'Na', 'K', 'HCO3', 'Cl', 'SO4']].add_suffix('_meq')


    for index, row in df.iterrows():
         Na_K, Ca, Mg = row['Na_meq']+row['K_meq'], row['Ca_meq'], row['Mg_meq'] 
         Cl, SO4, HCO3_CO3 = row['Cl_meq'], row['SO4_meq'], row['HCO3_meq']+row['CO3_meq']
    #apply some factor for the axis
    maxConNorm = max([Na_K, Ca, Mg, Cl, SO4, HCO3_CO3])*2
    #set of points of the Stiff diagram
    a = np.array([[0.5 + Cl/maxConNorm,1],[0.5 + SO4/maxConNorm,.5],[0.5 + HCO3_CO3/maxConNorm,0]
                  ,[0.5 - Mg/maxConNorm,0],[0.5 - Ca/maxConNorm,.5],[0.5 - Na_K/maxConNorm,1]])

    figura = diagramaStiff(a, maxConNorm, index)
    figura.savefig('../Svg/Stiff-'+str(index)+'.svg')
    figura.savefig('../Png/Stiff-'+str(index)+'.png') 




    datosQuimicaGeo = df.loc[:,'coordy':'coordx']
    datosQuimicaGeo.to_csv('E:/TESIS/Practica/Txt/datosQuimicaGeo.csv')

    imagePath = os.path.join(os.path.dirname(os.getcwd()),'Svg')
    imagePath = imagePath.replace('\\','/')
    imagePath

#style file generation
    archivoestilos = open('E:/TESIS/Practica/Txt/estilos_Qgis.sld','w')
    archivoestilos.write(encabezado)

    for index, row in df.iterrows():
        item = re.sub('%%path%%',imagePath,item)
        estiloitem = re.sub('%%index%%',index,item)
        archivoestilos.write(estiloitem)
    archivoestilos.write(final)

    archivoestilos.close()








df= pd.read_excel('E:/TESIS/Practica/Txt/df.xlsx')
plot(df, unit='mg/L', figname='Stiff diagram', figformat='jpg')