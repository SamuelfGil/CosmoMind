import pygame
import pygame.freetype

pygame.init()
pygame.freetype.init()
LARGURA = 800
ALTURA = 600

FUNDO = (10, 10, 30)
FUNDO_PAINEL = (15, 15, 45)
AZUL_ESC = (25, 35, 70)
AZUL = (50, 100, 200)
AZUL_HOVER = (70, 130, 240)
VERDE = (50, 200, 100)
VERDE_ESC = (30, 130, 60)
VERMELHO = (220, 70, 70)
VERMELHO_ESC = (150, 40, 40)
AMARELO = (255, 220, 50)
LARANJA = (255, 140, 30)
BRANCO = (240, 240, 255)
CINZA = (120, 130, 160)
CINZA_ESC = (55, 60, 85)
AMARELO_TIRO=(255, 255, 150)
VELOCIDADE_TIRO = 8
class AdaptadorFonte:
    def __init__(self, nome, tamanho, bold=False):
        self.font = pygame.freetype.SysFont(nome, tamanho)
        self.font.strong = bold
        self.tamanho = tamanho

    def render(self, texto, antialias, cor):
        surf, _ = self.font.render(texto, cor)
        return surf

    def size(self, texto):
        rect = self.font.get_rect(texto)
        return (rect.width, rect.height)

    def get_linesize(self):
        return int(self.tamanho * 1.2)

fonte_titulo = AdaptadorFonte("Arial", 34, bold=True)
fonte_pergunta = AdaptadorFonte("Arial", 19, bold=True)
fonte_alt = AdaptadorFonte("Arial", 16)
fonte_info = AdaptadorFonte("Arial", 18)
fonte_pequena = AdaptadorFonte("Arial", 14)