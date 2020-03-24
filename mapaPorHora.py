###
# Pega as posicoes dos veiculos em determinado horario e plota em um mapa
# --- Baixar o mapa da coordenada de cada horario para plotar
###

import datetime as dt
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

for i in range(0,24):
    lower_limit = dt.datetime(2014,2,4,i,0,0)
    upper_limit = dt.datetime(2014,2,4,i,59,59)

    df = pd.read_csv('~/Dropbox/my.folder/Pesquisa/Coding/Dados/roma_calibrated.csv')
    #print(df.loc[df['id'] == 101].long_x.min(), df.loc[df['id'] == 101].long_x.max(), df.loc[df['id'] == 101].lat_y.min(), df.loc[df['id'] == 101].lat_y.max())
    df['time'] = pd.to_datetime(df['time'])

    df2 = df.loc[(df['time'] < upper_limit) & (df['time'] > lower_limit)] #Separa as linhas com horario entre 5h e 5h59min
    #print(df2.long_x.min(), df2.long_x.max(), df2.lat_y.min(), df2.lat_y.max()) #printa os maximos e os minimos de cada eixo do DataFrame

    df2 = df2.sort_values('time')   #ordena o DataFrame por "data-hora"
    #df2 = df2.sort_values('id')   #ordena o DataFrame por "id"
    nome = './sortByTime/roma_' + str(i) + 'hTo' + str(i+1) + 'h_sorted_by_time.csv'
    df2.to_csv(nome, index = False) #salva o DataFrame para CSV

 ###
 # Printa as posicoes das coordenadas em um mapa
 ###
'''
BBox = (df2.long_x.min(),df2.long_x.max(),df2.lat_y.min(),df2.lat_y.max())
ruh_m = plt.imread('map.png') #mapa a ser usado de fundo

fig, ax = plt.subplots(figsize= (8,7))
ax.scatter(df.long_x, df.lat_y, zorder=1, alpha=0.2, c='b', s=10)
ax.set_title('Ploting all positions')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(ruh_m, zorder= 0, extent= BBox, aspect= 'equal')

plt.savefig('6-7.png')
'''
###
# Le os horarios de cada coordenada e salva aqueles entre 6h-7h
###
'''

#lower_limit = pd.Timestamp(2014,2,4,6) #limite inferior = 2014-02-04 06:00:00
#upper_limit = pd.Timestamp(2014,2,4,7) #limite superior = 2014-02-04 07:00:00

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