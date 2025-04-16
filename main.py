# main
import argparse
from rich.console import Console
from aventura_pkg import utils, jogador
from aventura_pkg.exportar_docstrings import exportar_docstrings_html

console = Console()

# Exporta as docstrings automaticamente ao iniciar o jogo
try:
    exportar_docstrings_html("aventura_pkg", "aventura_pkg.html")
    console.print("[green]📄 Documentação atualizada com sucesso: [bold]aventura_pkg.html[/bold][/green]\n")
except Exception as e:
    console.print(f"[red]❌ Erro ao gerar documentação: {e}[/red]\n")


def obter_dados_do_jogador():
    """
    Coleta as informações do jogador via terminal.

    Retorna:
        tuple: Uma tupla contendo o nome (str), cor (str), dificuldade (str) e se o som está ativo (bool).
    """
    nome = ""
    while not nome:
        console.print("[bold cyan]Digite o seu nome de jogador:[/bold cyan]", end=" ")
        nome = input().strip()
        if not nome:
            console.print("[red]⚠️ O nome não pode estar vazio. Tente novamente.[/red]")

    console.print('\n[bold cyan]Digite uma cor para o seu nome (ex: green, cyan, red):[/bold cyan]')
    cor = input('Cor do Nome: ').strip() or 'green'

    console.print('''\n[bold cyan]Escolha um nível de dificuldade: [/bold cyan]
    1 - fácil
    2 - médio
    3 - difícil
    4 - super-difícil
    5 - max-difícil ''')
    dificuldade_input = input('Nível de dificuldade: ').strip()

    dificuldade_map = {
        '1': 'facil',
        '2': 'medio',
        '3': 'dificil',
        '4': 'super-dificil',
        '5': 'max-dificil' 
    }
    dificuldade = dificuldade_map.get(dificuldade_input, 'facil')

    console.print('\n[bold cyan]Deseja desativar os sons do jogo? (s/n) [/bold cyan]')
    som_input = input('Desativar som: ').strip().lower()
    som_ativo = False if som_input == 's' else True

    return nome, cor, dificuldade, som_ativo

def main():
    """
    Ponto de entrada principal do jogo com suporte a argumentos via linha de comando.
    """
    parser = argparse.ArgumentParser(description="Jogo: Aventura no Labirinto")
    parser.add_argument('--name', type=str, help='Nome do jogador')
    parser.add_argument('--color', type=str, help='Cor do texto (ex: red, blue, green)')
    parser.add_argument('--dificuldade', type=str, choices=[
        'facil', 'medio', 'dificil', 'super-dificil', 'max-dificil'
    ], help='Nível de dificuldade')
    parser.add_argument('--som', dest='som', action='store_true', help='Ativa o som do jogo')
    parser.add_argument('--sem-som', dest='som', action='store_false', help='Desativa o som do jogo')
    parser.set_defaults(som=True)

    args = parser.parse_args()

    # Se não passou nada, entra no modo interativo
    if not (args.name and args.color and args.dificuldade):
        nome, cor, dificuldade, som_ativo = obter_dados_do_jogador()
        args.name = nome
        args.color = cor
        args.dificuldade = dificuldade
        args.som = som_ativo

    # Configura som globalmente
    jogador.configurar_som(args.som)
    console.print(f"\n🌟 Bem-vindo(a), [bold {args.color}]{args.name}[/bold {args.color}]! Prepare-se para a aventura!", style=args.color)

    utils.exibir_menu(args)

if __name__ == '__main__':
    main()
