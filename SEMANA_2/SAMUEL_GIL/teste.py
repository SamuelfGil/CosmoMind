import pygame
import random

pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CosmoMind - Estrelas Espaciais")
relogio = pygame.time.Clock()

# Cria uma superfície temporária de 15x15 pixels com fundo transparente
IMAGEM_BASE = pygame.Surface((15, 15), pygame.SRCALPHA)
# Desenha um círculo amarelo simulando a estrela para o teste
pygame.draw.circle(IMAGEM_BASE, (255, 255, 100), (7, 7), 6)

# Dicionário com tamanhos pré-calculados para cada velocidade
IMAGENS_POR_VELOCIDADE = {}
for v in range(1, 6):
    tamanho = v * 3 + 3
    IMAGENS_POR_VELOCIDADE[v] = pygame.transform.scale(IMAGEM_BASE, (tamanho, tamanho))


class Estrela:
    def __init__(estrela, velocidade):
        estrela.x = random.randint(0, LARGURA)
        estrela.y = random.randint(0, ALTURA)
        estrela.velocidade = velocidade

    def mover(estrela):
        estrela.y += estrela.velocidade
        if estrela.y > ALTURA:
            estrela.y = -20
            estrela.x = random.randint(0, LARGURA)
            estrela.velocidade = random.randint(1, 5)

    def desenhar(estrela, tela):
        imagem_certa = IMAGENS_POR_VELOCIDADE[estrela.velocidade]
        tela.blit(imagem_certa, (estrela.x, estrela.y))


# Lista com 80 estrelas
estrelas = [Estrela(velocidade=random.randint(1, 5)) for _ in range(80)]

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    for e in estrelas:
        e.mover()

    tela.fill((10, 10, 25))

    for e in estrelas:
        e.desenhar(tela)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()