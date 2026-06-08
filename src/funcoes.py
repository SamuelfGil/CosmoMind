from src.config import fonte_alt

def quebrar_linhas(texto, fonte, largura_max):
    palavras = texto.split(" ")
    linhas, atual = [], ""
    for p in palavras:
        teste = atual + (" " if atual else "") + p
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def renderizar_texto(surface, texto, fonte, cor, x, y, largura_max):
    linhas = quebrar_linhas(texto, fonte, largura_max)
    h = fonte.get_linesize()
    for i, l in enumerate(linhas):
        surface.blit(fonte.render(l, True, cor), (x, y + i * h))
    return len(linhas) * h


def altura_texto(texto, fonte, largura_max):
    return len(quebrar_linhas(texto, fonte, largura_max)) * fonte.get_linesize()