import pygame
import random
# Importa as configurações do arquivo que estruturamos antes
from src.config import LARGURA_TELA, ALTURA_TELA, BRANCO, AZUL, VERMELHO
def pegar_sprite(local_arquivo, x, y, width, height, scale=1):
    """Corta um único elemento de uma spritesheet BMP e remove o fundo."""
    
    
    sheet = pygame.image.load(local_arquivo).convert()

    
    image = pygame.Surface((width, height))
    
    
    image.blit(sheet, (0, 0), (x, y, width, height))
    
    
    cor_do_fundo = image.get_at((0, 0))
    image.set_colorkey(cor_do_fundo)
    
    
    if scale != 1:
        novo_largura = int(width * scale)
        novo_altura = int(height * scale)
        image = pygame.transform.scale(image, (novo_largura, novo_altura))
        
    return image
class Estrela:
    def __init__(estrela, velocidade):
        estrela.x = random.randint(0, LARGURA_TELA)
        estrela.y = random.randint(0, ALTURA_TELA)
        estrela.velocidade = velocidade
        
    def mover(estrela):
        estrela.y += estrela.velocidade
        if estrela.y > ALTURA_TELA:
            estrela.y = 0
            estrela.x = random.randint(0, LARGURA_TELA)
            
    def desenhar(estrela, tela):
        pygame.draw.circle(tela, BRANCO, (estrela.x, estrela.y), 2)