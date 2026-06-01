import pygame
import random

# Inicializa o Pygame
pygame.init()


LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CosmoMind - Estrelas")
relogio = pygame.time.Clock()


class Estrela:
    def __init__(estrela, velocidade):
        estrela.x = random.randint(0, LARGURA)
        estrela.y = random.randint(0, ALTURA)
        estrela.velocidade = velocidade
        
    def mover(estrela):
        estrela.y += estrela.velocidade
        # Se sair da tela por baixo, reaparece no topo
        if estrela.y > ALTURA:
            estrela.y = 0
            estrela.x = random.randint(0, LARGURA)
            
    def desenhar(estrela, tela):
        pygame.draw.circle(tela, (255, 255, 255), (estrela.x, estrela.y), 2)

# Cria uma lista com 50 estrelas, cada uma com uma velocidade aleatória
estrelas = [Estrela(velocidade=random.randint(1, 5)) for _ in range(50)]

# 5. LOOP PRINCIPAL DO JOGO (criei para testar se a janela esta funcionando)
rodando = True
while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
    
    for e in estrelas:
        e.mover()
        
    
    tela.fill((0, 0, 0)) 
    
    for e in estrelas:
        e.desenhar(tela)
        
    pygame.display.flip() 
    relogio.tick(60)       


pygame.quit()