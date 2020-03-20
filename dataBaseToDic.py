#####
# Converte os dados para dictionary
#####

import csv
from ponto import Ponto

with open('roma_5hTo6h_sorted_by_id.csv') as file:
    reader = csv.DictReader(file)

    line = reader.__next__() #le a primeira linha
    tag = line['id']
    print('\n\n\n\n' + str(tag) + ": ", end='')
    
    for line in reader:
        if tag != line['id']: #Quando a tag for modificada, printa nova tag
            tag = line['id']
            print('\n\n\n\n' + str(tag) + ": ", end='')

        coord = (float(line['lat_y']),float(line['long_x']))
        hour = line['time']

        pnt = {}
        pnt['Hora'] = hour
        pnt['Coord'] = coord

        newInstance = Ponto(pnt)
        print(newInstance, end=',')