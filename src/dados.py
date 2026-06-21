import os
import json

# Define o caminho dinâmico para o arquivo perguntas.json
# os.path.abspath(__file__) garante o caminho correto independente de onde o terminal foi aberto
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_PERGUNTAS = os.path.join(DIRETORIO_ATUAL, "..", "perguntas.json")

# Caminhos para salvar os dados de progresso e ranking (gerados na pasta raiz do projeto)
CAMINHO_RECORDE = os.path.join(DIRETORIO_ATUAL, "..", "recorde.txt")
CAMINHO_RANKING = os.path.join(DIRETORIO_ATUAL, "..", "ranking.json")

def carregar_perguntas():
    """Carrega o banco de perguntas estruturado a partir do arquivo JSON."""
    try:
        with open(CAMINHO_PERGUNTAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Erro: O arquivo perguntas.json não foi encontrado em: {CAMINHO_PERGUNTAS}")
        return []

def carregar_recorde():
    """Recupera a maior pontuação salva no sistema."""
    if not os.path.exists(CAMINHO_RECORDE):
        return 0
    try:
        with open(CAMINHO_RECORDE, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            return int(conteudo) if conteudo.isdigit() else 0
    except IOError:
        return 0

def salvar_recorde(nova_pontuacao):
    """Atualiza o recorde se a nova pontuação for maior que a anterior."""
    recorde_atual = carregar_recorde()
    if nova_pontuacao > recorde_atual:
        try:
            with open(CAMINHO_RECORDE, "w", encoding="utf-8") as f:
                f.write(str(nova_pontuacao))
        except IOError:
            print("Erro ao tentar salvar o novo recorde.")

def carregar_ranking():
    """Retorna a lista dos melhores pilotos ordenada por pontuação (Top 10)."""
    if not os.path.exists(CAMINHO_RANKING):
        return []
    try:
        with open(CAMINHO_RANKING, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_no_ranking(nickname, pontuacao):
    """Insere o jogador atual no ranking geral e ordena do maior para o menor."""
    if not nickname.strip():
        nickname = "Piloto Anônimo"
        
    ranking = carregar_ranking()
    ranking.append([nickname, pontuacao])
    
    # Ordena pelo maior número de pontos (index 1 do par)
    ranking.sort(key=lambda x: x[1], reverse=True)
    
    # Mantém apenas os 10 melhores resultados no arquivo
    ranking = ranking[:10]
    
    try:
        with open(CAMINHO_RANKING, "w", encoding="utf-8") as f:
            json.dump(ranking, f, indent=4, ensure_ascii=False)
    except IOError:
        print("Erro ao tentar atualizar o banco de dados do ranking.")