# Update 23/08 - 29/08

-> Desenvolvimento algoritmo de detecção de paradas

### • Proximos passos
-> Refatorar código

-> implementar limites e testar algoritmo de detecção de paradas

____________________________________________________________
# Pesquisa
Trabalho de pesquisa da área de Redes Veiculares.

Orientador: Dr. Felipe Cunha

Orientando: Tulio Polido

# Objetivo
Desenvolver uma análise estatística de uma base de dados de táxis de Roma utilizando ferramentas de Data Science como CPython, R Lang e OpenStreetMaps.

# Disposição dos dados
O trace está contido em um arquivo ".csv", onde cada linha representa um ponto do GPS contendo as seguintes informações: ID do veículo, data e hora, longitude, latitude e um inteiro definindo se aquele ponto está ou não calibrado.

| ID |  time  | long-x | lat-y | is_calibrated |
| ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
|  101 |  2014-02-04 05:00:01 | 12.48884 | 41.90304 | 1 |
|  101 |  2014-02-04 05:00:03 | 12.48875 | 41.90301 | 0 |

# Etapas
### • 1 - Análise inicial √
### • 2 - Algoritmo de detecção de paradas
### • 3 - Estudo da base de dados
### • 4 - Enriquecimento da base original e comparação dos resultados

# Análise inicial do trace de Roma
Pelo gráfico de densidade de veículos podemos inferir que há quatro picos principais de fluxo de veículos na cidade de Roma. Nos intervalos 7h-8h, 11h-12h, 15h-16h e 19h-20h. Esse fato demonstra o funcionamento de uma cidade, onde, normalmente, os cidadãos têm um horário para sair de casa e ir ao trabalho, um horário de almoço e um horário de retorno.

### • Gráfico de Densidade de veículos x Hora do dia
![Alt text](/graficos/dens_carros.png?raw=true "Densidade veicular x Hora do dia")

O mapa de calor do horário de 12h às 13h exibe o fluxo intenso de veículos concentrado na região central de Roma, além de um fluxo na direção sudoeste da cidade onde se localizam o aeroporto e porto da região.

### • Mapa de calor das 12h às 13h na cidade de Roma
![Alt text](/graficos/map_12hTo13h.png?raw=true "Mapa de calor - Roma - 12h-13h")

Para plotar outros mapas basta digitar no terminal na pasta do trabalho:

```
$ python3 -c "from mapaPorHora import *; osmPlot()" 12hTo13h
```

O horário pode ser trocado desde esteja no mesmo formato. Ex: 3hTo4h; 17hTo18h (Intervalos de 1h)

# Desenvolvimento do algoritmo de detecção de paradas

O algoritmo seguinte, proposto em [8], foi desenvolvido tendo como base a movimentação de pessoas. Para sua utilização com nossa base de dados de veículos, são necessárias adaptações.
```java
Entrada: (P -> Dados de GPS | limitDist -> limite de distância | limitTemp -> limite de tempo)
           
     i = 0 //variavel de controle
     numeroDePontos = |P|
     
     ENQUANTO i < numeroDePontos:
          j = i + 1 //j assume a posição seguinte a i
          
          ENQUANTO j < numeroDePontos:
               dist = Distancia(Pi, Pj) //dist recebe o valor da distancia entre os pontos i e j
               
               IF dist > limitDist:
                    tempo = Pj.tempo - Pi.Tempo //tempo recebe a diferença de tempo entre dois pontos
                    
                    IF tempo > limitTemp:
                         S.coord = CalculaMediaCoord({Pk | i <= k <= j}) //Calcula o ponto medio das coordenadas
                         S.arv = Pi.tempo //tempo de chegada
                         S.lev = Pj.tempo //tempo de saida
                         SP.insert(S)
                    i = j
                    break
               j = j + 1
     return SP
     
Saida: (SP -> lista com os pontos de parada)             
```

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

<a id="6">[6]</a> 
CINTRA, Marcos. 
A crise do trânsito em são paulo e seus custos.
**GV EXECUTIVO**, v. 12,n. 2, p. 58–61, 2013.

<a id="7">[7]</a> 
GONG, Lei et al. 
Identification of activity stop locations in gps trajectories by density-basedclustering method combined with support vector machines.
**Journal of Modern Transporta-tion**, Springer, v. 23, n. 3, p. 202–213, 2015.

<a id="8">[8]</a> 
LI, Quannan et al. 
Mining user similarity based on location history. In: **Proceedings of the 16th ACM SIGSPATIAL international conference on Advances in geographic information systems**. 2008. p. 1-10.

