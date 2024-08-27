"""Plots the vehicle route on the Rome map during an 1 hour period"""
import platform
import os.path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ID = 367
HORA = '12hTo13h' 

if platform.system() == 'Linux':
    path = '/home/tulionpl/Repos/Pesquisa'
else:
    path = '/Users/tuliopolido/Repos/Pesquisa'

def map():
    """Plots one map with all the vehicle points"""
    df = pd.read_csv(path + "/data/roma_calibrated_sorted.csv")
    df = df.loc[df['id'] == ID]
    #print(df)

    df.to_csv(path + "/data/sortByTime/roma_" + HORA + "_id_" + str(ID) + "_sorted_by_time.csv")
    longitudes = df['long_x'].to_numpy()
    latitudes = df['lat_y'].to_numpy()
    new = df['time'].str.split(" ", n=1, expand = True)
    
    horario = new[1]
    horario = horario.to_numpy()

    BBox = (df.long_x.min(),df.long_x.max(),df.lat_y.min(),df.lat_y.max())

    if(os.path.exists(path + '/img/backmaps/trackmap_id_'+ str(ID) +'.png')):
        ruh_m = plt.imread(path + '/img/backmaps/trackmap_id_'+ str(ID) +'.png')

        fig, ax = plt.subplots()
        ax.scatter(longitudes, latitudes, zorder=0.3, alpha=0.3, c='#d1432a', s=2)
        ax.set_xlim(BBox[0],BBox[1])
        ax.set_ylim(BBox[2],BBox[3])
        ax.imshow(ruh_m,zorder= 0, extent= BBox, aspect= 'equal')
        ax.tick_params(labelsize=8)
        plt.tight_layout(0) 
        plt.savefig(path + "/img/trackmap_id_"+str(ID)+".png", dpi=150)
        plt.close()
    else:
        print('Por favor crie o backmap com as seguintes coordenadas: ')
        print(BBox)
        print('Depois salve o arquivo no path: ' + path + '/img/backmaps/trackmap_id_'+ str(ID) +'.png')

def track():
    """Plots one map for each point of the vehicle"""
    df = pd.read_csv(path + "/data/sortByTime/roma_12hTo13h_sorted_by_time.csv")
    df = df.loc[df['id'] == ID]
    #print(df)

    df.to_csv(path + "/data/sortByTime/roma_" + HORA + "_id_" + str(ID) + "_sorted_by_time.csv")
    longitudes = df['long_x'].to_numpy()
    latitudes = df['lat_y'].to_numpy()
    new = df['time'].str.split(" ", n=1, expand = True)
    
    horario = new[1]
    horario = horario.to_numpy()

    BBox = (df.long_x.min(),df.long_x.max(),df.lat_y.min(),df.lat_y.max())

    if(os.path.exists(path + '/img/backmaps/trackmap_id_'+ str(ID) +'.png')):
        ruh_m = plt.imread(path + '/img/backmaps/trackmap_id_'+ str(ID) +'.png')

        for i in range(0,horario.size):
            if(i == 2000):
                fig, ax = plt.subplots()
                ax.scatter(longitudes[i], latitudes[i], zorder=1, alpha=1, c='#d1432a', s=10)
                ax.set_title('Trackmap ID ' + str(ID) + " " +str(i))
                ax.set_xlim(BBox[0],BBox[1])
                ax.set_ylim(BBox[2],BBox[3])
                ax.imshow(ruh_m,zorder= 0, extent= BBox, aspect= 'equal')
                ax.text(longitudes[i],latitudes[i],horario[i],fontsize=10)
                plt.savefig(path + "/img/trackmap_id_"+str(ID)+"_"+str(HORA)+"_"+str(i)+".png", dpi=150)
                plt.close()
    else:
        print('Por favor crie o backmap com as seguintes coordenadas: ')
        print(BBox)
        print('Depois salve o arquivo no path: ' +path+ '/img/backmaps/trackmap_id_'+ str(ID) +'.png')

#Driver

#map()
track()