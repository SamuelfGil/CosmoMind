import pygame
import random
import math
from src.config import LARGURA, ALTURA, BRANCO, AZUL_HOVER, VERMELHO, LARANJA

class Estrela:
    def __init__(self):
        self.x = random.randint(0, LARGURA)
        self.y = random.randint(0, ALTURA)
        self.velocidade = random.uniform(0.2, 1.2)
        self.tamanho = random.randint(1, 3)

    def mover(self):
        self.y += self.velocidade
        if self.y > ALTURA:
            self.y = 0
            self.x = random.randint(0, LARGURA)

    def desenhar(self, tela):
        pygame.draw.circle(tela, (200, 200, 255), (int(self.x), int(self.y)), self.tamanho)

LISTA_ESTRELAS = [Estrela() for _ in range(70)]

def desenhar_nave(tela, cx, cy, escudo_ativo=False):
    pontos = [
        (cx, cy - 22),       
        (cx - 18, cy + 16),  
        (cx, cy + 8),        
        (cx + 18, cy + 16)   
    ]
    pygame.draw.polygon(tela, (100, 180, 255), pontos)
    pygame.draw.polygon(tela, BRANCO, pontos, 2)

    pygame.draw.line(tela, LARANJA, (cx - 6, cy + 12), (cx - 6, cy + 20), 2)
    pygame.draw.line(tela, LARANJA, (cx + 6, cy + 12), (cx + 6, cy + 20), 2)

    if escudo_ativo:
        pygame.draw.circle(tela, AZUL_HOVER, (cx, cy), 32, 2)

class AsteroideMecanica:
    def __init__(self, x, y, raio=26):
        self.x = x
        self.y = y
        self.raio = raio
        
        self.pontos_relativos = []
        lados = 10 if raio > 40 else 7
        for i in range(lados):
            angulo = i * (2 * math.pi / lados)
            distancia = raio * random.uniform(0.75, 1.15)
            self.pontos_relativos.append((angulo, distancia))

    def desenhar(self, tela, angulo_rot):
        pontos_finais = []
        for ang, dist in self.pontos_relativos:
            nx = self.x + math.cos(ang + angulo_rot) * dist
            ny = self.y + math.sin(ang + angulo_rot) * dist
            pontos_finais.append((nx, ny))

        cor_corpo = (110, 75, 55) if self.raio < 40 else (145, 60, 50)
        pygame.draw.polygon(tela, cor_corpo, pontos_finais)
        pygame.draw.polygon(tela, (60, 40, 30) if self.raio < 40 else VERMELHO, pontos_finais, 2)

class Tiro:
    def __init__(self, x, y, alvo_x, alvo_y):
        self.x = x
        self.y = y
        self.raio = 4
        self.ativo = True
        
        dx = alvo_x - x
        dy = alvo_y - y
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            self.vx = (dx / dist) * 12.0
            self.vy = (dy / dist) * 12.0
        else:
            self.vx = 0
            self.vy = -12.0

    def mover(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > LARGURA or self.y < 0 or self.y > ALTURA:
            self.ativo = False

    def desenhar(self, tela):
        pygame.draw.circle(tela, (0, 255, 200), (int(self.x), int(self.y)), self.raio)