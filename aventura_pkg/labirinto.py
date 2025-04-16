# labirinto
"""
Módulo responsável pela criação e impressão do labirinto.
"""
import random
from rich import print
from rich.console import Console
from rich.text import Text
from aventura_pkg.jogador import movimentos ,pontuacao
import time
import os

def criar_labirinto(dificuldade):
    """
    Cria um labirinto com base no nível de dificuldade selecionado.

    Args:
        dificuldade (str): Nível de dificuldade escolhido pelo jogador.
            Pode ser: 'facil', 'medio', 'dificil', 'super-dificil' ou 'max-difícil'.

    Returns:
        list: Uma matriz (lista de listas) representando o labirinto gerado.
    """
    if dificuldade == 'facil':
        return gerar_labirinto_aleatorio(11, 11)
    elif dificuldade == 'medio':
        return gerar_labirinto_aleatorio(15, 15)
    elif dificuldade == 'dificil':
        return gerar_labirinto_aleatorio(19, 19)
    elif dificuldade == 'super-dificil':
        return gerar_labirinto_aleatorio(25, 25)
    elif dificuldade == 'max-dificil':
        return gerar_labirinto_aleatorio(31,31)
    else:
        raise ValueError("Dificuldade inválida.")


console = Console()

def imprimir_labirinto(labirinto, pos_jogador=None):
    """
    Imprime visualmente o labirinto no terminal usando cores e símbolos.

    Args:
        labirinto (list): Estrutura do labirinto (matriz de caracteres).
        pos_jogador (tuple, opcional): Posição atual do jogador no labirinto.
    """
    for i, linha in enumerate(labirinto):
        linha_colorida = Text()
        for j, celula in enumerate(linha):
            if (i, j) == tuple(pos_jogador):
                linha_colorida.append("😎", style="bold cyan")  # personagem
            elif celula == "#":
                linha_colorida.append("██", style="grey61")  # parede
            elif celula == ".":
                linha_colorida.append("  ")  # caminho vazio
            elif celula == "S":
                linha_colorida.append("S ", style="bold green")  # início
            elif celula == "F":
                linha_colorida.append("F ", style="bold red")  # fim
            elif celula == "*":
                linha_colorida.append("• ", style="yellow")  # parte da solução
            else:
                linha_colorida.append(f"{celula} ")
        console.print(linha_colorida)
    console.print()  # linha em branco

import random

def gerar_labirinto_aleatorio(linhas, colunas):
    """
    Gera um labirinto aleatório usando algoritmo de escavação com pilha.

    Args:
        linhas (int): Número de linhas do labirinto.
        colunas (int): Número de colunas do labirinto.

    Returns:
        list: Labirinto representado como uma matriz.
    """
    lab = [['#' for _ in range(colunas)] for _ in range(linhas)]

    def dentro_do_labirinto(x, y):
        return 0 < x < linhas-1 and 0 < y < colunas-1

    stack = [(1, 1)]
    lab[1][1] = ' '

    while stack:
        x, y = stack[-1]
        direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcoes)
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if dentro_do_labirinto(nx, ny) and lab[nx][ny] == '#':
                lab[nx][ny] = ' '
                lab[x + dx // 2][y + dy // 2] = ' '  # quebra a parede entre as células
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    lab[1][1] = ' '
    lab[linhas - 2][colunas - 2] = 'F'
    return lab



def animar_exemplo_labirinto():
    """
    Anima uma simulação visual de como o personagem atravessa um labirinto exemplo.

    Exibe o labirinto no terminal com movimento progressivo até o fim.
    """
    labirinto_exemplo = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', ' ', ' ', '#', ' ', ' ', ' ', '#', '#', '#'],
        ['#', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#'],
        ['#', '#', ' ', ' ', ' ', '#', '#', '#', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
        ['#', ' ', ' ', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', '#', ' ', '#', ' ', ' ', ' ', ' ', '#', '#'],
        ['#', '#', ' ', ' ', ' ', '#', '#', ' ', 'F', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        
    ]

    caminho = [(1,1), (1,2), (2,2), (3,2), (3,3), (3,4), (2,4), (1,4), (1,5), (1,6),
               (2,6), (2,7), (2,8), (3,8), (4,8), (4,7), (4,6), (5,6), (5,5), (5,4),
               (5,3), (5,2), (6,2), (7,2), (8,2), (8,3),(8,4), (7,4), (7,5), (7,6),
               (7,7), (8,7), (8,8)]

    for pos in caminho:
        i, j = pos
        mostrar_labirinto_exemplo(labirinto_exemplo, (i, j))
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

    console.print("\n[green]Este é um exemplo de como seu personagem se moverá até a saída (F)![/green]\n")


def mostrar_labirinto_exemplo(lab, posicao):
    """
    Exibe um frame do labirinto com o personagem na posição atual.
    
    Args:
        lab (list): Estrutura do labirinto como lista de listas.
        posicao (tuple): Posição (linha, coluna) do personagem.
    """
    for i, linha in enumerate(lab):
        linha_exibida = Text()
        for j, celula in enumerate(linha):
            if (i, j) == tuple(posicao):
                linha_exibida.append("😎", style="bold cyan")  # personagem
            elif celula == "#":
                linha_exibida.append("██", style="grey61")  # parede
            elif celula == ".":
                linha_exibida.append("  ")  # caminho vazio
            elif celula == "S":
                linha_exibida.append("S ", style="bold green")  # início
            elif celula == "F":
                linha_exibida.append("F ", style="bold red")  # fim
            elif celula == "*":
                linha_exibida.append("• ", style="yellow")  # parte da solução
            else:
                linha_exibida.append(f"{celula} ")
        console.print(linha_exibida)
    console.print()  # linha em branco