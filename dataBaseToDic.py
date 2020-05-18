#####
# Converte os dados para dictionary
#####
from datetime import datetime
import csv
from ponto import Ponto

newDict = {}

with open('./sortById/roma_5hTo6h_sorted_by_id.csv') as file:
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
        print(key, end='\n')
        for i in range(len(value)):
            pointData = value[i].pointData['Hora']
            pointData = datetime.strptime(pointData,'%Y-%d-%m %H:%M:%S') #converte string para datahora