import pygame
import json
import random
import sys
import os
import math
import pygame.freetype

# --- Inicialização ---
pygame.init()
pygame.freetype.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Espaço de Perguntas - CosmoMind")
relogio = pygame.time.Clock()

# --- Cores ---
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


# --- Fontes Adaptadas com Freetype ---
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


# ------------------------------------------------------------------ helpers de texto

def quebrar_linhas(texto, fonte, largura_max):
    palavras = texto.split(" ")
    linhas, atual = [], ""
    for p in palavras:
        teste = atual + (" " if atual else "") + p
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def renderizar_texto(surface, texto, fonte, cor, x, y, largura_max):
    linhas = quebrar_linhas(texto, fonte, largura_max)
    h = fonte.get_linesize()
    for i, l in enumerate(linhas):
        surface.blit(fonte.render(l, True, cor), (x, y + i * h))
    return len(linhas) * h


def altura_texto(texto, fonte, largura_max):
    return len(quebrar_linhas(texto, fonte, largura_max)) * fonte.get_linesize()


# ------------------------------------------------------------------ novo sistema de estrelas

IMAGEM_BASE = pygame.Surface((15, 15), pygame.SRCALPHA)
pygame.draw.circle(IMAGEM_BASE, (255, 255, 100), (7, 7), 6)

IMAGENS_POR_VELOCIDADE = {}
for v in range(1, 6):
    tamanho = v * 3 + 3
    IMAGENS_POR_VELOCIDADE[v] = pygame.transform.scale(IMAGEM_BASE, (tamanho, tamanho))


class Estrela:
    def __init__(estrela, velocidade=None):
        estrela.x = random.randint(0, LARGURA)
        estrela.y = random.randint(0, ALTURA)
        estrela.velocidade = velocidade if velocidade else random.randint(1, 5)

    def mover(estrela):
        estrela.y += estrela.velocidade
        if estrela.y > ALTURA:
            estrela.y = -20
            estrela.x = random.randint(0, LARGURA)
            estrela.velocidade = random.randint(1, 5)

    def desenhar(estrela, superficie):
        imagem_certa = IMAGENS_POR_VELOCIDADE[estrela.velocidade]
        superficie.blit(imagem_certa, (estrela.x, estrela.y))


# Inicializa a lista global com 80 estrelas dinâmicas
LISTA_ESTRELAS = [Estrela() for _ in range(80)]

# ------------------------------------------------------------------ nave

NAVE_CX = LARGURA // 2
NAVE_CY = ALTURA // 2


def pontos_nave(cx, cy, tamanho=18):
    return [
        (cx, cy - tamanho),
        (cx - tamanho * 0.7, cy + tamanho * 0.6),
        (cx, cy + tamanho * 0.2),
        (cx + tamanho * 0.7, cy + tamanho * 0.6),
    ]


def desenhar_nave(cx, cy, escudo_ativo=False):
    if escudo_ativo:
        s = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(s, (80, 160, 255, 55), (40, 40), 36)
        pygame.draw.circle(s, (100, 200, 255, 130), (40, 40), 36, 2)
        tela.blit(s, (cx - 40, cy - 40))

    pts = pontos_nave(cx, cy)
    pygame.draw.polygon(tela, (60, 160, 255), pts)
    pygame.draw.polygon(tela, (160, 220, 255), pts, 2)

    chama = [
        (cx - 8, cy + 18),
        (cx, cy + 18 + random.randint(6, 14)),
        (cx + 8, cy + 18),
    ]
    pygame.draw.polygon(tela, LARANJA, chama)


# ------------------------------------------------------------------ novo sistema de asteroide integrado

class AsteroideMecanica:
    def __init__(self, x, y, raio=26):
        self.raio = raio
        self.x = float(x)
        self.y = float(y)
        self.num_pontas = random.randint(8, 12)
        # Offsets baseados na lógica do seu segundo código
        self.offsets = [random.randint(-self.raio // 3, self.raio // 3) for _ in range(self.num_pontas)]

    def desenhar(self, superficie, angulo_rot=0.0):
        pontos = []
        for i in range(self.num_pontas):
            # Adicionado o angulo_rot para manter o efeito de rotação espacial do CosmoMind
            angulo = i * (2 * math.pi / self.num_pontas) + angulo_rot
            raio_atual = self.raio + self.offsets[i]
            px = self.x + raio_atual * math.cos(angulo)
            py = self.y + raio_atual * math.sin(angulo)
            pontos.append((px, py))

        # Mistura de cores: paleta marrom do seu código com as bordas dinâmicas do CosmoMind
        pygame.draw.polygon(superficie, (90, 50, 20), pontos)
        pygame.draw.polygon(superficie, (139, 69, 19), pontos, 2)


# ------------------------------------------------------------------ carregamento

def carregar_perguntas(caminho="perguntas.json"):
    if not os.path.exists(caminho):
        return [
            {"pergunta": "O que é um algoritmo?",
             "alternativas": ["Uma linguagem de programação",
                              "Uma sequência lógica e finita de passos para resolver um problema",
                              "Uma peça de hardware do computador",
                              "Um erro que ocorre durante a compilação"],
             "correta": 1},
            {"pergunta": "Para que serve o 'if/else'?",
             "alternativas": ["Repetir código infinitamente",
                              "Armazenar dados permanentemente",
                              "Executar blocos diferentes conforme uma condição",
                              "Declarar variáveis"],
             "correta": 2},
            {"pergunta": "O que é uma variável?",
             "alternativas": ["Altera a velocidade do processador.",
                              "Espaço na memória para armazenar um dado que pode mudar.",
                              "Palavra reservada que não pode ser modificada.",
                              "Laço de repetição que varia seus passos."],
             "correta": 1},
            {"pergunta": "Qual estrutura é melhor quando sabemos o número exato de repetições?",
             "alternativas": ["while", "if/else", "for", "switch/case"],
             "correta": 2},
            {"pergunta": "O que é recursividade?",
             "alternativas": ["Uma função que chama a si mesma para resolver partes menores do problema.",
                              "Um for dentro de outro for.",
                              "Um erro lógico que trava o computador.",
                              "Converter código-fonte em linguagem de máquina."],
             "correta": 0},
        ]
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


# ================================================================== CosmoMind

class CosmoMind:
    S_INICIO = "inicio"
    S_JOGANDO = "jogando"
    S_FEEDBACK = "feedback"
    S_GAMEOVER = "gameover"
    S_FIM = "fim"

    LETRAS = ["A", "B", "C", "D"]
    CORES_LETRAS = [(80, 120, 220), (180, 90, 200), (50, 170, 150), (200, 130, 40)]

    PAINEL_Y = 290
    PAINEL_H = ALTURA - PAINEL_Y - 4

    AST_INICIO_X = LARGURA - 60
    AST_INICIO_Y = 60
    VEL_BASE = 0.6
    VEL_AUMENTO = 0.45

    def __init__(self):
        self.todas = carregar_perguntas()
        self.reiniciar()

    def reiniciar(self):
        self.perguntas = random.sample(self.todas, len(self.todas))
        self.indice = 0
        self.pontuacao = 0
        self.estado = self.S_INICIO
        self.hover = -1
        self.selecionada = -1
        self.erros = 0

        # Instancia o novo asteroide usando a sua classe com os offsets customizados
        self.asteroide = AsteroideMecanica(self.AST_INICIO_X, self.AST_INICIO_Y, raio=24)
        self.ast_vel = self.VEL_BASE
        self.ast_rot = 0.0

        self.flash_timer = 0
        self.escudo_timer = 0
        self.ast_empurrado = False

        self._calcular_layout()

    def _calcular_layout(self):
        self.rects_alt = []
        if self.indice >= len(self.perguntas):
            return
        pergunta = self.perguntas[self.indice]
        x = 50
        lw = LARGURA - 100
        y = self.PAINEL_Y + 68
        gap = 7

        for i, alt in enumerate(pergunta["alternativas"]):
            h = max(44, altura_texto(alt, fonte_alt, lw - 44) + 18)
            self.rects_alt.append(pygame.Rect(x, y, lw, h))
            y += h + gap

    def processar_evento(self, evento):
        if evento.type == pygame.MOUSEMOTION:
            self._hover(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.estado == self.S_INICIO:
                self.estado = self.S_JOGANDO
            elif self.estado == self.S_JOGANDO:
                for i, r in enumerate(self.rects_alt):
                    if r.collidepoint(evento.pos):
                        self._responder(i)
                        break
            elif self.estado == self.S_FEEDBACK:
                self._avancar()
            elif self.estado in (self.S_GAMEOVER, self.S_FIM):
                if self._rect_btn().collidepoint(evento.pos):
                    self.reiniciar()

    def _hover(self, pos):
        if self.estado != self.S_JOGANDO:
            self.hover = -1
            return
        self.hover = next((i for i, r in enumerate(self.rects_alt) if r.collidepoint(pos)), -1)

    def _responder(self, idx):
        self.selecionada = idx
        correta = self.perguntas[self.indice]["correta"]
        if idx == correta:
            self.pontuacao += 1
            self.escudo_timer = 90
            self.ast_empurrado = True
        else:
            self.erros += 1
            self.ast_vel += self.VEL_AUMENTO
            self.flash_timer = 18
        self.estado = self.S_FEEDBACK

    def _avancar(self):
        self.selecionada = -1
        self.indice += 1
        if self.indice >= len(self.perguntas):
            self.estado = self.S_FIM
        else:
            self.estado = self.S_JOGANDO
            self._calcular_layout()

    def atualizar(self):
        # As estrelas se movem independente do estado do jogo (Menu, Jogando, etc)
        for estrela in LISTA_ESTRELAS:
            estrela.mover()

        if self.estado not in (self.S_JOGANDO, self.S_FEEDBACK):
            return

        self.ast_rot += 0.012

        # Lógica de perseguição matemática do Asteroide em direção à Nave
        dx = NAVE_CX - self.asteroide.x
        dy = (self.PAINEL_Y // 2 + 10) - self.asteroide.y
        dist = math.hypot(dx, dy)

        if dist < 1: return

        nx = dx / dist
        ny = dy / dist

        if self.ast_empurrado:
            self.asteroide.x -= nx * self.ast_vel * 5
            self.asteroide.y -= ny * self.ast_vel * 5
            self.ast_empurrado = False
        else:
            self.asteroide.x += nx * self.ast_vel
            self.asteroide.y += ny * self.ast_vel

        # Checa colisão física com a nave
        if dist - self.asteroide.raio < 18 + 4:
            self.estado = self.S_GAMEOVER

    def desenhar(self):
        tela.fill(FUNDO)

        # Renderiza as novas estrelas dinâmicas amarelas piscantes
        for estrela in LISTA_ESTRELAS:
            estrela.desenhar(tela)

        if self.estado == self.S_INICIO:
            self._d_inicio()
        elif self.estado in (self.S_JOGANDO, self.S_FEEDBACK):
            self._d_jogo()
        elif self.estado == self.S_GAMEOVER:
            self._d_gameover()
        elif self.estado == self.S_FIM:
            self._d_fim()

        pygame.display.flip()

    def _d_inicio(self):
        t = fonte_titulo.render("CosmoMind", True, AMARELO)
        tela.blit(t, t.get_rect(center=(LARGURA // 2, 160)))

        sub = fonte_info.render("Responda certo para afastar o asteroide!", True, BRANCO)
        tela.blit(sub, sub.get_rect(center=(LARGURA // 2, 220)))

        info = fonte_pequena.render("Se errar, o asteroide acelera — não deixe ele te atingir!", True, CINZA)
        tela.blit(info, info.get_rect(center=(LARGURA // 2, 255)))

        desenhar_nave(LARGURA // 2, 350)

        # Desenha o preview do novo asteroide de pontas
        preview_ast = AsteroideMecanica(LARGURA // 2 + 120, 320, raio=22)
        preview_ast.desenhar(tela, angulo_rot=0.3)

        seta = fonte_info.render("<- asteroide", True, LARANJA)
        tela.blit(seta, (LARGURA // 2 + 148, 310))

        nave_l = fonte_info.render("nave ->", True, (100, 180, 255))
        tela.blit(nave_l, (LARGURA // 2 - nave_l.get_width() - 26, 338))

        self._btn("Iniciar jogo", (LARGURA // 2, 440))

    def _d_jogo(self):
        pergunta = self.perguntas[self.indice]
        correta = pergunta["correta"]

        if self.flash_timer > 0:
            alfa = int(160 * self.flash_timer / 18)
            ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            ov.fill((200, 30, 30, alfa))
            tela.blit(ov, (0, 0))

        self._d_jogo_area(correta)
        self._d_painel_pergunta(pergunta, correta)

        if self.estado == self.S_FEEDBACK:
            d = fonte_pequena.render("Clique para continuar ->", True, CINZA)
            tela.blit(d, d.get_rect(center=(LARGURA // 2, ALTURA - 10)))

    def _d_jogo_area(self, correta):
        area_h = self.PAINEL_Y - 4
        pygame.draw.line(tela, AZUL_ESC, (0, self.PAINEL_Y - 2), (LARGURA, self.PAINEL_Y - 2), 1)

        bx, by, bw, bh = 12, 10, 200, 6
        pygame.draw.rect(tela, CINZA_ESC, (bx, by, bw, bh), border_radius=3)
        prog = int((self.indice / len(self.perguntas)) * bw)
        if prog:
            pygame.draw.rect(tela, AZUL, (bx, by, prog, bh), border_radius=3)

        pts = fonte_pequena.render(f"Pontos: {self.pontuacao}", True, AMARELO)
        tela.blit(pts, (LARGURA - pts.get_width() - 12, 8))

        num = fonte_pequena.render(f"{self.indice + 1}/{len(self.perguntas)}", True, CINZA)
        tela.blit(num, (bx, by + 12))

        perigo_txt = f"Vel. asteroide: {self.ast_vel:.1f}x"
        cor_vel = VERDE if self.ast_vel <= 1.2 else (LARANJA if self.ast_vel <= 2.0 else VERMELHO)
        vel_s = fonte_pequena.render(perigo_txt, True, cor_vel)
        tela.blit(vel_s, vel_s.get_rect(center=(LARGURA // 2, 24)))

        nave_y_area = area_h // 2 + 10
        desenhar_nave(NAVE_CX, nave_y_area, escudo_ativo=(self.escudo_timer > 0))

        # Restringe visualmente o y do asteroide para não vazar no painel inferior de perguntas
        ast_y_vis = self.asteroide.y
        if ast_y_vis > area_h - self.asteroide.raio:
            ast_y_vis = area_h - self.asteroide.raio

        # Renderiza o asteroide do jogo usando o seu modelo customizado
        backup_y = self.asteroide.y
        self.asteroide.y = ast_y_vis
        self.asteroide.desenhar(tela, self.ast_rot)
        self.asteroide.y = backup_y

        dist = math.hypot(NAVE_CX - self.asteroide.x, nave_y_area - self.asteroide.y)
        if dist < 140:
            av = fonte_pequena.render("! IMPACTO IMINENTE!", True, VERMELHO)
            tela.blit(av, av.get_rect(center=(LARGURA // 2, area_h - 18)))

    def _d_painel_pergunta(self, pergunta, correta):
        painel = pygame.Rect(0, self.PAINEL_Y, LARGURA, self.PAINEL_H)
        pygame.draw.rect(tela, FUNDO_PAINEL, painel)
        pygame.draw.rect(tela, AZUL_ESC, painel, 1)

        lw = LARGURA - 32
        renderizar_texto(tela, pergunta["pergunta"], fonte_pergunta, BRANCO, 16, self.PAINEL_Y + 10, lw)

        for i, (rect, alt) in enumerate(zip(self.rects_alt, pergunta["alternativas"])):
            self._d_alt(i, rect, alt, correta)

    def _d_alt(self, idx, rect, texto, correta):
        hover = idx == self.hover
        sel = idx == self.selecionada
        eh_correta = idx == correta
        feedback = self.estado == self.S_FEEDBACK

        if feedback:
            if sel and eh_correta:
                cf, cb, ct = VERDE_ESC, VERDE, BRANCO
            elif sel and not eh_correta:
                cf, cb, ct = VERMELHO_ESC, VERMELHO, BRANCO
            elif eh_correta:
                cf, cb, ct = VERDE_ESC, VERDE, BRANCO
            else:
                cf, cb, ct = CINZA_ESC, CINZA_ESC, CINZA
        else:
            cf = AZUL_ESC if hover else FUNDO_PAINEL
            cb = AZUL_HOVER if hover else AZUL_ESC
            ct = BRANCO

        pygame.draw.rect(tela, cf, rect, border_radius=8)
        pygame.draw.rect(tela, cb, rect, 2, border_radius=8)

        cx_ = rect.x + 20
        cy_ = rect.centery
        pygame.draw.circle(tela, self.CORES_LETRAS[idx], (cx_, cy_), 12)

        letra_surf = fonte_alt.render(self.LETRAS[idx], True, BRANCO)
        tela.blit(letra_surf, letra_surf.get_rect(center=(cx_, cy_)))

        if feedback and (sel or eh_correta):
            ic = "Y" if eh_correta else "X"
            cic = VERDE if eh_correta else VERMELHO
            is_ = fonte_alt.render(ic, True, cic)
            tela.blit(is_, is_.get_rect(midright=(rect.right - 10, cy_)))

        tw = rect.width - 50
        renderizar_texto(tela, texto, fonte_alt, ct,
                         rect.x + 38,
                         rect.centery - altura_texto(texto, fonte_alt, tw) // 2,
                         tw)

    def _d_gameover(self):
        ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        ov.fill((220, 50, 30, 80))
        tela.blit(ov, (0, 0))

        # Desenha o impacto usando a sua lógica de render do asteroide
        impacto_ast = AsteroideMecanica(NAVE_CX, NAVE_CY, raio=40)
        impacto_ast.desenhar(tela, self.ast_rot)

        t = fonte_titulo.render("IMPACTO!", True, VERMELHO)
        tela.blit(t, t.get_rect(center=(LARGURA // 2, 160)))

        s = fonte_info.render(f"Pontos: {self.pontuacao}  * Erros: {self.erros}", True, BRANCO)
        tela.blit(s, s.get_rect(center=(LARGURA // 2, 220)))

        msg = fonte_info.render("O asteroide te alcançou...", True, LARANJA)
        tela.blit(msg, msg.get_rect(center=(LARGURA // 2, 265)))

        self._btn("Tentar novamente", (LARGURA // 2, 340))

    def _d_fim(self):
        total = len(self.perguntas)
        pct = self.pontuacao / total * 100

        if pct == 100:
            msg, cm = "Piloto perfeito! Nenhum asteroide te pegou!", AMARELO
        elif pct >= 70:
            msg, cm = "Ótima pilotagem, astronauta!", VERDE
        elif pct >= 50:
            msg, cm = "Missão concluída, mas com danos...", LARANJA
        else:
            msg, cm = "A nave sofreu bastante. Estude mais!", VERMELHO

        t = fonte_titulo.render("Missão concluída!", True, BRANCO)
        tela.blit(t, t.get_rect(center=(LARGURA // 2, 130)))

        pl = fonte_titulo.render(f"{self.pontuacao} / {total}", True, AMARELO)
        tela.blit(pl, pl.get_rect(center=(LARGURA // 2, 210)))

        p2 = fonte_info.render(f"{pct:.0f}% de aproveitamento  * {self.erros} erro(s)", True, CINZA)
        tela.blit(p2, p2.get_rect(center=(LARGURA // 2, 265)))

        ms = fonte_info.render(msg, True, cm)
        tela.blit(ms, ms.get_rect(center=(LARGURA // 2, 315)))

        self._btn("Jogar novamente", (LARGURA // 2, 400))

    def _btn(self, texto, centro):
        r = pygame.Rect(0, 0, 230, 48)
        r.center = centro
        mouse = pygame.mouse.get_pos()
        cor = AZUL_HOVER if r.collidepoint(mouse) else AZUL
        pygame.draw.rect(tela, cor, r, border_radius=11)
        s = fonte_info.render(texto, True, BRANCO)
        tela.blit(s, s.get_rect(center=r.center))

    def _rect_btn(self):
        r = pygame.Rect(0, 0, 230, 48)
        if self.estado == self.S_GAMEOVER:
            r.center = (LARGURA // 2, 340)
        else:
            r.center = (LARGURA // 2, 400)
        return r


# ================================================================== main

def main():
    jogo = CosmoMind()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit();
                sys.exit()
            jogo.processar_evento(ev)

        jogo.atualizar()
        jogo.desenhar()
        relogio.tick(60)


if __name__ == "__main__":
    main()