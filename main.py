import pygame
import sys
from src.config import LARGURA, ALTURA
from src.jogo import CosmoMind

# O ponto de partida que inicia o executável do jogo
def main():
    pygame.init()
    
    # Configura a janela física do jogo e o título que fica lá em cima da barra da janela
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Espaço de Perguntas - CosmoMind")
    
    # Objeto de controle de tempo pra cravar os frames do jogo
    relogio = pygame.time.Clock()

    # Cria a instância da lógica principal do jogo
    jogo = CosmoMind(tela)

    # Loop Infinito (principal) que fica rodando enquanto o jogo estiver aberto
    while True:
        # Loop de escuta de eventos nativos do sistema operacional
        for ev in pygame.event.get():
            # Se fechar no X da janela ou apertar ESC, mata o processo na hora
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Manda o evento coletado pras regras internas do jogo avaliarem
            jogo.processar_evento(ev)

        # Trata o tempo dos timers de efeitos visuais a cada rodada do loop
        if jogo.flash_timer > 0:
            jogo.flash_timer -= 1
        if jogo.escudo_timer > 0:
            jogo.escudo_timer -= 1

        # Roda a física de movimento das entidades e colisões
        jogo.atualizar()
        
        # Redesenha todas as imagens atualizadas na tela de fundo
        jogo.desenhar()

        # Atualiza o monitor com o frame novo que acabou de ser processado
        pygame.display.flip()
        
        # Garante que o jogo vai rodar cravado a 60 FPS pra não estourar a CPU
        relogio.tick(60)


if __name__ == "__main__":
    # Só chama a função se o script for executado diretamente pelo terminal
    main()