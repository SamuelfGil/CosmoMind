import pygame
import random
import math

pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CosmoMind - Asteroides")
relogio = pygame.time.Clock()


class Asteroide:
    def __init__(asteroide):
        asteroide.raio = random.randint(15, 35)
        asteroide.x = random.randint(asteroide.raio, LARGURA - asteroide.raio)
        asteroide.y = -asteroide.raio
        asteroide.velocidade = random.randint(2, 3)
        asteroide.ativo = True
        asteroide.num_pontas = random.randint(8, 12)
        asteroide.offsets = [random.randint(-asteroide.raio // 3, asteroide.raio // 3) for _ in
                             range(asteroide.num_pontas)]

    def mover(asteroide):
        asteroide.y += asteroide.velocidade
        if asteroide.y - asteroide.raio > ALTURA:
            asteroide.ativo = False

    def desenhar(asteroide, tela):
        pontos = []
        for i in range(asteroide.num_pontas):
            angulo = i * (2 * math.pi / asteroide.num_pontas)
            raio_atual = asteroide.raio + asteroide.offsets[i]
            px = asteroide.x + raio_atual * math.cos(angulo)
            py = asteroide.y + raio_atual * math.sin(angulo)
            pontos.append((px, py))

        pygame.draw.polygon(tela, (90, 50, 20), pontos)
        pygame.draw.polygon(tela, (139, 69, 19), pontos, 2)


asteroides = [Asteroide() for _ in range(3)]

rodando = True
while rodando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    for a in asteroides:
        a.mover()
        if not a.ativo:
            asteroides[asteroides.index(a)] = Asteroide()

    tela.fill((0, 0, 0))

    for a in asteroides:
        a.desenhar(tela)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()