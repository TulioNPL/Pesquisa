###
# Pega as posicoes dos veiculos em determinado horario e plota em um mapa
# --- Baixar o mapa da coordenada de cada horario para plotar
###

import datetime as dt
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

#lower_limit = pd.Timestamp(2014,2,4,6) #limite inferior = 2014-02-04 06:00:00
#upper_limit = pd.Timestamp(2014,2,4,7) #limite superior = 2014-02-04 07:00:00

lower_limit = dt.datetime(2014,2,4,6,0,0)
upper_limit = dt.datetime(2014,2,4,6,59,59)

df = pd.read_csv('./Dados/roma_calibrated.csv')
#print(df.loc[df['id'] == 101].long_x.min(), df.loc[df['id'] == 101].long_x.max(), df.loc[df['id'] == 101].lat_y.min(), df.loc[df['id'] == 101].lat_y.max())
df['time'] = pd.to_datetime(df['time'])

df2 = df.loc[(df['time'] < upper_limit) & (df['time'] > lower_limit)]
#print(df2.long_x.min(), df2.long_x.max(), df2.lat_y.min(), df2.lat_y.max())

BBox = (df2.long_x.min(),df2.long_x.max(),df2.lat_y.min(),df2.lat_y.max())
ruh_m = plt.imread('./Dados/map.png')

fig, ax = plt.subplots(figsize= (8,7))
ax.scatter(df.long_x, df.lat_y, zorder=1, alpha=0.2, c='b', s=10)
ax.set_title('Ploting all positions')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(ruh_m, zorder= 0, extent= BBox, aspect= 'equal')

plt.savefig('6-7.png')

###
# Le os horarios de casa coordenada e salva aqueles entre 6h-7h
###
'''
with open('./Dados/roma_calibrated.csv') as file:
    reader = csv.DictReader(file)

    limite_sup = dt.time(7,0,0)
    limite_inf = dt.time(5,59,59)

    for line in reader:
        hora = line['time']
        
        obj_hora = dt.datetime.strptime(hora, '%Y-%m-%d %H:%M:%S')

        if(obj_hora.time() < limite_sup and obj_hora.time() > limite_inf):
            #print(obj_hora.date())
            print(obj_hora.time())
'''