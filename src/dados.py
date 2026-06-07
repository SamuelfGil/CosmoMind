import os
import json

def carregar_perguntas(caminho="perguntas.json"):
    if not os.path.exists(caminho):
        perguntas_padrao = [
            {"pergunta": "O que é um algoritmo?",
             "alternativas": ["Uma linguagem de programação",
                              "Uma sequência lógica e finita de passos para resolver um problema",
                              "Uma peça de hardware do computador",
                              "Um erro que ocorre durante a compilação"],
             "correta": 1},
            {"pergunta": "Para que serve o 'if/else'?",
             "alternativas": ["Repetir código infinitamente",
                              "Armazenar dados permanentemente",
                              "Executar blocos diferentes conforme uma condição",
                              "Declarar variáveis"],
             "correta": 2},
            {"pergunta": "O que é uma variável?",
             "alternativas": ["Altera a velocidade do processador.",
                              "Espaço na memória para armazenar um dado que pode mudar.",
                              "Palavra reservada que não pode ser modificada.",
                              "Laço de repetição que varia seus passos."],
             "correta": 1},
            {"pergunta": "Qual estrutura é melhor quando sabemos o número exato de repetições?",
             "alternativas": ["while", "if/else", "for", "switch/case"],
             "correta": 2},
            {"pergunta": "O que é recursividade?",
             "alternativas": ["Uma função que chama a si mesma para resolver partes menores do problema.",
                              "Um for dentro de outro for.",
                              "Um erro lógico que trava o computador.",
                              "Converter código-fonte em linguagem de máquina."],
             "correta": 0},
        ]
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(perguntas_padrao, f, ensure_ascii=False, indent=4)
        return perguntas_padrao

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)