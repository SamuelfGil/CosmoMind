from src.config import fonte_alt

# Lógica para quebrar o texto em várias linhas se ele for maior que a largura da caixa
def quebrar_linhas(texto, fonte, largura_max):
    palavras = texto.split(" ")
    linhas, atual = [], ""
    
    for p in palavras:
        teste = atual + (" " if atual else "") + p
        # Se a palavra couber na linha atual, mantém ela ali
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            # Se não couber, fecha a linha atual e joga a palavra pra próxima
            if atual:
                linhas.append(atual)
            atual = p
            
    # Não esquecer de pegar a última palavra que sobrou no loop
    if atual:
        linhas.append(atual)
    return linhas


# Desenha o texto quebrado na tela, linha por linha, respeitando a altura
def renderizar_texto(surface, texto, fonte, cor, x, y, largura_max):
    linhas = quebrar_linhas(texto, fonte, largura_max)
    h = fonte.get_linesize()
    
    for i, l in enumerate(linhas):
        surface.blit(fonte.render(l, True, cor), (x, y + i * h))
        
    # Retorna o tamanho vertical total que o texto usou na tela
    return len(linhas) * h


# Calcula o tamanho do texto antes de desenhar (bom pra ajustar o tamanho das caixas)
def altura_texto(texto, fonte, largura_max):
    return len(quebrar_linhas(texto, fonte, largura_max)) * fonte.get_linesize()