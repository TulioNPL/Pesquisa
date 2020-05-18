#####
# Converte os dados para dictionary
#####
from datetime import datetime
from datetime import timedelta
from ponto import Ponto
import csv
import matplotlib.pyplot as plt

newDict = {}
maxDelta = timedelta(hours=0,minutes=0,seconds=30)
intervalos = []

with open('./sortById/roma_12hTo13h_sorted_by_id.csv') as file:
    reader = csv.DictReader(file)

    line = reader.__next__() #le a primeira linha
    tag = line['id']


    newDict[tag] = [] #cria uma lista onde serao adicionados os pontos de cada id
    
    #Ciclo que percorre todas as linhas, le os pontos e os salva nos respectivos ids no Dictionary
    for line in reader:
        if tag != line['id']: #Quando a tag for modificada, cria uma nova key
            tag = line['id']
            newDict[tag] = []

        coord = (float(line['lat_y']),float(line['long_x']))
        hour = line['time']

        #Cria uma nova instancia de Ponto
        pnt = {}
        pnt['Hora'] = hour
        pnt['Coord'] = coord
        newInstance = Ponto(pnt)
        
        newDict[tag].append(newInstance)

    for key,value in newDict.items():
        #print(key, end='\n')

        
        for i in range(len(value)-1):
            pointData = value[i].pointData['Hora']
            pointData2 = value[i+1].pointData['Hora']

            pointData = datetime.strptime(pointData,'%Y-%d-%m %H:%M:%S') #converte string para datahora
            pointData2 = datetime.strptime(pointData2,'%Y-%d-%m %H:%M:%S')

            intervalo = pointData2-pointData
            intervalos.append(intervalo.total_seconds())
            #print(intervalos)

            '''
            if(intervalo > maxDelta):
                print(intervalo.total_seconds())
            '''

    #print(max(intervalos))

    plt.hist(intervalos,density=True,bins=1601)
    plt.xlabel('segundos')
    plt.ylabel('frequencia')
    plt.show()
