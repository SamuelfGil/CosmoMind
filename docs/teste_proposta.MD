# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

---

## 1. Nome provisório do jogo

> CosmoMind

## 2. Integrantes do grupo

- Nome 1: Alexandre Sampaio Guimarães Ribeiro
- Nome 2: Lucas Araújo Asth
- Nome 3: Samuel Abreu Silva de Oliveira Bispo
- Nome 4: Samuel Ferreira Gil

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

> Jogo de nave com tiros com alvos fixos / Arcade (Perguntas e Respostas Interativo)

## 4. Descrição geral do jogo

Descrição:

> No jogo, o jogador estará no comando de uma nave espacial e terá de responder perguntas corretamente para conseguir atirar lasers e destruir os asteroides correspondentes que estão vindo em sua direção.

## 5. Objective do jogador

Objetivo:

> Sobreviver o máximo possível, acumulando o máximo de pontos que puder ao eliminar os alvos através do acerto das perguntas propostas.

## 6. Regras principais

Regras do grupo:

- **Regra 1:** O jogador inicia a partida com 10 pontos de vida.
- **Regra 2:** O contato da nave com um asteroide associado a uma questão não respondida ou respondida incorretamente fará o jogador perder 1 ponto de vida (ou mais, dependendo do nível de dificuldade da pergunta).
- **Regra 3:** Ao acertar uma sequência de 5 respostas corretas, o jogador recupera 1 ponto de vida.
- **Regra 4:** Quando o número de pontos de vida chegar a zero, o jogo é finalizado automaticamente.
- **Regra 5:** Os asteroides cujas perguntas associadas forem respondidas incorretamente ganharão velocidade extra na tela.
- **Regra 6:** O jogador ganhará pontos após a eliminação de cada asteroide, variando de acordo com a dificuldade da pergunta relacionada.

## 7. Condição de vitória

Condição de vitória:

> Sobreviver ao maior número de ondas de asteroides que conseguir respondendo corretamente às perguntas e alcançar a maior pontuação possível dentro do ranking local.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> O jogo é encerrado imediatamente quando o jogador perde todos os seus 10 pontos de vida ou quando digita o comando voluntário "SAIR".

## 9. Elementos previstos no jogo

### Jogador ou elemento principal
> Uma nave espacial posicionada estrategicamente, controlada e defendida pelo jogador, que dispara projéteis que acertarão os alvos apenas ao validar respostas corretas.

### Obstáculos, inimigos ou desafios
> Asteroides que surgem em ondas direcionadas à nave do jogador, cada um atrelado a um desafio/pergunta conceitual com velocidades dinâmicas.

### Itens, alvos ou objetos de interação
> Caixa de texto e interface de seleção de perguntas/asteroides, onde o acerto atua como o gatilho de eliminação dos alvos.

### Pontuação, vidas, tempo ou progresso
> Barra/contador de pontos de vida (limitado ao máximo de 10), placar de pontuação de eliminação (score infinito), multiplicadores por sequências de acertos e controle de nickname. Elementos visuais e decorativos de ambientação espacial preenchem o cenário.

## 10. Controles previstos

Controles do grupo:

- **Teclado Numérico / Seleção:** Servirá para selecionar o asteroide ou a pergunta específica que o usuário deseja tentar responder.
- **Caixa de Entrada de Texto:** Digitação manual da resposta ou de comandos do sistema.
- **ENTER:** Envia a resposta final digitada pelo jogador. Se estiver correta, a nave dispara um tiro laser que destrói o asteroide selecionado; caso contrário, o tiro erra o alvo. Também serve para enviar comandos de sistema (como o comando de saída).

## 11. Organização inicial do código

Organização planejada:

- `main.py`: Inicializa o ecossistema do Pygame e invoca as telas principais;
- `src/jogo.py`: Contém o loop principal do jogo (gerenciamento de estados, eventos, atualizações e desenho);
- `src/config.py`: Guarda as configurações globais de constantes, tais como tamanho da janela, taxas de atualização (FPS) e paletas de cores;
- `src/funcoes.py`: Contém as funções auxiliares do sistema;
- `src/dados.py`: Contém funções dedicadas à persistência de dados (leitura e escrita de arquivos);
- `src/perguntas.json`: Arquivo estruturado que armazena a base de dados de perguntas, alternativas e níveis de dificuldade;
- `src/score.txt`: Arquivo texto para persistência e armazenamento do histórico de pontuações dos jogadores para o ranking.

## 12. Recursos externos previstos

Recursos previstos:

- Imagens e elementos visuais de plano de fundo espaciais obtidos de bancos gratuitos;
- Efeitos sonoros gratuitos para disparos de lasers, explosão/destruição de asteroides e alertas sonoros indicadores de baixa vida;
- Tipografia / Fonte personalizada em estilo *8-bit* (estética retrô/arcade).

## 13. Principais dificuldades esperadas

Dificuldades previstas:

- **Dificuldade 1:** Balancear e definir uma curva de velocidade ideal para a descida dos asteroides;
- **Dificuldade 2:** Alimentar e estruturar o arquivo JSON com uma quantidade satisfatória de perguntas e respostas;
- **Dificuldade 3:** Criar e renderizar uma ambientação/cenário dinâmico no espaço sem prejudicar o desempenho;
- **Dificuldade 4:** Administrar o tempo limite para as respostas de forma justa para o usuário;
- **Dificuldade 5:** Arquitetar a colisão entre os asteroides e o limite de defesa da nave;
- **Dificuldade 6:** Organização modular do código e versionamento em equipe utilizando o Git/GitHub;
- **Dificuldade 7:** Desenvolvimento da lógica de ordenação e persistência estável para a criação do ranking.

## 14. Escopo mínimo para a entrega final

Escopo mínimo:

> O jogo iniciará em uma tela de menu/boas-vindas onde o jogador digita seu nickname e inicia a partida. Posteriormente, será aberta a tela principal ambientada no espaço exibindo a nave e os asteroides movendo-se em sua direção. Na parte inferior da interface, haverá um painel HUD fixo contendo os dados em tempo real do jogador: pontos de vida atuais, pontuação de eliminação (score) e o nickname registrado, além da área para exibição de perguntas.

## 15. Possíveis melhorias, caso haja tempo

Melhorias possíveis:

- **Melhoria 1:** Inclusão de efeitos sonoros diversificados e trilha sonora de fundo;
- **Melhoria 2:** Sistema progressivo de aumento automático de dificuldade por ondas de tempo;
- **Melhoria 3:** Implementação de diferentes skins estéticas para a nave espacial do jogador;
- **Melhoria 4:** Variações nos efeitos sonoros e cores dos tiros lasers;
- **Melhoria 5:** Múltiplos planos de fundo ou cenários espaciais que mudam de acordo com o progresso;
- **Melhoria 6:** Diferentes modelos e texturas de sprites para os asteroides (variação por tamanho/peso).
