import unittest
import pygame
from src.funcoes import quebrar_linhas, altura_texto

class TestCosmoMindFuncoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializa o pygame em modo dummy (sem abrir janela) apenas para carregar fontes nos testes
        pygame.font.init()
        cls.fonte_teste = pygame.font.SysFont("Arial", 20)

    def test_quebrar_linhas_texto_curto(self):
        texto = "Janela de Teste"
        resultado = quebrar_linhas(texto, self.fonte_teste, 400)
        self.assertTrue(len(resultado) >= 1)
        self.assertIn("Janela", resultado[0])

    def test_altura_texto_retorno_valido(self):
        texto = "Linha unica de teste para verificar a medicao de altura do painel."
        altura = altura_texto(texto, self.fonte_teste, 300)
        self.assertGreater(altura, 0)
        self.assertIsInstance(altura, int)

if __name__ == "__main__":
    unittest.main()