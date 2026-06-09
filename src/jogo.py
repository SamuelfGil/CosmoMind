import pygame
import random
import math
from src.config import *
from src.funcoes import renderizar_texto, altura_texto
from src.dados import carregar_perguntas
from src.sprites import LISTA_ESTRELAS, desenhar_nave, AsteroideMecanica, Tiro

# Sistema central que controla as telas e regras do jogo
class CosmoMind:
    # Os estados possíveis da nossa máquina de estados do jogo
    S_INICIO = "inicio"
    S_NICKNAME = "nickname"
    S_JOGANDO = "jogando"
    S_FEEDBACK = "feedback"
    S_GAMEOVER = "gameover"
    S_FIM = "fim"

    LETRAS = ["A", "B", "C", "D"]
    CORES_LETRAS = [(80, 120, 220), (180, 90, 200), (50, 170, 150), (200, 130, 40)]

    # Onde começa a divisão do painel inferior
    PAINEL_Y = 290
    PAINEL_H = ALTURA - PAINEL_Y - 4

    # Onde o asteroide nasce e as suas velocidades
    AST_INICIO_X = LARGURA - 60
    AST_INICIO_Y = 60
    VEL_BASE = 0.6
    VEL_AUMENTO = 0.45

    def __init__(self, tela):
        self.tela = tela
        # Puxa o banco de dados das perguntas do arquivo JSON
        self.todas = carregar_perguntas()
        self.reiniciar()

    def reiniciar(self):
        # Embaralha as perguntas pra toda partida ser diferente
        self.perguntas = random.sample(self.todas, len(self.todas))
        self.indice = 0
        self.pontuacao = 0
        self.estado = self.S_INICIO
        self.hover = -1
        self.selecionada = -1
        self.erros = 0

        self.nickname = ""
        self.max_caracteres = 12

        # Spawna o asteroide no canto superior direito
        self.asteroide = AsteroideMecanica(self.AST_INICIO_X, self.AST_INICIO_Y, raio=24)
        self.ast_vel = self.VEL_BASE
        self.ast_rot = 0.0

        # Timers que controlam efeitos visuais temporários 
        self.flash_timer = 0
        self.escudo_timer = 0
        
        # Gerenciamento dos lasers disparados pela nave
        self.tiros = []
        self.asteroide_destruido = False

        self._calcular_layout()

    def _calcular_layout(self):
        # Cria os retângulos de colisão das 4 alternativas com base no tamanho do texto delas
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
        # Escuta os movimentos e cliques do jogador
        if evento.type == pygame.MOUSEMOTION:
            self._hover(evento.pos)
        elif evento.type == pygame.KEYDOWN:
            if self.estado == self.S_NICKNAME:
                if evento.key == pygame.K_BACKSPACE:
                    self.nickname = self.nickname[:-1]
                elif evento.key == pygame.K_RETURN:
                    if len(self.nickname.strip()) > 0:
                        self.estado = self.S_JOGANDO
                else:
                    if len(self.nickname) < self.max_caracteres:
                        if evento.unicode.isalnum() or evento.unicode == " ":
                            self.nickname += evento.unicode
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.estado == self.S_INICIO:
                self.estado = self.S_NICKNAME
            elif self.estado == self.S_NICKNAME:
                if self._rect_btn_nickname().collidepoint(evento.pos):
                    if len(self.nickname.strip()) > 0:
                        self.estado = self.S_JOGANDO
            elif self.estado == self.S_JOGANDO:
                # Checa se o clique aconteceu dentro de algum botão de alternativa
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
        # Verifica se o mouse tá passando por cima de alguma alternativa pra dar o efeito visual
        if self.estado != self.S_JOGANDO:
            self.hover = -1
            return
        self.hover = next((i for i, r in enumerate(self.rects_alt) if r.collidepoint(pos)), -1)

    def _responder(self, idx):
        # Valida se a resposta que o player escolheu está certa ou errada
        self.selecionada = idx
        correta = self.perguntas[self.indice]["correta"]
        
        if idx == correta:
            self.pontuacao += 1
            self.escudo_timer = 90 # Liga o escudo por 90 frames
            
            # Atira o laser na direção exata do asteroide
            nave_x = LARGURA // 2
            nave_y = (self.PAINEL_Y // 2 + 10)
            novo_tiro = Tiro(nave_x, nave_y, self.asteroide.x, self.asteroide.y)
            self.tiros.append(novo_tiro)
        else:
            self.erros += 1
            self.ast_vel += self.VEL_AUMENTO # Punição: o asteroide acelera se errar
            self.flash_timer = 18             # Tela pisca em vermelho
            
        self.estado = self.S_FEEDBACK

    def _avancar(self):
        # Passa pra próxima pergunta do quiz
        self.selecionada = -1
        self.indice += 1
        
        # Se explodiu o asteroide na rodada passada, cria um novo no topo pra continuar o jogo
        if self.asteroide_destruido:
            self.asteroide = AsteroideMecanica(self.AST_INICIO_X, self.AST_INICIO_Y, raio=24)
            self.asteroide_destruido = False
            
        # Vê se o banco de perguntas acabou pra fechar a partida
        if self.indice >= len(self.perguntas):
            self.estado = self.S_FIM
        else:
            self.estado = self.S_JOGANDO
            self._calcular_layout()

    def atualizar(self):
        # Atualiza a movimentação de tudo que roda em tempo real na gameplay
        for estrela in LISTA_ESTRELAS:
            estrela.mover()

        # Mexe os tiros e remove da memória os que saíram da tela
        for tiro in self.tiros[:]:
            tiro.mover()
            if not tiro.ativo:
                self.tiros.remove(tiro)

        if self.estado not in (self.S_JOGANDO, self.S_FEEDBACK):
            return

        self.ast_rot += 0.012 # Faz o asteroide girar de leve enquanto cai

        NAVE_CX = LARGURA // 2
        nave_y_area = (self.PAINEL_Y // 2 + 10)

        # Move o asteroide em linha reta mirando o centro da nave
        if not self.asteroide_destruido:
            dx = NAVE_CX - self.asteroide.x
            dy = nave_y_area - self.asteroide.y
            dist = math.hypot(dx, dy)

            if dist >= 1:
                nx = dx / dist
                ny = dy / dist
                self.asteroide.x += nx * self.ast_vel
                self.asteroide.y += ny * self.ast_vel

            # Se a distância entre o asteroide e a nave for menor que o raio deles: BATEU (acaba o jogo)
            if dist - self.asteroide.raio < 18 + 4:
                self.estado = self.S_GAMEOVER

        # Checa colisão entre os lasers e o asteroide ativo
        if not self.asteroide_destruido:
            for tiro in self.tiros[:]:
                dist_tiro = math.hypot(tiro.x - self.asteroide.x, tiro.y - self.asteroide.y)
                if dist_tiro < (tiro.raio + self.asteroide.raio):
                    self.asteroide_destruido = True # Quebra o asteroide
                    if tiro in self.tiros:
                        self.tiros.remove(tiro)     # Remove o laser da tela
                    break

    def desenhar(self):
        # Gerenciador de renderização das telas com base no estado do jogo
        self.tela.fill(FUNDO)

        for estrela in LISTA_ESTRELAS:
            estrela.desenhar(self.tela)

        if self.estado == self.S_INICIO:
            self._d_inicio()
        elif self.estado == self.S_NICKNAME:
            self._d_nickname()
        elif self.estado in (self.S_JOGANDO, self.S_FEEDBACK):
            self._d_jogo()
        elif self.estado == self.S_GAMEOVER:
            self._d_gameover()
        elif self.estado == self.S_FIM:
            self._d_fim()

    def _d_inicio(self):
        # Render da tela inicial (Menu Principal)
        t = fonte_titulo.render("CosmoMind", True, AMARELO)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 160)))

        sub = fonte_info.render("Responda certo para destruir o asteroide!", True, BRANCO)
        self.tela.blit(sub, sub.get_rect(center=(LARGURA // 2, 220)))

        info = fonte_pequena.render("Se errar, o asteroide acelera — destrua-o antes do impacto!", True, CINZA)
        self.tela.blit(info, info.get_rect(center=(LARGURA // 2, 255)))

        desenhar_nave(self.tela, LARGURA // 2, 350)

        preview_ast = AsteroideMecanica(LARGURA // 2 + 120, 320, raio=22)
        preview_ast.desenhar(self.tela, angulo_rot=0.3)

        seta = fonte_info.render("<- asteroide", True, LARANJA)
        self.tela.blit(seta, (LARGURA // 2 + 148, 310))

        nave_l = fonte_info.render("nave ->", True, (100, 180, 255))
        self.tela.blit(nave_l, (LARGURA // 2 - nave_l.get_width() - 26, 338))

        self._btn("Iniciar jogo", (LARGURA // 2, 440))

    def _d_nickname(self):
        t = fonte_titulo.render("Identificação do Piloto", True, AMARELO)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 160)))

        sub = fonte_info.render("Digite seu nickname para o painel de comando:", True, BRANCO)
        self.tela.blit(sub, sub.get_rect(center=(LARGURA // 2, 220)))

        caixa_texto = pygame.Rect(0, 0, 340, 50)
        caixa_texto.center = (LARGURA // 2, 290)
        
        cor_borda = VERDE if len(self.nickname.strip()) > 0 else AZUL
        pygame.draw.rect(self.tela, FUNDO_PAINEL, caixa_texto, border_radius=8)
        pygame.draw.rect(self.tela, cor_borda, caixa_texto, 2, border_radius=8)

        if self.nickname == "":
            txt_surf = fonte_info.render("Sua Tag de Voo...", True, CINZA)
        else:
            txt_surf = fonte_info.render(self.nickname, True, BRANCO)
            
        self.tela.blit(txt_surf, txt_surf.get_rect(center=caixa_texto.center))

        cont_txt = f"{len(self.nickname)}/{self.max_caracteres}"
        cont_surf = fonte_pequena.render(cont_txt, True, CINZA)
        self.tela.blit(cont_surf, (caixa_texto.right - cont_surf.get_width(), caixa_texto.bottom + 6))

        if len(self.nickname.strip()) > 0:
            self._btn("Confirmar Entrada", (LARGURA // 2, 410))
            dica_enter = fonte_pequena.render("ou pressione ENTER", True, CINZA)
            self.tela.blit(dica_enter, dica_enter.get_rect(center=(LARGURA // 2, 452)))

    def _rect_btn_nickname(self):
        r = pygame.Rect(0, 0, 230, 48)
        r.center = (LARGURA // 2, 410)
        return r

    def _d_jogo(self):
        # Render da área de jogo activa
        pergunta = self.perguntas[self.indice]
        correta = pergunta["correta"]

        # Desenha o flash vermelho na tela se o player tiver tomado dano
        if self.flash_timer > 0:
            alfa = int(160 * self.flash_timer / 18)
            ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            ov.fill((200, 30, 30, alfa))
            self.tela.blit(ov, (0, 0))

        self._d_jogo_area(correta)
        self._d_painel_pergunta(pergunta, correta)

        if self.estado == self.S_FEEDBACK:
            d = fonte_pequena.render("Clique para continuar ->", True, CINZA)
            self.tela.blit(d, d.get_rect(center=(LARGURA // 2, ALTURA - 10)))

    def _d_jogo_area(self, correta):
        # Desenha os elements espaciais (HUD, Nave, Lasers e Asteroide)
        area_h = self.PAINEL_Y - 4
        pygame.draw.line(self.tela, AZUL_ESC, (0, self.PAINEL_Y - 2), (LARGURA, self.PAINEL_Y - 2), 1)

        # Desenha a barrinha de progresso das fases
        bx, by, bw, bh = 12, 10, 200, 6
        pygame.draw.rect(self.tela, CINZA_ESC, (bx, by, bw, bh), border_radius=3)
        prog = int((self.indice / len(self.perguntas)) * bw)
        if prog:
            pygame.draw.rect(self.tela, AZUL, (bx, by, prog, bh), border_radius=3)

        # Desenha os indicadores de pontos na interface gráfica
        pts = fonte_pequena.render(f"Pontos: {self.pontuacao}", True, AMARELO)
        self.tela.blit(pts, (LARGURA - pts.get_width() - 12, 8))

        num = fonte_pequena.render(f"{self.indice + 1}/{len(self.perguntas)}", True, CINZA)
        self.tela.blit(num, (bx, by + 12))

        nick_txt = fonte_pequena.render(f"Piloto: {self.nickname}", True, BRANCO)
        self.tela.blit(nick_txt, (bx, by + 28))

        perigo_txt = f"Vel. asteroide: {self.ast_vel:.1f}x"
        cor_vel = VERDE if self.ast_vel <= 1.2 else (LARANJA if self.ast_vel <= 2.0 else VERMELHO)
        vel_s = fonte_pequena.render(perigo_txt, True, cor_vel)
        self.tela.blit(vel_s, vel_s.get_rect(center=(LARGURA // 2, 24)))

        NAVE_CX = LARGURA // 2
        nave_y_area = area_h // 2 + 10
        desenhar_nave(self.tela, NAVE_CX, nave_y_area, escudo_ativo=(self.escudo_timer > 0))

        for tiro in self.tiros:
            tiro.desenhar(self.tela)

        # Só desenha o asteroide se ele não tiver sido destruído pelo laser
        if not self.asteroide_destruido:
            ast_y_vis = self.asteroide.y
            # Trava visual pra impedir o sprite do asteroide de vazar pra dentro do menu de texto
            if ast_y_vis > area_h - self.asteroide.raio:
                ast_y_vis = area_h - self.asteroide.raio

            backup_y = self.asteroide.y
            self.asteroide.y = ast_y_vis
            self.asteroide.desenhar(self.tela, self.ast_rot)
            self.asteroide.y = backup_y

            # Alerta piscante de proximidade perigosa
            dist = math.hypot(NAVE_CX - self.asteroide.x, nave_y_area - self.asteroide.y)
            if dist < 140:
                av = fonte_pequena.render("! IMPACTO IMINENTE!", True, VERMELHO)
                self.tela.blit(av, av.get_rect(center=(LARGURA // 2, area_h - 18)))

    def _d_painel_pergunta(self, pergunta, correta):
        # Montagem do retângulo cinza do painel inferior
        painel = pygame.Rect(0, self.PAINEL_Y, LARGURA, self.PAINEL_H)
        pygame.draw.rect(self.tela, FUNDO_PAINEL, painel)
        pygame.draw.rect(self.tela, AZUL_ESC, painel, 1)

        lw = LARGURA - 32
        renderizar_texto(self.tela, pergunta["pergunta"], fonte_pergunta, BRANCO, 16, self.PAINEL_Y + 10, lw)

        # Loop pra renderizar os 4 botões de alternativas
        for i, (rect, alt) in enumerate(zip(self.rects_alt, pergunta["alternativas"])):
            self._d_alt(i, rect, alt, correta)

    def _d_alt(self, idx, rect, texto, correta):
        # Define as cores do botão variando de acordo se está focado, clicado, certo ou errado
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

        pygame.draw.rect(self.tela, cf, rect, border_radius=8)
        pygame.draw.rect(self.tela, cb, rect, 2, border_radius=8)

        # Desenha a bolinha colorida com as letras das alternativas (A, B, C, D)
        cx_ = rect.x + 20
        cy_ = rect.centery
        pygame.draw.circle(self.tela, self.CORES_LETRAS[idx], (cx_, cy_), 12)

        letra_surf = fonte_alt.render(self.LETRAS[idx], True, BRANCO)
        self.tela.blit(letra_surf, letra_surf.get_rect(center=(cx_, cy_)))

        # Coloca o ícone de feedback rápido (X ou Y) no canto direito do botão
        if feedback and (sel or eh_correta):
            ic = "Y" if eh_correta else "X"
            cic = VERDE if eh_correta else VERMELHO
            is_ = fonte_alt.render(ic, True, cic)
            self.tela.blit(is_, is_.get_rect(midright=(rect.right - 10, cy_)))

        tw = rect.width - 50
        renderizar_texto(self.tela, texto, fonte_alt, ct,
                         rect.x + 38,
                         rect.centery - altura_texto(texto, fonte_alt, tw) // 2,
                         tw)

    def _d_gameover(self):
        # Render da tela de derrota se o asteroide bater na nave
        ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        ov.fill((220, 50, 30, 80))
        self.tela.blit(ov, (0, 0))

        NAVE_CX = LARGURA // 2
        NAVE_CY = (self.PAINEL_Y // 2 + 10)
        impacto_ast = AsteroideMecanica(NAVE_CX, NAVE_CY, raio=40)
        impacto_ast.desenhar(self.tela, self.ast_rot)

        t = fonte_titulo.render("IMPACTO!", True, VERMELHO)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 160)))

        s = fonte_info.render(f"Pontos: {self.pontuacao}  * Erros: {self.erros}", True, BRANCO)
        self.tela.blit(s, s.get_rect(center=(LARGURA // 2, 220)))

        msg = fonte_info.render("O asteroide te alcançou...", True, LARANJA)
        self.tela.blit(msg, msg.get_rect(center=(LARGURA // 2, 265)))

        self._btn("Tentar novamente", (LARGURA // 2, 340))

    def _d_fim(self):
        # Render da tela final de vitória
        total = len(self.perguntas)
        pct = self.pontuacao / total * 100

        # Mensagens baseadas na porcentagem de acertos do jogador
        if pct == 100:
            msg, cm = f"Piloto perfeito! Nenhum asteroide te pegou, {self.nickname}!", AMARELO
        elif pct >= 70:
            msg, cm = "Ótima pilotagem, astronauta!", VERDE
        elif pct >= 50:
            msg, cm = "Missão concluída, mas com danos...", LARANJA
        else:
            msg, cm = "A nave sofreu bastante. Estude mais!", VERMELHO

        t = fonte_titulo.render("Missão concluída!", True, BRANCO)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 130)))

        pl = fonte_titulo.render(f"{self.pontuacao} / {total}", True, AMARELO)
        self.tela.blit(pl, pl.get_rect(center=(LARGURA // 2, 210)))

        p2 = fonte_info.render(f"{pct:.0f}% de aproveitamento  * {self.erros} erro(s)", True, CINZA)
        self.tela.blit(p2, p2.get_rect(center=(LARGURA // 2, 265)))

        ms = fonte_info.render(msg, True, cm)
        self.tela.blit(ms, ms.get_rect(center=(LARGURA // 2, 315)))

        self._btn("Jogar novamente", (LARGURA // 2, 400))

    def _btn(self, texto, centro):
        # Função genérica pra fazer os botões azuis que reagem ao mouse (hover)
        r = pygame.Rect(0, 0, 230, 48)
        r.center = centro
        mouse = pygame.mouse.get_pos()
        cor = AZUL_HOVER if r.collidepoint(mouse) else AZUL
        pygame.draw.rect(self.tela, cor, r, border_radius=11)
        s = fonte_info.render(texto, True, BRANCO)
        self.tela.blit(s, s.get_rect(center=r.center))

    def _rect_btn(self):
        # Retorna o hitbox do botão final de reinicialização pra checar os cliques
        r = pygame.Rect(0, 0, 230, 48)
        if self.estado == self.S_GAMEOVER:
            r.center = (LARGURA // 2, 340)
        else:
            r.center = (LARGURA // 2, 400)
        return r