import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ID = 3
HORA = '18hTo19h' 

def track():
    df = pd.read_csv("./sortByTime/roma_18hTo19h_sorted_by_time.csv")
    df = df.loc[df['id'] == ID]
    #print(df)

    df.to_csv("./sortByTime/roma_" + HORA + "_id_" + str(ID) + "_sorted_by_time.csv")
    longitudes = df['long_x'].to_numpy()
    latitudes = df['lat_y'].to_numpy()
    new = df['time'].str.split(" ", n=1, expand = True)
    
    horario = new[1]
    horario = horario.to_numpy()

    BBox = (df.long_x.min(),df.long_x.max(),df.lat_y.min(),df.lat_y.max())
#    print(BBox)

    ruh_m = plt.imread('./graficos/backmaps/trackmap_id_'+ str(ID) +'.png')
    #fig, ax = plt.subplots()

    for i in range(0,horario.size):
    #for i in range(0,1000):
        fig, ax = plt.subplots()
        ax.scatter(longitudes[i], latitudes[i], zorder=1, alpha=1, c='#d1432a', s=10)
        ax.set_title('Trackmap ID ' + str(ID) + " " +str(i))
        ax.set_xlim(BBox[0],BBox[1])
        ax.set_ylim(BBox[2],BBox[3])
        ax.imshow(ruh_m,zorder= 0, extent= BBox, aspect= 'equal')
        ax.text(longitudes[i],latitudes[i],horario[i],fontsize=10)
        plt.savefig("./graficos/trackmap_id_3/trackmap_id_"+str(ID)+"_"+str(HORA)+"_"+str(i)+".png", dpi=400)
        plt.close()

    #plt.show()

#Driver
track()