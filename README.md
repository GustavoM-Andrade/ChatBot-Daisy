# 🌼 DAISY — sua assistente virtual

A **DAISY** é uma assistente virtual bem-humorada, criada para facilitar as
pequenas tarefas do dia a dia: organizar rotinas, montar listas de compras,
planejar horários, sugerir refeições, revisar textos, fazer cálculos básicos e
dar aquela mãozinha com decisões cotidianas — sempre com um tom prático e leve.

> **Lema da DAISY:** "Deixa comigo! Porque complicar o que já é complicado é
> coisa de segunda-feira."

Projeto mínimo e didático: um chatbot web feito com **Flask** que gera respostas
usando o **Amazon Bedrock** (Claude Haiku 4.5).

## ✨ Funcionalidades

- Página de chat com tema escuro futurista (dourado + vermelho neon).
- Respostas geradas pelo Amazon Bedrock via `boto3`.
- Memória de conversa: a DAISY lembra do contexto da conversa atual.
- Personalidade e limites concentrados em um `SYSTEM_PROMPT`.

## 🧱 Stack

- **Python + Flask** (backend e rotas)
- **HTML + CSS + JavaScript** puro (frontend em um único arquivo)
- **Amazon Bedrock** via `boto3` (`bedrock-runtime`, `invoke_model`)
- **Model ID:** `us.anthropic.claude-haiku-4-5-20251001-v1:0`
- **Região:** `us-east-1`

## 📁 Estrutura do projeto

```
meu-chatbot/
├── app.py              # Servidor Flask: rotas / e /chat e chamada ao Bedrock
├── requirements.txt    # Dependências (flask, boto3)
├── templates/
│   └── index.html      # Página de chat
└── .kiro/              # Steering e spec do projeto
```

## ✅ Pré-requisitos

- Python 3.9 ou superior.
- Uma conta AWS com acesso ao modelo **Claude Haiku 4.5** habilitado no Amazon
  Bedrock (console: *Bedrock → Model access*, região `us-east-1`).
- Credenciais AWS válidas (chave de acesso e chave secreta).

## 🚀 Como rodar

1. (Opcional, recomendado) Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux / macOS
   # .venv\Scripts\activate       # Windows
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure as credenciais AWS **por variáveis de ambiente** (nunca no código):

   ```bash
   export AWS_ACCESS_KEY_ID=sua-chave
   export AWS_SECRET_ACCESS_KEY=sua-chave-secreta
   export AWS_DEFAULT_REGION=us-east-1
   ```

4. Rode o servidor:

   ```bash
   python app.py
   ```

5. Abra no navegador: <http://localhost:5000>

## 🔌 API

### `GET /`

Exibe a página de chat (`templates/index.html`).

### `POST /chat`

Recebe uma mensagem e devolve a resposta da DAISY.

**Requisição:**

```json
{ "message": "Me ajuda a montar uma lista de compras?" }
```

**Resposta (200):**

```json
{ "reply": "Claro! Aqui vai uma lista básica e prática..." }
```

**Mensagem vazia (400):**

```json
{ "error": "A mensagem não pode estar vazia." }
```

**Falha ao gerar a resposta (500):**

```json
{ "error": "Ops, deu ruim aqui: ..." }
```

## 🔒 Segurança

As credenciais AWS vêm **exclusivamente de variáveis de ambiente** e nunca são
escritas no código. O arquivo `.gitignore` já ignora `.env` e afins para evitar
o versionamento acidental de segredos.

## 📝 Notas

- A memória de conversa (`conversation_history`) é global e vive enquanto o
  servidor estiver rodando — é reiniciada a cada restart e compartilhada na
  instância. Adequado para uso local e didático.
- Projeto propositalmente simples: sem banco de dados, autenticação, testes
  automatizados ou frameworks adicionais.
