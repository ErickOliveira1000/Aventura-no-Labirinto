# exportar docstring
import importlib
import inspect
import os
from deep_translator import GoogleTranslator

def traduzir(texto):
    """
    Traduz um texto para o português usando o GoogleTranslator.

    Args:
        texto (str): Texto a ser traduzido.

    Returns:
        str: Texto traduzido ou original se houver erro.
    """
    try:
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except Exception:
        return texto  # Se der erro na tradução, retorna o texto original

def exportar_docstrings_html(pacote='aventura_pkg', arquivo_saida='aventura_pkg.html'):
    """
    Exporta as docstrings do pacote especificado para um arquivo HTML, com tradução para português.

    Args:
        pacote (str): Nome do pacote a ser documentado.
        arquivo_saida (str): Caminho do arquivo HTML de saída.
    """
    caminho_pacote = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", pacote))

    if not os.path.isdir(caminho_pacote):
        raise FileNotFoundError(f"O diretório do pacote {pacote} não foi encontrado em {caminho_pacote}")

    html = ["<html><head><meta charset='utf-8'><title>Documentação do pacote</title></head><body>"]
    html.append(f"<h1>Documentação do pacote: {pacote}</h1>")

    for nome_arquivo in os.listdir(caminho_pacote):
        if nome_arquivo.endswith(".py") and not nome_arquivo.startswith("__"):
            nome_modulo = f"{pacote}.{nome_arquivo[:-3]}"
            try:
                modulo = importlib.import_module(nome_modulo)
            except ModuleNotFoundError:
                continue

            html.append(f"<h2>Módulo: {nome_modulo}</h2>")

            doc_modulo = inspect.getdoc(modulo)
            if doc_modulo:
                doc_traduzida = traduzir(doc_modulo)
                html.append(f"<pre>{doc_traduzida}</pre>")

            for nome, objeto in inspect.getmembers(modulo):
                if inspect.isfunction(objeto) or inspect.isclass(objeto):
                    doc = inspect.getdoc(objeto)
                    if doc:
                        tipo = "Função" if inspect.isfunction(objeto) else "Classe"
                        doc_traduzida = traduzir(doc)
                        html.append(f"<h3>{tipo}: {nome}</h3>")
                        html.append(f"<pre>{doc_traduzida}</pre>")

    html.append("</body></html>")

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
