import os 
import re
import numpy as np
import itertools

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

pontos = []
casas = []
ultima_linha = -1


with open("matriz.txt", "r", encoding="utf-8") as arquivo:
    limpar_terminal()
    linhas = arquivo.readlines()
    for i in range(len(linhas)):
        ultima_linha += 1
        pontos_por_linha = linhas[i].split()
        pontos.append(pontos_por_linha)
        j = -1
        ultima_coluna = -1
        for elemento in pontos[i]:
            j += 1
            ultima_coluna += 1
            if elemento == 'R':
                pos_origem = f'{i} {j}'
            elif elemento != '0':
                casas.append(f'{elemento}:{i} {j}')

# pos_origem = np.array(pos_origem, dtype=int)
casaA = (re.findall(r'\d+',casas[1]))

print(*pontos, sep='\n\n')
print('\nponto de origem: ', pos_origem)
print('casas na matriz: ', casas,'\n')
        

def combinatoria_de_caminhos(pos_origem, casas):
    nome_casas = []
    cordenada_casas = []
    for i in range(len(casas)):
        separacao = casas[i].split(':')
        letra_casa = separacao[0]
        pos_casa = separacao[1]

        nome_casas.append(letra_casa)
        cordenada_casas.append(pos_casa)

    
    permutacoes = itertools.permutations(nome_casas)
    lista_de_permutacoes = list(permutacoes)        # Permutação que define todos caminhos possíveis

    nome_casas.append('R')
    cordenada_casas.append(pos_origem)
    combinacoes = itertools.combinations(nome_casas, 2)
    lista_de_combinacoes = list(combinacoes)        # Combinação que define todas duplas possíveis para calculo de distância

    return lista_de_permutacoes, lista_de_combinacoes, cordenada_casas
    
    
def calcular_distancias(pos_origem, cordenadas, combinacao):
    cord_casa_array = []

    for i in range(len(cordenadas)):
        valor_da_pos = (re.findall(r'\d+', cordenadas[i]))
        pos_casa = np.array(valor_da_pos, dtype=int)
        cord_casa_array.append(pos_casa)

    distancias = [np.abs(a - b) for a, b in itertools.combinations(cord_casa_array, 2)]
    somas = [int(np.sum(array)) for array in distancias]

    dict_distancias = dict(zip(combinacao, somas))

    return dict_distancias


permutacao, combinacao, cordenadas = combinatoria_de_caminhos(pos_origem, casas)
#print(combinacao)
#print(cordenadas)
#print(permutacao)
print(calcular_distancias(pos_origem, cordenadas, combinacao), sep='\n')