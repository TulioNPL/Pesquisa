import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

class calc:
    def qtdCarros(horario):
        str = 'roma_' + horario + '_sorted_by_id.csv'
        df = pd.read_csv(str)
        numCarros = df['id'].nunique()
        return numCarros

#Driver

for i in range(0,24):
    horario = str(i) + 'hTo' + str(i+1) + 'h'
    print(horario)
x = calc.qtdCarros('5hTo6h')
print(x)