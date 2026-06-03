import pygame
import random

pygame.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CosmoMind - Asteroides")
relogio = pygame.time.Clock()

#define as propriedadesm como largura altura e velocidade
class Asteroide:
    def __init__(asteroide):
        asteroide.x= random.randint(20, LARGURA - 80)
        asteroide.y= -60
        asteroide.velocidade = random.randint(2, 3)
        asteroide.largura =random.randint (20,70)
        asteroide.altura= random.randint (20,70)
        asteroide.ativo =True

    def mover(asteroide):
        asteroide.y += asteroide.velocidade
        if asteroide.y > ALTURA:
            asteroide.ativo = False

    #função que atribue a posição e o aspécto do asteroide
    def desenhar(asteroide, tela):
        pygame.draw.rect(tela, (139,69,19), (asteroide.x, asteroide.y, asteroide.largura, asteroide.altura))


# Cria uma lista com 3 asteroides mas da pra ir alterando
asteroides = [Asteroide() for _ in range(3)]

#loop para continuar rodando
rodando = True
while rodando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    for a in asteroides:
        a.mover()
        # Se o asteroide saiu da tela, cria um novo no lugar
        if not a.ativo:
            asteroides[asteroides.index(a)] = Asteroide()

    tela.fill((0, 0, 0))

    for a in asteroides:
        a.desenhar(tela)

    pygame.display.flip()
    relogio.tick(60)


pygame.quit()