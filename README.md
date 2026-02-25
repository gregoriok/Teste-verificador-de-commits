# 🤖 AI PR QA Assistant

Uma automação que utiliza IA para melhorar a comunicação entre
**Desenvolvimento e QA** dentro de Pull Requests.

Ao abrir ou atualizar um PR, o workflow analisa as alterações e gera
automaticamente um comentário com:

-   ✅ Descrição mais clara e estruturada da mudança\
-   🧪 Sugestões de cenários de teste\
-   ⚠️ Possíveis riscos e regressões\
-   🔍 Pontos de atenção técnica

------------------------------------------------------------------------

## 🚀 Motivação

Em muitos times, a descrição do PR é superficial:

> "Ajustes"\
> "Correções"\
> "Refatoração"

Isso gera retrabalho, dúvidas e ruído na comunicação com QA.

Este projeto nasceu para reduzir essa fricção e melhorar a qualidade das
entregas.

------------------------------------------------------------------------

## 🏗️ Como funciona

1.  O desenvolvedor abre ou atualiza um Pull Request.
2.  O GitHub Actions é disparado.
3.  O script:
    -   Busca título, descrição e arquivos alterados via API do GitHub.
    -   Consolida os diffs.
    -   Envia para um modelo de IA.
4.  A IA retorna:
    -   Análise estruturada
    -   Sugestões de teste
    -   Riscos potenciais
5.  Um comentário é criado automaticamente no PR.

------------------------------------------------------------------------

## 🛠️ Tecnologias utilizadas

-   Python 3.11
-   GitHub Actions
-   GitHub REST API
-   Google Gemini API (ou outro modelo compatível)

------------------------------------------------------------------------

## ⚙️ Setup

### 1️⃣ Clone o repositório

``` bash
git clone https://github.com/gregoriok/Teste-verificador-de-commits.git
cd seurepo
```

------------------------------------------------------------------------

### 2️⃣ Instale dependências

``` bash
pip install requests python-dotenv google-genai
```

------------------------------------------------------------------------

### 3️⃣ Configure variáveis de ambiente

Crie um `.env`:

    GITHUB_TOKEN=seu_token
    GEMINI_KEY=sua_chave_api
    GITHUB_REPOSITORY=user/repo

Adicione `.env` ao `.gitignore`.

------------------------------------------------------------------------

### 4️⃣ Rodar localmente

Para testar com o último PR aberto:

``` bash
python scripts/analyzer.py
```

------------------------------------------------------------------------

## 🔐 Configuração no GitHub Actions

Adicione os secrets no repositório:

-   `GEMINI_KEY`

O `GITHUB_TOKEN` já é fornecido automaticamente pelo GitHub.

Certifique-se de adicionar permissões no workflow:

``` yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

------------------------------------------------------------------------

## 📌 Workflow exemplo

``` yaml
name: AI PR Analyzer

permissions:
  contents: read
  pull-requests: write
  issues: write

on:
  pull_request:
    types: [opened, edited, synchronize]
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install requests python-dotenv google-generativeai

      - name: Run AI analysis
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GEMINI_KEY: ${{ secrets.GEMINI_KEY }}
        run: python scripts/analyzer.py
```

------------------------------------------------------------------------

## 🎯 Próximos passos

-   Evitar comentários duplicados
-   Atualizar comentário existente em vez de criar novo
-   Comentar diretamente em linhas específicas do diff
-   Adicionar score de risco do PR
-   Transformar em GitHub App

------------------------------------------------------------------------
