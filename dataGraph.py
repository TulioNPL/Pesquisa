######
# Printa um grafo do ID 101
######

import csv
import networkx as nx
import matplotlib.pyplot as plt

with open('./Dados/roma_calibrated.csv') as file:
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