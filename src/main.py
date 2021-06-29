import csv
import math
import platform
import os.path
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
import geopandas
import numpy as np
from scipy.stats import norm

from ponto import Ponto

#  Lista de cores a serem utilizadas no mapa
listaCores = ['#d1432a', '#34f32a', '#ff3456']
#  dictionary com os pontos referentes a cada id
pontos = {}
#  dictionary com os intervalos de tempos entre os pontos para cada id
timeGaps = {}
#  dictionary os intervalos de distancias entre os pontos para cada id
coordGaps = {}
#  dict em que cada chave contera uma lista com os indices onde as separações devem ser feitas
separator = {}
#  lista com todos intervalos de tempo entre os pontos
allTimeGaps = []
timeGapsDiscrete = []
#  lista com todos intervalos de distancia entre os pontos
allCoordGaps = []
coordGapsDiscrete = []
#  listas dos pontos iniciais e finais de cada viagem
orig = []
dest = []

travels = []
keys = []
limitDist = 25
limitTempo = timedelta(seconds=10)

if platform.system() == 'Linux':
    path = '/home/tulionpl/Repos/Pesquisa'
else:
    path = '/Users/tuliopolido/Repos/Pesquisa'


def cdfTempo():
    """Função que plota uma cdf com os dados de distancia entre pontos de todos veículos"""

    x = [i for i in timeGapsDiscrete if i <= 100]

    #  Definição dos valores da lista
    sigma = np.std(x)
    mu = sum(x)/len(x)
    n_bins = 100

    _, ax = plt.subplots(figsize=(8, 4))

    #  Histograma cumulativo
    _, bins, _ = ax.hist(x, n_bins, density=True, histtype='step',
                         cumulative=True, label='Empírica')

    #  Distribuição esperada
    y = ((1 / (np.sqrt(2 * np.pi) * sigma))
         * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))

    y = y.cumsum()
    y /= y[-1]

    ax.plot(bins, y, 'r--', linewidth=1.5, label='Teórica')

    #  Histograma cumulativo inverso
    # ax.hist(x, bins=bins, density=True, histtype='step',
    #       cumulative=-1,label='Emp. Inversa')

    #  Detalhes do gráfico
    ax.grid(True)
    ax.legend(loc='right')
    ax.set_title('Função de Densidade Cumulativa - Tempo entre pontos')
    ax.set_xlabel('Tempo em segundos')
    ax.set_ylabel('Probabilidade cumulativa de ocorrência')

    plt.savefig(path+'/img/cdfTempo.png')
    plt.show()


def cdfDistancia():
    """Função que plota uma cdf com os dados de distancia entre pontos de todos veículos"""

    x = [i for i in coordGapsDiscrete if i <= 100]

    #  Definição dos valores da lista
    sigma = np.std(x)
    mu = sum(x)/len(x)
    n_bins = 100

    _, ax = plt.subplots(figsize=(8, 4))

    #  Histograma cumulativo
    _, bins, _ = ax.hist(x, n_bins,
                         density=True, histtype='step',
                         cumulative=True, label='Empírica')

    #  Distribuição esperada
    y = ((1 / (np.sqrt(2 * np.pi) * sigma))
         * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))

    y = y.cumsum()
    y /= y[-1]

    ax.plot(bins, y, 'r--', linewidth=1.5, label='Teórica')

    #  Histograma cumulativo inverso
    # ax.hist(x, bins=bins, density=True, histtype='step',
    #       cumulative=-1,label='Emp. Inversa')

    #  Detalhes do gráfico
    ax.grid(True)
    ax.legend(loc='right')
    ax.set_title('Função de Densidade Cumulativa - Distância entre pontos')
    ax.set_xlabel('Distância em metros')
    ax.set_ylabel('Probabilidade cumulativa de ocorrência')

    plt.savefig(path+'/img/cdfDistancia.png')
    plt.show()


def boxplotDistancia():
    """Função que plota os boxplots com os dados de distancia entre pontos de todos veículos"""

    fig1, ax1 = plt.subplots()
    ax1.set_title('Boxplot de Distância de Todos veículos')
    my_boxes = ax1.boxplot(allCoordGaps)
    plt.yscale('log')
    plt.ylabel('Distância em metros')

    #  Grab the relevant Line2D instances from the boxplot dictionary
    iqr = my_boxes['boxes'][0]
    caps = my_boxes['caps']
    med = my_boxes['medians'][0]
    fly = my_boxes['fliers'][0]

    #  The x position of the median line
    xpos = med.get_xdata()

    #  Lets make the text have a horizontal offset which is some
    #  fraction of the width of the box
    xoff = 0.10 * (xpos[1] - xpos[0])

    #  The x position of the labels
    xlabel = xpos[1] + xoff

    #  The median is the y-position of the median line
    median = med.get_ydata()[1]

    #  The 25th and 75th percentiles are found from the
    #  top and bottom (max and min) of the box
    pc25 = iqr.get_ydata().min()
    pc75 = iqr.get_ydata().max()

    #  The caps give the vertical position of the ends of the whiskers
    capbottom = caps[0].get_ydata()[0]
    captop = caps[1].get_ydata()[0]

    #  Make some labels on the figure using the values derived above
    ax1.text(xlabel, median, 'Mediana = {:6.3g}'.format(median), va='center')
    ax1.text(xlabel, pc25, '1˚ quartil = {:6.3g}'.format(pc25), va='center')
    ax1.text(xlabel, pc75, '3˚ quartil = {:6.3g}'.format(pc75), va='center')
    ax1.text(xlabel, capbottom, 'Limite Inferior = {:6.3g}'.format(
        capbottom), va='center')
    ax1.text(xlabel, captop, 'Limite Superior = {:6.3g}'.format(
        captop), va='center')
    plt.savefig(path+'/img/boxplot_distancia_geral.png', dpi=100)
    plt.show()


def boxplotTempo():
    """Função que plota os boxplots com os dados de tempo entre pontos de todos veículos"""

    fig1, ax1 = plt.subplots()
    ax1.set_title('Boxplot de Tempo de Todos veículos')
    my_boxes = ax1.boxplot(allTimeGaps)
    plt.yscale('log')
    plt.ylabel('Tempo em segundos')

    #  Grab the relevant Line2D instances from the boxplot dictionary
    iqr = my_boxes['boxes'][0]
    caps = my_boxes['caps']
    med = my_boxes['medians'][0]
    fly = my_boxes['fliers'][0]

    #  The x position of the median line
    xpos = med.get_xdata()

    #  Lets make the text have a horizontal offset which is some
    #  fraction of the width of the box
    xoff = 0.10 * (xpos[1] - xpos[0])

    #  The x position of the labels
    xlabel = xpos[1] + xoff

    #  The median is the y-position of the median line
    median = med.get_ydata()[1]

    #  The 25th and 75th percentiles are found from the
    #  top and bottom (max and min) of the box
    pc25 = iqr.get_ydata().min()
    pc75 = iqr.get_ydata().max()

    #  The caps give the vertical position of the ends of the whiskers
    capbottom = caps[0].get_ydata()[0]
    captop = caps[1].get_ydata()[0]

    #  Make some labels on the figure using the values derived above
    ax1.text(xlabel, median, 'Mediana = {:6.3g}'.format(median), va='center')
    ax1.text(xlabel, pc25, '1˚ quartil = {:6.3g}'.format(pc25), va='center')
    ax1.text(xlabel, pc75, '3˚ quartil = {:6.3g}'.format(pc75), va='center')
    ax1.text(xlabel, capbottom, 'Limite inferior = {:6.3g}'.format(
        capbottom), va='center')
    ax1.text(xlabel, captop, 'Limite Superior = {:6.3g}'.format(
        captop), va='center')
    plt.savefig(path+'/img/boxplot_tempo_geral.png', dpi=100)
    plt.show()


def tempoDoisPontos(i, j, pontos):
    """Função para calcular o tempo entre dois pontos

    Argumentos:
    i -- Posição do primeiro ponto
    j -- Posição do segundo ponto
    pontos -- lista de pontos
    """

    ponto1 = pontos[i]
    ponto2 = pontos[j]
    pointTime = ponto1.pointData['Hora']
    pointTime = datetime.strptime(pointTime, '%Y-%d-%m %H:%M:%S')
    pointTime2 = ponto2.pointData['Hora']
    pointTime2 = datetime.strptime(pointTime2, '%Y-%d-%m %H:%M:%S')

    tempo = pointTime2-pointTime

    return tempo


def distDoisPontos(i, j, pontos):
    """Função para calcular a distância entre dois pontos"""

    dist = 0

    for k in range(i, j):
        point1 = pontos[k]
        point2 = pontos[k+1]

        pointCoord1 = point1.pointData['Coord']
        pointCoord2 = point2.pointData['Coord']

        dist += convertHaversine(pointCoord1[0],
                                 pointCoord1[1], pointCoord2[0], pointCoord2[1])

    return dist


def convertHaversine(x1, y1, x2, y2):
    """Função para converter coordenadas geográficas para distância 
        em metros utilizando o algoritmo de Haversine

        x1 -- Latitude do ponto 1
        y1 -- Longitude do ponto 1
        x2 -- Latitude do ponto 2
        y2 -- Longitude do ponto 2
    """

    R = 6378.137
    dLat = x2 * math.pi / 180 - x1 * math.pi / 180
    dLon = y2 * math.pi / 180 - y1 * math.pi / 180

    a = (math.sin(dLat/2) * math.sin(dLat/2) + math.cos(x1 * math.pi / 180)
         * math.cos(x2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2))

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    return d * 1000  # retorna o valor em metros


def histTempo():
    """Função para plotar um histograma dos tempos entre pontos consecutivos"""

    plt.hist(allTimeGaps, bins=1000)
    plt.title('Histograma: Tempo entre pontos')
    plt.yscale('log')
    plt.xlabel('Tempo em segundos')
    plt.ylabel('Quantidade em log')
    plt.savefig(path+'/img/histTempo.png', dpi=100)
    plt.show()


def histDistancia():
    """Função para plotar um histograma das distâncias entre pontos consecutivos"""

    plt.hist(allCoordGaps, bins=1000)
    plt.title('Histograma: Distancia entre pontos')
    plt.yscale('log')
    plt.xlabel('Distância em metros')
    plt.ylabel('Quantidade em log')
    plt.savefig(path+'/img/histDistancia.png', dpi=100)
    plt.show()


def printaCorridas():
    """Função para plotar as corridas de um ID selecionado em um mapa."""

    print("\n" + str(keys))
    veic = int(input("Selecione um ID da lista acima ou 0 para sair: "))
    strveic = str(veic)

    while veic != 0:
        if strveic in keys:
            df = pd.read_csv(path+"/data/roma_calibrated_sorted.csv")
            df = df.loc[df['id'] == veic]

            #  Pegar Max e Min das coordenadas geograficas
            BBox = BBox = (df.long_x.min(), df.long_x.max(),
                           df.lat_y.min(), df.lat_y.max())

            #  Se a imagem de fundo existir, iterar entre os pontos da lista
            #  de paradas e printar todas coordenadas entre i e i+1
            if os.path.exists(path+'/img/backmaps/trackmap_id_' + str(veic) + '.png'):
                ruh_m = plt.imread(
                    path+'/img/backmaps/trackmap_id_' + str(veic) + '.png')
                fig, ax = plt.subplots()

                cor = 0
                for i in range(len(separator[strveic])-1):
                    inicio = int(separator[strveic][i])
                    fim = int(separator[strveic][i+1])
                    caminho = df.iloc[inicio:fim+1]

                    longitudes = caminho['long_x'].to_numpy()
                    latitudes = caminho['lat_y'].to_numpy()

                    ax.scatter(longitudes, latitudes, zorder=0.3,
                               alpha=0.3, c=listaCores[cor], s=2)
                    cor += 1
                    if cor > 2:
                        cor = 0

                ax.set_xlim(BBox[0], BBox[1])
                ax.set_ylim(BBox[2], BBox[3])
                ax.imshow(ruh_m, zorder=0, extent=BBox, aspect='equal')
                ax.tick_params(labelsize=8)
                plt.tight_layout(pad=0)
                plt.savefig(path+"/img/trackmap_id_"+str(veic)+".png", dpi=200)
                plt.close()

            #  Se a imagem nao existir printar os Max e Min das coordenadas
            #  e pedir ao usuario para criar a imagem
            else:
                print('Por favor crie o backmap com as seguintes coordenadas: ')
                print(BBox)
                print('Depois salve o arquivo no path: ' + path
                      + '/img/backmaps/trackmap_id_' + str(veic) + '.png')
        else:
            print("O ID nao existe")

        print("\n" + str(keys))
        veic = int(input("Selecione outro ID da lista acima ou 0 para sair: "))


def stayPoint_Detection():
    """Algoritmo para detecção de paradas"""

    print('\nColetando pontos de parada...')
    for key in keys:
        separator[key] = []
        numPontos = len(pontos[key])

        i = 0
        while i < numPontos-1:
            dist = distDoisPontos(i, i+1, pontos[key])

            if dist > limitDist:
                tempo = tempoDoisPontos(i, i+1, pontos[key])

                if tempo > limitTempo:
                    separator[key].append(i)
            i += 1

        separator[key].append(numPontos-1)  # Adiciona ponto final
    print('Pronto!')


def atualizarDados():
    """Função para ler a base de dados original e calcular as variações de tempo e distâncias"""

    tags = []
    teste = keys.copy()
    keys.clear()
    allCoordGaps.clear()
    allTimeGaps.clear()
    with open(path+'/data/roma_calibrated_sorted.csv') as file:
        reader = csv.DictReader(file)

        line = reader.__next__()
        tag = line["id"]
        keys.append(line["id"])

        #  cria uma lista onde serao adicionados os pontos de cada id
        pontos[tag] = []
        print('Lendo banco de dados...')

        #  Ciclo que percorre todas as linhas, le os pontos e
        #  os salva nos respectivos ids no Dictionary
        for line in reader:
            tags.append(line['id'])
            if tag != line['id']:  # Quando a tag for modificada, cria uma nova key
                tag = line['id']
                pontos[tag] = []
                keys.append(line['id'])

            coord = (float(line['lat_y']), float(line['long_x']))
            hour = line['time']

            #  Cria uma nova instancia de Ponto
            pnt = {}
            pnt['Hora'] = hour
            pnt['Coord'] = coord
            newInstance = Ponto(pnt)

            pontos[tag].append(newInstance)
        print('Pronto!')

        print('Calculando distâncias e tempos...')
        #  for que percorre cada key no dict
        for key, value in pontos.items():
            timeGaps[key] = []
            coordGaps[key] = []

            #  for que percorre cada valor presente na key
            for i in range(len(value)-1):
                point1 = value[i]
                point2 = value[i+1]

                pointCoord1 = point1.pointData['Coord']
                pointCoord2 = point2.pointData['Coord']

                #  converte string para datahora
                pointTime = point1.pointData['Hora']
                pointTime = datetime.strptime(pointTime, '%Y-%d-%m %H:%M:%S')
                pointTime2 = point2.pointData['Hora']
                pointTime2 = datetime.strptime(pointTime2, '%Y-%d-%m %H:%M:%S')

                timeGap = pointTime2-pointTime
                timeGaps[key].append(timeGap.total_seconds())
                allTimeGaps.append(timeGap.total_seconds())

                coordGaps[key].append(convertHaversine(pointCoord1[0], pointCoord1[1],
                                                       pointCoord2[0], pointCoord2[1]))
                allCoordGaps.append(convertHaversine(pointCoord1[0], pointCoord1[1],
                                                     pointCoord2[0], pointCoord2[1]))

    print('Salvando dados...')
    with open(path+'/data/ids.txt', 'w') as file:
        file.seek(0)
        for tag in tags:
            file.write('%s\n' % tag)
        file.truncate()

    with open(path+'/data/hora.txt', 'w') as file:
        file.seek(0)
        for key in keys:
            for line in pontos[key]:
                file.write('%s\n' % line.pointData['Hora'])
        file.truncate()

    with open(path+'/data/coordenadas.txt', 'w') as file:
        file.seek(0)
        for key in keys:
            for line in pontos[key]:
                file.write('%s\n' % str(line.pointData['Coord']))
        file.truncate()

    with open(path+'/data/timeGaps.txt', 'w') as file:
        file.seek(0)
        for line in allTimeGaps:
            file.write('%f\n' % line)
        file.truncate()

    with open(path+'/data/coordGaps.txt', 'w') as file:
        file.seek(0)
        for line in allCoordGaps:
            file.write('%.16f\n' % line)
        file.truncate()

    with open(path+'/data/keys.txt', 'w') as file:
        file.seek(0)
        for line in keys:
            file.write('%s\n' % line)
        file.truncate()
    print('Pronto!')


def lerDados():
    """Função para ler a base de dados com os valores ja calculados"""

    print('Lendo dados...')
    with open(path+'/data/timeGaps.txt', 'r') as file:
        allTimeGaps = list(map(float, file.readlines())).copy()

    with open(path+'/data/coordGaps.txt', 'r') as file:
        allCoordGaps = list(map(float, file.readlines())).copy()

    with open(path+'/data/keys.txt', 'r') as file:
        keys = list(map(str, file.readlines())).copy()
        keys = list(map(str.strip, keys)).copy()

    timeGapsDiscrete = list(map(int, allTimeGaps)).copy()
    coordGapsDiscrete = list(map(int, allCoordGaps)).copy()

    #  le arquivo com a lista de sequencia de ids
    with open(path+'/data/ids.txt', 'r') as file:
        ids = list(map(str, file.readlines())).copy()
        ids = list(map(str.strip, ids)).copy()

    #  le arquivo com a lista de sequencia de coordenadas
    with open(path+'/data/coordenadas.txt', 'r') as file:
        crds = list(map(str, file.readlines())).copy()
        crds = list(map(str.strip, crds)).copy()
        crds = list(map(eval, crds)).copy()

    #  le arquivo com a lista de sequencia de horas
    with open(path+'/data/hora.txt', 'r') as file:
        hrs = list(map(str, file.readlines())).copy()
        hrs = list(map(str.strip, hrs)).copy()

    #  inicializa o dict de pontos com uma lista para cada id
    for id in ids:
        pontos[id] = []

    for i in range(0, len(hrs)):
        pnt = {}
        pnt['Hora'] = hrs[i]
        pnt['Coord'] = crds[i]
        newInstance = Ponto(pnt)
        pontos[ids[i]].append(newInstance)

    print('Pronto!')

    return allTimeGaps, allCoordGaps, timeGapsDiscrete, coordGapsDiscrete, keys, pontos


def matrixOD():
    """Função que cria a matriz de origem de destino definindo um grid no mapa"""
    if (len(orig) == 0 or len(dest) == 0):
        print("\nColetando dados de origem e destino...")
        getOD()
        print("Pronto!")
    #  Juntar orig e dest em 1 unico dataframe
    df_origin = pd.DataFrame(columns=['x', 'y'])
    df_destiny = pd.DataFrame(columns=['x', 'y'])

    for pnt in orig:
        df_origin = df_origin.append({'x': pnt.pointData['Coord'][0],
                                      'y': pnt.pointData['Coord'][1]},
                                     ignore_index=True)

    for pnt in dest:
        df_destiny = df_destiny.append({'x': pnt.pointData['Coord'][0],
                                        'y': pnt.pointData['Coord'][1]},
                                       ignore_index=True)

    df_union = pd.concat([df_origin, df_destiny])

    #  Transformar os DataFrames para GeoDataFrame
    '''
    gdf_origin = geopandas.GeoDataFrame(df_origin, geometry=geopandas.points_from_xy(df_origin.x, df_origin.y),
                                        crs=4326)

    gdf_origin = gdf_origin.drop(columns=['x', 'y'])

    gdf_destiny = geopandas.GeoDataFrame(df_destiny,
                                         geometry=geopandas.points_from_xy(
                                             df_destiny.x, df_destiny.y),
                                         crs="+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs")

    gdf_destiny = gdf_destiny.drop(columns=['x', 'y'])
    gdf_origin.plot(markersize=.1, figsize=(8, 8))
    print(gdf_origin)'''

    #  Criar os limites para a area de exibicao baseado nos dados do dataframe
    limits = (df_union.x.min(), df_union.x.max(),
              df_union.y.min(), df_union.y.max())

    #  Dividir a area em um grid

    sizeX = (limits[1] - limits[0]) / 15 #  largura de cada grid
    sizeY = (limits[3] - limits[2]) / 10.2 #  altura de cada grid

    #  Como representar o grid numa estrutura de dados? <<<<<<< EIS A QUESTAO

    #Criar vetores com os intervalos onde ficarão cada linha do grid

    #  Plotar o grid
    #  Plotar os pontos
    #  Colocar o mapa de Roma de fundo


def getOD():
    """Função para calcular os pontos iniciais e finais de cada viagem"""

    for key in keys:
        lastPos = len(pontos[key]) - 1

        pt = pontos[key][0]
        orig.append(pt)

        for i in range(len(separator[key])-1):
            intervalo = separator[key][i]
            dest.append(pontos[key][intervalo])
            orig.append(pontos[key][intervalo+1])

        pt = pontos[key][lastPos]
        dest.append(pt)


#  Driver
allTimeGaps, allCoordGaps, timeGapsDiscrete, coordGapsDiscrete, keys, pontos = lerDados()
stayPoint_Detection()
matrixOD()
'''
print("\nMenu:\n \
    (0)Sair\n \
    (1)Gerar Histograma de Tempo\n \
    (2)Gerar Histograma de Distância\n \
    (3)Plotar as viagens de um ID\n \
    (4)Gerar boxplot de tempo\n \
    (5)Gerar boxplot de distância\n \
    (6)Gerar CDF de distância\n \
    (7)Gerar CDF de tempo\n \
    (8)Gerar matrix OD \
    (9)Atualizar dados")
resp = int(input("Digite sua opção: "))
print()

while(resp != 0):
    if resp == 1:
        histTempo()
    elif resp == 2:
        histDistancia()
    elif resp == 3:
        printaCorridas()
    elif resp == 4:
        boxplotTempo()
    elif resp == 5:
        boxplotDistancia()
    elif resp == 6:
        cdfDistancia()
    elif resp == 7:
        cdfTempo()
    elif resp == 8:
        getOD()
    elif resp == 9:
        atualizarDados()

    print("\nMenu:\n \
    (0)Sair\n \
    (1)Gerar Histograma de Tempo\n \
    (2)Gerar Histograma de Distância\n \
    (3)Plotar as viagens de um ID\n \
    (4)Gerar boxplot de tempo\n \
    (5)Gerar boxplot de distância\n \
    (6)Gerar CDF de distância\n \
    (7)Gerar CDF de tempo\n \
    (8)Gerar matrix OD \
    (9)Atualizar dados")
    resp = int(input("Digite sua opção: "))
    print()'''
