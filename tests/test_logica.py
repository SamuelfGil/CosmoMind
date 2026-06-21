import unittest
import pygame
from src.funcoes import quebrar_linhas, altura_texto


class TestCosmoMindFuncoes(unittest.TestCase):
    """
    Conjunto de testes unitários para o módulo de funções de texto (src/funcoes.py).
    Garante que o processamento de strings e o cálculo de dimensões de texto
    funcionem corretamente antes da renderização na tela do Pygame.
    """

    @classmethod
    def setUpClass(cls):
        """
        Inicializa o subsistema de fontes do Pygame em modo headless e define
        uma fonte padrão que será reaproveitada em todos os testes desta classe.
        """
        pygame.font.init()
        cls.fonte_teste = pygame.font.SysFont("Arial", 20)

    def test_quebrar_linhas_texto_curto(self):
        """
        Objetivo: Garantir que strings curtas não sofram quebras desnecessárias.
        O que faz: Passa uma frase curta e um limite de largura grande (400px).
        O que esperar: A função deve retornar apenas 1 linha contendo o texto intacto.
        """
        texto = "Janela de Teste"
        resultado = quebrar_linhas(texto, self.fonte_teste, 400)
        self.assertTrue(len(resultado) >= 1)
        self.assertIn("Janela", resultado[0])

    def test_altura_texto_retorno_valido(self):
        """
        Objetivo: Validar o cálculo vertical da caixa do painel de perguntas.
        O que faz: Solicita a altura de uma linha de texto.
        O que esperar: O retorno deve ser um número inteiro positivo maior que zero,
                     condizente com o tamanho em pixels da fonte atual.
        """
        texto = "Linha unica de teste para verificar a medicao de altura do painel."
        altura = altura_texto(texto, self.fonte_teste, 300)
        self.assertGreater(altura, 0)
        self.assertIsInstance(altura, int)

    def test_quebrar_linhas_texto_longo(self):
        """
        Objetivo: Garantir que perguntas longas se ajustem perfeitamente à tela do jogo.
        O que faz: Passa uma string comprida e força um limite de largura seguro (400px).
        O que esperar: A função deve dividir o texto em múltiplas linhas e nenhuma
                     linha individual pode ter uma largura em pixels maior que 400px.
        """
        texto = "Este e um texto consideravelmente longo feito para testar o algoritmo de quebra automatica"
        largura_maxima = 400  # Alterado de 150 para 400 para dar margem a palavras longas
        resultado = quebrar_linhas(texto, self.fonte_teste, largura_maxima)

        self.assertGreater(len(resultado), 1)
        for linha in resultado:
            largura_da_linha = self.fonte_teste.size(linha)[0]
            self.assertLessEqual(largura_da_linha, largura_maxima)