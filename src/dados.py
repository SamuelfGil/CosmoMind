import os
import json

def carregar_perguntas(caminho="perguntas.json"):
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_recorde(caminho="data/recorde.txt"):
    pasta = os.path.dirname(caminho)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
    if not os.path.exists(caminho):
        return 0
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            return int(conteudo) if conteudo.isdigit() else 0
    except:
        return 0

def salvar_recorde(pontuacao, caminho="data/recorde.txt"):
    recorde_atual = carregar_recorde(caminho)
    if pontuacao > recorde_atual:
        pasta = os.path.dirname(caminho)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(str(pontuacao))
        return True
    return False

def carregar_ranking(caminho="data/ranking.txt"):
    if not os.path.exists(caminho):
        return []
    
    lista_ranking = []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                if ":" in linha:
                    nome, pts = linha.strip().split(":", 1)
                    if pts.isdigit():
                        lista_ranking.append((nome, int(pts)))
    except:
        pass
    
    lista_ranking.sort(key=lambda x: x[1], reverse=True)
    return lista_ranking[:10]

def salvar_no_ranking(nickname, pontuacao, caminho="data/ranking.txt"):
    pasta = os.path.dirname(caminho)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
        
    tag_piloto = nickname.strip() if nickname.strip() else "Piloto_Anonimo"
    ranking_atual = carregar_ranking(caminho)
    
    ranking_atual.append((tag_piloto, pontuacao))
    ranking_atual.sort(key=lambda x: x[1], reverse=True)
    top_10 = ranking_atual[:10]
    
    with open(caminho, "w", encoding="utf-8") as f:
        for nome, pts in top_10:
            f.write(f"{nome}:{pts}\n")