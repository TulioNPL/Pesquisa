import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

class calc:
    def qtdCarros(horario):
        """Calcula a qtd de carros durante um periodo de uma hora especificado"""
        str = './sortById/roma_' + horario + '_sorted_by_id.csv'
        df = pd.read_csv(str)
        numCarros = df['id'].nunique()
        return numCarros

    def grafCarros():
        nCarros = []
        listHora = []

        for i in range(0,24):
            horario = str(i) + 'hTo' + str(i+1) + 'h'
            x = calc.qtdCarros(horario)
            listHora.append(i)
            nCarros.append(x)
        listHora.append(24)

        fig, ax = plt.subplots()

        index = np.arange(len(nCarros))
        bar_width = 1
        score_label = np.arange(0,250,25)
        bar = ax.bar(index, nCarros, bar_width, label='Quantidade de Carros',align='edge',edgecolor='#000000')

        #setting labels
        ax.set_ylabel('Quantidade de Carros')
        ax.set_xlabel('Hora do dia')

        #setting axis
        ax.set_xticks(index)
        ax.set_xticklabels(listHora,{'fontsize':7})
        ax.set_yticks(score_label)
        ax.set_yticklabels(score_label)

        for i in index:
            ax.annotate(
                '{}'.format(bar[i].get_height()),
                xy=(bar[i].get_x(),bar[i].get_height()),
                xytext=(0,2),
                textcoords='offset points',
                va='bottom',
                size=7
            )

        plt.title('Quantidade de carros x Hora do dia')

        plt.savefig('./graficos/carros_x_hora.png')
        plt.show()
        



#Driver
calc.grafCarros()