import os
import json

# Captura o diretório atual onde este script 'dados.py' está localizado
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho relativo apontando para uma pasta acima (raiz) para buscar o arquivo JSON de perguntas
CAMINHO_PERGUNTAS = os.path.join(DIRETORIO_ATUAL, "..", "perguntas.json")

# Estabelece os caminhos absolutos para persistência local de recordes absolutos e dados do ranking de jogadores
CAMINHO_RECORDE = os.path.join(DIRETORIO_ATUAL, "..", "recorde.txt")
CAMINHO_RANKING = os.path.join(DIRETORIO_ATUAL, "..", "ranking.json")


def carregar_perguntas():
    """Carrega o banco de questões estruturado a partir de um arquivo JSON externo.

    Returns:
        list: Lista de dicionários contendo perguntas, alternativas e respostas corretas.
              Retorna uma lista vazia se ocorrer erro na leitura.
    """
    try:
        # Tenta abrir o arquivo JSON em modo leitura com codificação 
        with open(CAMINHO_PERGUNTAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Exibe aviso técnico amigável no terminal caso o arquivo não exista ou esteja corrompido
        print(f"Erro: O arquivo perguntas.json não foi encontrado em: {CAMINHO_PERGUNTAS}")
        return []


def carregar_recorde():
    """Recupera a maior pontuação global registrada historicamente.

    Returns:
        int: O valor inteiro numérico correspondente ao maior recorde salvo.
    """
    # Retorna pontuação zerada padrão caso o arquivo físico de texto não tenha sido criado ainda
    if not os.path.exists(CAMINHO_RECORDE):
        return 0
    try:
        with open(CAMINHO_RECORDE, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            # Valida se o conteúdo é composto apenas por números inteiros antes de converter
            return int(conteudo) if conteudo.isdigit() else 0
    except IOError:
        return 0


def salvar_recorde(nova_pontuacao):
    """Substitui o recorde atual se a pontuação alcançada nesta rodada for maior.

    Args:
        nova_pontuacao (int): A pontuação atual obtida pelo jogador no término da partida.
    """
    recorde_atual = carregar_recorde()
    # Verifica de forma lógica se a pontuação atual superou o recorde estabelecido anteriormente
    if nova_pontuacao > recorde_atual:
        try:
            with open(CAMINHO_RECORDE, "w", encoding="utf-8") as f:
                f.write(str(nova_pontuacao))
        except IOError:
            print("Erro ao tentar salvar o novo recorde.")


def carregar_ranking():
    """Retorna a listagem atual ordenada contendo os 10 melhores pilotos.

    Returns:
        list of list: Lista contendo sublistas no formato [nome_piloto, pontuacao].
    """
    if not os.path.exists(CAMINHO_RANKING):
        return []
    try:
        with open(CAMINHO_RANKING, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_no_ranking(nickname, pontuacao):
    """Insere o jogador no ranking local, reordena e limita o armazenamento aos 10 melhores.

    Args:
        nickname (str): Nome ou alcunha fornecido pelo jogador.
        pontuacao (int): Pontuação final acumulada obtida.
    """
    # Tratamento preventivo para strings vazias ou compostas apenas por espaços em branco
    if not nickname.strip():
        nickname = "Piloto Anônimo"
        
    ranking = carregar_ranking()
    # Adiciona a nova entrada de dados contendo o par [nome, pontos] à lista geral carregada
    ranking.append([nickname, pontuacao])
    
    # Ordena a lista de forma decrescente utilizando o campo pontuação (índice 1 da sublista) como chave
    ranking.sort(key=lambda x: x[1], reverse=True)
    
    # Aplica um fatiamento estrito para manter e salvar exclusivamente o Top 10 no arquivo final
    ranking = ranking[:10]
    
    try:
        with open(CAMINHO_RANKING, "w", encoding="utf-8") as f:
            # Transforma a lista em texto identado legível no JSON sem desconfigurar caracteres acentuados
            json.dump(ranking, f, indent=4, ensure_ascii=False)
    except IOError:
        print("Erro ao tentar atualizar o banco de dados do ranking.")