def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except FileNotFoundError:
        return 0
PERGUNTAS = [
    {
        "pergunta": "Qual é o planeta mais próximo do Sol?",
        "alternativas": ["A) Terra", "B) Marte", "C) Mercúrio"],
        "correta": "C"
    },
    {
        "pergunta": "O que significa a sigla NASA?",
        "alternativas": ["A) National Aeronautics and Space Administration", "B) New Aero Space Association", "C) Night Astronomy Station"],
        "correta": "A"
    },
    {
        "pergunta": "Pergunta 3 - Exemplo",
        "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3"],
        "correta": "B"
    },
    {
        "pergunta": "Pergunta 4 - Exemplo",
        "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3"],
        "correta": "A"
    },
    {
        "pergunta": "Pergunta 5 - Exemplo",
        "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3"],
        "correta": "C"
    },
    {
        "pergunta": "Pergunta 6 - Exemplo",
        "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3"],
        "correta": "B"
    },
    {
        "pergunta": "Pergunta 7 - Exemplo",
        "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3"],
        "correta": "A"
    },
    {
        "pergunta": "Pergunta 8 - Exemplo",
        "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3"],
        "correta": "C"
    },
    {
        "pergunta": "Pergunta 9 - Exemplo",
        "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3"],
        "correta": "B"
    },
    {
        "pergunta": "Pergunta 10 - Exemplo",
        "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3"],
        "correta": "A"
    }
]