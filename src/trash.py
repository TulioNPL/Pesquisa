###
# Arquivo de códigos lixo que podem vir a ser úteis no futuro
###
''' dataBaseToDic.py: ______________________________________________________________________________
    #ciclo para gerar os indices onde as viagens de cada key serão divididas
    for key in keys:
        flag = False #Se true, entao o tempo decorrido permite a criacao de uma nova trip
        tempo = 0
        separator[key] = []

        if(len(coordGaps[key]) > 0): #confere se o vetor não está vazio
            for i in range(0,len(coordGaps[key])-1): 
                if(timeGaps[key][i] != 0): #confere se o tempo de gravação entre dois pontos não é zero
                    if(coordGaps[key][i]/timeGaps[key][i] < 0.1):
                        tempo += timeGaps[key][i]
                    else:
                        if(flag):
                            separator[key].append(i)
                            flag = False
                            tempo = 0
                        else:
                            tempo = 0
                            flag = False

                    if(tempo > 30.0):
                        flag = True

        print('\n'+ key + ': ', end='')
        print(separator[key])
'''

'''Haversine Test ______________________________________________________________________________________________
import math

def convertHaversine(x1,y1,x2,y2):
    R = 6378.137
    dLat = x2 * math.pi / 180 - x1 * math.pi / 180
    dLon = y2 * math.pi / 180 - y1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(x1 * math.pi / 180) * math.cos(x2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    return d* 1000 #retorna o valor em metros

lat1 = -19.881364
long1 = -43.922003
lat2 = -19.878815
long2 = -43.926031

print("Distância de acordo com Google Maps: 500 metros")
print(convertHaversine(lat1,long1,lat2,long2))'''

''' _________________________________________________________________________________________________________________
######
# Printa um grafo do ID 101
######

import csv
import networkx as nx
import matplotlib.pyplot as plt

with open('./data/roma_calibrated.csv') as file:
    reader = csv.DictReader(file) 
    g = nx.Graph() #grafo g
    pos = [] #lista de pares ordenados
    
    row = reader.__next__()
    tag = row['id']

    i = 0 #contador de vertices
    for row in reader:
        if row['id'] == tag:  
            g.add_node(i) #adiciona vertice da posicao atual
            if i > 0:
                g.add_edge(i-1,i) #adiciona arestas entre a posicao atual e a anterior
            pos.append([float(row['long_x']),float(row['lat_y'])])  #add a latitude e longitude como pares ordenados convertendo para float
            i += 1
        else:
            nx.draw(g, pos,node_size=5, edge_labels=True) #Desenha o grafo
            plt.savefig(str(tag)+".jpg",format='jpg') #Salva o grafo como JPG
            #plt.show()
            i = 0
            g = nx.Graph()

        tag = row['id']
'''

'''dfSort.py_____________________________________________________________________________________________________________________
import datetime as dt
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

###
# Separa o csv em diversos arquivos menores pela hora do dia e ordena por data-hora ou id
###

for i in range(0,24):
    lower_limit = dt.datetime(2014,2,4,i,0,0)
    upper_limit = dt.datetime(2014,2,4,i,59,59)

    df = pd.read_csv('~/Dropbox/my.folder/Pesquisa/Coding/Dados/roma_calibrated.csv')
    #print(df.loc[df['id'] == 101].long_x.min(), df.loc[df['id'] == 101].long_x.max(), df.loc[df['id'] == 101].lat_y.min(), df.loc[df['id'] == 101].lat_y.max())
    df['time'] = pd.to_datetime(df['time'])

    df2 = df.loc[(df['time'] < upper_limit) & (df['time'] > lower_limit)] #Separa as linhas com horario entre 5h e 5h59min
    #print(df2.long_x.min(), df2.long_x.max(), df2.lat_y.min(), df2.lat_y.max()) #printa os maximos e os minimos de cada eixo do DataFrame

    #df2 = df2.sort_values('time')   #ordena o DataFrame por "data-hora"
    df2 = df2.sort_values(['id','time'])   #ordena o DataFrame por "id"
    nome = './sortById/roma_' + str(i) + 'hTo' + str(i+1) + 'h_sorted_by_id.csv'
    df2.to_csv(nome, index = False) #salva o DataFrame para CSV

###
#   Ordena o csv em horario e id
###

df = pd.read_csv('~/Dropbox/my.folder/Pesquisa/Coding/Dados/roma_calibrated.csv')
df['time'] = pd.to_datetime(df['time'])
df = df.sort_values(['id','time'])
df.to_csv('./data/roma_calibrated_sorted.csv', index = False)
''' 