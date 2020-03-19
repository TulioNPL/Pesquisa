#####
# Converte os dados para dictionary
#####

import datetime as dt
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

with open('./Dados/roma_calibrated.csv') as file:
    reader = csv.DictReader(file)

    line = reader.__next__()
    tag = line['id']
    print('\n\n\n\n' + str(tag) + ": ", end='')
    
    for line in reader:
        if tag != line['id']:
            tag = line['id']
            print('\n\n\n\n' + str(tag) + ": ", end='')

        coord = (float(line['lat_y']),float(line['long_x']))
        hour = line['time']

        pnt = {}
        pnt['Hora'] = hour
        pnt['Coord'] = coord

        newInstance = ponto.Ponto(pnt)
        print(newInstance, end=',')