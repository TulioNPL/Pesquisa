###
# Pega as posicoes dos veiculos em determinado horario e plota em um mapa
# --- Baixar o mapa da coordenada de cada horario para plotar
###

import datetime as dt
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter
import gmplot
import sys

def gMapsPlot():
    """Plota o mapa de calor utilizando o Google Maps"""

    df = pd.read_csv('./data/sortById/roma_12hTo13h_sorted_by_id.csv')
    lat = df['lat_y']
    lng = df['long_x']

    mid_lat = (df.lat_y.min() + df.lat_y.max()) / 2 #latitude media
    mid_lng = (df.long_x.min() + df.long_x.max()) / 2 #longitude media

    gmap = gmplot.GoogleMapPlotter(mid_lat,mid_lng,12) #(x,y,zoom)
    gmap.heatmap(lat,lng)
    gmap.draw('./img/heatmap_12hTo13h.html')

def my_plot(x,y,s,bins=1000):
    """Plota um mapa de calor"""

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent

def heatHistogramPlot():
    """Plota o histograma 2d das posicoes dos veiculos"""

    df = pd.read_csv('./data/sortById/roma_12hTo13h_sorted_by_id.csv')

    fig, ax = plt.subplots()

    img,extent = my_plot(df.long_x,df.lat_y,128)
    ax.imshow(img,extent=extent,origin='lower',cmap=cm.jet)
    ax.set_title('Heatmap')
    plt.savefig('./img/heat_histogram_12hTo13h.png')
    plt.show()

def osmPlot():
    """Plota o mapa utilizando Open Street Maps"""

    horario = str(sys.argv[1])
    
    path = './data/sortById/roma_' + horario + '_sorted_by_id.csv'
    print('Acessando dados de: ' + path)
    df = pd.read_csv(path)

    BBox = (df.long_x.min(),df.long_x.max(),df.lat_y.min(),df.lat_y.max()) #limites laterais do mapa
    print(df.long_x.min(),df.long_x.max(),df.lat_y.min(),df.lat_y.max())
    ruh_m = plt.imread('./img/backmaps/backmap_' + horario + '.png') #mapa a ser usado de fundo

    fig, ax = plt.subplots()
    ax.scatter(df.long_x, df.lat_y, zorder=1, alpha=0.008, c='#d1432a', s=10)
    ax.set_title('Mapa de Calor - ' + horario)
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m,zorder= 0, extent= BBox, aspect= 'equal')

    path = './img/map_' + horario + '.png'
    print('Gráfico salvo como: ' + path)
    plt.savefig(path, dpi=500)
    plt.show()
