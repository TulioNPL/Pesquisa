# Update 10/05 - 16/05

-> Desenvolvimento do Dictionary
```python
     Dict = {'ID':[(hora,coord),(hora,coord),...)],'ID2':[(hora,coord),(hora,coord),...]...}
```
-> Update dos arquivos ordenados por ID. ('Hora' adicionada como segunda chave de ordenação)


____________________________________________________________
# Pesquisa
Trabalho de pesquisa da área de Redes Veiculares

Orientador: Dr. Felipe Cunha

Orientando: Tulio Polido

# Objetivo
Desenvolver uma análise estatística de uma base de dados de táxis de Roma utilizando ferramentas de Data Science como CPython, R Lang e OpenStreetMaps.

# Análise do trace de Roma

### Gráfico de Densidade de veículos x Hora do dia
![Alt text](/graficos/dens_carros.png?raw=true "Densidade veicular x Hora do dia")

### Gráfico da Quantidade de veículos x Hora do dia
![Alt text](/graficos/carros_x_hora.png?raw=true "Quantidade de veículos x Hora do dia")

### Gráfico da Porcentagem de carros x Hora do dia
![Alt text](/graficos/porc_carros_x_hora.png?raw=true "Porcentagem de carros x Hora do dia")

### Mapa de calor das 12h às 13h na cidade de Roma
![Alt text](/graficos/map_12hTo13h.png?raw=true "Mapa de calor - Roma - 12h-13h")

Para plotar outros mapas basta digitar no terminal na pasta do trabalho:

```
$ python3 -c "from mapaPorHora import *; osmPlot()" 12hTo13h
```

O horário pode ser trocado desde esteja no mesmo formato. Ex: 3hTo4h; 17hTo18h (Intervalos de 1h)

### [Link ID 3 12hTo13h trackmaps](https://drive.google.com/open?id=1ZT1g-8yMePK_pGOis_BGHNlAE-JPxBtO)

# Referências Bibliográficas

<a id="1">[1]</a> 
KONG, Xiangjie et al. 
Mobility dataset generation for vehicular social networks based on floating car data. 
**IEEE Transactions on Vehicular Technology**, v. 67, n. 5, p. 3874-3886, 2018.

<a id="2">[2]</a> 
BASTA, Nardine et al. 
Generic Geo-Social Mobility Model for VANET. 
In: **2016 IEEE 84th Vehicular Technology Conference (VTC-Fall)**. IEEE, 2016. p. 1-5.

<a id="3">[3]</a> 
NING, Zhaolong et al. 
Vehicular social networks: Enabling smart mobility. 
**IEEE Communications Magazine**, v. 55, n. 5, p. 16-55, 2017.

<a id="4">[4]</a> 
GAINARU, Ana; DOBRE, Ciprian; CRISTEA, Valentin. 
A realistic mobility model based on social networks for the simulation of VANETs. 
In: **VTC Spring 2009-IEEE 69th Vehicular Technology Conference**. IEEE, 2009. p. 1-5.

<a id="5">[5]</a> 
CELES, Clayson; BOUKERCHE, Azzedine; LOUREIRO, Antonio AF. 
Towards Understanding of Bus Mobility for Intelligent Vehicular Networks Using Real-World Data. 
In: **2019 IEEE Global Communications Conference (GLOBECOM)**. IEEE, 2019. p. 1-6.
