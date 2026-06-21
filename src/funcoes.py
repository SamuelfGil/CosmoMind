import pygame


def quebrar_linhas(texto, fonte, largura_max):
    """Divide dinamicamente um texto longo em uma lista de linhas que cabem na largura máxima.

    Garante que as palavras não fiquem cortadas pela metade na borda da tela.

    Args:
        texto (str): O texto bruto que precisa ser adaptado e quebrado.
        fonte (pygame.font.Font): A fonte ativa utilizada para medir o tamanho dos caracteres.
        largura_max (int): Largura de limite horizontal em pixels permitida para a caixa de texto.

    Returns:
        list of str: Lista onde cada item representa uma linha de texto já formatada.
    """
    
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""
    
    for palavra in palavras:
        
        test_linha = linha_atual + (" " if linha_atual else "") + palavra
        
        
        if fonte.size(test_linha)[0] <= largura_max:
            linha_atual = test_linha
        else:
            # Caso estoure o limite máximo, a linha acumulada anterior fecha e é adicionada à lista
            linhas.append(linha_atual)
            
            linha_atual = palavra
            

    if linha_atual:
        linhas.append(linha_atual)
    return linhas


def altura_texto(texto, fonte, largura_max):
    """Calcula a altura total em pixels que um texto ocupará após ser envelopado/quebrado.

    Muito útil para dimensionamento dinâmico de caixas de diálogo, botões e painéis.

    Args:
        texto (str): O texto que será verificado.
        fonte (pygame.font.Font): A fonte que será usada no desenho.
        largura_max (int): Largura máxima disponível em pixels.

    Returns:
        int: Altura total estimada necessária em pixels para acomodar todas as linhas.
    """
    # Obtém a lista de linhas estruturadas quebrando o texto
    linhas = quebrar_linhas(texto, fonte, largura_max)
    # Multiplica a quantidade de linhas geradas pela altura vertical padrão (get_linesize) da fonte
    return len(linhas) * fonte.get_linesize()


def renderizar_texto(tela, texto, fonte, cor, x, y, largura_max):
    """Quebra e desenha na superfície da tela um bloco de texto com múltiplas linhas alinhadas.

    Args:
        tela (pygame.Surface): A superfície/janela de renderização do Pygame onde o texto será desenhado.
        texto (str): O texto bruto completo a ser renderizado.
        fonte (pygame.font.Font): O objeto de fonte contendo o estilo e tamanho definido.
        cor (tuple): Cor do texto no formato RGB (R, G, B).
        x (int): Coordenada horizontal superior esquerda de destino para o desenho.
        y (int): Coordenada vertical de início do topo do bloco.
        largura_max (int): Limite máximo horizontal de pixel para quebra de segurança.
    """
    # Processa as quebras ideais do texto antes de iniciar as operações gráficas de pintura
    linhas = quebrar_linhas(texto, fonte, largura_max)
    
    # Itera desenhando linha por linha ajustando sequencialmente o deslocamento vertical 'y'
    for i, linha in enumerate(linhas):
        # Transforma os caracteres de texto legíveis em superfícies de pixels renderizadas (Antialiasing ligado)
        surf = fonte.render(linha, True, cor)
        # Copia os pixels da superfície renderizada da linha para as coordenadas exatas da tela de exibição
        tela.blit(surf, (x, y + i * fonte.get_linesize()))