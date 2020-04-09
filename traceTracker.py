import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ID = 3

def track():
    df = pd.read_csv("./sortByTime/roma_18hTo19h_sorted_by_time.csv")
    df = df.loc[df['id'] == ID]
    #print(df)

    df.to_csv("./sortByTime/roma_12hTo13h_id_" + str(ID) + "_sorted_by_time.csv")
    longitudes = df['long_x'].to_numpy()
    latitudes = df['lat_y'].to_numpy()
    new = df['time'].str.split(" ", n=1, expand = True)
    
    horario = new[1]
    horario = horario.to_numpy()

    BBox = (df.long_x.min(),df.long_x.max(),df.lat_y.min(),df.lat_y.max())
    print(BBox)

    ruh_m = plt.imread('./graficos/backmaps/trackmap_id_'+ str(ID) +'.png')

    fig, ax = plt.subplots()
    ax.scatter(df.long_x, df.lat_y, zorder=1, alpha=1, c='#d1432a', s=10)
    ax.set_title('Trackmap ID ' + str(ID))
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m,zorder= 0, extent= BBox, aspect= 'equal')

    for i in range(0,horario.size):
        if i % 25 == 0:
            ax.text(longitudes[i],latitudes[i],horario[i],fontsize=10)

    plt.show()

#Driver
track()