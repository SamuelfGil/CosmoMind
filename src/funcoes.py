import pygame

def quebrar_linhas(texto, fonte, largura_max):
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""
    
    for palavra in palavras:
        # CORRIGIDO: alterado de palabra para palavra
        test_linha = linha_atual + (" " if linha_atual else "") + palavra
        if fonte.size(test_linha)[0] <= largura_max:
            linha_atual = test_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return linhas

def altura_texto(texto, fonte, largura_max):
    linhas = quebrar_linhas(texto, fonte, largura_max)
    return len(linhas) * fonte.get_linesize()

def renderizar_texto(tela, texto, fonte, cor, x, y, largura_max):
    linhas = quebrar_linhas(texto, fonte, largura_max)
    for i, linha in enumerate(linhas):
        surf = fonte.render(linha, True, cor)
        tela.blit(surf, (x, y + i * fonte.get_linesize()))