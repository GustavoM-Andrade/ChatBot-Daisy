# Design — Chatbot DAISY

Documento de design do projeto **DAISY**, uma assistente virtual bem-humorada
para tarefas simples do dia a dia. Este documento descreve a arquitetura, as
rotas, o fluxo de dados e as decisões técnicas, sempre em conformidade com a
steering do projeto (`.kiro/steering/chatbot.md`).

## 1. Visão geral

A DAISY é uma aplicação web mínima e didática: um servidor Flask serve uma
página de chat e repassa as mensagens do usuário ao Amazon Bedrock, devolvendo
a resposta gerada pelo modelo. A personalidade e os limites do bot vivem em um
único `SYSTEM_PROMPT` no backend.

Princípios de design:

- **Mínimo e didático:** poucos arquivos, código simples e comentado em português.
- **Sem persistência:** nenhuma sessão, banco de dados ou histórico no servidor.
- **Segurança de credenciais:** chaves AWS vêm apenas de variáveis de ambiente.

## 2. Stack técnica

| Camada            | Tecnologia                                             |
|-------------------|--------------------------------------------------------|
| Backend           | Python + Flask                                         |
| Frontend          | HTML + CSS + JavaScript puro (um arquivo)              |
| IA / LLM          | Amazon Bedrock via `boto3` (`bedrock-runtime`)         |
| Model ID          | `us.anthropic.claude-haiku-4-5-20251001-v1:0`          |
| Região AWS        | `us-east-1`                                            |
| Execução          | `python app.py` em `localhost:5000`                    |

Dependências (`requirements.txt`): `flask`, `boto3`.

## 3. Estrutura de arquivos

```
meu-chatbot/
├── app.py              # Servidor Flask + integração com o Bedrock
├── requirements.txt    # flask, boto3
└── templates/
    └── index.html      # Página de chat (HTML, CSS e JS)
```

## 4. Arquitetura e fluxo de dados

```
┌───────────────┐    POST /chat               ┌──────────────┐    invoke_model     ┌─────────────────┐
│   Navegador   │  {"message": "..."}         │    Flask     │  ─────────────────▶ │  Amazon Bedrock │
│ (index.html)  │ ──────────────────────────▶ │   (app.py)   │                     │   Claude Haiku  │
│               │ ◀────────────────────────── │              │ ◀───────────────────│      4.5        │
└───────────────┘    {"reply": "..."}         └──────────────┘    texto gerado     └─────────────────┘
```

Passo a passo:

1. O usuário acessa `GET /` e recebe a página de chat (`templates/index.html`).
2. Ao enviar uma mensagem, o JavaScript faz `POST /chat` com `{"message": "..."}`.
3. O Flask valida a mensagem e monta o corpo da requisição para o Bedrock,
   incluindo o `SYSTEM_PROMPT` (personalidade da DAISY) e a mensagem do usuário.
4. O Bedrock responde com o texto gerado.
5. O Flask devolve `{"reply": "..."}` e o frontend exibe a resposta no chat.

## 5. Rotas (contrato da API)

### `GET /`

- **Função:** exibe a página de chat.
- **Resposta:** HTML renderizado de `templates/index.html`.

### `POST /chat`

- **Função:** recebe a mensagem do usuário e devolve a resposta da DAISY.
- **Request body (JSON):**

  ```json
  { "message": "texto do usuário" }
  ```

- **Resposta de sucesso — 200 OK:**

  ```json
  { "reply": "resposta gerada pela DAISY" }
  ```

- **Mensagem vazia — 400 Bad Request:**

  ```json
  { "error": "A mensagem não pode estar vazia." }
  ```

  A mensagem é considerada vazia quando ausente ou composta apenas de espaços
  (após `strip()`).

- **Falha no Bedrock — 500 Internal Server Error:**

  ```json
  { "error": "Ops, deu ruim aqui: <detalhe>" }
  ```

> Observação: `app.json.ensure_ascii = False` garante que os acentos apareçam
> legíveis no JSON de resposta.

## 6. Integração com o Amazon Bedrock

- Cliente criado com `boto3.client("bedrock-runtime", region_name="us-east-1")`.
- Chamada via `invoke_model` usando o Model ID (perfil de inferência) exato:
  `us.anthropic.claude-haiku-4-5-20251001-v1:0`.
- Corpo da requisição no formato da API Messages da Anthropic no Bedrock:

  ```json
  {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "system": "<SYSTEM_PROMPT da DAISY>",
    "messages": [
      { "role": "user", "content": "<mensagem do usuário>" }
    ]
  }
  ```

- A resposta é lida de `response["body"]` (stream de bytes com JSON) e o texto é
  extraído de `content[0]["text"]`.

### Credenciais

As credenciais AWS (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e região) são
fornecidas **exclusivamente por variáveis de ambiente**. Nenhuma chave é escrita
no código-fonte.

## 7. Personalidade (SYSTEM_PROMPT)

A identidade, o tom de voz e os limites da DAISY ficam concentrados na constante
`SYSTEM_PROMPT` dentro de `app.py`. Em resumo, o prompt define:

- **Identidade:** assistente bem-humorada, prática e levemente sarcástica.
- **Domínio:** tarefas simples do cotidiano (rotinas, listas, horários, refeições,
  textos, cálculos básicos, conversões, ideias criativas).
- **Limites:** não atua como especialista médico, jurídico ou financeiro; não
  inventa informações; explica limitações com naturalidade.
- **Tom:** humor leve sem ridicularizar, empatia em situações delicadas, respostas
  objetivas e organizadas em listas/etapas quando fizer sentido.
- **Regras:** responder em português brasileiro, evitar perguntas desnecessárias,
  nunca afirmar ter executado ações externas que não pode realizar.

## 8. Frontend (`templates/index.html`)

- Página única com HTML, CSS e JavaScript embutidos.
- Exibe mensagens do usuário e da DAISY em balões distintos.
- Mostra um indicador de "pensando" enquanto aguarda a resposta.
- Faz `fetch("/chat")` com `POST` e trata os casos de sucesso e de erro
  (400/500 e falha de rede), exibindo uma mensagem amigável.

## 9. Tratamento de erros

| Situação                     | Status | Comportamento                                  |
|------------------------------|--------|------------------------------------------------|
| Mensagem vazia               | 400    | Retorna `{"error": "..."}` sem chamar o Bedrock |
| Falha ao invocar o Bedrock   | 500    | Captura a exceção e retorna `{"error": "..."}`  |
| Falha de rede (frontend)     | —      | Exibe mensagem amigável no chat                 |

## 10. Execução local

```bash
pip install -r requirements.txt

export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1

python app.py
```

Acesse `http://localhost:5000`.

## 11. Fora de escopo (conforme a steering)

- Não usar FastAPI, Django, banco de dados, LangChain, RAG, autenticação ou login.
- Não criar testes automatizados.
- Não usar OpenAI nem outras APIs de IA além do Bedrock.
