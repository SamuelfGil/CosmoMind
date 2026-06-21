import pygame
import sys
from src.config import LARGURA, ALTURA
from src.jogo import CosmoMind
from src.audio import audio

def main():
    """Ponto de entrada principal do programa. Inicializa o Pygame, o laço de eventos e gerencia a taxa de quadros."""
    # Inicializa os componentes base do framework Pygame
    pygame.init()
    
    # Define o tamanho e cria a janela de exibição principal
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("CosmoMind - Quiz Espacial de Programação")
    
    # Inicia a execução da música ambiente em loop contínuo
    audio.iniciar_musica()

    # Instancia o controlador de clock/tempo para estabilização de FPS
    relogio = pygame.time.Clock()
    
    # Instancia o núcleo lógico do jogo passando a janela ativa
    jogo = CosmoMind(tela)
    
    rodando = True
    # Laço principal de execução (Main Game Loop)
    while rodando:
        # Captura e trata a fila de eventos gerados pelo sistema operacional
        for evento in pygame.event.get():
            # Interrompe o laço de execução caso o usuário feche a janela ou clique em sair
            if evento.type == pygame.QUIT:
                rodando = False
                
            # Repassa o evento capturado para tratamento interno da máquina de estados do quiz
            jogo.processar_evento(evento)
            
        # Executa as rotinas físicas de física matemática e contagem de tempo
        jogo.atualizar()
        
        # Limpa e repinta todos os pixels da tela conforme o estado gráfico correspondente
        jogo.desenhar()
        
        # Inverte os buffers ocultos de desenho tornando as atualizações visíveis na tela (Double Buffering)
        pygame.display.flip()
        
        # Bloqueia a execução do laço garantindo uma taxa estável cravada em 60 quadros por segundo
        relogio.tick(60)
        
    # Desativa de forma segura os subsistemas do Pygame ao sair do loop principal
    pygame.quit()
    # Encerra o interpretador Python limpando os processos do sistema operacional
    sys.exit()

if __name__ == "__main__":
    # Garante a execução isolada e segura do script principal
    main()