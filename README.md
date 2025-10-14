# Fly Food 🚁

<p align="center">
  <img src="https://i.ibb.co/TxftJ0c5/Fly-food-logo.png" alt="Fly-food-logo" border="0">
</p>

<p align="center">
  <strong>Uma ferramenta de desktop para otimização de rotas de entrega, que calcula o caminho mais curto para visitar múltiplos pontos em um mapa de grade.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/Status-Funcional-green?style=for-the-badge" alt="Status: Funcional">
</p>

## 📜 Índice

1.  [Sobre o Projeto](#-sobre-o-projeto)
2.  [Preview da Aplicação](#-preview-da-aplicação)
3.  [Funcionalidades Principais](#-funcionalidades-principais)
4.  [Tecnologias Utilizadas](#-tecnologias-utilizadas)
5.  [Como Executar](#-como-executar)
6.  [Formato do Arquivo de Entrada](#-formato-do-arquivo-de-entrada)
7.  [Como Contribuir](#-como-contribuir)
8.  [Licença](#-licença)

---

## 🎯 Sobre o Projeto

O **Fly Food** foi desenvolvido como uma solução para um desafio logístico clássico, conhecido como o Problema do Caixeiro Viajante (PCV). O objetivo é encontrar a rota mais eficiente para um drone de entrega que precisa partir de um ponto de origem (`R`), visitar uma série de destinos e retornar à base.

A aplicação utiliza um mapa em formato de grade, lido a partir de um arquivo de texto simples, e aplica um algoritmo de força bruta para calcular a distância Manhattan entre todos os pontos. Ao testar todas as permutações de rotas possíveis, o Fly Food garante a descoberta do caminho com a menor distância total, otimizando tempo e recursos de entrega.

---

## ✨ Preview da Aplicação

A interface gráfica foi projetada para ser simples e direta, focando na usabilidade.

| Tela Principal | Resultado do Cálculo |
| :---: | :---: |
| *<center>(Screenshot da sua aplicação com o campo de texto vazio ou com a mensagem inicial)</center>* | *<center>(Screenshot da sua aplicação exibindo uma rota calculada, a distância e o tempo de execução)</center>* |

---

## 🚀 Funcionalidades Principais

-   **Interface Gráfica Intuitiva:** Uma janela simples construída com Tkinter para facilitar a interação.
-   **Carregamento de Mapas:** Selecione e carregue facilmente arquivos `.txt` que definem a grade de entrega.
-   **Cálculo de Rota Ótima:** Utiliza um algoritmo de força bruta para encontrar a menor rota possível, visitando todos os pontos de entrega.
-   **Métrica de Distância Manhattan:** Ideal para cenários de grade, onde o movimento é restrito a direções horizontais e verticais.
-   **Exibição Clara de Resultados:** Apresenta a menor distância encontrada, a sequência do caminho ideal e o tempo de processamento do cálculo.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
| :--- | :--- |
| **Python** | Linguagem principal do projeto. |
| **Tkinter** | Biblioteca nativa para a construção da interface gráfica (GUI). |
| **NumPy** | Utilizada para criar e gerenciar a matriz de distâncias entre os pontos de forma eficiente. |
| **itertools** | Ferramenta essencial para gerar todas as permutações de rotas para a solução de força bruta. |
| **Pathlib** | Garante que os caminhos para os assets da GUI funcionem em qualquer sistema operacional. |
| **Bibliotecas Padrão** | `os`, `re`, `time` e `math` para operações com arquivos, expressões regulares, medição de tempo e cálculos. |

---

## ⚙️ Como Executar

Siga os passos abaixo para executar o Fly Food em seu ambiente local.

### Pré-requisitos
-   Python 3.10 ou superior
-   Git

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_AQUI]
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```

2.  **Crie e ative um ambiente virtual (Recomendado):**
    ```bash
    # Cria o ambiente
    python -m venv venv

    # Ativa o ambiente
    # No Windows:
    venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
    
3.  **Instale as dependências:**
    Crie um arquivo chamado `requirements.txt` na raiz do projeto com o seguinte conteúdo:
    ```txt
    numpy
    ```
    Em seguida, instale-o com o pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    O ponto de entrada da interface gráfica é o arquivo `gui.py`.
    ```bash
    python gui.py
    ```

---

## 📄 Formato do Arquivo de Entrada

Para que o cálculo funcione corretamente, o arquivo `.txt` deve seguir uma estrutura específica:

1.  A **primeira linha** deve conter as dimensões da grade: `Linhas Colunas` (separadas por um espaço).
2.  As **linhas seguintes** devem representar a grade, onde:
    -   `0` representa um espaço vazio.
    -   `R` representa o ponto de partida e de chegada (origem).
    -   Qualquer outra letra (ex: `A`, `B`, `C`) representa um ponto de entrega.

**Exemplo de um arquivo `mapa.txt` válido:**
