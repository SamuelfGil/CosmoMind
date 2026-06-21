import unittest
import os

# Força o Pygame a rodar sem abrir telas físicas enquanto manipula retângulos ou vetores
os.environ["SDL_VIDEODRIVER"] = "dummy"

from src.sprites import Estrela
from src.config import ALTURA


class TestCosmoMindMecanicas(unittest.TestCase):
    """
    Conjunto de testes focados nas mecânicas físicas e movimentação de objetos (src/sprites.py).
    Verifica as posições matemáticas das entidades dinâmicas do plano de fundo.
    """

    def test_reset_estrela_ao_passar_da_tela(self):
        """
        Objetivo: Validar a ilusão de ótica de deslocamento infinito pelo espaço.
        O que faz: Instancia uma estrela e altera artificialmente sua coordenada Y
                  para além da resolução de altura configurada para o monitor (ALTURA + 5).
        O que esperar: Ao invocar o método mover(), a estrela deve detectar o transbordo
                     e teleportar sua coordenada vertical imediatamente de volta para 0.
        """
        estrela = Estrela()

        estrela.y = ALTURA + 5
        estrela.mover()

        self.assertEqual(estrela.y, 0)