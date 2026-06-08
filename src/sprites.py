import pygame
import random
import math
from src.config import LARGURA, ALTURA, LARANJA, AMARELO_TIRO, VELOCIDADE_TIRO

# Criando um cache de imagens para as estrelas não pesarem o jogo gerando superfícies novas toda hora
IMAGEM_BASE = pygame.Surface((15, 15), pygame.SRCALPHA)
pygame.draw.circle(IMAGEM_BASE, (255, 255, 100), (7, 7), 6)

IMAGENS_POR_VELOCIDADE = {}
for v in range(1, 6):
    tamanho = v * 3 + 3
    IMAGENS_POR_VELOCIDADE[v] = pygame.transform.scale(IMAGEM_BASE, (tamanho, tamanho))


# Classe que cuida do efeito de fundo das estrelas correndo (Efeito Parallax)(Gil efeito)
class Estrela:
    def __init__(self, velocidade=None):
        self.x = random.randint(0, LARGURA)
        self.y = random.randint(0, ALTURA)
        # Se não passar velocidade, escolhe uma aleatória (mais rápidas parecem maiores/mais perto)
        self.velocidade = velocidade if velocidade else random.randint(1, 5)

    def mover(self):
        self.y += self.velocidade
        # Se passou do final da tela, joga de volta pro topo em uma posição X nova
        if self.y > ALTURA:
            self.y = -20
            self.x = random.randint(0, LARGURA)
            self.velocidade = random.randint(1, 5)

    def desenhar(self, superficie):
        # Puxa a imagem do tamanho certo direto do nosso cache
        imagem_certa = IMAGENS_POR_VELOCIDADE[self.velocidade]
        superficie.blit(imagem_certa, (self.x, self.y))

# Gera a lista com as 80 estrelas do plano de fundo
LISTA_ESTRELAS = [Estrela() for _ in range(80)]


# Desenha o triângulo que forma o visual da nave
def pontos_nave(cx, cy, tamanho=18):
    return [
        (cx, cy - tamanho),                        # Bico
        (cx - tamanho * 0.7, cy + tamanho * 0.6),  # Asa esquerda
        (cx, cy + tamanho * 0.2),                  # Meio da base
        (cx + tamanho * 0.7, cy + tamanho * 0.6),  # Asa direita
    ]


def desenhar_nave(superficie, cx, cy, escudo_ativo=False):
    # Se o escudo tiver ativo, desenha a bolha azul translúcida em volta da nave
    if escudo_ativo:
        s = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(s, (80, 160, 255, 55), (40, 40), 36)
        pygame.draw.circle(s, (100, 200, 255, 130), (40, 40), 36, 2)
        superficie.blit(s, (cx - 40, cy - 40))

    # Desenha o polígono da nave
    pts = pontos_nave(cx, cy)
    pygame.draw.polygon(superficie, (60, 160, 255), pts)
    pygame.draw.polygon(superficie, (160, 220, 255), pts, 2)

    # Efeito do foguinho do motor oscilando de tamanho aleatoriamente
    chama = [
        (cx - 8, cy + 18),
        (cx, cy + 18 + random.randint(6, 14)),
        (cx + 8, cy + 18),
    ]
    pygame.draw.polygon(superficie, LARANJA, chama)


# Inimigo gerado com pontas irregulares pra parecer uma rocha real e ficar diferente(qualuquer coisa mudamos depois)
class AsteroideMecanica:
    def __init__(self, x, y, raio=26):
        self.raio = raio
        self.x = float(x)
        self.y = float(y)
        self.num_pontas = random.randint(8, 12)
        # Cria pequenas imperfeições no raio de cada ponta pra não ficar um círculo perfeito
        self.offsets = [random.randint(-self.raio // 3, self.raio // 3) for _ in range(self.num_pontas)]

    def desenhar(self, superficie, angulo_rot=0.0):
        pontos = []
        # Calcula a posição de cada quina do asteroide usando seno/cosseno e a rotação atual
        for i in range(self.num_pontas):
            angulo = i * (2 * math.pi / self.num_pontas) + angulo_rot
            raio_atual = self.raio + self.offsets[i]
            px = self.x + raio_atual * math.cos(angulo)
            py = self.y + raio_atual * math.sin(angulo)
            pontos.append((px, py))

        # Pinta o asteroide de marrom
        pygame.draw.polygon(superficie, (90, 50, 20), pontos)
        pygame.draw.polygon(superficie, (139, 69, 19), pontos, 2)


# Classe do laser que a nave solta quando você acerta a pergunta
class Tiro:
    def __init__(self, x, y, destino_x, destino_y):
        self.x = float(x)
        self.y = float(y)
        self.raio = 4
        self.ativo = True

        # Vetores matemáticos para fazer o tiro ir exatamente na direção do asteroide
        dx = destino_x - x
        dy = destino_y - y
        distancia = math.hypot(dx, dy)

        if distancia == 0:
            self.dx = 0
            self.dy = -1
        else:
            # Normaliza o vetor pra velocidade do tiro não variar com a distância
            self.dx = dx / distancia
            self.dy = dy / distancia

    def mover(self):
        self.x += self.dx * VELOCIDADE_TIRO
        self.y += self.dy * VELOCIDADE_TIRO

        # Se o tiro sumir da tela, marca ele como inativo pro jogo apagar ele da memória
        if self.x < 0 or self.x > LARGURA or self.y < 0 or self.y > ALTURA:
            self.ativo = False

    def desenhar(self, superficie):
        # Desenha o laser com duas camadas de cor pra dar efeito de brilho
        pygame.draw.circle(superficie, AMARELO_TIRO, (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(superficie, LARANJA, (int(self.x), int(self.y)), self.raio + 2, 1)