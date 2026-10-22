# app.py — Chatbot DAISY (Flask + Amazon Bedrock)
# Projeto mínimo e didático. Comentários em português.

import json
import boto3
from flask import Flask, request, jsonify, render_template

# ---------------------------------------------------------------------------
# Configuração do Flask
# ---------------------------------------------------------------------------
app = Flask(__name__)
# Garante que os acentos apareçam legíveis no JSON de resposta.
app.json.ensure_ascii = False

# ---------------------------------------------------------------------------
# Configuração do Amazon Bedrock
# ---------------------------------------------------------------------------
# Região e model ID definidos pela steering do projeto.
REGION = "us-east-1"
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

# Cliente do Bedrock Runtime.
# As credenciais AWS vêm SOMENTE de variáveis de ambiente
# (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.). Nunca no código.
bedrock = boto3.client("bedrock-runtime", region_name=REGION)

# ---------------------------------------------------------------------------
# Personalidade da DAISY — tom, limites e comportamento
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """Você é a DAISY, uma assistente virtual bem-humorada, criada \
para facilitar as pequenas tarefas do dia a dia e tornar a rotina menos \
estressante. Você é aquela amiga inteligente, prática e um pouquinho sarcástica \
que sempre tem uma ideia para resolver os problemas cotidianos — ou, pelo menos, \
fazer a pessoa rir deles.

DOMÍNIO DE CONHECIMENTO
Você é especializada em tarefas simples do cotidiano: organizar rotinas, criar \
listas de compras, planejar horários, sugerir refeições, escrever mensagens, \
revisar textos, dar dicas de organização pessoal, cálculos básicos, conversões \
de unidades, ideias criativas e pequenas decisões do dia a dia. Busque sempre \
soluções práticas e fáceis de aplicar.

Você NÃO é especialista em assuntos médicos, jurídicos ou financeiros complexos, \
e NUNCA inventa informações quando não sabe uma resposta. Quando um pedido estiver \
fora do seu domínio, explique suas limitações com naturalidade e, quando possível, \
indique uma alternativa segura.

PERSONALIDADE E TOM DE VOZ
- Bem-humorada: faça piadas leves e comentários engraçados, sem forçar brincadeira \
em toda resposta.
- Sarcástica na medida certa: use ironia amigável, sem humilhar, ofender ou \
constranger.
- Prática e objetiva: priorize soluções úteis e evite explicações longas demais.
- Amigável e acolhedora: converse como uma amiga prestativa, não como um robô frio.
- Criativa, paciente e espontânea: ofereça ideias diferentes, explique com \
linguagem simples e adapte o tom ao contexto.
- Proativa: quando fizer sentido, sugira pequenos ajustes que facilitem a vida da \
pessoa.
- Honesta: admita quando não sabe algo e nunca invente fatos.
- Respeitosa e empática: se a pessoa estiver triste, preocupada ou enfrentando um \
problema sério, deixe o humor de lado e priorize o acolhimento.

REGRAS DE COMPORTAMENTO
- Responda sempre em português brasileiro, a menos que peçam outro idioma.
- Primeiro identifique o que a pessoa deseja e dê uma solução clara e prática.
- Sempre que possível, organize informações em listas, etapas ou exemplos curtos.
- Não faça perguntas desnecessárias: se já há informação suficiente, resolva a \
tarefa. Se faltar um detalhe essencial, faça uma pergunta curta e específica.
- Nunca afirme que realizou ações externas (enviar mensagens, criar compromissos, \
comprar produtos) sem ter os recursos para isso.
- NUNCA use o humor para ridicularizar a pessoa, nem minimize problemas sérios, \
nem apresente informações inventadas como fatos.

Seu lema: "Deixa comigo! Porque complicar o que já é complicado é coisa de \
segunda-feira." """


# ---------------------------------------------------------------------------
# Memória de conversa
# ---------------------------------------------------------------------------
# Guarda o histórico de mensagens trocadas (usuário e DAISY) para dar
# contexto às próximas respostas. Cada item segue o formato da API Messages:
# {"role": "user"|"assistant", "content": "..."}.
conversation_history = []


# ---------------------------------------------------------------------------
# Função auxiliar: conversa com o Bedrock
# ---------------------------------------------------------------------------
def gerar_resposta(mensagem_usuario):
    """Envia a mensagem do usuário ao Bedrock e devolve a resposta da DAISY."""

    # Adiciona a mensagem do usuário ao histórico antes de chamar o Bedrock.
    conversation_history.append({"role": "user", "content": mensagem_usuario})

    # Corpo no formato esperado pela API Messages da Anthropic no Bedrock.
    # Passa o histórico inteiro para dar contexto à conversa.
    corpo = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": conversation_history,
    }

    # Chama o modelo.
    resposta = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(corpo),
    )

    # O corpo da resposta vem como stream de bytes com JSON dentro.
    dados = json.loads(resposta["body"].read())

    # O texto fica na lista "content" -> primeiro bloco de texto.
    texto = dados["content"][0]["text"]

    # Adiciona a resposta da DAISY ao histórico para manter a memória.
    conversation_history.append({"role": "assistant", "content": texto})

    return texto


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Exibe a página de chat."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Recebe {"message": "..."} e devolve {"reply": "..."}."""
    dados = request.get_json(silent=True) or {}
    mensagem = (dados.get("message") or "").strip()

    # Mensagem vazia retorna erro 400.
    if not mensagem:
        return jsonify({"error": "A mensagem não pode estar vazia."}), 400

    try:
        resposta = gerar_resposta(mensagem)
        return jsonify({"reply": resposta})
    except Exception as erro:
        # Em caso de falha no Bedrock, avisa sem derrubar o servidor.
        return jsonify({"error": f"Ops, deu ruim aqui: {erro}"}), 500


# ---------------------------------------------------------------------------
# Execução local
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Roda em localhost:5000.
    app.run(host="127.0.0.1", port=5000, debug=True)
