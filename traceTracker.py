import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def track():
    df = pd.read_csv("./sortByTime/roma_12hTo13h_sorted_by_time.csv")
    df = df.loc[df['id'] == 7]

    longitudes = df['long_x'].to_numpy()
    latitudes = df['lat_y'].to_numpy()
    new = df['time'].str.split(" ", n=1, expand = True)
    
    horario = new[1]
    horario = horario.to_numpy()

    BBox = (df.long_x.min(),df.long_x.max(),df.lat_y.min(),df.lat_y.max())
    #print(BBox)
    ruh_m = plt.imread('./graficos/trackmap_id_7.png')

    fig, ax = plt.subplots()
    ax.scatter(df.long_x, df.lat_y, zorder=1, alpha=1, c='#d1432a', s=10)
    ax.set_title('Trackmap ID 7')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m,zorder= 0, extent= BBox, aspect= 'equal')

    for i in range(0,horario.size):
        ax.text(longitudes[i],latitudes[i],horario[i],fontsize=8)

    plt.show()


#Driver
track()