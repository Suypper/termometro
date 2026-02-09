# 🌡️ O Termômetro

Uma aplicação de linha de comando (CLI) robusta e amigável para consulta de dados climáticos em tempo real, construída com Python.

O sistema consome a API do OpenWeatherMap para fornecer informações precisas sobre temperatura, sensação térmica, umidade e condições do vento para qualquer cidade do mundo.

## ✨ Funcionalidades

-   **Consulta em Tempo Real**: Obtém dados atualizados diretamente da API OpenWeatherMap.
-   **Múltiplas Cidades**: Suporte para consultar várias cidades de uma só vez (ex: `London, Tokyo, Paris`).
-   **Sistema de Cache Inteligente**:
    -   Armazena resultados localmente por 5 minutos.
    -   Evita requisições desnecessárias à API e economiza sua quota.
    -   Indica visualmente quando o dado veio do cache (📦).
-   **Exportação Automática**:
    -   Cada consulta realizada com sucesso gera um arquivo JSON detalhado.
    -   Arquivos salvos automaticamente na pasta `exports/` para organização.
-   **Interface Rica**: Exibição formatada com emojis e unidades métricas (Celsius, m/s).
-   **Tratamento de Erros**: Mensagens amigáveis para cidades não encontradas ou problemas de conexão.

## 📋 Pré-requisitos

-   Python 3.11+
-   Conta gratuita no [OpenWeatherMap](https://openweathermap.org/api) para obter uma API Key.

## 🚀 Instalação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/o-termometro.git
    cd o-termometro
    ```

2.  Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Linux/Mac
    source venv/bin/activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure as variáveis de ambiente:
    ```bash
    # Copie o exemplo
    cp .env.example .env
    
    # Edite o arquivo .env e adicione sua API KEY do OpenWeatherMap
    ```

## 💻 Uso

Execute a aplicação via terminal:

```bash
python -m src.main
```

### Exemplo de Interação

```text
🌡️  O TERMÔMETRO - Consulta de Clima

Digite o nome da cidade (ou 'sair' para encerrar): London, Tokyo

========================================
🌡️  CLIMA EM LONDON
========================================
... (dados do clima) ...
💾 Dados salvos em: exports\clima_London_20240209_165026.json

========================================
🌡️  CLIMA EM TOKYO
========================================
... (dados do clima) ...
💾 Dados salvos em: exports\clima_Tokyo_20240209_165027.json
```

## kw Estrutura do Projeto

```
o-termometro/
├── exports/         # 📂 Arquivos JSON gerados (ignorados no git)
├── src/
│   ├── main.py      # Ponto de entrada e orquestração
│   ├── cliente.py   # Cliente API com implementação de Cache
│   ├── modelos.py   # Modelos de dados (Pydantic)
│   └── config.py    # Gerenciamento de configurações (.env)
├── tests/           # Testes automatizados
├── .env.example     # Modelo de variáveis de ambiente
├── .gitignore       # Arquivos ignorados pelo git
├── requirements.txt # Dependências do projeto
└── README.md        # Documentação
```

## 📚 Conceitos Praticados

-   [x] Classes e Orientação a Objetos (POO)
-   [x] Type Hints e validação estática
-   [x] **Pydantic** para validação e modelagem de dados
-   [x] Tratamento de exceções (Error Handling)
-   [x] Consumo de API REST (`requests`)
-   [x] **Caching** em memória (TTL)
-   [x] Manipulação de Arquivos (**File I/O** e JSON)
-   [x] Variáveis de ambiente (`python-dotenv`)
-   [x] Estrutura de projeto profissional

## 📝 Licença

MIT