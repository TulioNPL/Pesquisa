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

    df2 = df2.sort_values('time')   #ordena o DataFrame por "data-hora"
    #df2 = df2.sort_values('id')   #ordena o DataFrame por "id"
    nome = './sortByTime/roma_' + str(i) + 'hTo' + str(i+1) + 'h_sorted_by_time.csv'
    df2.to_csv(nome, index = False) #salva o DataFrame para CSV