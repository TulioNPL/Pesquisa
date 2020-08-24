#####
# Converte os dados para dictionary
#####
from datetime import datetime
from datetime import timedelta
from ponto import Ponto
import csv
import math
import matplotlib.pyplot as plt

newDict = {}
maxDelta = timedelta(hours=0,minutes=0,seconds=30)
timeGaps = {} #lista com os intervalos de tempos entre os pontos
coordGaps = {} #lista com os intervalos de distancias entre os pontos
allTimeGaps = []
allCoordGaps = []
travels = [] #lista de viagens
keys = [] #lista dos ids

def convertHaversine(x1,y1,x2,y2):
    R = 6378.137
    dLat = x2 * math.pi / 180 - x1 * math.pi / 180
    dLon = y2 * math.pi / 180 - y1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(x1 * math.pi / 180) * math.cos(x2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    return d* 1000 #retorna o valor em metros

def histTempo(allTimeGaps):
    print(max(allTimeGaps))
    print(min(allTimeGaps))
    plt.hist(allTimeGaps, bins=1000)
    plt.yscale('log')
    plt.show()

def histDistancia(allCoordGaps):
    plt.hist(allCoordGaps, bins=1000)
    plt.yscale('log')
    plt.show()

with open('./roma_calibrated_sorted.csv') as file:
#with open('./sortById/roma_12hTo13h_sorted_by_id.csv') as file:
    reader = csv.DictReader(file)

    line = reader.__next__() #le a primeira linha
    tag = line['id']
    keys.append(line['id'])

    newDict[tag] = [] #cria uma lista onde serao adicionados os pontos de cada id
    
    #Ciclo que percorre todas as linhas, le os pontos e os salva nos respectivos ids no Dictionary
    for line in reader:
        if tag != line['id']: #Quando a tag for modificada, cria uma nova key
            tag = line['id']
            newDict[tag] = []
            keys.append(line['id'])

        coord = (float(line['lat_y']),float(line['long_x']))
        hour = line['time']

        #Cria uma nova instancia de Ponto
        pnt = {}
        pnt['Hora'] = hour
        pnt['Coord'] = coord
        newInstance = Ponto(pnt)
        
        newDict[tag].append(newInstance)

    #for que percorre cada key no dict
    for key,value in newDict.items():
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

    histTempo(allTimeGaps)
    #histDistancia(allCoordGaps)

'''
    separator = {} #dict em que cada chave contera uma lista com os indices onde as separações devem ser feitas

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