import pygame
import pygame.freetype

# Inicializa o que o pygame precisa pra desenhar a tela e os textos
pygame.init()
pygame.freetype.init()

# Resolução da tela do jogo
LARGURA = 800
ALTURA = 600

# Paleta de cores do jogo (padrão RGB)
FUNDO = (10, 10, 30)            # Azul escuro pro espaço
FUNDO_PAINEL = (15, 15, 45)     # Fundo do painel de perguntas
AZUL_ESC = (25, 35, 70)         # Borda padrão das caixas
AZUL = (50, 100, 200)           # Cor dos botões e da barra de progresso
AZUL_HOVER = (70, 130, 240)     # Cor de quando o mouse passa por cima do botão
VERDE = (50, 200, 100)          # Feedback de acerto
VERDE_ESC = (30, 130, 60)       # Caixa da resposta certa
VERMELHO = (220, 70, 70)        # Feedback de erro
VERMELHO_ESC = (150, 40, 40)    # Caixa da resposta errada
AMARELO = (255, 220, 50)        # Destaques e pontuação
LARANJA = (255, 140, 30)        # Fogo do motor e contorno do tiro
BRANCO = (240, 240, 255)        # Cor geral dos textos
CINZA = (120, 130, 160)         # Textos secundários e dicas
CINZA_ESC = (55, 60, 85)        # Fundo da barra de progresso esvaziada

# Configurações do laser da nave
AMARELO_TIRO = (255, 255, 150)
VELOCIDADE_TIRO = 8

# ajuste pra adaptar a biblioteca freetype pro jeito antigo de usar fontes (gil rever)
class AdaptadorFonte:
    def __init__(self, nome, tamanho, bold=False):
        self.font = pygame.freetype.SysFont(nome, tamanho)
        self.font.strong = bold
        self.tamanho = tamanho

    def render(self, texto, antialias, cor):
        # Retorna só a superfície do texto ignorando o rect nativo dele
        surf, _ = self.font.render(texto, cor)
        return surf

    def size(self, texto):
        # Mede o tamanho em pixels que o texto vai ocupar na tela
        rect = self.font.get_rect(texto)
        return (rect.width, rect.height)

    def get_linesize(self):
        # Calcula o espaçamento pro texto não ficar um em cima do outro na próxima linha
        return int(self.tamanho * 1.2)

# Definindo os tamanhos de fonte que o jogo vai usar
fonte_titulo = AdaptadorFonte("Arial", 34, bold=True)
fonte_pergunta = AdaptadorFonte("Arial", 19, bold=True)
fonte_alt = AdaptadorFonte("Arial", 16)
fonte_info = AdaptadorFonte("Arial", 18)
fonte_pequena = AdaptadorFonte("Arial", 14)