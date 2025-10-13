import os
import re
import numpy as np
import itertools
from tkinter import filedialog
import time
import math


def selecionar_arquivo(entry_widget):
    """
    Recebe o widget de texto como parâmetro para poder escrever nele.
    Reconhece quando o arquivo é carregado.
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
    iniciar_tempo = time.perf_counter()

    global caminho_do_arquivo
    # Verifica se um arquivo foi selecionado primeiro
    if not caminho_do_arquivo:
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", "Erro: Por favor, carregue um arquivo .txt primeiro.")
        return
    entry_widget.delete("1.0", "end")
    entry_widget.insert("1.0", "Calculando.....")
    entry_widget.update_idletasks()
    try:
        
        pontos = []
        casas = []

        with open(caminho_do_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            primeira_linha = linhas[0]
            qntd_linhas, qntd_colunas = primeira_linha.split(' ')
            qntd_linhas = int(qntd_linhas) # Identifica entrada de linhas e colunas
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

        def separando_cordenadas(pos_origem, casas):
            """
            Faz a separação das cordenadas dos nomes (Ex: (A: 1 1) para (A) e (1 1)).
            Também adiciona a posição de origem às casas (Ex: (A B C) para (R A B C))
            """

            nome_casas = []
            cordenada_casas = []
            for i in range(len(casas)):
                separacao = casas[i].split(':')
                letra_casa = separacao[0]
                pos_casa = separacao[1]
                nome_casas.append(letra_casa)
                cordenada_casas.append(pos_casa)

            # adiciona R (origem)
            nome_casas.append('R')
            cordenada_casas.append(pos_origem)

            return nome_casas, cordenada_casas

        def calcular_matriz_distancias(cordenadas, nome_casas):
            """
            Cria uma matriz NxN com a distância Manhattan entre todos os pontos.
            Também cria um dicionário para acessar distâncias por nome ('A','B',...).
            """
            n = len(cordenadas)
            matriz = np.zeros((n, n), dtype=int)

            # Converter todas as coordenadas de string "i j" para tuplas (i,j)
            coords_numericas = []
            for c in cordenadas:
                numeros = re.findall(r'\d+', c)
                linha = int(numeros[0])
                coluna = int(numeros[1])
                coords_numericas.append((linha, coluna))

            # Preenche a matriz de distâncias
            for i in range(n):
                for j in range(n):
                    x1, y1 = coords_numericas[i]
                    x2, y2 = coords_numericas[j]
                    distancia = abs(x1 - x2) + abs(y1 - y2)
                    matriz[i][j] = distancia

            # Cria um dicionário de distâncias com pares de nomes
            dict_distancias = {}
            for i in range(n):
                for j in range(n):
                    a = nome_casas[i]
                    b = nome_casas[j]
                    dict_distancias[(a, b)] = matriz[i][j]

            return dict_distancias

        def calcular_caminhos(distancias, nome_casas):
            """
            Testa todas as permutações (força bruta), sem armazenar todas na memória.
            Mantém apenas o menor caminho encontrado.
            """
            menor_distancia = math.inf
            menor_permutacao = ()

            # As casas que não são 'R'
            casas_sem_R = [c for c in nome_casas if c != 'R']

            for permutacao in itertools.permutations(casas_sem_R):
                caminho = ['R'] + list(permutacao) + ['R']

                soma_distancia_do_caminho = 0
                for i in range(len(caminho) - 1):
                    a = caminho[i]
                    b = caminho[i + 1]
                    soma_distancia_do_caminho += distancias[(a, b)]

                if soma_distancia_do_caminho < menor_distancia:
                    menor_distancia = soma_distancia_do_caminho
                    menor_permutacao = caminho

            return menor_distancia, menor_permutacao
        
        

        # Execução das funções
        nome_casas, cordenadas = separando_cordenadas(pos_origem, casas)
        distancias = calcular_matriz_distancias(cordenadas, nome_casas)
        resposta, menor_caminho = calcular_caminhos(distancias, nome_casas)

        encerrar_tempo = time.perf_counter()
        tempo_de_execucao = encerrar_tempo - iniciar_tempo

        resultado_formatado = (
            f"Menor distância: {resposta}\n\n"
            f"Percorrendo o caminho:\n{' -> '.join(menor_caminho)}\n\n"
            f"Tempo gasto no cálculo:\n{tempo_de_execucao:.4f} s"
        )

        # Limpa o campo de texto e insere o novo resultado
        entry_widget.delete("1.0", "end")
        entry_widget.insert("1.0", resultado_formatado)
        
    except Exception as e:
        if not MemoryError:
            entry_widget.delete("1.0", "end")
            entry_widget.insert("1.0", f"Ocorreu um erro:\nTecnicamente: {e}\n\nVerifique se o formato do arquivo .txt está na forma certa:\n"
            "EX:\n"
            "33\n"
            "C00\n00B\nR0A\n")
