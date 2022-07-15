#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd  # Librería para el uso y manejo de archivos excel y cvs
import re, os, glob, shutil  # Libría para usar expresiones regulares
import plotnine as p9  # Librería para gráficos
import matplotlib as plt #Libreria matplotlib
from plotnine import ggplot, aes, geom_boxplot, stat_bin, geom_bar, geom_histogram, geom_point, geom_path, geom_errorbar, geom_smooth
from funciones import *
from variables import *
# Librería plotnine y sus apartados, para el uso de gráficos y sus componentes

# Carga de los archivos al programa
df1 = pd.read_excel("E:/TESIS/Practica/BDD_orden_phreqc.xlsx")
df2 = pd.read_excel("E:/TESIS/Practica/BDD_compilada_practica.xlsx")
df3 = pd.read_excel("E:/TESIS/Practica/BDD_aCompletar.xlsx")


# # Archivo BDD_compilada_practica (DF2)

# In[2]:


df2 = df2.sort_values(by=['Fecha'], ascending=[False])  # Ordenar por fecha
df2.rename(columns={'Hora de Muestreo': 'Hora',
                    'QA/QC': 'QAQC',
                    'Caudales (L/s)': 'Caudal (L/s)',
                    'pH lab': 'pH',
                    'ORP Lab (mV)': 'ORP  (mV)',
                    'O.D. Lab': 'O.D. (%)',
                    'Alcalinidad Bicarbonato (mg/L de CaCO3)': 'Alcalinidad (mg/L de CaCO3)'
                    }, inplace=True)  # Renombre de columnas


# In[3]:


df2.reset_index(drop=True, inplace=True)  # Crear un nuevo index
# Unión de dos columnas con distintos formatos
df2['Hora'] = df2['Hora'].fillna('')  # Eliminar datos NaN

# Unión de columnas Fecha y Hora con un espacio entre medio
df2['Fecha y Hora'] = df2['Fecha'].astype(str) + ' ' + df2['Hora'].astype(str)
# Transforma el tipo de dato de string a tipo tiempo(datatime)
df2['Fecha y Hora'] = pd.to_datetime(df2['Fecha y Hora'])
# Unión de columnas Punto, Fecha y Hora con un "_" entre medio
df2['Codigo Muestra'] = df2['Punto'] + '_' + df2['Fecha y Hora'].astype(str)


# In[4]:


# Colocar la columna Codigo Muestra de las primeras
# Crear una lista con todos los nombres de las columnas del dataframe
cols = df2.columns.tolist()

# Codigo qque reubica la última columna a la primera posición( 0 )
cols = cols[-1:] + cols[:-1]
# Codigo qque reubica la última columna a la primera posición( 0 )
df2 = df2[cols]

# Eliminando columnas 'Fecha y hora', 'fecha', 'Hora' y 'Punto'
cols2 = df2.columns.tolist()
cols2 = cols[0:4] + cols[9:46]  # Elimina las columnas entre estos dos rangos
df2 = df2[cols2]  # Elimina las columnas entre estos dos rangos




# # Archivo BDD_aCompletar (DF3)

# In[5]:


# Se elimino la fila 2, ya que puede que afecte al programa
df3 = df3.drop([0])

"""
DATOS CAMPO:
    Caudal(L/s), Alcalinidad (mg/L de CaCO3), pH, C.E.S.(25°C)(uS/cm),
    C.E. Actual(uS/cm), ORP  (mV), Temperatura (°C), O.D. (%), O.D.  (ppm)
"""
df3.rename(columns={'Punto AMTC': 'Punto',
                    'RIO': 'Río',
                    }, inplace=True)  # Cambio de nombre a columna

df3['Fecha y hora'] = df3['Fecha y hora'].astype(
    str)  # Transforma el tipo tiempo a string

# Unión de columnas "Punto" y "Fecha y Hora" con un "_" entre medio
df3['Codigo Muestra'] = df3['Punto'] + '_' + df3['Fecha y hora']
# poner la columna Codigo Muestra de las primeras
cols = df3.columns.tolist()
cols = cols[-1:] + cols[:-1]
df3 = df3[cols]
# Eliminando columnas 'Fecha y hora' y 'Punto'
cols2 = df2.columns.tolist()
cols2 = cols[0:3] + cols[5:158]
df3 = df3[cols2]
# Reemplaza los valores NaN con cero(0) para que la columna tenga un solo tipo de dato(int)
df3['Caudal (L/s)'] = df3['Caudal (L/s)'].fillna(0)

# print(df3.head())


# # Unión DF2 y DF3

# In[6]:


# Union de DF3 y DF2 usando como eje la columna 'Codigo Muestra' y los valores de las filas que sean iguales
# en un excel y en el otro

df4 = pd.merge(df3, df2, on='Codigo Muestra', suffixes=(" Campo", " Lab"))
# print(df4.head())

# crear un dataframe ordenado a partir de DF4
cols2 = df4.columns.tolist()
cols = cols2[0:6] + cols2[156:159] + cols2[160:167] + cols2[6:12] + \
    cols2[168:172] + cols2[13:156] + cols2[172:179] + cols2[179:195]
df5 = df4[['Codigo Muestra', 'Punto','coordx','coordy', 'QAQC Lab', 'QAQC Campo', 'Caudal (L/s) Campo','C.E. Actual  (uS/cm)', 'Alcalinidad (mg/L de CaCO3) Campo', 'Alcalinidad (mg/L de CaCO3) Lab', 'Alcalinidad Carbonatos (Laboratorio) (mg CaCO3/L)', 'Alcalinidad Bicarbonato (Laboratorio) (mg/L de HCO3)', 'Alcalinidad Bicarbonato (Campo) (mg/L de HCO3)', 'Alcalinidad Total (mg CaCO3/L)', 'pH Campo', 'pH Lab', 'Temperatura (°C)', 'Cloruros. Cl-', 'Sulfuros', 'N-NO2. Nitrito (mg N/L)', 'N-NO3. Nitrato (mg N/L)', 'Nitrógeno de Nitrito y Nitrato', 'F. Fluoruro', 'Bromuro', 'P-PO4. Fosfato', 'Fosfato (mg P/L)', 'Ag_diss_ppb', 'Ag_tot_ppb', 'Al_diss_ppb', 'Al_tot_ppb', 'As_diss_ppb', 'As_tot_ppb', 'Au_diss_ppb', 'Au_tot_ppb', 'B_diss_ppb', 'B_tot_ppb', 'Ba_diss_ppb', 'Ba_tot_ppb', 'Be_diss_ppb', 'Be_tot_ppb', 'Bi_diss_ppb', 'Bi_tot_ppb', 'Br_diss_ppb', 'Br_tot_ppb', 'Ca_diss_ppb', 'Ca_tot_ppb', 'Cd_diss_ppb', 'Cd_tot_ppb', 'Ce_diss_ppb', 'Ce_tot_ppb', 'Cl_diss_ppb', 'Cl_tot_ppb', 'Co_diss_ppb', 'Co_tot_ppb', 'Cr_diss_ppb', 'Cr_tot_ppb', 'Cs_diss_ppb', 'Cs_tot_ppb', 'Cu_diss_ppb', 'Cu_tot_ppb', 'Dy_diss_ppb', 'Dy_tot_ppb', 'Er_diss_ppb', 'Er_tot_ppb', 'Eu_diss_ppb', 'Eu_tot_ppb', 'Fe_diss_ppb', 'Fe_tot_ppb', 'Ga_diss_ppb', 'Ga_tot_ppb', 'Gd_diss_ppb', 'Gd_tot_ppb', 'Ge_diss_ppb', 'Ge_tot_ppb', 'Hf_diss_ppb', 'Hf_tot_ppb', 'Hg_diss_ppb',
           'Hg_tot_ppb', 'Ho_diss_ppb', 'Ho_tot_ppb', 'In_diss_ppb', 'In_tot_ppb', 'K_diss_ppb', 'K_tot_ppb', 'La_diss_ppb', 'La_tot_ppb', 'Li_diss_ppb', 'Li_tot_ppb', 'Lu_diss_ppb', 'Lu_tot_ppb', 'Mg_diss_ppb', 'Mg_tot_ppb', 'Mn_diss_ppb', 'Mn_tot_ppb', 'Mo_diss_ppb', 'Mo_tot_ppb', 'Na_diss_ppb', 'Na_tot_ppb', 'Nb_diss_ppb', 'Nb_tot_ppb', 'Nd_diss_ppb', 'Nd_tot_ppb', 'Ni_diss_ppb', 'Ni_tot_ppb', 'P_diss_ppb', 'P_tot_ppb', 'Pb_diss_ppb', 'Pb_tot_ppb', 'Pd_diss_ppb', 'Pd_tot_ppb', 'Pr_diss_ppb', 'Pr_tot_ppb', 'Pt_diss_ppb', 'Pt_tot_ppb', 'Rb_diss_ppb', 'Rb_tot_ppb', 'Re_diss_ppb', 'Re_tot_ppb', 'Rh_diss_ppb', 'Rh_tot_ppb', 'Ru_diss_ppb', 'Ru_tot_ppb', 'S_diss_ppb', 'S_tot_ppb', 'Sb_diss_ppb', 'Sb_tot_ppb', 'Sc_diss_ppb', 'Sc_tot_ppb', 'Se_diss_ppb', 'Se_tot_ppb', 'Si_diss_ppb', 'Si_tot_ppb', 'Sm_diss_ppb', 'Sm_tot_ppb', 'Sn_diss_ppb', 'Sn_tot_ppb', 'SO4_diss ', 'SO4_tot ', 'Sr_diss_ppb', 'Sr_tot_ppb', 'Ta_diss_ppb', 'Ta_tot_ppb', 'Tb_diss_ppb', 'Tb_tot_ppb', 'Te_diss_ppb', 'Te_tot_ppb', 'Th_diss_ppb', 'Th_tot_ppb', 'Ti_diss_ppb', 'Ti_tot_ppb', 'Tl_diss_ppb', 'Tl_tot_ppb', 'Tm_diss_ppb', 'Tm_tot_ppb', 'U_diss_ppb', 'U_tot_ppb', 'V_diss_ppb', 'V_tot_ppb', 'W_diss_ppb', 'W_tot_ppb', 'Y_diss_ppb', 'Y_tot_ppb', 'Yb_diss_ppb', 'Yb_tot_ppb', 'Zn_diss_ppb', 'Zn_tot_ppb', 'Zr_diss_ppb', 'Zr_tot_ppb']]
# Reordenamiento de columnas.


tot = r'(\D{1,2}?_tot_ppb)'  # regex para elementos_tot_ppb
Tot = r'(\D{1,2}?\d_tot)'  # regex para la terminación _tot


# # Eliminar y ordenar colum

# Crear una lista con todos los nombres de las columnas del dataframe
col = df5.columns.tolist()

f = re.compile(tot)  # Establece una busqueda según el patrón
# Crea una lista de todas las coincidencias encontradas en la lista "col"
col2 = list(filter(f.match, col))

f2 = re.compile(Tot)  # Establece una busqueda según el patrón
# Crea una lista de todas las coincidencias encontradas en la lista "col"
col3 = list(filter(f2.match, col))

# Función df.drop= elimina las columnas(axis=1) que se le indica por una lista
df5 = df5.drop(col2, axis=1)  # Terminación _tot_ppb
df5 = df5.drop(col3, axis=1)  # Terminación _tot

# print(df5)


df5.rename(columns={'SO4_diss ': 'SO4_diss_ppb'},
           inplace=True)  # Renombrar la columna SO4_tot

################################
# Actualiza la lista con todos los nombres de las columnas del dataframe
col = df5.columns.tolist()

# Renombra las listas que tengan la terminación "XX_diss_ppb" por "XX Disuelto"
df5.columns = df5.columns.str.replace('_diss_ppb', ' Disuelto')
#df5.to_excel('DF5_WQ.xlsx')
#rem = df5[["QAQC Lab", "QAQC Campo", "Alcalinidad Carbonatos (Laboratorio) (mg CaCO3/L)",
#           'Alcalinidad Bicarbonato (Laboratorio) (mg/L de HCO3)','Alcalinidad (mg/L de CaCO3) Lab',
 #          "Alcalinidad Bicarbonato (Campo) (mg/L de HCO3)", "Alcalinidad Total (mg CaCO3/L)", "pH Lab",
 #          "Sulfuros", "Nitrógeno de Nitrito y Nitrato", "Bromuro", "P-PO4. Fosfato", "Fosfato (mg P/L)"]]  # Columnas a eliminar
#df5 = df5.drop(rem, axis=1)  # Eliminación de columnas


df6 = df5

col = df6.columns.tolist()

# Renombra las listas que tengan la terminación "XX Disuelto" por ""
df6.columns = df6.columns.str.replace(' Disuelto', '')

#Cloro de DF3(ppb)
#df6.rename(columns={"Punto": "Label",'Alcalinidad (mg/L de CaCO3) Campo':'CaCO3',"pH Campo": "pH"}, inplace=True)

#Cloro de DF2(ppm= mg/l)
df6.rename(columns={"Punto": "Label",'Alcalinidad (mg/L de CaCO3) Campo':'CaCO3',"pH Campo": "pH", "Cl":"Cloro" ,"Cloruros. Cl-":"Cl"}, inplace=True)


df6.loc[36,['Ca']]=0.000000001#Evitar error con ceros
df6["CO3"] = 0.000000001


#####################################################

#TODO EN mg/L

#Cationes
# Ca, K, Mg, Na estan en ppb, pero ppb= microg/L y (microg/L)/1000= mg/L
df6["Ca"]=df6['Ca']/1000
df6["K"]=df6['K']/1000
df6["Mg"]=df6['Mg']/1000
df6["Na"]=df6['Na']/1000

#Aniones

df6["SO4"]=(df6['SO4'])
df6["HCO3"]=(df6['CaCO3']*1.22) #Conversión de alcalinidad a mg/L HCO3
#df6["Cl"]=(df6['Cl']/1000)#Cloro de DF3(ppb)
df6["Cl"]=df6['Cl']#Cloro de DF2(ppm= mg/l)

#######################################################
"""
#TODO EN meq/L

#Cationes
# Ca, K, Mg, Na estan en ppb, pero ppb= microg/L y (microg/L)/1000= mg/L
df6["Ca"]=(df6['Ca']/1000)/20
df6["K"]=(df6['K']/1000)/39
df6["Mg"]=(df6['Mg']/1000)/12.16
df6["Na"]=(df6['Na']/1000)/23

#Aniones

df6["SO4"]=(df6['SO4'])/48
df6["HCO3"]=df5['CaCO3']*1.22 #Conversión de alcalinidad a mg/L HCO3
df6['HCO3']= (df6['HCO3'])/61.01
#df6["Cl"]=(df6['Cl']/1000)/35.5#Cloro de DF3(ppb)
df6["Cl"]=(df6['Cl'])/35.5#Cloro de DF2(ppm= mg/l)
"""
############################################################
df6["TDS"]=df6['C.E. Actual  (uS/cm)']*0.7 #TDS(mg/L) a partir de conductividad electrica

df6["Size"] = df6['pH']*10
#df6["Size"] =df6['C.E. Actual  (uS/cm)']
df6["Alpha"] = 0.7# 0= transparente
df6['Marker'] = 'o'
df6['Sample'] = df6['pH']


# Asignando un color a cada grupo de datos
df6.loc[df6['Label'] == 'AMTC1', 'Color'] = '#00FFFF'
df6.loc[df6['Label'] == 'AMTC2', 'Color'] = '#ff00ee'
df6.loc[df6['Label'] == 'AMTC3', 'Color'] = '#0000FF'
df6.loc[df6['Label'] == 'AMTC4', 'Color'] = '#FF3030'
df6.loc[df6['Label'] == 'AMTC5', 'Color'] = '#00C957'
df6.loc[df6['Label'] == 'AMTC6', 'Color'] = '#FFD700'
df6.loc[df6['Label'] == 'AMTC7', 'Color'] = '#030303'
df6.loc[df6['Label'] == 'AMTC8', 'Color'] = '#8470FF'
df6.loc[df6['Label'] == 'AMTC9', 'Color'] = '#FF00FF'
df6.loc[df6['Label'] == 'AMTC10', 'Color'] = '#00FA9A'
df6.loc[df6['Label'] == 'AMTC11', 'Color'] = '#FFBBFF'
df6.loc[df6['Label'] == 'AMTC12', 'Color'] = '#FF8247'
df6.loc[df6['Label'] == 'AMTC13', 'Color'] = '#8A360F'

from wqchartpy import triangle_piper, durvo_modf, schoeller, stiff

#Draw the diagram
#triangle_piper.plot(df6, unit='mg/L', figname='triangle Piper diagram', figformat='jpg')

#durvo_modf.plot(df6, unit='mg/L', figname='Durov diagram', figformat='jpg')

#schoeller.plot(df6, unit='mg/L', figname='Schoeller diagram', figformat='jpg')
df7= df6

F=r'([0-9]{4}\-[0-9]{2})'

df7['Año-Mes']=df7['Codigo Muestra'].str.extract(F , expand=True)#Crea una nueva colmna solo con datos de las fechas


print("Diagramas de Stiff:")
print("Oprción 1: Septiembre 2016")
print('Opción 2: Diciembre 2016')
print('Opción 3: Enero 2017')
print('Opción 4: Febrero 2017')
print('Opcion 5: Mayo 2017')

i= int(input('Elija una opción: '))
df7.rename(columns={'Codigo Muestra': 'Estacion' }, inplace=True) 


for x in [i]:
    if x == 1:
      df8= df7.iloc[0:14]
      stiff.plot(df8, unit='mg/L', figformat='svg')
      Sep2016 = df8.loc[:,['Estacion','coordx','coordy']]
      Sep2016.to_csv('Sep2016_XY.csv')


    elif x== 2:
        df8= df7.iloc[46:61]
        df8.reset_index(inplace=True, drop=False)
        stiff.plot(df8, unit='mg/L', figname='Stiff Dic2016', figformat='svg')
        Dic2016 = df8.loc[:,['Estacion','coordx','coordy']]
        Dic2016.to_csv('Dic2016_XY.csv')


    elif x== 3:
        df8= df7.iloc[62:77]
        df8.reset_index(inplace=True, drop=False)
        stiff.plot(df8, unit='mg/L', figname='Stiff Ene2017', figformat='svg')
        Ene2017 = df8.loc[:,['Estacion','coordx','coordy']]
        Ene2017.to_csv('Ene2017_XY.csv')

    elif x== 4:
        df8= df7.iloc[78:100]
        df8.reset_index(inplace=True, drop=False)
        stiff.plot(df8, unit='mg/L', figname='Stiff Feb2017', figformat='svg')
        Feb2017 = df8.loc[:,['Estacion','coordx','coordy']]
        Feb2017.to_csv('Feb2017_XY.csv')


    elif x== 5:
        df8= df7.iloc[137:151]
        df8.reset_index(inplace=True, drop=False)
        stiff.plot(df8, unit='mg/L', figname='Stiff May2017', figformat='svg')
        May2017 = df8.loc[:,['Estacion','coordx','coordy']]
        May2017.to_csv('May2017_XY.csv')

    
    else:
        print("Elija una opción correcta")



df8.to_csv('datosQuimicaGeo.csv')
imagePath = os.path.join(os.path.dirname(os.getcwd()),'Practica')
imagePath = imagePath.replace('\\','/')


#style file generation
archivoestilos = open('E:/TESIS/Practica/Estilos_Qgis.sld','w')

archivoestilos.write(encabezado)
df8.set_index('Estacion',inplace = True)
for index, row in df8.iterrows():
    item = re.sub('%%path%%',imagePath,item)
    estiloitem = re.sub('%%index%%',index,item)
    archivoestilos.write(estiloitem)
archivoestilos.write(final)

archivoestilos.close()