import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 

class calc:
    def qtdCarros(horario):
        """Calcula a qtd de carros durante um periodo de uma hora especificado"""
        str = './data/sortById/roma_' + horario + '_sorted_by_id.csv'
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

        plt.savefig('./img/carros_x_hora.png')
        plt.show()
        
    def histCarros():
        nCarros = np.empty(0,dtype=int)
        listHora = []
        totalCarros = 0

        for i in range(0,24):
            horario = str(i) + 'hTo' + str(i+1) + 'h'
            x = calc.qtdCarros(horario)
            totalCarros += x
            listHora.append(i)
            nCarros = np.append(nCarros,x)
        listHora.append(24)

        porcCarros = (nCarros * 100)/totalCarros 

        fig, ax = plt.subplots()
    
        index = np.arange(len(porcCarros))
        bar_width = 1
        score_label = np.arange(0,10,1)
        bar = ax.bar(index,porcCarros,bar_width,label='Porcentagem de Carros',align='edge')

        #setting labels
        ax.set_ylabel('Porcentagem de carros')
        ax.set_xlabel('Hora do dia')

        #setting axis
        ax.set_xticks(index)
        ax.set_xticklabels(listHora,{'fontsize':7})
        ax.set_yticks(score_label)
        ax.set_yticklabels(score_label)

        plt.savefig("./img/perc_carros_x_hora.png")
        plt.show()

    def funcDensidade():
        carros = []
        listHora = []

        for i in range(0,24):
            horario = str(i) + 'hTo' + str(i+1) + 'h'
            x = calc.qtdCarros(horario)
            newlist = [i] * x
            carros.extend(newlist)
            listHora.append(i)

        index = np.arange(len(listHora))

        fig, ax = plt.subplots()

        ax.set_xticks(index)
        ax.set_xticklabels(listHora,{'fontsize':7})

        #print(carros)
        sns.distplot(carros, kde_kws={"color":"r"})
        plt.savefig('./img/dens_carros.png')
        plt.show()