import pygame
import sys
from src.config import LARGURA, ALTURA
from src.jogo import CosmoMind


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Espaço de Perguntas - CosmoMind")
    relogio = pygame.time.Clock()

    jogo = CosmoMind(tela)

    while True:
        # Eventos globais do sistema
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Repassa eventos dinâmicos para a mecânica interna
            jogo.processar_evento(ev)

        # Atualizações lógicas de temporizadores, timers e posicionamento
        if jogo.flash_timer > 0:
            jogo.flash_timer -= 1
        if jogo.escudo_timer > 0:
            jogo.escudo_timer -= 1

        jogo.atualizar()
        jogo.desenhar()

        pygame.display.flip()
        relogio.tick(60)


if __name__ == "__main__":
    main()