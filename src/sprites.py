import pygame
import random
import math
from src.config import LARGURA, ALTURA, BRANCO, AZUL_HOVER, VERMELHO, LARANJA

class Estrela:
    """Representa uma partícula individual do efeito de fundo de rolagem de estrelas (Parallax)."""

    def __init__(self):
        """Inicializa coordenadas randômicas, diâmetro e velocidades para o efeito de profundidade."""
        self.x = random.randint(0, LARGURA)
        self.y = random.randint(0, ALTURA)
        # Estrelas mais rápidas e maiores criam ilusão de proximidade física tridimensional
        self.velocidade = random.uniform(0.2, 1.2)
        self.tamanho = random.randint(1, 3)

    def mover(self):
        """Aplica deslocamento vertical e reseta a posição no topo caso ultrapasse a borda inferior."""
        self.y += self.velocidade
        if self.y > ALTURA:
            self.y = 0
            self.x = random.randint(0, LARGURA)

    def desenhar(self, tela):
        """Renderiza a partícula na superfície gráfica.

        Args:
            tela (pygame.Surface): Superfície de destino.
        """
        pygame.draw.circle(tela, (200, 200, 255), (int(self.x), int(self.y)), self.tamanho)


# Inicialização estática do lote fixo de 70 estrelas de fundo
LISTA_ESTRELAS = [Estrela() for _ in range(70)]


def desenhar_nave(tela, cx, cy, escudo_ativo=False):
    """Desenha geometricamente a nave do jogador através de polígonos vetoriais.

    Args:
        tela (pygame.Surface): Superfície gráfica onde a nave será pintada.
        cx (int): Posição X central da nave.
        cy (int): Posição Y central da nave.
        escudo_ativo (bool, optional): Se True, desenha uma barreira circular azul ao redor. Padrão: False.
    """
    # Mapeamento de vértices triangulares da aeronave estilizada
    pontos = [
        (cx, cy - 22),       # Nariz / Proa
        (cx - 18, cy + 16),  # Asa Esquerda
        (cx, cy + 8),        # Popa / Centro de empuxo
        (cx + 18, cy + 16)   # Asa Direita
    ]
    # Preechimento do corpo e contorno linear
    pygame.draw.polygon(tela, (100, 180, 255), pontos)
    pygame.draw.polygon(tela, BRANCO, pontos, 2)

    # Propulsores de fogo traseiros (Efeito de chamas laranjas fixas)
    pygame.draw.line(tela, LARANJA, (cx - 6, cy + 12), (cx - 6, cy + 20), 2)
    pygame.draw.line(tela, LARANJA, (cx + 6, cy + 12), (cx + 6, cy + 20), 2)

    # Renderiza círculo de força de barreira defensiva caso esteja ativo por acertos de quiz
    if escudo_ativo:
        pygame.draw.circle(tela, AZUL_HOVER, (cx, cy), 32, 2)


class AsteroideMecanica:
    """Gera e gerencia a estrutura geométrica irregular e única de um asteroide."""

    def __init__(self, x, y, raio=26):
        """Calcula de forma pseudo-aleatória os pontos e deformações do corpo rochoso.

        Args:
            x (float): Coordenada horizontal de spawn inicial.
            y (float): Coordenada vertical de spawn inicial.
            raio (int, optional): Raio médio de tamanho do corpo. Padrão: 26.
        """
        self.x = x
        self.y = y
        self.raio = raio
        
        self.pontos_relativos = []
        # Define a quantidade de lados com base na escala (Boss tem formato mais detalhado)
        lados = 10 if raio > 40 else 7
        for i in range(lados):
            # Divide o círculo (2 * PI) igualmente de acordo com a quantidade de lados
            angulo = i * (2 * math.pi / lados)
            # Aplica distorção de distância radial para gerar uma rocha irregular e não circular perfeito
            distancia = raio * random.uniform(0.75, 1.15)
            self.pontos_relativos.append((angulo, distancia))

    def desenhar(self, tela, angulo_rot):
        """Gira e renderiza os pontos irregulares do asteroide na tela.

        Args:
            tela (pygame.Surface): Tela de desenho.
            angulo_rot (float): Ângulo atual de rotação em radianos.
        """
        pontos_finais = []
        # Transforma coordenadas polares nativas (ângulo, distância) em cartesianas (X, Y) com rotação
        for ang, dist in self.pontos_relativos:
            nx = self.x + math.cos(ang + angulo_rot) * dist
            ny = self.y + math.sin(ang + angulo_rot) * dist
            pontos_finais.append((nx, ny))

        # Altera a cor do corpo dependendo do tamanho (Asteroides maiores/Boss ficam avermelhados)
        cor_corpo = (110, 75, 55) if self.raio < 40 else (145, 60, 50)
        pygame.draw.polygon(tela, cor_corpo, pontos_finais)
        pygame.draw.polygon(tela, (60, 40, 30) if self.raio < 40 else VERMELHO, pontos_finais, 2)


class Tiro:
    """Gerencia projéteis a laser de alta velocidade projetados da nave contra alvos asteroides."""

    def __init__(self, x, y, alvo_x, alvo_y):
        """Calcula os componentes vetoriais de velocidade necessários para guiar o tiro até o alvo.

        Args:
            x (float): Posição horizontal inicial (Boca do canhão da nave).
            y (float): Posição vertical inicial.
            alvo_x (float): Coordenada X alvo do asteroide capturado no instante do disparo.
            alvo_y (float): Coordenada Y alvo do asteroide.
        """
        self.x = x
        self.y = y
        self.raio = 4
        self.ativo = True
        
        # Distâncias parciais nos eixos X e Y até o alvo
        dx = alvo_x - x
        dy = alvo_y - y
        dist = math.hypot(dx, dy)
        
        # Divide pelo vetor hipotenusa para obter a direção e multiplica pelo multiplicador de velocidade fixo (12.0)
        if dist > 0:
            self.vx = (dx / dist) * 12.0
            self.vy = (dy / dist) * 12.0
        else:
            self.vx = 0
            self.vy = -12.0

    def mover(self):
        """Aplica deslocamento constante nas coordenadas e inativa o laser caso saia das bordas da tela."""
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > LARGURA or self.y < 0 or self.y > ALTURA:
            self.ativo = False

    def desenhar(self, tela):
        """Desenha a esfera de plasma energética de cor ciano.

        Args:
            tela (pygame.Surface): Janela de renderização.
        """
        pygame.draw.circle(tela, (0, 255, 200), (int(self.x), int(self.y)), self.raio)