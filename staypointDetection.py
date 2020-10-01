#####
# Converte os dados para dictionary
#####
from datetime import datetime
from datetime import timedelta
from ponto import Ponto
import csv
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os.path

listaCores = ['#d1432a','#34f32a','#ff3456','#003456']
pontos = {} #dictionary com os pontos referentes a cada id
timeGaps = {} #dictionary com os intervalos de tempos entre os pontos para cada id
coordGaps = {} #dictionary os intervalos de distancias entre os pontos para cada id
separator = {} #dict em que cada chave contera uma lista com os indices onde as separações devem ser feitas
allTimeGaps = [] #lista com todos intervalos de tempo entre os pontos
allCoordGaps = [] #lista com todos intervalos de distancia entre os pontos
travels = [] #lista de viagens
keys = [] #lista dos ids
limitDist = 21
limitTempo = timedelta(seconds=2)

def boxplotDistancia():
    """Função que plota os boxplots de todos veículos"""

    fig1, ax1 = plt.subplots()
    ax1.set_title('Boxplot de Distância de Todos veículos')
    my_boxes = ax1.boxplot(allCoordGaps)
    plt.yscale('log')
    plt.ylabel('Distância em metros')

    # Grab the relevant Line2D instances from the boxplot dictionary
    iqr = my_boxes['boxes'][0]
    caps = my_boxes['caps']
    med = my_boxes['medians'][0]
    fly = my_boxes['fliers'][0]

    # The x position of the median line
    xpos = med.get_xdata()

    # Lets make the text have a horizontal offset which is some 
    # fraction of the width of the box
    xoff = 0.10 * (xpos[1] - xpos[0])

    # The x position of the labels
    xlabel = xpos[1] + xoff

    # The median is the y-position of the median line
    median = med.get_ydata()[1]

    # The 25th and 75th percentiles are found from the
    # top and bottom (max and min) of the box
    pc25 = iqr.get_ydata().min()
    pc75 = iqr.get_ydata().max()

    # The caps give the vertical position of the ends of the whiskers
    capbottom = caps[0].get_ydata()[0]
    captop = caps[1].get_ydata()[0]

    # Make some labels on the figure using the values derived above
    ax1.text(xlabel, median,'Mediana = {:6.3g}'.format(median), va='center')
    ax1.text(xlabel, pc25,'1˚ quartil = {:6.3g}'.format(pc25), va='center')
    ax1.text(xlabel, pc75,'3˚ quartil = {:6.3g}'.format(pc75), va='center')
    ax1.text(xlabel, capbottom,'Limite Inferior = {:6.3g}'.format(capbottom), va='center')
    ax1.text(xlabel, captop,'Limite Superior = {:6.3g}'.format(captop), va='center')
    plt.savefig('./graficos/Boxplots_distancias/boxplot_distancia_geral.png',dpi=400)
    plt.show()

def boxplotTempo():
    """Função que plota os boxplots de todos veículos"""

    fig1, ax1 = plt.subplots()
    ax1.set_title('Boxplot de Tempo de Todos veículos')
    my_boxes = ax1.boxplot(allTimeGaps)
    plt.yscale('log')
    plt.ylabel('Tempo em segundos')

     # Grab the relevant Line2D instances from the boxplot dictionary
    iqr = my_boxes['boxes'][0]
    caps = my_boxes['caps']
    med = my_boxes['medians'][0]
    fly = my_boxes['fliers'][0]

    # The x position of the median line
    xpos = med.get_xdata()

    # Lets make the text have a horizontal offset which is some 
    # fraction of the width of the box
    xoff = 0.10 * (xpos[1] - xpos[0])

    # The x position of the labels
    xlabel = xpos[1] + xoff

    # The median is the y-position of the median line
    median = med.get_ydata()[1]

    # The 25th and 75th percentiles are found from the
    # top and bottom (max and min) of the box
    pc25 = iqr.get_ydata().min()
    pc75 = iqr.get_ydata().max()

    # The caps give the vertical position of the ends of the whiskers
    capbottom = caps[0].get_ydata()[0]
    captop = caps[1].get_ydata()[0]

    # Make some labels on the figure using the values derived above
    ax1.text(xlabel, median,'Mediana = {:6.3g}'.format(median), va='center')
    ax1.text(xlabel, pc25,'1˚ quartil = {:6.3g}'.format(pc25), va='center')
    ax1.text(xlabel, pc75,'3˚ quartil = {:6.3g}'.format(pc75), va='center')
    ax1.text(xlabel, capbottom,'Limite inferior = {:6.3g}'.format(capbottom), va='center')
    ax1.text(xlabel, captop,'Limite Superior = {:6.3g}'.format(captop), va='center')
    plt.savefig('./graficos/Boxplots_tempo/boxplot_tempo_geral.png',dpi=400)
    plt.show()

def tempoDoisPontos(i,j,pontos):
    """Função para calcular o tempo entre dois pontos"""

    ponto1 = pontos[i]
    ponto2 = pontos[j]
    pointTime = ponto1.pointData['Hora']
    pointTime = datetime.strptime(pointTime,'%Y-%d-%m %H:%M:%S')
    pointTime2 = ponto2.pointData['Hora']
    pointTime2 = datetime.strptime(pointTime2,'%Y-%d-%m %H:%M:%S')

    tempo = pointTime2-pointTime

    return tempo

def distDoisPontos(i,j,pontos):
    """Função para calcular a distância entre dois pontos"""

    dist = 0

    for k in range(i,j):
        point1 = pontos[k]
        point2 = pontos[k+1]

        pointCoord1 = point1.pointData['Coord']
        pointCoord2 = point2.pointData['Coord']

        dist += convertHaversine(pointCoord1[0],pointCoord1[1],pointCoord2[0],pointCoord2[1])

    return dist

def convertHaversine(x1,y1,x2,y2):
    """Função para converter coordenadas geográficas para distância em metros utilizando o algoritmo de Haversine"""

    R = 6378.137
    dLat = x2 * math.pi / 180 - x1 * math.pi / 180
    dLon = y2 * math.pi / 180 - y1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(x1 * math.pi / 180) * math.cos(x2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    return d* 1000 #retorna o valor em metros

def histTempo():
    """Função para plotar um histograma dos tempos entre pontos consecutivos"""

    plt.hist(allTimeGaps, bins=1000)
    plt.title('Histograma: Tempo entre pontos')
    plt.yscale('log')
    plt.xlabel('Tempo em segundos')
    plt.ylabel('Quantidade')
    plt.savefig('./graficos/histTempo.png',dpi=400)
    plt.show()

def histDistancia():
    """Função para plotar um histograma das distâncias entre pontos consecutivos"""

    plt.hist(allCoordGaps, bins=1000)
    plt.title('Histograma: Distancia entre pontos')
    plt.yscale('log')
    plt.xlabel('Distância em metros')
    plt.ylabel('Quantidade')
    plt.savefig('./graficos/histDistancia.png',dpi=400)
    plt.show()

def printaCorridas():
    print("\n" + str(keys))
    veic = int(input("Selecione um ID da lista acima: "))
    strveic = str(veic)

    if strveic in keys:
        df = pd.read_csv("./roma_calibrated_sorted.csv")
        df = df.loc[df['id'] == veic]

        BBox = BBox = (df.long_x.min(),df.long_x.max(),df.lat_y.min(),df.lat_y.max())

        if os.path.exists('./graficos/backmaps/trackmap_id_'+ str(veic) +'.png'):
            ruh_m = plt.imread('./graficos/backmaps/trackmap_id_'+ str(veic) +'.png')
            fig, ax = plt.subplots()

            cor = 0
            for i in range(len(separator[strveic])-1):
                inicio = int(separator[strveic][i])
                fim = int(separator[strveic][i+1])
                caminho = df.iloc[inicio:fim+1]

                longitudes = caminho['long_x'].to_numpy()
                latitudes = caminho['lat_y'].to_numpy()

                ax.scatter(longitudes, latitudes, zorder=0.3, alpha=0.3, c=listaCores[cor], s=2)
                cor +=1 
                if cor > 3:
                    cor = 0
            ax.set_xlim(BBox[0],BBox[1])
            ax.set_ylim(BBox[2],BBox[3])
            ax.imshow(ruh_m,zorder= 0, extent= BBox, aspect= 'equal')
            ax.tick_params(labelsize=8)
            plt.tight_layout(0) 
            plt.savefig("./graficos/trackmap_id_"+str(veic)+".png", dpi=400)
            plt.close()          

        #Se a imagem de fundo existir, iterar entre os pontos da lista de paradas e printar todas coordenadas entre i e i+1
        #Pegar Max e Min das coordenadas geograficas
        #Se a imagem nao existir printar os Max e Min das coordenadas e pedir ao usuario para criar a imagem
        else:
            print('Por favor crie o backmap com as seguintes coordenadas: ')
            print(BBox)
            print('Depois salve o arquivo no path: ' + './graficos/backmaps/trackmap_id_'+ str(veic) +'.png')
    else:
        print("O ID nao existe")

def stayPoint_Detection():
    """Algoritmo para detecção de paradas"""
    
    print('\nColetando pontos de parada...')
    for key in keys:
        separator[key] = []
        numPontos = len(pontos[key])
        
        i = 0
        while i < numPontos:
            j = i + 1
            while j < numPontos:      
                dist =  distDoisPontos(i,j,pontos[key])
                if dist > limitDist: 
                    tempo = tempoDoisPontos(i,j,pontos[key])  
                    
                    if tempo > limitTempo:
                       separator[key].append(i)

                    i = j    
                    j = numPontos #forca a parada do ciclo
                j = j + 1
            
            if j == numPontos:
                i = numPontos
        separator[key].append(numPontos-1) #Adiciona ponto final
    print('Pronto!')
    printaCorridas()

def lerDados():
    """Função para ler a base de dados e calcular as variações de tempo e distâncias"""

    with open('./roma_calibrated_sorted.csv') as file:
    #with open('./sortById/roma_12hTo13h_sorted_by_id.csv') as file:
        reader = csv.DictReader(file)

        line = reader.__next__() #le a primeira linha
        tag = line['id']
        keys.append(line['id'])

        pontos[tag] = [] #cria uma lista onde serao adicionados os pontos de cada id
        print('Lendo banco de dados...')

        #Ciclo que percorre todas as linhas, le os pontos e os salva nos respectivos ids no Dictionary
        for line in reader:
            if tag != line['id']: #Quando a tag for modificada, cria uma nova key
                tag = line['id']
                pontos[tag] = []
                keys.append(line['id'])

            coord = (float(line['lat_y']),float(line['long_x']))
            hour = line['time']

            #Cria uma nova instancia de Ponto
            pnt = {}
            pnt['Hora'] = hour
            pnt['Coord'] = coord
            newInstance = Ponto(pnt)
            
            pontos[tag].append(newInstance)
        print('Pronto!')
        print('Calculando distâncias e tempos...')

        #for que percorre cada key no dict
        for key,value in pontos.items():
            timeGaps[key] = []
            coordGaps[key] = []

            #for que percorre cada valor presente na key
            for i in range(len(value)-1):
                point1 = value[i]
                point2 = value[i+1]

                pointCoord1 = point1.pointData['Coord']
                pointCoord2 = point2.pointData['Coord']

                pointTime = point1.pointData['Hora']
                pointTime = datetime.strptime(pointTime,'%Y-%d-%m %H:%M:%S') #converte string para datahora
                pointTime2 = point2.pointData['Hora']
                pointTime2 = datetime.strptime(pointTime2,'%Y-%d-%m %H:%M:%S')

                timeGap = pointTime2-pointTime
                timeGaps[key].append(timeGap.total_seconds())
                allTimeGaps.append(timeGap.total_seconds())

                coordGaps[key].append(convertHaversine(pointCoord1[0],pointCoord1[1],pointCoord2[0],pointCoord2[1]))
                allCoordGaps.append(convertHaversine(pointCoord1[0],pointCoord1[1],pointCoord2[0],pointCoord2[1]))
        print('Pronto!')

#Driver
lerDados()
print("\nMenu:\n (0)Sair\n (1)Gerar Histograma de Tempo\n (2)Gerar Histograma de Distância\n (3)Gerar lista de paradas\n (4)Gerar boxplot de tempo\n (5)Gerar boxplot de distância")
resp = int(input("Digite sua opção: "))

while(resp != 0):
    if resp == 1:
        histTempo()
    elif resp == 2:
        histDistancia()
    elif resp == 3:
        stayPoint_Detection()
    elif resp == 4:
        boxplotTempo()
    elif resp == 5:
        boxplotDistancia()
    print("\nDigite:\n (0)Sair\n (1)Gerar Histograma de Tempo\n (2)Gerar Histograma de Distância\n (3)Gerar lista de paradas\n (4)Gerar boxplot de tempo\n (5)Gerar boxplot de distância")
    resp = int(input())