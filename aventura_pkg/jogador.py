# jogador
"""
Módulo responsável pelo controle do jogador no labirinto.

Gerencia a movimentação, pontuação, sons e interação com o teclado
durante o jogo. Também inclui funcionalidades como mostrar a solução
recursiva do labirinto e retorno ao menu.
"""
import os
from pynput import keyboard
from . import labirinto
from rich.console import Console
from rich.panel import Panel
import pygame

pygame.init()
pygame.mixer.init()

som_passo = pygame.mixer.Sound("sons/passo.mp3")
som_vitoria = pygame.mixer.Sound("sons/vitoria.mp3")
som_saida = pygame.mixer.Sound("sons/saida.mp3")

som_ativado = True  # Som ativado por padrão

def configurar_som(ativo: bool):
    """
    Ativa ou desativa os efeitos sonoros do jogo.

    Args:
        ativo (bool): Se True, o som será ativado. Caso contrário, desativado.
    """
    global som_ativado
    som_ativado = ativo

jogador_pos = [0, 0]
pontuacao = 0
movimentos = 0
fim_jogo = False
console = Console()

# Referência para função de retorno ao menu (a ser atribuída externamente)
voltar_menu_callback = None

def limpar_tela():
    """Limpa o terminal conforme o sistema operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')


def iniciar_jogador(dificuldade: str):
    """
    Inicializa a posição e pontuação do jogador com base na dificuldade.

    Args:
        dificuldade (str): Um dos níveis ('facil', 'medio', 'dificil',
                           'super-dificil', 'max-dificil').
    """
    global jogador_pos, pontuacao
    jogador_pos = [1, 1]
    
    if dificuldade == "facil":
        pontuacao = 500
    elif dificuldade == "medio":
        pontuacao = 1000
    elif dificuldade == "dificil":
        pontuacao = 1600
    elif dificuldade == "super-dificil":
        pontuacao = 2500
    elif dificuldade == "max-dificil":
        pontuacao = 3000
    else:
        pontuacao = 500  # Padrão
    

def mover(direcao, lab):
    """
    Move o jogador no labirinto, se possível, e atualiza o estado do jogo.

    Args:
        direcao (str): Direção do movimento ('up', 'down', 'left', 'right').
        lab (list[list[str]]): Estrutura do labirinto.
    """
    global jogador_pos, pontuacao, fim_jogo

    i, j = jogador_pos
    nova_pos = jogador_pos[:]

    if direcao == "up":
        nova_pos[0] -= 1
    elif direcao == "down":
        nova_pos[0] += 1
    elif direcao == "left":
        nova_pos[1] -= 1
    elif direcao == "right":
        nova_pos[1] += 1
    
    if 0 <= nova_pos[0] < len(lab) and 0 <= nova_pos[1] < len(lab[0]):
        if lab[nova_pos[0]][nova_pos[1]] != "#":
            jogador_pos[:] = nova_pos
            pontuar()
            if som_ativado:
                som_passo.play()  #  toca o som de passo
            if lab[nova_pos[0]][nova_pos[1]] == "F":
                if som_ativado:
                    som_vitoria.play()  # som de vitória
                console.print(Panel.fit(
                    "[bold green]🎉 Você venceu o labirinto! Parabéns![/bold green]\n[cyan]Voltando ao menu...[/cyan]",
                    title="Fim de jogo",
                    border_style="bold green"
                ))
                encerrar_jogo()
    limpar_tela()  # limpar tela
    console.print(f"[green]Numero de movimentos:[/green] {movimentos}")
    console.print(f"[yellow]Pontuação:[/yellow] {pontuacao}")
    
    labirinto.imprimir_labirinto(lab, jogador_pos)
    

def pontuar():
    """
    Atualiza a pontuação e incrementa o número de movimentos do jogador.
    """
    global movimentos
    global pontuacao
    pontuacao -= 10
    movimentos += 1

def encerrar_jogo():
    """
    Encerra o jogo, imprime mensagem de despedida e retorna ao menu, se aplicável.
    """
    global fim_jogo
    fim_jogo = True
    if som_ativado:
        som_saida.play()  # som de saída
    console.print(Panel.fit(
        "[bold red]👋 Saindo do jogo. Até a próxima, aventureiro(a)![/bold red]",
        title="Saída",
        border_style="red"
    ))
    if voltar_menu_callback:
        voltar_menu_callback()  # Retorna ao menu principal


def aguardar_movimento(lab):
    """
    Aguarda a entrada do jogador via teclado e processa os comandos.

    Args:
        lab (list[list[str]]): Estrutura do labirinto.
    """
    console.print("[bold cyan]Use as setas do teclado para se mover. Pressione ESC para sair.[/bold cyan]\n")

    def on_press(tecla):
        global fim_jogo

        try:
            match tecla:
                case keyboard.Key.up:
                    mover("up", lab)
                case keyboard.Key.down:
                    mover("down", lab)
                case keyboard.Key.left:
                    mover("left", lab)
                case keyboard.Key.right:
                    mover("right", lab)
                case keyboard.Key.esc:
                    encerrar_jogo()
                    return False
        except Exception as e:
            console.print(f"[red]Erro ao processar tecla: {e}[/red]")

        if fim_jogo:
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def mostrar_solucao_recursiva(labirinto, inicio=(1, 1), caminho=None, visitados=None):
    """
    Resolve o labirinto de forma recursiva e retorna o caminho até a saída.

    Args:
        labirinto (list[list[str]]): Estrutura do labirinto.
        inicio (tuple): Coordenadas iniciais do jogador.
        caminho (list): Caminho acumulado durante a recursão.
        visitados (set): Conjunto de coordenadas já visitadas.

    Returns:
        list: Lista de tuplas representando o caminho da solução, ou None se não houver solução.
    """
    if caminho is None:
        caminho = []
    if visitados is None:
        visitados = set()

    i, j = inicio

    if not (0 <= i < len(labirinto) and 0 <= j < len(labirinto[0])):
        return None  # Fora dos limites

    if labirinto[i][j] == '#' or (i, j) in visitados:
        return None  # Parede ou já visitado

    caminho.append((i, j))
    visitados.add((i, j))

    if labirinto[i][j] == 'F':
        return caminho  # Solução encontrada

    # Movimentos possíveis: cima, baixo, esquerda, direita
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        proximo = (i + di, j + dj)
        resultado = mostrar_solucao_recursiva(labirinto, proximo, caminho[:], visitados.copy())
        if resultado:
            return resultado

    return None  # Sem solução a partir desse caminho
