# Nome do Jogo

CosmoMind

## Integrantes do grupo

- Alexandre Sampaio Guimarães Ribeiro
- Lucas Araújo Asth
- Samuel Abreu Silva de Oliveira Bispo
- Samuel Ferreira Gil

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

No jogo CosmoMind, o jogador assume o comando de uma nave espacial em um ambiente estilo Arcade totalmente interativo. Para disparar lasers e destruir os asteroides que avançam em sua direção com velocidades dinâmicas, o usuário deve responder corretamente a perguntas conceituais atreladas a cada obstáculo. Se a resposta for incorreta, o asteroide ganha velocidade extra na tela; caso atinja a nave, o jogador perderá pontos de vida.

## Objetivo do jogador

O objetivo é sobreviver ao maior número de ondas de asteroides que conseguir e alcançar a maior pontuação possível dentro do ranking local, acumulando pontos ao eliminar os alvos através do acerto das perguntas propostas.

## Regras do jogo

- O jogador inicia a partida com 10 pontos de vida.
- O contato da nave com um asteroide associado a uma questão não respondida ou respondida incorretamente fará o jogador perder no mínimo 1 ponto de vida (podendo perder mais dependendo da dificuldade da pergunta).
- Ao acertar uma sequência de 5 respostas corretas, o jogador recupera 1 ponto de vida (limitado ao máximo de 10).
- Os asteroides cujas perguntas associadas forem respondidas incorretamente ganharão velocidade extra na tela.
- O jogador ganhará pontos após a eliminação de cada asteroide, variando de acordo com a dificuldade da pergunta relacionada.
- A partida é encerrada automaticamente quando o número de pontos de vida chegar a zero ou quando o comando voluntário de saída for acionado ou quando acabar todas as perguntas.

## Controles

- Mouse / Seleção: Servirá para selecionar o asteroide ou a pergunta específica que o usuário deseja tentar responder.
- Teclado: Servirá para a pessoa inserir seu nickname e sair do jogo.
- ENTER: Envia a resposta final digitada ou os comandos do sistema. Se a resposta estiver correta, a nave dispara um tiro laser que destrói o asteroide selecionado; caso contrário, o tiro erra o alvo.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/SamuelfGil/CosmoMind.git
cd CosmoMind
pip install pygame-ce
pip install numpy
python main.py
```

## Como executar os testes


```bash
pip install pytest
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
