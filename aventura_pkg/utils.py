# utils
"""
Funções utilitárias: menu, instruções e lógica de início de jogo.
"""
from rich.console import Console
from aventura_pkg import labirinto, jogador
from aventura_pkg.labirinto import animar_exemplo_labirinto
from rich.panel import Panel
import time

console = Console()

def exibir_menu(args):
    """
    Exibe o menu principal do jogo e gerencia as opções escolhidas pelo jogador.

    Args:
        args: Argumentos de linha de comando contendo nome, cor e dificuldade.
    """
    nome = args.name
    cor = args.color
    dificuldade = args.dificuldade
    console.print(f"\n[bold {cor}]Olá {nome}![/bold {cor}]")
    console.print(f"[yellow]Dificuldade atual:[/yellow] {dificuldade}")

    jogador.iniciar_jogador(dificuldade)

    while True:
        console.print("\n[bold cyan]Menu Principal[/bold cyan]")
        console.print("1. Instruções")
        console.print("2. Jogar")
        console.print("3. Ver solução")
        console.print("4. Sair")

        opcao = input("Escolha uma opção: ")

        # Verificação se a entrada é válida
        if opcao not in ['1', '2', '3', '4']:
            console.print("[red]Opção inválida. Tente novamente.[/red]")
            continue  # Continua o loop até uma opção válida ser escolhida

        match opcao:
            case '1':
                imprimir_instrucoes_animadas()
            case '2':
                '''import pygame
                pygame.init()'''
                console.print(f"\n{args.name}, vamos jogar!", style=args.color)
                iniciar_jogo(args)
            case '3':
                console.print("Calculando a solução do labirinto...\n", style="yellow")
                lab = labirinto.criar_labirinto(args.dificuldade)
                solucao = jogador.mostrar_solucao_recursiva(lab)
                if solucao:
                    for passo in solucao:
                        i, j = passo
                        lab[i][j] = "*" if lab[i][j] != "F" else "F"
                    labirinto.imprimir_labirinto(lab, solucao[-1])
                    console.print(f"\n[green]Caminho encontrado com {len(solucao)} passos.[/green]")
                else:
                    console.print("[red]Nenhuma solução encontrada.[/red]")
            case '4':
                console.print("Até a próxima! 🖖", style="green")
                break

def imprimir_instrucoes_animadas():
    """
    Exibe as instruções do jogo junto com uma animação de movimentação no labirinto.
    """
    instrucoes = (
        "[bold magenta]Instruções do Jogo[/bold magenta]\n\n"
        "- Use as setas do teclado para mover o personagem.\n"
        "- Encontre a saída do labirinto para vencer.\n"
        "- Vença todos os níveis de dificuldades.\n"
        "- Boa sorte!\n"
    )
    
    console.clear()
    console.print(Panel(instrucoes, title="📜 Instruções", border_style="magenta"))

    time.sleep(10)  # Tempo para leitura das instruções

    console.print("\n[bold blue]Exemplo de movimentação:[/bold blue]")
    animar_exemplo_labirinto()


def iniciar_jogo(args):
    """
    Inicia o jogo com o labirinto gerado e configura a lógica de retorno ao menu após o fim do jogo.

    Args:
        args: Argumentos de linha de comando contendo nome, cor e dificuldade.
    """
    from . import labirinto, jogador

    def voltar_ao_menu():
        """
        Função interna para retornar ao menu principal após o fim do jogo.
        """
        input("\nPressione Enter para voltar ao menu...")
        exibir_menu(args)  # Volta ao menu principal

    jogador.voltar_menu_callback = voltar_ao_menu  # Define o callback de retorno ao menu

    print(f"\n{args.name}, vamos jogar!")
    lab = labirinto.criar_labirinto(args.dificuldade)
    jogador.iniciar_jogador(args.dificuldade)
    labirinto.imprimir_labirinto(lab, jogador.jogador_pos)

    jogador.aguardar_movimento(lab)


