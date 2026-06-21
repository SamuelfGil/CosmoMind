import pygame
import random
import math
from src.config import *
from src.funcoes import renderizar_texto, altura_texto
from src.dados import carregar_perguntas, carregar_recorde, salvar_recorde, salvar_no_ranking, carregar_ranking
from src.sprites import LISTA_ESTRELAS, desenhar_nave, AsteroideMecanica, Tiro
from src.audio import audio
from SEMANA_2.SAMUEL_ABREU.sair import rect_btn_sair_jogo, desenhar_btn_sair_jogo, rect_btn_sair_ranking, desenhar_btn_sair_ranking

class CosmoMind:
    """Gerenciador principal da máquina de estados, mecânicas de quiz e jogabilidade do CosmoMind."""

    # Definição dos estados do jogo
    S_INICIO = "inicio"
    S_NICKNAME = "nickname"
    S_JOGANDO = "jogando"
    S_FEEDBACK = "feedback"
    S_GAMEOVER = "gameover"
    S_FIM = "fim"
    S_RANKING = "ranking"

    # Configurações de exibição de alternativas
    LETRAS = ["A", "B", "C", "D"]
    CORES_LETRAS = [(80, 120, 220), (180, 90, 200), (50, 170, 150), (200, 130, 40)]

    # Layout da interface inferior (Painel do Quiz)
    PAINEL_Y = 400
    PAINEL_H = ALTURA - PAINEL_Y - 4

    # Parâmetros de spawn e velocidade inicial do perigo espacial
    AST_INICIO_X = LARGURA - 100
    AST_INICIO_Y = 80
    VEL_BASE = 0.5
    VEL_AUMENTO = 0.35

    def __init__(self, tela):
        """Inicializa a estrutura do jogo, vincula a tela e carrega o banco de dados de perguntas.

        Args:
            tela (pygame.Surface): Janela principal de renderização do jogo.
        """
        self.tela = tela
        self.todas_perguntas = carregar_perguntas()
        self.nickname = ""
        self.max_caracteres = 12
        self.reiniciar()

    def reiniciar(self):
        """Zera o progresso do jogador e reinicia as variáveis para uma nova partida."""
        self.estado = self.S_INICIO
        self.pontuacao = 0
        self.erros = 0
        self.vida = 10
        self.nivel_atual = 1
        # Mapeamento do número de perguntas necessárias para avançar em cada nível/setor
        self.perguntas_por_nivel = {1: 5, 2: 7, 3: 10, 4: 12, 5: 15}
        self.is_boss = False
        self._configurar_nivel()

    def _recuperar_vida(self):
        """Concede 1 ponto de integridade de escudo à nave, limitando ao máximo de 10."""
        if self.vida < 10:
            self.vida += 1
            audio.tocar(audio.bonus)

    def _configurar_nivel(self):
        """Prepara e embaralha o lote de perguntas do nível atual e reinicia os sub-timers."""
        qtd_necessaria = self.perguntas_por_nivel.get(self.nivel_atual, 5)
        pool = list(self.todas_perguntas) if self.todas_perguntas else []
        
        # Fallback de segurança caso o arquivo perguntas.json esteja ausente ou vazio
        if not pool:
            pool = [{
                "pergunta": "Alerta! perguntas.json nao encontrado na raiz do projeto.", 
                "alternativas": ["Verificar local do arquivo", "Criar perguntas.json", "Reiniciar o terminal", "Apenas continuar"], 
                "correta": 0
            }]

        # Garante volume de perguntas suficiente no pool clonando-o recursivamente se necessário
        while len(pool) < (qtd_necessaria + 10): 
            pool.extend(pool)
            
        # Seleciona perguntas aleatórias do pool disponível
        self.perguntas = random.sample(pool, len(pool)) 
        self.indice = 0
        self.hover = -1
        self.selecionada = -1
        self.combo_acertos = 0
        self.tempo_restante = 30.0
        self.asteroide_destruido = False
        self.tiros = []
        self.ast_rot = 0.0
        self.flash_timer = 0
        self.escudo_timer = 0
        self.is_boss = False

        self._gerar_novo_asteroide()
        self._preparar_pergunta_atual()

    def _preparar_pergunta_atual(self):
        """Extrai a pergunta atual e embaralha as alternativas remapeando o índice da resposta certa."""
        if self.indice >= len(self.perguntas):
            return

        pergunta_crua = self.perguntas[self.indice]
        
        # Recupera o texto literal da alternativa correta original antes do embaralhamento
        indice_original = pergunta_crua["correta"]
        texto_correto = pergunta_crua["alternativas"][indice_original]

        # Clona e embaralha a exibição das opções para o jogador
        alts_embaralhadas = list(pergunta_crua["alternativas"])
        random.shuffle(alts_embaralhadas)

        # Localiza dinamicamente onde a resposta certa foi parar após o embaralhamento
        self.indice_correto_atual = alts_embaralhadas.index(texto_correto)
        self.alternativas_atuais = alts_embaralhadas
        
        # Recalcula as caixas geométricas clicáveis de resposta
        self._calcular_layout()

    def _obter_dificuldade_atual(self):
        """Determina a dificuldade da pergunta de forma cíclica com base no índice.

        Returns:
            str: "facil", "medio" ou "dificil".
        """
        ciclo = self.indice % 3
        if ciclo == 0:
            return "facil"
        elif ciclo == 1:
            return "medio"
        else:
            return "dificil"

    def _gerar_novo_asteroide(self):
        """Gera a física e dimensões de um asteroide comum ou do Boss no final do jogo."""
        # O boss aparece na última pergunta do último setor (Setor 5, Pergunta 10)
        self.is_boss = (self.nivel_atual == 5 and self.indice == 9)
        
        if self.is_boss:
            self.asteroide_vida = 3
            self.ast_vel = self.VEL_BASE * 0.55  # Deslocamento imponente e pesado
            self.asteroide = AsteroideMecanica(self.AST_INICIO_X, self.AST_INICIO_Y, raio=65)
        else:
            self.asteroide_vida = 1
            self.ast_vel = self.VEL_BASE + (self.nivel_atual * 0.15)  # Acelera conforme o progresso do jogo
            self.asteroide = AsteroideMecanica(self.AST_INICIO_X, self.AST_INICIO_Y, raio=26)
        self.asteroide_destruido = False

    def _calcular_layout(self):
        """Calcula dinamicamente a altura e posicionamento vertical das caixas das alternativas."""
        self.rects_alt = []
        x = 60
        lw = LARGURA - 120
        y = self.PAINEL_Y + 75
        gap = 8

        for alt in self.alternativas_atuais:
            # Adapta a altura da caixa baseando-se no tamanho do texto envelopado
            h = max(46, altura_texto(alt, fonte_alt, lw - 50) + 18)
            self.rects_alt.append(pygame.Rect(x, y, lw, h))
            y += h + gap

    def processar_evento(self, evento):
        """Gerencia e direciona as interações por teclado e mouse conforme o estado ativo.

        Args:
            evento (pygame.event.Event): Evento capturado pelo loop principal do jogo.
        """
        # Atualiza a detecção de passagem de mouse (hover)
        if evento.type == pygame.MOUSEMOTION:
            self._hover(evento.pos)
            
        # Processamento de entradas via Teclado
        elif evento.type == pygame.KEYDOWN:
            if self.estado == self.S_NICKNAME:
                if evento.key == pygame.K_BACKSPACE:
                    self.nickname = self.nickname[:-1]
                elif evento.key == pygame.K_RETURN:
                    if len(self.nickname.strip()) > 0:
                        audio.tocar(audio.clique)
                        self.estado = self.S_JOGANDO
                else:
                    # Permite apenas caracteres alfanuméricos e espaço dentro do limite da tag
                    if len(self.nickname) < self.max_caracteres:
                        if evento.unicode.isalnum() or evento.unicode == " ":
                            self.nickname += evento.unicode
                            
        # Processamento de interações via Cliques do Mouse (Botão Esquerdo)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Botão global de desistência rápido integrado
            if self.estado in (self.S_JOGANDO, self.S_FEEDBACK) and rect_btn_sair_jogo().collidepoint(evento.pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif self.estado == self.S_INICIO:
                audio.tocar(audio.clique)
                self.estado = self.S_NICKNAME
            elif self.estado == self.S_NICKNAME:
                if self._rect_btn_nickname().collidepoint(evento.pos):
                    if len(self.nickname.strip()) > 0:
                        audio.tocar(audio.clique)
                        self.estado = self.S_JOGANDO
            elif self.estado == self.S_JOGANDO:
                # Verifica qual alternativa foi clicada pelo jogador
                for i, r in enumerate(self.rects_alt):
                    if r.collidepoint(evento.pos):
                        self._responder(i)
                        break
            elif self.estado == self.S_FEEDBACK:
                # Qualquer clique na tela sai do modo de exibição de resposta
                self._avancar()
            elif self.estado in (self.S_GAMEOVER, self.S_FIM):
                if self._rect_btn().collidepoint(evento.pos):
                    audio.tocar(audio.clique)
                    salvar_recorde(self.pontuacao)
                    salvar_no_ranking(self.nickname, self.pontuacao)
                    self.estado = self.S_RANKING
            elif self.estado == self.S_RANKING:
                if self._rect_btn_ranking().collidepoint(evento.pos):
                    audio.tocar(audio.clique)
                    self.reiniciar()
                elif rect_btn_sair_ranking().collidepoint(evento.pos):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _hover(self, pos):
        """Verifica a posição do mouse para aplicar efeitos visuais de realce (hover)."""
        if self.estado != self.S_JOGANDO:
            self.hover = -1
            return
        # Retorna o índice do retângulo sob o cursor, ou -1 caso esteja fora das caixas
        self.hover = next((i for i, r in enumerate(self.rects_alt) if r.collidepoint(pos)), -1)

    def _responder(self, idx):
        """Processa a opção escolhida, aplicando recompensas de acertos ou penalidades de erro."""
        self.selecionada = idx
        dificuldade = self._obter_dificuldade_atual()
        
        # Compara se a alternativa escolhida coincide com o índice correto remapeado
        if idx == self.indice_correto_atual:
            valores_pontos = {"facil": 10, "medio": 20, "dificil": 30}
            self.pontuacao += valores_pontos.get(dificuldade, 10)
            self.combo_acertos += 1

            audio.tocar(audio.acerto)
            audio.tocar(audio.tiro)

            # Recompensa por combo: a cada 5 acertos seguidos, recupera integridade
            if self.combo_acertos == 5:
                self._recuperar_vida()
                self.combo_acertos = 0
            self.escudo_timer = 90  # Ativa efeito visual de barreira defensiva na nave
            
            # Instancia o laser projetado em direção às coordenadas do perigo asteroide
            self.tiros.append(Tiro(LARGURA // 2, (self.PAINEL_Y // 2 + 20), self.asteroide.x, self.asteroide.y))
        else:
            # Penalidade por erro
            self.pontuacao = max(0, self.pontuacao - 10)
            self.erros += 1
            self.combo_acertos = 0 
            self.ast_vel += self.VEL_AUMENTO  # O asteroide ganha velocidade em direção à nave
            self.flash_timer = 18  # Ativa efeito de lampejo vermelho na tela de jogo
            audio.tocar(audio.erro)            
            
        self.estado = self.S_FEEDBACK

    def _avancar(self):
        """Avança para a próxima pergunta do lote ou faz a transição de setor (nível)."""
        self.selecionada = -1
        self.indice += 1
        self.tempo_restante = 30.0  # Reinicia o cronômetro para a nova pergunta

        limite_atual = self.perguntas_por_nivel.get(self.nivel_atual, 5)

        if self.indice >= limite_atual:
            if self.nivel_atual < 5:
                self.nivel_atual += 1
                audio.tocar(audio.nivel_up)
                self._configurar_nivel()
            else:
                # Partida finalizada com sucesso ao esgotar o setor 5
                audio.tocar(audio.vitoria)
                self.estado = self.S_FIM
                return
        else:
            # Caso o asteroide anterior tenha sido pulverizado, gera um novo alvo para a próxima pergunta
            if self.asteroide_destruido:
                self._gerar_novo_asteroide()

        self.estado = self.S_JOGANDO
        self._preparar_pergunta_atual()

    def atualizar(self):
        """Gerencia toda a física vetorial de movimentação, contagem de tempo e colisões (60 FPS)."""
        # Faz o scroll de movimento do fundo estrelado
        for estrela in LISTA_ESTRELAS:
            estrela.mover()

        # Atualiza a trajetória balística dos lasers ativos e remove os tiros inativos
        for tiro in self.tiros[:]:
            tiro.mover()
            if not tiro.ativo:
                self.tiros.remove(tiro)

        if self.estado not in (self.S_JOGANDO, self.S_FEEDBACK):
            return

        # Mecânica do cronômetro de contagem regressiva da rodada ativa
        if self.estado == self.S_JOGANDO:
            self.tempo_restante -= 1 / 60.0  # Deduz o delta-time baseado em 60Hz estável
            if self.tempo_restante <= 0:
                # Força penalidade por esgotamento de tempo, tratando como erro
                self.tempo_restante = 30.0
                self.pontuacao = max(0, self.pontuacao - 10)
                self.erros += 1
                self.combo_acertos = 0
                self.ast_vel += self.VEL_AUMENTO
                self.flash_timer = 18
                audio.tocar(audio.erro)
                self._avancar()

        self.ast_rot += 0.012  # Atualiza rotação geométrica do asteroide
        if self.escudo_timer > 0:
            self.escudo_timer -= 1

        # Definição do ponto central geométrico onde a nave está ancorada
        NAVE_CX = LARGURA // 2
        nave_y_area = (self.PAINEL_Y // 2 + 20)

        # 1. Movimentação física vetorial do asteroide perseguidor em direção à nave
        if not self.asteroide_destruido:
            dx = NAVE_CX - self.asteroide.x
            dy = nave_y_area - self.asteroide.y
            dist = math.hypot(dx, dy)  # Calcula a distância linear hipotenusa entre os pontos

            if dist >= 1:
                # Normaliza o vetor de aproximação multiplicando pela velocidade definida
                self.asteroide.x += (dx / dist) * self.ast_vel
                self.asteroide.y += (dy / dist) * self.ast_vel

            # Detecção de Colisão de proximidade: Asteroide atingiu o casco protetor da nave
            if dist - self.asteroide.raio < 24:
                if self.is_boss:
                    self.vida -= 7  # Dano massivo causado pelo Boss
                else:
                    dif = self._obter_dificuldade_atual()
                    # O dano varia de acordo com a dificuldade da pergunta falhada
                    self.vida -= {"facil": 3, "medio": 2, "dificil": 1}.get(dif, 1)
                audio.tocar(audio.impacto)
                self.combo_acertos = 0
                self.asteroide_destruido = True 
                
                # Validação de derrota (Game Over)
                if self.vida <= 0:
                    self.vida = 0
                    self.estado = self.S_GAMEOVER
                    audio.tocar(audio.gameover)
                else:
                    self._avancar()
                    self._gerar_novo_asteroide()

        # 2. Interseção de colisão: Tiro laser atingiu o corpo do asteroide
        if not self.asteroide_destruido:
            for tiro in self.tiros[:]:
                dist_tiro = math.hypot(tiro.x - self.asteroide.x, tiro.y - self.asteroide.y)
                if dist_tiro < (tiro.raio + self.asteroide.raio):
                    if tiro in self.tiros:
                        self.tiros.remove(tiro)
                    
                    self.asteroide_vida -= 1
                    audio.tocar(audio.tiro_impacto)
                    # Verifica eliminação do alvo
                    if self.asteroide_vida <= 0:
                        if self.is_boss:
                            self.pontuacao += 1000  # Recompensa bônus por abater o Boss
                            audio.tocar(audio.vitoria)  
                        self.asteroide_destruido = True
                        audio.tocar(audio.explosao)
                    break

    def desenhar(self):
        """Garante a limpeza e pintura correta dos elementos visuais dependendo do estado atual."""
        self.tela.fill(FUNDO)
        # Renderiza a camada mais profunda (Fundo Estrelado)
        for estrela in LISTA_ESTRELAS:
            estrela.desenhar(self.tela)

        # Roteamento de telas gráficas do jogo
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
        elif self.estado == self.S_RANKING:
            self._d_ranking()

    def _d_inicio(self):
        """Desenha a tela de menu inicial."""
        t = fonte_titulo.render("CosmoMind", True, AMARELO)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 200)))
        sub = fonte_info.render("Responda certo para destruir o asteroide!", True, BRANCO)
        self.tela.blit(sub, sub.get_rect(center=(LARGURA // 2, 270)))
        info = fonte_pequena.render("Errar alternativas reduz 10 pontos. Sobreviva ao Boss na Pergunta 10 do Setor 5!", True, CINZA)
        self.tela.blit(info, info.get_rect(center=(LARGURA // 2, 310)))
        desenhar_nave(self.tela, LARGURA // 2, 440)
        self._btn("Iniciar jogo", (LARGURA // 2, 560))

    def _d_nickname(self):
        """Desenha a interface de coleta de nome/identificação do piloto."""
        t = fonte_titulo.render("Identificação do Piloto", True, AMARELO)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 200)))
        sub = fonte_info.render("Digite seu nickname para o painel de comando:", True, BRANCO)
        self.tela.blit(sub, sub.get_rect(center=(LARGURA // 2, 270)))
        
        caixa_texto = pygame.Rect(0, 0, 380, 52)
        caixa_texto.center = (LARGURA // 2, 350)
        pygame.draw.rect(self.tela, FUNDO_PAINEL, caixa_texto, border_radius=8)
        pygame.draw.rect(self.tela, AZUL, caixa_texto, 2, border_radius=8)

        txt_surf = fonte_info.render(self.nickname if self.nickname else "Sua Tag de Voo...", True, BRANCO if self.nickname else CINZA)
        self.tela.blit(txt_surf, txt_surf.get_rect(center=caixa_texto.center))
        self._btn("Confirmar Entrada", (LARGURA // 2, 480))

    def _d_jogo(self):
        """Desenha o loop ativo da área de combate espacial combinada ao painel de perguntas."""
        pergunta = self.perguntas[self.indice]

        # Renderiza o flash de dano vermelho translúcido na tela (Alpha Blending)
        if self.flash_timer > 0:
            alfa = int(160 * self.flash_timer / 18)
            ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            ov.fill((200, 30, 30, alfa))
            self.tela.blit(ov, (0, 0))
            self.flash_timer -= 1

        self._d_jogo_area()
        self._d_painel_pergunta(pergunta)

        if self.estado == self.S_FEEDBACK:
            d = fonte_pequena.render("Clique em qualquer lugar para carregar a próxima pergunta ->", True, AMARELO)
            self.tela.blit(d, d.get_rect(center=(LARGURA // 2, ALTURA - 15)))

    def _d_jogo_area(self):
        """Renderiza o espaço superior de gameplay (nave, estrelas, laser e asteroides)."""
        area_h = self.PAINEL_Y - 4
        pygame.draw.line(self.tela, AZUL_ESC, (0, self.PAINEL_Y - 2), (LARGURA, self.PAINEL_Y - 2), 2)
        desenhar_btn_sair_jogo(self.tela)

        # Interface da barra de progresso do nível atual
        bx, by, bw, bh = 20, 20, 250, 8
        pygame.draw.rect(self.tela, CINZA_ESC, (bx, by, bw, bh), border_radius=4)
        
        limite_atual = self.perguntas_por_nivel.get(self.nivel_atual, 5)
        prog = int((min(self.indice, limite_atual) / limite_atual) * bw)
        if prog:
            pygame.draw.rect(self.tela, AZUL_HOVER, (bx, by, prog, bh), border_radius=4)

        # Renderização do HUD de pontuação, integridade e tempo
        recorde_atual = carregar_recorde()
        pts_surf = fonte_info.render(f"PONTOS: {self.pontuacao} (Max: {recorde_atual})", True, AMARELO)
        self.tela.blit(pts_surf, (LARGURA - pts_surf.get_width() - 20, 15))

        cor_vida = VERDE if self.vida > 5 else (AMARELO if self.vida > 2 else VERMELHO)
        vida_txt = fonte_info.render(f"INTEGRIDADE DA NAVE: {self.vida}/10 " + ("█" * self.vida), True, cor_vida)
        self.tela.blit(vida_txt, (LARGURA - vida_txt.get_width() - 20, 45))

        t_surf = fonte_info.render(f"TEMPO: {max(0.0, self.tempo_restante):.1f}s", True, BRANCO)
        self.tela.blit(t_surf, (LARGURA - t_surf.get_width() - 20, 75))

        lbl_fase = "⚠️ COMBATE CRÍTICO: ALVO BOSS ATIVO" if self.is_boss else f"SETOR ESPACIAL: 0{self.nivel_atual}/05"
        fase_surf = fonte_info.render(lbl_fase, True, VERMELHO if self.is_boss else AZUL_HOVER)
        self.tela.blit(fase_surf, (20, 45))

        num = fonte_pequena.render(f"Progresso do Banco: Seq {self.indice + 1}/{limite_atual}", True, CINZA)
        self.tela.blit(num, (20, 75))

        # Renderiza a tag de trancamento de mira (Lock-On) sobre o asteroide
        if not self.asteroide_destruido:
            lbl_ast = f"ALVO LOCK-ON" if not self.is_boss else f"⚠️ ALVO CRÍTICO BOSS: {self.asteroide_vida}/3 RESISTÊNCIA"
            ast_hp_surf = fonte_pequena.render(lbl_ast, True, LARANJA if not self.is_boss else VERMELHO)
            self.tela.blit(ast_hp_surf, ast_hp_surf.get_rect(center=(self.asteroide.x, max(15, self.asteroide.y - self.asteroide.raio - 15))))

        # Desenha a nave (com ou sem escudo protetor)
        desenhar_nave(self.tela, LARGURA // 2, area_h // 2 + 30, escudo_ativo=(self.escudo_timer > 0))

        # Desenha os disparos de laser ativos
        for tiro in self.tiros:
            tiro.desenhar(self.tela)

        # Impede que o asteroide ultrapasse visualmente o divisor do painel de perguntas
        if not self.asteroide_destruido:
            backup_y = self.asteroide.y
            if self.asteroide.y > area_h - self.asteroide.raio:
                self.asteroide.y = area_h - self.asteroide.raio
            self.asteroide.desenhar(self.tela, self.ast_rot)
            self.asteroide.y = backup_y

    def _d_painel_pergunta(self, pergunta):
        """Renderiza o quadro inferior com o enunciado e as alternativas embaralhadas."""
        painel = pygame.Rect(0, self.PAINEL_Y, LARGURA, self.PAINEL_H)
        pygame.draw.rect(self.tela, FUNDO_PAINEL, painel)
        lw = LARGURA - 120
        
        dif_tag = f" [Dificuldade: {self._obter_dificuldade_atual().upper()}]"
        renderizar_texto(self.tela, pergunta["pergunta"] + dif_tag, fonte_pergunta, BRANCO, 60, self.PAINEL_Y + 20, lw)

        # Exibe as alternativas na interface gráfica
        for i, (rect, alt) in enumerate(zip(self.rects_alt, self.alternativas_atuais)):
            self._d_alt(i, rect, alt, self.indice_correto_atual)

    def _d_alt(self, idx, rect, texto, correta):
        """Pinta individualmente cada caixa de alternativa aplicando coloração de feedback."""
        hover = idx == self.hover
        sel = idx == self.selecionada
        eh_correta = idx == correta
        feedback = self.estado == self.S_FEEDBACK

        # Define as cores do botão baseado se o jogo está mostrando a resposta certa ou não
        if feedback:
            if sel and eh_correta: cf, cb, ct = VERDE_ESC, VERDE, BRANCO
            elif sel and not eh_correta: cf, cb, ct = VERMELHO_ESC, VERMELHO, BRANCO
            elif eh_correta: cf, cb, ct = VERDE_ESC, VERDE, BRANCO
            else: cf, cb, ct = CINZA_ESC, CINZA_ESC, CINZA
        else:
            cf = AZUL_ESC if hover else FUNDO_PAINEL
            cb = AZUL_HOVER if hover else AZUL_ESC
            ct = BRANCO

        pygame.draw.rect(self.tela, cf, rect, border_radius=6)
        pygame.draw.rect(self.tela, cb, rect, 2, border_radius=6)

        # Desenha a bolinha indicativa com a letra da alternativa (A, B, C, D)
        cx_ = rect.x + 25
        cy_ = rect.centery
        pygame.draw.circle(self.tela, self.CORES_LETRAS[idx], (cx_, cy_), 13)
        letra_surf = fonte_alt.render(self.LETRAS[idx], True, BRANCO)
        self.tela.blit(letra_surf, letra_surf.get_rect(center=(cx_, cy_)))

        tw = rect.width - 60
        renderizar_texto(self.tela, texto, fonte_alt, ct, rect.x + 50, rect.centery - altura_texto(texto, fonte_alt, tw) // 2, tw)

    def _d_gameover(self):
        """Renderiza a tela de derrota por destruição estrutural."""
        ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        ov.fill((180, 20, 20, 95))
        self.tela.blit(ov, (0, 0))

        t = fonte_titulo.render("NAVE DESTRUÍDA EM COMBATE", True, VERMELHO)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 250)))
        s = fonte_info.render(f"Pontuação alcançada: {self.pontuacao} pontos | Parou no Nível {self.nivel_atual}", True, BRANCO)
        self.tela.blit(s, s.get_rect(center=(LARGURA // 2, 320)))
        self._btn("Ver Painel de Ranking", (LARGURA // 2, 450))

    def _d_fim(self):
        """Renderiza a tela de vitória por conclusão da campanha espacial."""
        t = fonte_titulo.render("VITÓRIA SUPREMA: CONSTELAÇÃO SALVA!", True, VERDE)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 220)))
        pl = fonte_titulo.render(f"Pontuação Final: {self.pontuacao}", True, AMARELO)
        self.tela.blit(pl, pl.get_rect(center=(LARGURA // 2, 300)))
        ms = fonte_info.render(f"Parabéns Comandante {self.nickname}! Todos os setores foram pacificados.", True, BRANCO)
        self.tela.blit(ms, ms.get_rect(center=(LARGURA // 2, 370)))
        self._btn("Ver Painel de Ranking", (LARGURA // 2, 500))

    def _d_ranking(self):
        """Renderiza o quadro estilizado contendo a tabela do Top 10 melhores pontuações."""
        t = fonte_titulo.render("🏆 CLASSIFICAÇÃO DOS MELHORES PILOTOS 🏆", True, AMARELO)
        self.tela.blit(t, t.get_rect(center=(LARGURA // 2, 60)))

        top_10 = carregar_ranking()

        start_y = 140
        row_h = 42
        box_w = 600
        box_x = (LARGURA - box_w) // 2

        # Cabeçalho da tabela do ranking
        pygame.draw.rect(self.tela, AZUL_ESC, (box_x, start_y, box_w, row_h), border_radius=4)
        h_pos = fonte_info.render("POS", True, BRANCO)
        h_nome = fonte_info.render("PILOTO", True, BRANCO)
        h_pts = fonte_info.render("PONTOS", True, BRANCO)
        self.tela.blit(h_pos, (box_x + 20, start_y + 8))
        self.tela.blit(h_nome, (box_x + 120, start_y + 8))
        self.tela.blit(h_pts, (box_x + box_w - 120, start_y + 8))

        # Renderiza as linhas do ranking (linhas de 1 a 10)
        for i in range(10):
            curr_y = start_y + row_h + (i * row_h) + (i * 4)
            bg_cor = FUNDO_PAINEL if i < len(top_10) else CINZA_ESC
            pygame.draw.rect(self.tela, bg_cor, (box_x, curr_y, box_w, row_h), border_radius=4)

            # Destaca com uma borda amarela caso a linha pertença ao jogador atual
            if i < len(top_10) and top_10[i][0] == self.nickname and top_10[i][1] == self.pontuacao:
                pygame.draw.rect(self.tela, AMARELO, (box_x, curr_y, box_w, row_h), 2, border_radius=4)

            pos_surf = fonte_info.render(f"{i+1:02d}º", True, AMARELO if i < 3 else BRANCO)
            self.tela.blit(pos_surf, (box_x + 20, curr_y + 8))

            if i < len(top_10):
                nome, pts = top_10[i]
                nome_surf = fonte_info.render(str(nome), True, BRANCO)
                pts_surf = fonte_info.render(f"{pts} pts", True, AMARELO)
                self.tela.blit(nome_surf, (box_x + 120, curr_y + 8))
                self.tela.blit(pts_surf, (box_x + box_w - 120, curr_y + 8))
            else:
                vazio_surf = fonte_info.render("---", True, CINZA)
                self.tela.blit(vazio_surf, (box_x + 120, curr_y + 8))
                self.tela.blit(vazio_surf, (box_x + box_w - 120, curr_y + 8))

        self._btn_voltar_ranking("Voltar para o Menu", (LARGURA // 2, ALTURA - 60))
        desenhar_btn_sair_ranking(self.tela)

    def _btn(self, texto, centro):
        """Gera um botão azul clicável padrão com efeito hover responsivo."""
        r = pygame.Rect(0, 0, 280, 52)
        r.center = centro
        mouse = pygame.mouse.get_pos()
        cor = AZUL_HOVER if r.collidepoint(mouse) else AZUL
        pygame.draw.rect(self.tela, cor, r, border_radius=8)
        s = fonte_info.render(texto, True, BRANCO)
        self.tela.blit(s, s.get_rect(center=r.center))

    def _btn_voltar_ranking(self, texto, centro):
        """Gera o botão verde específico da tela de ranking."""
        r = self._rect_btn_ranking()
        mouse = pygame.mouse.get_pos()
        cor = VERDE if r.collidepoint(mouse) else VERDE_ESC
        pygame.draw.rect(self.tela, cor, r, border_radius=8)
        s = fonte_info.render(texto, True, BRANCO)
        self.tela.blit(s, s.get_rect(center=r.center))

    def _rect_btn_nickname(self):
        """Retorna o retângulo de colisão do botão da tela de nickname."""
        r = pygame.Rect(0, 0, 260, 52)
        r.center = (LARGURA // 2, 480)
        return r

    def _rect_btn(self):
        """Retorna o retângulo de colisão dinâmico para os botões de fim de jogo e gameover."""
        r = pygame.Rect(0, 0, 280, 52)
        r.center = (LARGURA // 2, 450) if self.estado == self.S_GAMEOVER else (LARGURA // 2, 500)
        return r

    def _rect_btn_ranking(self):
        """Retorna o retângulo de colisão do botão de retorno posicionado no ranking."""
        r = pygame.Rect(0, 0, 280, 52)
        r.center = (LARGURA // 2, ALTURA - 60)
        return r