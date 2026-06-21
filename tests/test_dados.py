import unittest
import os
from src.dados import (
    carregar_recorde,
    salvar_recorde,
    carregar_ranking,
    salvar_no_ranking,
    CAMINHO_RECORDE,
    CAMINHO_RANKING
)


class TestCosmoMindDados(unittest.TestCase):
    """
    Conjunto de testes para persistência e higienização de dados (src/dados.py).
    Valida a gravação de arquivos de texto e JSON, garantindo isolamento através
    de backups automatizados para proteger o progresso real do desenvolvedor.
    """

    def setUp(self):
        """
        Executado ANTES de cada teste. Identifica se existem arquivos reais de
        recorde e ranking no sistema, faz um backup temporário de seus conteúdos
        e limpa o ambiente para iniciar os testes a partir do zero absoluto.
        """
        self.backup_recorde = None
        self.backup_ranking = None

        if os.path.exists(CAMINHO_RECORDE):
            with open(CAMINHO_RECORDE, "r", encoding="utf-8") as f:
                self.backup_recorde = f.read()
            os.remove(CAMINHO_RECORDE)

        if os.path.exists(CAMINHO_RANKING):
            with open(CAMINHO_RANKING, "r", encoding="utf-8") as f:
                self.backup_ranking = f.read()
            os.remove(CAMINHO_RANKING)

    def tearDown(self):
        """
        Executado DEPOIS de cada teste. Remove os arquivos gerados pelo ambiente
        de testes simulado e restaura integralmente os arquivos originais e
        pontuações verdadeiras do desenvolvedor que foram guardados no setUp.
        """
        if os.path.exists(CAMINHO_RECORDE):
            os.remove(CAMINHO_RECORDE)
        if os.path.exists(CAMINHO_RANKING):
            os.remove(CAMINHO_RANKING)

        if self.backup_recorde is not None:
            with open(CAMINHO_RECORDE, "w", encoding="utf-8") as f:
                f.write(self.backup_recorde)

        if self.backup_ranking is not None:
            with open(CAMINHO_RANKING, "w", encoding="utf-8") as f:
                f.write(self.backup_ranking)

    def test_carregar_recorde_inexistente(self):
        """
        Objetivo: Garantir tolerância a falhas caso o jogo rode pela primeira vez.
        O que faz: Tenta ler o recorde em um cenário onde o arquivo recorde.txt não existe.
        O que esperar: A função deve interceptar a ausência e retornar o valor padrão 0.
        """
        self.assertEqual(carregar_recorde(), 0)

    def test_salvar_novo_recorde_maior(self):
        """
        Objetivo: Validar o filtro condicional de gravação de pontuações máximas.
        O que faz: Salva um recorde de 50 pontos. Em seguida, tenta gravar 30 pontos.
        O que esperar: O arquivo deve registrar 50 e rejeitar a pontuação menor de 30.
        """
        salvar_recorde(50)
        self.assertEqual(carregar_recorde(), 50)

        salvar_recorde(30)
        self.assertEqual(carregar_recorde(), 50)

    def test_salvar_no_ranking_higieniza_nickname_vazio(self):
        """
        Objetivo: Evitar falhas visuais ou linhas vazias na tabela de classificação.
        O que faz: Envia uma string contendo apenas espaços em branco como nome do jogador.
        O que esperar: O sistema deve higienizar a entrada com .strip() e substituir
                     automaticamente o texto por 'Piloto Anônimo'.
        """
        salvar_no_ranking("   ", 100)
        ranking = carregar_ranking()
        self.assertEqual(ranking[0][0], "Piloto Anônimo")

    def test_ranking_ordenacao_e_limite(self):
        """
        Objetivo: Assegurar o comportamento clássico de uma tabela de Arcade/Fliperama.
        O que faz: Insere progressivamente 12 pontuações diferentes de forma desordenada.
        O que esperar: O arquivo JSON resultante deve conter exatamente 10 registros (Top 10)
                     e a maior pontuação inserida deve estar na primeira posição (índice 0).
        """
        for i in range(1, 13):
            salvar_no_ranking(f"Piloto_{i}", i * 10)

        ranking = carregar_ranking()

        self.assertEqual(len(ranking), 10)
        self.assertEqual(ranking[0][0], "Piloto_12")
        self.assertEqual(ranking[0][1], 120)