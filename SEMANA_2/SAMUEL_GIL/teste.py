import pygame
import random

pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CosmoMind - Estrelas Espaciais")
relogio = pygame.time.Clock()

# Carrega a imagem base
IMAGEM_BASE = pygame.image.load("estrela.png").convert_alpha()

# --- NOVO: Criamos um dicionário com tamanhos pré-calculados para cada velocidade ---
# Velocidade 1 terá tamanho 6x6, velocidade 5 terá tamanho 18x18, etc.
IMAGENS_POR_VELOCIDADE = {}
for v in range(1, 6):
    tamanho = v * 3 + 3  # Ajuste esses números para mudar o tamanho das estrelas
    IMAGENS_POR_VELOCIDADE[v] = pygame.transform.scale(IMAGEM_BASE, (tamanho, tamanho))


class Estrela:
    def __init__(estrela, velocidade):
        estrela.x = random.randint(0, LARGURA)
        estrela.y = random.randint(0, ALTURA)
        estrela.velocidade = velocidade

    def mover(estrela):
        estrela.y += estrela.velocidade
        if estrela.y > ALTURA:
            estrela.y = -20  # Começa um pouco acima do topo para não brotar do nada
            estrela.x = random.randint(0, LARGURA)
            # Ao resetar, dá uma nova velocidade aleatória para variar o cenário
            estrela.velocidade = random.randint(1, 5)

    def desenhar(estrela, tela):
        # Busca a imagem correspondente à velocidade atual da estrela
        imagem_certa = IMAGENS_POR_VELOCIDADE[estrela.velocidade]
        tela.blit(imagem_certa, (estrela.x, estrela.y))


# Cria uma lista com 80 estrelas (aumentei um pouco porque as menores dão sensação de vazio)
estrelas = [Estrela(velocidade=random.randint(1, 5)) for _ in range(80)]

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    for e in estrelas:
        e.mover()

    tela.fill((10, 10, 25))  # Um tom de azul escuro/espacial em vez de preto puro

    for e in estrelas:
        e.desenhar(tela)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()