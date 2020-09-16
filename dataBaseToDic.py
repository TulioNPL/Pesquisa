#####
# Converte os dados para dictionary
#####
from datetime import datetime
from datetime import timedelta
from ponto import Ponto
import csv
import math
import matplotlib.pyplot as plt

pontos = {} #dictionary com os pontos referentes a cada id
timeGaps = {} #dictionary com os intervalos de tempos entre os pontos para cada id
coordGaps = {} #dictionary os intervalos de distancias entre os pontos para cada id
allTimeGaps = [] #lista com todos intervalos de tempo entre os pontos
allCoordGaps = [] #lista com todos intervalos de distancia entre os pontos
travels = [] #lista de viagens
keys = [] #lista dos ids
limitDist = 5
limitTempo = timedelta(minutes=10)

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

    lerDados()
    plt.hist(allTimeGaps, bins=1000)
    plt.title('Histograma: Tempo entre pontos')
    plt.yscale('log')
    plt.xlabel('Tempo em segundos')
    plt.ylabel('Quantidade')
    plt.savefig('./graficos/histTempo.png',dpi=400)
    plt.show()

def histDistancia():
    """Função para plotar um histograma das distâncias entre pontos consecutivos"""

    lerDados()
    plt.hist(allCoordGaps, bins=1000)
    plt.title('Histograma: Distancia entre pontos')
    plt.yscale('log')
    plt.xlabel('Distância em metros')
    plt.ylabel('Quantidade')
    plt.savefig('./graficos/histDistancia.png',dpi=400)
    plt.show()

def stayPoint_Detection():
    """Algoritmo para detecção de paradas"""

    lerDados()
    separator = {} #dict em que cada chave contera uma lista com os indices onde as separações devem ser feitas

    print('Coletando pontos de parada...')
    for key in keys:
        separator[key] = []
        numPontos = len(pontos[key])
        print('Key = ' + str(key))

        i = 0
        while i < numPontos:
            j = i + 1
            while j < numPontos:      
                dist =  distDoisPontos(i,j,pontos[key])
                if dist > limitDist: 
                    tempo = tempoDoisPontos(i,j,pontos[key])  
                    
                    if tempo > limitTempo: #criar limite de tempo com dateTime
                        print(tempo)
                        print(str(i) + ' -> ' + str(j) + '    ||||    Tempo: ' + str(tempo)) #teste
                        ### CRIAR NOVO PONTO DE PARADA E INSERIR NA LISTA
                    
                    i = j    
                    j = numPontos #forca a parada do ciclo
                j = j + 1
            
            if j == numPontos:
                i = numPontos
    print('Pronto!')

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

print("Digite: (1)Gerar Histograma de Tempo     (2)Gerar Histograma de Distância   (3)Gerar lista de paradas")
resp = int(input())
if resp == 1:
    histTempo()
elif resp == 2:
    histDistancia()
elif resp == 3:
    stayPoint_Detection()