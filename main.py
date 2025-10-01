import os 
import re
import numpy as np
import itertools

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

pontos = []
casas = []


with open("matriz.txt", "r", encoding="utf-8") as arquivo:
    limpar_terminal()
    linhas = arquivo.readlines()
    primeira_linha = linhas[0]
    qntd_linhas, qntd_colunas = primeira_linha.split(' ')
    qntd_linhas = int(qntd_linhas)
    qntd_colunas = int(qntd_colunas.replace('\n',''))
    print(qntd_linhas, qntd_colunas)

    linhas_sem_a_primeira = linhas[1:]

    for i in range(qntd_linhas):
        pontos_por_linha = linhas_sem_a_primeira[i].split()
        pontos.append(pontos_por_linha)
        j = -1
        for elemento in pontos[i]:
            j += 1
            if elemento == 'R':
                pos_origem = f'{i} {j}'
            elif elemento != '0':
                casas.append(f'{elemento}:{i} {j}')  
    #for i in range(len(linhas_sem_a_primeira)):
    #    pontos_por_linha = linhas_sem_a_primeira[i].split()
    #    pontos.append(pontos_por_linha)
    #    j = -1
    #    for elemento in pontos[i]:
    #        j += 1
    #        if elemento == 'R':
    #            pos_origem = f'{i} {j}'
    #        elif elemento != '0':
    #            casas.append(f'{elemento}:{i} {j}')        

def combinatoria_de_caminhos(pos_origem, casas):
    nome_casas_perm = []
    nome_casas_comb = []
    cordenada_casas = []
    for i in range(len(casas)):
        separacao = casas[i].split(':')
        letra_casa = separacao[0]
        pos_casa = separacao[1]

        nome_casas_perm.append(letra_casa)
        nome_casas_comb.append(letra_casa)
        cordenada_casas.append(pos_casa)

    nome_casas_perm.insert(0,'R')
    nome_casas_perm.insert(-1,'R')
    elemento_fixo = 'R'
    
    permutacoes = list(itertools.permutations(nome_casas_perm))
    # Fixando o R inicial e o R final
    permutacoes_com_R_fixo = [r for r in permutacoes if (r[0] == elemento_fixo) and (r[-1] == elemento_fixo)]
    # Tirando caminhos duplicados com o set, já que tem 2 R 
    lista_de_permutacoes = list(set(permutacoes_com_R_fixo))# Permutação que define todos caminhos possíveis


    nome_casas_comb.append('R')
    cordenada_casas.append(pos_origem)
    combinacoes = itertools.permutations(nome_casas_comb, 2)
    lista_de_combinacoes = list(combinacoes)        # Arranjo que define todas duplas possíveis para calculo de distância

    return lista_de_permutacoes, lista_de_combinacoes, cordenada_casas
    
    
def calcular_distancias(cordenadas, combinacao):
    cord_casa_array = []

    for i in range(len(cordenadas)):
        valor_da_pos = (re.findall(r'\d+', cordenadas[i]))
        pos_casa = np.array(valor_da_pos, dtype=int)
        cord_casa_array.append(pos_casa)

    distancias = [np.abs(a - b) for a, b in itertools.permutations(cord_casa_array, 2)]
    somas = [int(np.sum(array)) for array in distancias]

    dict_distancias = dict(zip(combinacao, somas))

    return dict_distancias

def calcular_caminhos(distancias, permutacao):
    menor_distancia = 999999999999999
    menor_permutacao = ()
    for i in range(len(permutacao)):
        soma_distancia_do_caminho = 0
        
        
        for j in range(len(permutacao[i])):
            try:
                cada_distancia = (f'{permutacao[i][j]}', f'{permutacao[i][j+1]}')
                valor_cada_distancia = distancias[cada_distancia]
                soma_distancia_do_caminho += valor_cada_distancia
            except:
                pass
        #print(soma_distancia_do_caminho)
        
        if soma_distancia_do_caminho < menor_distancia:
            menor_distancia = soma_distancia_do_caminho
            menor_permutacao = permutacao[i]
    return menor_distancia, menor_permutacao
        


#print(*pontos, sep='\n\n')
#print('\nponto de origem: ', pos_origem)
#print('casas na matriz: ', casas,'\n')

permutacao, combinacao, cordenadas = combinatoria_de_caminhos(pos_origem, casas)
#print(combinacao)
#print(cordenadas)
#print(permutacao)
distancias = calcular_distancias( cordenadas, combinacao)
#print(distancias)
print(calcular_caminhos(distancias, permutacao))
