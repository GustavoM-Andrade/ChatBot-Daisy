# Requisitos — Chatbot DAISY

## Introdução

A DAISY é uma assistente virtual bem-humorada, criada para facilitar pequenas
tarefas do dia a dia. Este documento descreve os requisitos de uma aplicação web
mínima e didática que serve uma página de chat e gera respostas com o Amazon
Bedrock, em conformidade com a steering do projeto
(`.kiro/steering/chatbot.md`).

## Requisitos

### Requisito 1 — Servir a página de chat

**User Story:** Como usuário, quero abrir a aplicação no navegador e ver uma
página de chat, para poder conversar com a DAISY.

#### Critérios de Aceitação

1. QUANDO o usuário acessar a rota `GET /` ENTÃO o sistema DEVE responder com
   status 200 e a página `templates/index.html`.
2. QUANDO a página carregar ENTÃO o sistema DEVE exibir uma área de conversa e um
   campo para digitar mensagens.

### Requisito 2 — Enviar mensagem e receber resposta

**User Story:** Como usuário, quero enviar uma mensagem e receber a resposta da
DAISY, para resolver minhas tarefas do dia a dia.

#### Critérios de Aceitação

1. QUANDO o usuário enviar `POST /chat` com corpo `{"message": "..."}` válido
   ENTÃO o sistema DEVE responder com status 200 e corpo `{"reply": "..."}`.
2. QUANDO o sistema gerar a resposta ENTÃO ele DEVE usar o Amazon Bedrock
   (`bedrock-runtime`, `invoke_model`) na região `us-east-1` com o Model ID
   `us.anthropic.claude-haiku-4-5-20251001-v1:0`.
3. QUANDO a resposta JSON contiver acentos ENTÃO o sistema DEVE retorná-los
   legíveis (`app.json.ensure_ascii = False`).

### Requisito 3 — Validação de mensagem vazia

**User Story:** Como usuário, quero um retorno claro quando enviar uma mensagem
vazia, para entender que preciso digitar algo.

#### Critérios de Aceitação

1. QUANDO o usuário enviar `POST /chat` com `message` vazio ou ausente ENTÃO o
   sistema DEVE responder com status 400.
2. QUANDO a mensagem contiver apenas espaços em branco ENTÃO o sistema DEVE
   tratá-la como vazia e responder com status 400.
3. QUANDO ocorrer o erro 400 ENTÃO o sistema DEVE retornar um corpo JSON com uma
   mensagem de erro e NÃO DEVE chamar o Amazon Bedrock.

### Requisito 4 — Tratamento de falhas na geração

**User Story:** Como usuário, quero que o chat não quebre quando houver um
problema no servidor de IA, para continuar usando a aplicação.

#### Critérios de Aceitação

1. QUANDO a chamada ao Amazon Bedrock falhar ENTÃO o sistema DEVE responder com
   status 500 e um corpo JSON com mensagem de erro amigável.
2. QUANDO ocorrer uma falha de rede no frontend ENTÃO a interface DEVE exibir uma
   mensagem amigável sem travar a página.

### Requisito 5 — Personalidade e tom da DAISY

**User Story:** Como usuário, quero que a DAISY responda com um tom prático e
bem-humorado, para que a conversa seja leve e útil.

#### Critérios de Aceitação

1. O sistema DEVE concentrar a identidade, o tom de voz e os limites da DAISY em
   uma constante `SYSTEM_PROMPT` no `app.py`.
2. QUANDO a DAISY responder ENTÃO ela DEVE usar português brasileiro por padrão.
3. QUANDO um pedido estiver fora do domínio (assuntos médicos, jurídicos ou
   financeiros complexos) ENTÃO a DAISY DEVE explicar suas limitações e NÃO DEVE
   inventar informações.

### Requisito 6 — Segurança de credenciais

**User Story:** Como mantenedor do projeto, quero que as credenciais AWS nunca
fiquem no código, para proteger as chaves de acesso.

#### Critérios de Aceitação

1. O sistema DEVE obter as credenciais AWS exclusivamente de variáveis de
   ambiente.
2. O sistema NÃO DEVE conter chaves de acesso escritas no código-fonte.

### Requisito 7 — Stack e restrições do projeto

**User Story:** Como mantenedor, quero que o projeto permaneça mínimo e didático,
para facilitar o aprendizado e a manutenção.

#### Critérios de Aceitação

1. O sistema DEVE usar Python com Flask, com `app.py` na raiz e a página em
   `templates/index.html`.
2. O sistema DEVE declarar as dependências `flask` e `boto3` em
   `requirements.txt` e rodar com `python app.py` em `localhost:5000`.
3. O sistema NÃO DEVE usar FastAPI, Django, banco de dados, LangChain, RAG,
   autenticação, login, testes automatizados, nem OpenAI ou outras APIs de IA
   além do Bedrock.
