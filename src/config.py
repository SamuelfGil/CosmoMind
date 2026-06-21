import pygame

# Inicialização compulsória dos módulos internos do Pygame e renderizadores de texto
pygame.init()
pygame.font.init()

# Configurações de Dimensão da Janela de Exibição
LARGURA = 1024
ALTURA = 720

# Paleta de Cores em Formato RGB 
FUNDO = (10, 10, 22)
FUNDO_PAINEL = (18, 18, 38)

BRANCO = (240, 240, 255)
CINZA = (160, 165, 180)
CINZA_ESC = (45, 45, 65)

AZUL = (40, 90, 210)
AZUL_ESC = (25, 45, 110)
AZUL_HOVER = (60, 140, 255)

VERDE = (40, 210, 110)
VERDE_ESC = (20, 100, 50)

VERMELHO = (220, 50, 70)
VERMELHO_ESC = (110, 25, 35)

LARANJA = (240, 110, 40)
AMARELO = (250, 210, 50)

# Inicialização e Configuração das Fontes Tipográficas do Sistema
fonte_titulo = pygame.font.SysFont("Arial", 36, bold=True)
fonte_pergunta = pygame.font.SysFont("Arial", 22, bold=True)
fonte_alt = pygame.font.SysFont("Arial", 18)
fonte_info = pygame.font.SysFont("Arial", 18, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 14)