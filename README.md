### • Proximos passos
Documentação da pesquisa até o momento:

-> Finalizar a persistência de dados

-> Boxplot para CDF(explicar os dados utilizados)

-> Explicar o uso das cores

-> Explorar os tamanhos das viagens
____________________________________________________________
# Pesquisa
Trabalho de pesquisa da área de Redes Veiculares.

Orientador: Dr. Felipe Cunha

Orientando: Tulio Polido

# Objetivo
Desenvolver uma análise estatística de uma base de dados de táxis de Roma utilizando ferramentas de Data Science como CPython e OpenStreetMaps.

# Disposição dos dados
O trace está contido em um arquivo ".csv", onde cada linha representa um ponto do GPS contendo as seguintes informações: ID do veículo, data e hora, longitude, latitude e um inteiro definindo se aquele ponto está ou não calibrado.

| ID |  time  | long-x | lat-y | is_calibrated |
| ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
|  101 |  2014-02-04 05:00:01 | 12.48884 | 41.90304 | 1 |
|  101 |  2014-02-04 05:00:03 | 12.48875 | 41.90301 | 0 |

# Etapas
### • 1 - Análise inicial √
### • 2 - Algoritmo de detecção de paradas √
### • 3 - Estudo da base de dados
### • 4 - Enriquecimento da base original e comparação dos resultados

# Análise inicial do trace de Roma
Pelo gráfico de densidade de veículos podemos inferir que há quatro picos principais de fluxo de veículos na cidade de Roma. Nos intervalos 7h-8h, 11h-12h, 15h-16h e 19h-20h. Esse fato demonstra o funcionamento de uma cidade, onde, normalmente, os cidadãos têm um horário para sair de casa e ir ao trabalho, um horário de almoço e um horário de retorno.

### • Gráfico de Densidade de veículos x Hora do dia
![Alt text](/img/dens_carros.png?raw=true "Densidade veicular x Hora do dia")

O mapa de calor do horário de 12h às 13h exibe o fluxo intenso de veículos concentrado na região central de Roma, além de um fluxo na direção sudoeste da cidade onde se localizam o aeroporto e porto da região.

### • Mapa de calor das 12h às 13h na cidade de Roma
![Alt text](/img/map_12hTo13h.png?raw=true "Mapa de calor - Roma - 12h-13h")

*Para plotar outros mapas basta digitar no terminal na pasta do trabalho:

```
$ python3 -c "from mapaPorHora import *; osmPlot()" 12hTo13h
```

*O horário pode ser trocado desde esteja no mesmo formato. Ex: 3hTo4h; 17hTo18h (Intervalos de 1h)

# Desenvolvimento do algoritmo de detecção de paradas

O algoritmo seguinte, proposto em [8], foi desenvolvido tendo como base a movimentação de pessoas. Nele, a proposta principal é reconhecer os momentos que o indivíduo circula em determinada área durante um limite máximo de tempo. Caso a movimentação se enquadre nos limites propostos, esse intervalo pode ser considerado um ponto de parada. 

Para sua utilização com nossa base de dados de veículos, foram necessárias algumas adaptações. A principal é o resultado retornado pela função, que ao invés de retornar uma lista contendo um ponto com coordenada e horário de chegada e saída, retorna o intervalo entre dois pontos considerados fim e início de outra viagem. Com essa lista, é possível pegar todos os pontos de determinado veículo e dividí-lo nos intervalos retornados pela função, construindo suas trajetórias.

### Staypoint detection algorithm [8]
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

Esse algoritmo não tem uma boa detecção de viagens em veículos, como pode ser observado no mapa exibido abaixo: 
![Alt text](/img/trackmap_id_329_old.png?raw=true "Mapa do ID 329 v1")

O principal problema detectado é a grande fragmentação gerada ao se utilizar duas variáveis auxiliares i e j, que definem quais sequências de pontos consecutivos devem ser definidos como momentos de paradas. Essa técnica é funcional para detectar pontos de parada de um pedestre que possivelmente entrou em um edifício e se deslocou dentro dele por um tempo, porém ao se analisar veículos em rodovias, o mesmo é ineficiente. Deste modo, um novo algoritmo precisou ser desenvolvido, em que apenas uma variável auxiliar fosse utilizadas e a análise fosse feita não em um conjunto de pontos, mas de forma singular.

### Algoritmo de detecção de paradas
O algoritmo a seguir analisa os intervalos entre cada 2 pontos de GPS de forma singular. Isso impede a fragmentação das trajetórias preditas, e gera resultados mais convincentes das possíveis viagens feitas por um veículo.

```java
Entrada: (P -> Dados de GPS | limitDist -> limite de distância | limitTemp -> limite de tempo)
           
     i = 0 //variavel de controle
     numeroDePontos = |P|
     
     ENQUANTO i < numeroDePontos-1:
  
           dist = Distancia(Pᴵ, Pᴵ⁺¹) //dist recebe o valor da distancia entre os pontos i e i+1
               
           IF dist > limitDist:
                    tempo = Pᴵ⁺¹.tempo - Pᴵ.Tempo //tempo recebe a diferença de tempo entre dois pontos
                    
                    IF tempo > limitTemp:
                         SP.append(i) //Adiciona i na lista de paradas
     return SP
     
Saida: (SP -> lista com os pontos de parada)             
```

Os limites definidos para o algoritmo foram escolhidos tendo como base principal valores próximos ao limite superior dos dados de tempo e distâncias. A ideia é estabelecer um limite máximo de tempo em que o carro pode ficar parado sem que seja considerada uma nova viagem, bem como uma distância mínima que o carro deve percorrer entre dois pontos. Os valores de referência podem ser observados nos gráficos abaixo.
### Boxplot das distâncias
![Alt text](/img/Boxplots_distancias/boxplot_distancia_geral.png?raw=true "Boxplot distancias")

### Boxplot dos tempos
![Alt text](/img/Boxplots_tempo/boxplot_tempo_geral.png?raw=true "Boxplot distancias")

Para dar ao algoritmo uma margem de segurança, evitando que viagens fossem separadas, os valores selecionados estão um pouco acima dos limites exibidos nos boxplots anteriores. Abaixo pode ser observado o resultado da nova versão, onde há uma fragmentação muito menor e maior continuidade das trajetórias.

![Alt text](/img/trackmap_id_329.png?raw=true "Mapa do ID 329 v2")

# Criação da matriz O/D

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

