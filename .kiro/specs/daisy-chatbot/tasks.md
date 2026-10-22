# Tarefas — Chatbot DAISY

Plano de implementação da DAISY, seguindo a steering do projeto
(`.kiro/steering/chatbot.md`) e o `design.md`. Sem testes automatizados e sem
tarefas opcionais.

- [x] 1. Criar a estrutura base do projeto
  - Criar a pasta `meu-chatbot/` com `app.py` na raiz e a pasta `templates/`.
  - Criar o `requirements.txt` com as dependências `flask` e `boto3`.

- [x] 2. Configurar o aplicativo Flask
  - Inicializar o Flask em `app.py`.
  - Definir `app.json.ensure_ascii = False` para acentos legíveis no JSON.

- [x] 3. Definir a personalidade da DAISY (SYSTEM_PROMPT)
  - Criar a constante `SYSTEM_PROMPT` com identidade, tom de voz, domínio e
    limites da DAISY, conforme a steering.

- [x] 4. Configurar o cliente do Amazon Bedrock
  - Criar o cliente `boto3.client("bedrock-runtime", region_name="us-east-1")`.
  - Definir o Model ID exato `us.anthropic.claude-haiku-4-5-20251001-v1:0`.
  - Garantir que as credenciais AWS venham apenas de variáveis de ambiente.

- [x] 5. Implementar a função de geração de resposta
  - Montar o corpo no formato da API Messages da Anthropic (`anthropic_version`,
    `max_tokens`, `system`, `messages`).
  - Chamar `invoke_model` e extrair o texto de `content[0]["text"]`.

- [x] 6. Implementar a rota `GET /`
  - Renderizar e servir a página `templates/index.html`.

- [x] 7. Implementar a rota `POST /chat`
  - Ler `{"message": "..."}` do corpo da requisição.
  - Retornar erro 400 quando a mensagem estiver vazia.
  - Chamar a função de geração e retornar `{"reply": "..."}`.
  - Tratar falhas do Bedrock retornando erro 500 com mensagem amigável.

- [x] 8. Criar a página de chat `templates/index.html`
  - Montar o HTML com área de conversa e formulário de envio.
  - Adicionar o CSS simples para os balões de mensagem e layout.

- [x] 9. Implementar o JavaScript do frontend
  - Enviar a mensagem via `fetch("/chat")` com `POST` e JSON.
  - Exibir mensagens do usuário e da DAISY e um indicador de "pensando".
  - Tratar respostas de erro (400/500) e falha de rede com mensagem amigável.

- [x] 10. Validar a execução local
  - Rodar com `python app.py` em `localhost:5000`.
  - Conferir manualmente o fluxo: abrir `/`, enviar mensagem e receber resposta.
