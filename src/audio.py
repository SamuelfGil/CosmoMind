import numpy as np
import pygame

if not pygame.mixer.get_init():
    pygame.mixer.init(44100, -16, 2, 512)

TAXA_AMOSTRAGEM = 44100


def _para_som(onda):
    onda = np.clip(onda, -1, 1)
    audio16 = (onda * 32767).astype(np.int16)
    estereo = np.column_stack([audio16, audio16]).copy()
    return pygame.sndarray.make_sound(estereo)


def _envelope(n, ataque=0.01, soltura=0.15):
    # Suaviza início e fim do som pra não estalar (clipping) nas caixinhas
    env = np.ones(n)
    a = int(n * ataque)
    s = int(n * soltura)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if s > 0:
        env[-s:] *= np.linspace(1, 0, s)
    return env


def _tom(freq, duracao, volume=0.4, forma="seno", destino=None):
    # Gera um tom simples. Se "destino" for passado, a frequência desliza até lá (efeito de sirene/laser)
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
    # Junta várias notas (freq, duracao) em sequência, pra fazer jingles
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
    # Ruído branco com fade -> serve pra explosão
    n = int(TAXA_AMOSTRAGEM * duracao)
    onda = np.random.uniform(-1, 1, n)
    onda *= _envelope(n, 0.005, 0.5)
    return _para_som(onda * volume)


def _trilha_suspense(duracao=8.0, volume=0.22):
    """Gera uma trilha ambiente de suspense: drone grave + pulso tipo batimento cardíaco"""
    n = int(TAXA_AMOSTRAGEM * duracao)
    t = np.linspace(0, duracao, n, False)

    # Drone grave com tremolo lento -> cria a tensão de fundo
    drone = np.sin(2 * np.pi * 55 * t)
    tremolo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t)
    drone *= tremolo

    # Pulso tipo batimento cardíaco, ~70 bpm
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

    # Camada aguda e dissonante que entra e sai, dá um clima mais tenso
    aguda = np.sin(2 * np.pi * 440 * t) * 0.06 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t))

    onda = drone * 0.5 + pulso * 0.5 + aguda
    return _para_som(onda * volume)


class Audio:
    def __init__(self):
        self.clique = _tom(600, 0.05, 0.25, "quadrada")
        self.tiro = _tom(950, 0.12, 0.3, "quadrada", destino=250)
        self.acerto = _sequencia([(523, 0.08), (784, 0.14)], volume=0.35)
        self.erro = _tom(180, 0.35, 0.45, "quadrada", destino=80)
        self.explosao = _ruido(0.5, 0.5)
        self.alerta = _tom(720, 0.18, 0.25, "seno")
        self.gameover = _sequencia([(400, 0.25), (300, 0.25), (180, 0.5)], volume=0.4)
        self.vitoria = _sequencia([(523, 0.15), (659, 0.15), (784, 0.15), (1046, 0.4)], volume=0.35)

        
        self.impacto = _ruido(0.25, 0.55)                 # asteroide bateu na nave
        self.tiro_impacto = _tom(500, 0.08, 0.3, "triangular", destino=150)  # laser acertou o alvo
        self.bonus = _sequencia([(660, 0.08), (880, 0.08), (1320, 0.12)], volume=0.3)  # combo deu vida extra
        self.nivel_up = _sequencia([(440, 0.12), (554, 0.12), (659, 0.12), (880, 0.2)], volume=0.35)  # subiu de setor

        self.trilha = _trilha_suspense()
        self.trilha.set_volume(0.35)

    def iniciar_musica(self):
        self.trilha.play(loops=-1)

    def parar_musica(self):
        self.trilha.stop()

    def tocar(self, som):
        som.play()


audio = Audio()