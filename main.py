import pygame
import sys
from src.config import LARGURA, ALTURA
from src.jogo import CosmoMind
from src.audio import audio

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("CosmoMind - Quiz Espacial de Programação")
    
    audio.iniciar_musica()

    relogio = pygame.time.Clock()
    jogo = CosmoMind(tela)
    
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            jogo.processar_evento(evento)
            
        jogo.atualizar()
        jogo.desenhar()
        
        pygame.display.flip()
        relogio.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()