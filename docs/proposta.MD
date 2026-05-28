# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

Escreva aqui o nome provisório do jogo.

Exemplo:

> Corrida dos Obstáculos

## 2. Integrantes do grupo

Liste os integrantes do grupo.

- Nome 1: 
- Nome 2:
- Nome 3:
- Nome 4:

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

JOGO DE PERGUNTAS E RESPOSTAS INTERATIVO

## 4. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará.

Procure responder:

- O que aparece na tela?
- O que o jogador controla?
- O que o jogador precisa fazer?
- Quais desafios aparecem durante a partida?

Descrição:

O JOGADOR QUE ESTARÁ NO COMANDO DE UMA NAVE ESPACIAL, TERÁ DE RESPONDER PERGUNTAS CORRETAMENTE PARA ATIRAR LASERS E CONSEGUIR DESTRUIR ASTEROIDES QUE ESTÃO VINDO EM SUA DIREÇÃO


## 5. Objetivo do jogador

Explique qual é o objetivo principal do jogador.

Exemplos:

- coletar o maior número possível de itens;
- sobreviver pelo maior tempo possível;
- chegar até o final do labirinto;
- acertar alvos;
- responder perguntas corretamente;
- evitar obstáculos;
- quebrar todos os blocos.

Objetivo:

SOBREVIVER O MÁXIMO POSSÍVEL, ACUMULANDO O MÁXIMO DE PONTOS QUE DER AO ELINAR ALVOS AO RESPONDER PERGUNTAS CORRETAMENTE.

## 6. Regras principais

Liste as principais regras do jogo.

Exemplo:

- O jogador começa com 3 vidas.
- Cada moeda coletada vale 10 pontos.
- Cada colisão com obstáculo remove 1 vida.
- A partida termina quando as vidas chegam a zero.
- O jogador vence se alcançar 100 pontos.

Regras do grupo:

- Regra 1: O JOGADOR INICIA COM 10 PONTOS DE VIDA.
- Regra 2: O CONTATO COM UM ASTEROIDE ASSOCIADO A UMA QUESTÃO QUE NÃO FOI RESPONDIDA OU RESPONDIDA INCORRETAMENTE FARÁ COM QUE O JOGADOR PERCA 1 PONTO DE VIDA OU MAIS A DEPENDER DA DIFICULDADE DELA.
- Regra 3: AO ACERTAR UMA SEQUENCIA DE 5 RESPOSTAS CORRETAS, O JOGADOR RECUPERA UM PONTO DE VIDA.
- Regra 4: QUANDO O NÚMERO DE PONTOS DE VIDA CHEGAR A ZERO O JOGO É FINALIZADO.
- Regra 5: OS ASTEROIDES EM QUE SUAS PERGUNTAS ASSOCIADAS  FOREM RESPONDIDAS INCORRETAMENTE GANHARÃO VELOCIDADE.
- Regra 6: O JOGADOR GANHARÁ PONTOS PONTOS APÓS A ELIMINAÇÃO DE ASTEROIDES (OS PONTOS VÃO VARIAR DE ACORDO COM A DIFICULDADE DA PERGUNTA RELACIONADA).

## 7. Condição de vitória

Explique como o jogador vence ou conclui o jogo.

Exemplos:

- atingir determinada pontuação;
- chegar ao final da fase;
- sobreviver até o tempo acabar;
- responder uma quantidade mínima de perguntas;
- quebrar todos os blocos.

Condição de vitória:

SOBREVIVER AO MÁXIMO DE ONDAS DE ASTEROIDES QUE CONSEGUIR RESPONDENDO CORRETAMENTE AS PERGUNTAS E SER O PLAYER COM MAIOR QUANTIDADE DE PONTOS DENTRO DO RANKING.

## 8. Condição de derrota ou encerramento

Explique como o jogador perde ou quando a partida termina.

Exemplos:

- perder todas as vidas;
- acabar o tempo;
- colidir com determinado obstáculo;
- errar muitas perguntas;
- deixar a bola cair, no caso de Breakout ou Pong.

Condição de derrota ou encerramento:

O JOGO É ENCERRADO APÓS O JOGADOR PERDER TODOS OS SEUS PONTOS DE VIDA OU DIGITAR "SAIR".

## 9. Elementos previstos no jogo

Descreva os principais elementos que farão parte do jogo.

## Jogador ou elemento principal

Exemplo: 

> Um personagem controlado pelas setas do teclado.

Descrição:

> NAVE CONTROLADA PELO JOGADOR QUE IRÁ ATIRAR AO RESPONDER PERGUNTAS.

## Obstáculos, inimigos ou desafios

Exemplo:

> Obstáculos aparecem em posições aleatórias e devem ser evitados.

Descrição:

> Escreva aqui.

## Itens, alvos ou objetos de interação

Exemplo:

> Moedas aparecem na tela e aumentam a pontuação quando coletadas.

Descrição:

> Escreva aqui.

## Pontuação, vidas, tempo ou progresso

Exemplo:

> O jogador começa com 3 vidas e ganha 10 pontos por item coletado.

Descrição:

> Escreva aqui.

## 10. Controles previstos

Informe os comandos que serão utilizados pelo jogador.

Exemplo:

- Seta para cima: mover para cima
- Seta para baixo: mover para baixo
- Seta para esquerda: mover para esquerda
- Seta para direita: mover para direita
- Espaço: realizar ação
- ESC: sair do jogo

Controles do grupo:

- ENTER: ENVIAR A RESPOSTA DO JOGADOR, CASO SEJA A RESPOSTA CORRETA SAIRÁ UM TIRO EM DIREÇÃO A UM ASTEROIDE E O DESTRUIRÁ, CASO CONTRAŔIO O TIRO ERRARÁ. PODENDO TAMBÉM SER UM COMANDO DE SAIDA DO JOGO.
- TECLADO NUMÉRICO: SERVIRÁ PARA SELECIONAR O ASTEROIDE/PERGUNTA A SER RESPONDIDA

## 11. Organização inicial do código

Explique como o grupo pretende organizar o código.

Exemplo:

- `main.py`: inicia o jogo;
- `src/jogo.py`: contém o loop principal;
- `src/config.py`: guarda configurações como tamanho da tela e cores;
- `src/funcoes.py`: contém funções auxiliares;
- `src/dados.py`: contém funções de leitura e escrita de arquivos.

Organização planejada:


- `main.py`: inicia o jogo;
- `src/jogo.py`: contém o loop principal;
- `src/config.py`: guarda configurações como tamanho da tela e cores;
- `src/funcoes.py`: contém funções auxiliares;
- `src/perguntas.json`: contém as perguntas que serão usadas durante o jogo;
- `src/score.txt`: contém os scores dos players;
- `src/dados.py`: contém funções de leitura e escrita de arquivos.


## 12. Recursos externos previstos

Informe se o grupo pretende utilizar imagens, sons, fontes, tutoriais ou códigos externos.

Exemplo:

- imagens obtidas de banco gratuito;
- sons gratuitos;
- tutorial usado apenas como referência;
- fonte personalizada.

Recursos previstos:

- videos obtidas de banco gratuito;
- sons gratuitos para os tiros, destruição dos asteroides sons de sinalização de baixa vida;
- fonte personalizada de 8 bits.

Caso não pretenda utilizar recursos externos, escreva:

> Não pretendemos utilizar recursos externos.

## 13. Principais dificuldades esperadas

Liste as dificuldades que o grupo acredita que poderá enfrentar.

Exemplos:

- movimentação do jogador;
- colisão entre objetos;
- controle de tempo;
- criação do ranking;
- organização do código;
- uso do GitHub;
- testes;
- exibição de textos na tela.

Dificuldades previstas:

- Dificuldade 1: Definir uma velocidade ideal para os asteroides;
- Dificuldade 2: Conseguir alimentar o banco de dados com perguntas suficientes;
- Dificuldade 3: Criar a ambientação/cenário;
- Dificuldade 4: Criar a ambientação/cenário;
- Dificuldade 5: Organização do código;
- Dificuldade 6: Uso do GitHub;
- Dificuldade 7: Criação do ranking.


## 14. Escopo mínimo para a entrega final

Descreva qual será a versão mínima aceitável do jogo.

Esta seção é importante para evitar que o grupo escolha uma ideia grande demais.

Exemplo:

> A versão mínima do jogo terá um personagem controlado pelo teclado, obstáculos aparecendo na tela, sistema de vidas, sistema de pontuação e tela de fim de jogo.

Escopo mínimo:

> INICIAŔA EM UMA TELA ONDE O JOGADOR IRÁ ESCREVER SEU NICKNAME E INICIAR O JOGO, POSTERIORMENTE, SERÁ ABERTA UMA OUTRA TELA AMBIENTADA NO ESPAÇO QUE TERÁ A NAVE DO PLAYER E OS ASTEROIDES VOANDO EM DIREÇÃO A ELA. NA PARTE INFERIOR DA TELA, ESTARÃO CONTIDAS AS INFORMAÇÕES DO JOGADOR (PONTOS DE VIDA , PONTOS DE ELIMINAÇÃO/SCORE E NICKNAME)

## 15. Possíveis melhorias, caso haja tempo

Liste funcionalidades extras que o grupo poderá implementar se conseguir concluir o escopo mínimo.

Exemplos:

- tela inicial;
- sons;
- fases;
- aumento de dificuldade;
- ranking;
- animações;
- novos tipos de obstáculos;
- diferentes personagens;
- menu de pausa.

Melhorias possíveis:

- Melhoria 1: Sons
- Melhoria 2: Aumento de dificuldade;
- Melhoria 3: Diferentes skins de nave;
- Melhoria 4: Diferentes sons de tiro;
- Melhoria 5: Diferentes cenários;
- Melhoria 6: Skins dos asteroides.
