import pygame
from src.config import LARGURA, ALTURA, VERMELHO_ESC, BRANCO, fonte_pequena, fonte_info

def rect_btn_sair_jogo():
    # Posição do botão pequeno de sair, durante a partida
    r = pygame.Rect(0, 0, 90, 30)
    r.center = (LARGURA // 2, 25)
    return r

def desenhar_btn_sair_jogo(tela):
    retangulo = rect_btn_sair_jogo()
    pygame.draw.rect(tela, VERMELHO_ESC, retangulo, border_radius=6)
    texto = fonte_pequena.render("Sair", True, BRANCO)
    tela.blit(texto, texto.get_rect(center=retangulo.center))

def rect_btn_sair_ranking():
    # Posição do botão de sair na tela de ranking
    r = pygame.Rect(0, 0, 280, 52)
    r.center = (LARGURA // 2, ALTURA - 130)
    return r

def desenhar_btn_sair_ranking(tela):
    retangulo = rect_btn_sair_ranking()
    pygame.draw.rect(tela, VERMELHO_ESC, retangulo, border_radius=8)
    texto = fonte_info.render("Sair do Jogo", True, BRANCO)
    tela.blit(texto, texto.get_rect(center=retangulo.center))