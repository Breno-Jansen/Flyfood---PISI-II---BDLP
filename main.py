import os 
import re
import numpy as np
import itertools
from tkinter import filedialog

def selecionar_arquivo(entry_widget):
    """
    Recebe o widget de texto como parâmetro para poder escrever nele.
    """
    global caminho_do_arquivo
    filetypes = (('Text files', '*.txt'), ('All files', '*.*'))
    fpath = filedialog.askopenfilename(title="Selecione o arquivo de matriz", filetypes=filetypes)
    if fpath:
        caminho_do_arquivo = fpath
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", f"Arquivo carregado:\n{os.path.basename(caminho_do_arquivo)}")


def executar_calculo(entry_widget):
    """
    Esta função é chamada pelo button_1.
    Executa toda a lógica de cálculo e exibe o resultado em entry_widget.
    """
    global caminho_do_arquivo
    # Verifica se um arquivo foi selecionado primeiro
    if not caminho_do_arquivo:
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", "Erro: Por favor, carregue um arquivo .txt primeiro.")
        return

    try:
        pontos = []
        casas = []

        with open(caminho_do_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            primeira_linha = linhas[0]
            qntd_linhas, qntd_colunas = primeira_linha.split(' ')
            qntd_linhas = int(qntd_linhas)
            qntd_colunas = int(qntd_colunas.replace('\n',''))
            linhas_sem_a_primeira = linhas[1:]

            for i in range(qntd_linhas):
                pontos_por_linha = linhas_sem_a_primeira[i].split()
                pontos.append(pontos_por_linha)
                for j in range(qntd_colunas):
                    elemento = pontos[i][j]
                    if elemento == 'R':
                        pos_origem = f'{i} {j}'
                    elif elemento != '0':
                        casas.append(f'{elemento}:{i} {j}')     

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
            menor_distancia = -1
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
        
                if (soma_distancia_do_caminho < menor_distancia) or (menor_distancia == -1):
                    menor_distancia = soma_distancia_do_caminho
                    menor_permutacao = permutacao[i]
            return menor_distancia, menor_permutacao

        permutacao, combinacao, cordenadas = combinatoria_de_caminhos(pos_origem, casas)
        distancias = calcular_distancias(cordenadas, combinacao)
        resposta, menor_caminho = calcular_caminhos(distancias, permutacao)

        resultado_formatado = (
            f"Menor distância: {resposta}\n\n"
            f"Percorrendo o caminho:\n{' -> '.join(menor_caminho)}"
        )

        # Limpa o campo de texto e insere o novo resultado
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", resultado_formatado)
        
    except Exception as e:
        # Em caso de erro na leitura ou processamento, exibe o erro na interface
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", f"Ocorreu um erro:\n{e}\n\nVerifique o formato do arquivo .txt.")


