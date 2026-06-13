import json
def carregar_ranking():
    arquivo = open("ranking.json", "r")
    conteudo = arquivo.read()
    arquivo.close()

    lista_bruta = json.loads(conteudo)

    # Ordena do maior para o menor pontos (bubble sort simples)
    lista = lista_bruta
    tamanho = len(lista)

    for i in range(tamanho):
        for j in range(tamanho - 1 - i):
            if lista[j]["pontos"] < lista[j + 1]["pontos"]:
                temporario = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = temporario

    return lista

resposta = carregar_ranking ()
for posicao in range(len(resposta)):
    print(posicao + 1, resposta[posicao]["nickname"], resposta[posicao]["pontos"])