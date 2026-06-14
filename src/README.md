# Código-fonte (`src`)

Esta pasta contém os módulos principais do jogo.

---

## Arquivos

* **`jogo.py`**: Contém o loop principal do jogo, gerenciamento de eventos, atualização de estados e renderização dos painéis e telas.
* **`config.py`**: Centraliza as constantes globais do projeto, como dimensões da tela, paleta de cores, instâncias de fontes adaptadas e configurações de FPS.
* **`funcoes.py`**: Concentra as funções auxiliares e utilitárias de regra e lógica (como o sistema de quebra e renderização dinâmica de texto).
* **`sprites.py`**: Responsável pelas entidades visuais do jogo, gerenciando o comportamento e desenho das estrelas de fundo, da nave do jogador e dos asteroides mecânicos.
* **`dados.py`**: Cuida da persistência de dados, sendo responsável pela leitura e gravação do arquivo JSON que alimenta o banco de perguntas.
* **`audio.py`**: Gerencia toda a parte sonora do jogo. Utiliza síntese matemática (via numpy e pygame.mixer) para gerar dinamicamente os efeitos de lasers, explosões, acertos, erros e a trilha sonora de suspense, dispensando o uso de arquivos de áudio externos..
---

## Dica de evolução

> 💡 **Mantenha o código limpo:** Quando o projeto crescer, continue dividindo as responsabilidades em módulos pequenos e especializados. Isso facilita a manutenção, a caça a bugs e a implementação de novas mecânicas espaciais no futuro!