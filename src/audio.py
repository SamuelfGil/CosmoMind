import numpy as np
import pygame

# Inicializa o mixer do Pygame se ainda não tiver sido iniciado
if not pygame.mixer.get_init():
    pygame.mixer.init(44100, -16, 2, 512)

# Constante de amostragem padrão para áudio com qualidade de CD (44.1 kHz)
TAXA_AMOSTRAGEM = 44100


def _para_som(onda):
    """Converte um array NumPy de ondas sonoras em um objeto de som do Pygame."""
    # Garante que os valores da onda fiquem estritamente entre os limites de -1 e 1
    onda = np.clip(onda, -1, 1)
    
    # Converte os números flutuantes para inteiros de 16 bits 
    audio16 = (onda * 32767).astype(np.int16)
    
    # Duplica o canal gerando uma matriz de duas colunas para som Estéreo 
    estereo = np.column_stack([audio16, audio16]).copy()
    
    # Transforma a matriz de dados brutos em um objeto de áudio do Pygame
    return pygame.sndarray.make_sound(estereo)


def _envelope(n, ataque=0.01, soltura=0.15):
    """Gera um envelope simplificado (Ataque e Soltura) para suavizar o som."""
    env = np.ones(n)
    
    # Calcula a quantidade exata de amostras para o início (a) e fim (s)
    a = int(n * ataque)
    s = int(n * soltura)
    
    # Aplica rampa linear crescente de 0 a 1 no início do som 
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
        
    # Aplica rampa linear decrescente de 1 a 0 no final do som 
    if s > 0:
        env[-s:] *= np.linspace(1, 0, s)
        
    return env


def _tom(freq, duracao, volume=0.4, forma="seno", destino=None):
    """Gera um tom sintético com opção de modulação de frequência ."""
    n = int(TAXA_AMOSTRAGEM * duracao)
    t = np.linspace(0, duracao, n, False)

    if destino is not None:
        freqs = np.linspace(freq, destino, n)
        fase = 2 * np.pi * np.cumsum(freqs) / TAXA_AMOSTRAGEM
    else:
        fase = 2 * np.pi * freq * t

    if forma == "quadrada":
        onda = np.sign(np.sin(fase))
    elif forma == "triangular":
        onda = 2 * np.abs(2 * ((fase / (2 * np.pi)) % 1) - 1) - 1
    else:
        onda = np.sin(fase)

    onda *= _envelope(n)
    return _para_som(onda * volume)


def _sequencia(notas, volume=0.35, forma="seno"):
    """Concatena uma lista de notas musicais para criar pequenas melodias ou jingles."""
    pedacos = []
    
    for freq, duracao in notas:
        n = int(TAXA_AMOSTRAGEM * duracao)
        t = np.linspace(0, duracao, n, False)
        
        if forma == "quadrada":
            onda = np.sign(np.sin(2 * np.pi * freq * t))
        else:
            onda = np.sin(2 * np.pi * freq * t)
            
        onda *= _envelope(n, 0.02, 0.2)
        pedacos.append(onda)
        
    return _para_som(np.concatenate(pedacos) * volume)


def _ruido(duracao, volume=0.4):
    """Gera ruído branco aleatório, ideal para criar efeitos de explosão ou impacto."""
    n = int(TAXA_AMOSTRAGEM * duracao)
    onda = np.random.uniform(-1, 1, n)
    onda *= _envelope(n, 0.005, 0.5)
    return _para_som(onda * volume)


def _trilha_suspense(duracao=8.0, volume=0.22):
    """Gera uma trilha sonora ambiente contínua com drone grave e batimento cardíaco."""
    n = int(TAXA_AMOSTRAGEM * duracao)
    t = np.linspace(0, duracao, n, False)

    drone = np.sin(2 * np.pi * 55 * t)
    tremolo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t)
    drone *= tremolo

    pulso = np.zeros(n)
    intervalo = 60 / 70
    pos = 0.0
    
    while pos < duracao:
        idx = int(pos * TAXA_AMOSTRAGEM)
        dur_batida = 0.15
        nb = int(TAXA_AMOSTRAGEM * dur_batida)
        if idx + nb < n:
            tb = np.linspace(0, dur_batida, nb, False)
            batida = np.sin(2 * np.pi * 110 * tb) * np.exp(-tb * 18)
            pulso[idx:idx + nb] += batida
        pos += intervalo

    aguda = np.sin(2 * np.pi * 440 * t) * 0.06 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t))

    onda = drone * 0.5 + pulso * 0.5 + aguda
    return _para_som(onda * volume)


class Audio:
    """Gerenciador central do sistema de áudio e efeitos sonoros gerados dinamicamente do jogo."""

    def __init__(self):
        
        VOLUME_MESTRE = 0.3

        # Efeitos Básicos de Interface e Interação
        self.clique = _tom(600, 0.05, 0.25 * VOLUME_MESTRE, "quadrada")
        self.tiro = _tom(950, 0.12, 0.3 * VOLUME_MESTRE, "quadrada", destino=250)
        self.acerto = _sequencia([(523, 0.08), (784, 0.14)], volume=0.35 * VOLUME_MESTRE)
        self.erro = _tom(180, 0.35, 0.45 * VOLUME_MESTRE, "quadrada", destino=80)
        self.explosao = _ruido(0.5, 0.5 * VOLUME_MESTRE)
        self.alerta = _tom(720, 0.18, 0.25 * VOLUME_MESTRE, "seno")
        self.gameover = _sequencia([(400, 0.25), (300, 0.25), (180, 0.5)], volume=0.4 * VOLUME_MESTRE)
        self.vitoria = _sequencia([(523, 0.15), (659, 0.15), (784, 0.15), (1046, 0.4)], volume=0.35 * VOLUME_MESTRE)

        # Efeitos de Jogabilidade Espacial (Gameplay)
        self.impacto = _ruido(0.25, 0.55 * VOLUME_MESTRE)
        self.tiro_impacto = _tom(500, 0.08, 0.3 * VOLUME_MESTRE, "triangular", destino=150)
        self.bonus = _sequencia([(660, 0.08), (880, 0.08), (1320, 0.12)], volume=0.3 * VOLUME_MESTRE)
        self.nivel_up = _sequencia([(440, 0.12), (554, 0.12), (659, 0.12), (880, 0.2)], volume=0.35 * VOLUME_MESTRE)

        # Configuração da música ambiente
        self.trilha = _trilha_suspense(volume=0.22 * VOLUME_MESTRE)
        # Ajuste fino adicional apenas para a trilha não cobrir os efeitos
        self.trilha.set_volume(0.25)

    def iniciar_musica(self):
        """Inicia a reprodução contínua da música de fundo (loop infinito)."""
        self.trilha.play(loops=-1)

    def parar_musica(self):
        """Interrompe a reprodução da música de fundo imediatamente."""
        self.trilha.stop()

    def tocar(self, som):
        """Reproduz um objeto de áudio individual do jogo de forma não bloqueante."""
        som.play()


# Instanciação global automatizada para uso direto nos outros módulos do jogo
audio = Audio()