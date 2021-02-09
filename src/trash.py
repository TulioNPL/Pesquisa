###
# Arquivo de códigos lixo que podem vir a ser úteis no futuro
###
''' dataBaseToDic.py:
    #ciclo para gerar os indices onde as viagens de cada key serão divididas
    for key in keys:
        flag = False #Se true, entao o tempo decorrido permite a criacao de uma nova trip
        tempo = 0
        separator[key] = []

        if(len(coordGaps[key]) > 0): #confere se o vetor não está vazio
            for i in range(0,len(coordGaps[key])-1): 
                if(timeGaps[key][i] != 0): #confere se o tempo de gravação entre dois pontos não é zero
                    if(coordGaps[key][i]/timeGaps[key][i] < 0.1):
                        tempo += timeGaps[key][i]
                    else:
                        if(flag):
                            separator[key].append(i)
                            flag = False
                            tempo = 0
                        else:
                            tempo = 0
                            flag = False

                    if(tempo > 30.0):
                        flag = True

        print('\n'+ key + ': ', end='')
        print(separator[key])
'''

'''Haversine Test
import math

def convertHaversine(x1,y1,x2,y2):
    R = 6378.137
    dLat = x2 * math.pi / 180 - x1 * math.pi / 180
    dLon = y2 * math.pi / 180 - y1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(x1 * math.pi / 180) * math.cos(x2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    return d* 1000 #retorna o valor em metros

lat1 = -19.881364
long1 = -43.922003
lat2 = -19.878815
long2 = -43.926031

print("Distância de acordo com Google Maps: 500 metros")
print(convertHaversine(lat1,long1,lat2,long2))'''