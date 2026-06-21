# Testes Automatizados — CosmoMind

Esta pasta contém a suíte de testes automatizados do projeto **CosmoMind**. Os testes foram reestruturados de forma modular para garantir a integridade das mecânicas, regras de persistência de dados e renderização de componentes de interface sem a necessidade de inicializar janelas gráficas (modo *headless*).

---

## 📂 Estrutura de Arquivos de Teste

A suíte é composta por **8 testes automatizados** distribuídos em três módulos especializados:

* **`test_logica.py` (3 testes)**: Valida as funções puras de manipulação de strings e cálculo de dimensões textuais do módulo `src/funcoes.py`. Garante o comportamento correto do algoritmo de quebra de linhas para perguntas longas.
* **`test_dados.py` (4 testes)**: Valida os mecanismos de persistência do sistema (`src/dados.py`), incluindo carregamento de recordes, salvamento condicional de pontuações máximas, higienização de nomes e o limite/ordenação do Top 10 do Ranking JSON.
* **`test_sprites.py` (1 teste)**: Valida as regras físicas de atualização de entidades espaciais de `src/sprites.py`, assegurando que o loop infinito do cenário (reset das estrelas de fundo ao ultrapassarem o limite da tela) funcione matematicamente.

---

## 🚀 Como Executar os Testes

O projeto utiliza o **`pytest`** como motor de execução devido à sua capacidade de *Test Discovery* (descoberta automática de arquivos e métodos iniciados com o prefixo `test_`).

### 1. Pré-requisitos (Instalação do Pytest)
Antes de rodar o comando, é necessário garantir que o `pytest` está instalado no ambiente. Escolha o comando de acordo com o seu sistema operacional:

* **No Windows (Prompt de Comando / PowerShell) ou Ambientes Virtuais (venv):**
  ```cmd
  pip install pytest