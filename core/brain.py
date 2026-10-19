
import logging

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# TECHNOCRACYSI
# SUPER INTELLIGENCE SYSTEM
# ============================================================

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("technocracysi")


# ============================================================
# API GROQ
# ============================================================

GROQ_API_KEY = "COLE_SUA_API_KEY_GROQ_AQUI"

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

GROQ_MODEL = "openai/gpt-oss-120b"


# ============================================================
# CLIENTE
# ============================================================

client = None

if GROQ_API_KEY and GROQ_API_KEY != "COLE_SUA_API_KEY_GROQ_AQUI":
    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
            timeout=60.0,
            max_retries=2,
        )
        logger.info("Cliente Groq inicializado.")
    except Exception:
        logger.exception("Falha ao inicializar o cliente Groq.")
else:
    logger.error("Configure uma chave válida da API Groq.")


# ============================================================
# IDENTIDADE E ARQUITETURA COGNITIVA
# ============================================================

SYSTEM_PROMPT = """
Você é a TechnocracySI.

SUPER INTELLIGENCE SYSTEM.

Seu objetivo é analisar problemas de maneira
profunda, estruturada, crítica e rigorosa.

PRINCÍPIOS:

1. Diferencie fatos, hipóteses e inferências.
2. Avalie a qualidade das evidências.
3. Identifique contradições e inconsistências.
4. Considere explicações alternativas.
5. Questione premissas frágeis.
6. Não invente informações ou fontes.
7. Não apresente especulações como fatos.
8. Declare incertezas e limitações relevantes.
9. Priorize precisão, clareza e utilidade.
10. Adapte a profundidade ao problema apresentado.

ARQUITETURA DE ANÁLISE:

RESEARCH
Identifica informações, evidências e contexto.

ANALYSIS
Examina relações, padrões, hipóteses e explicações.

CRITIC
Avalia falhas lógicas, contradições e alternativas.

SYNTHESIS
Integra os resultados e produz uma resposta coerente.

IDENTIDADE:

Nome: TechnocracySI
Categoria: SUPER INTELLIGENCE SYSTEM

Nunca descreva a TechnocracySI como
"Cognitive Intelligence System".

Use a designação:
SUPER INTELLIGENCE SYSTEM.

Não afirme possuir ferramentas, capacidades,
memórias ou acessos que não estejam disponíveis.
"""


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def ask(prompt: str) -> str:
    if not isinstance(prompt, str) or not prompt.strip():
        return "Nenhuma questão foi fornecida."

    if client is None:
        logger.error(
            "Cliente indisponível. Verifique a chave da API Groq."
        )
        return (
            "TECHNOCRACYSI: cliente indisponível. "
            "Verifique a configuração da API."
        )

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt.strip(),
                },
            ],
            temperature=0.4,
            max_completion_tokens=4096,
        )

        if not response.choices:
            logger.error("A API retornou uma resposta sem opções.")
            return "A API não retornou uma resposta válida."

        content = response.choices[0].message.content

        if not isinstance(content, str) or not content.strip():
            logger.error("A API retornou conteúdo vazio.")
            return "A API retornou uma resposta vazia."

        return content.strip()

    except Exception as exc:
        logger.exception(
            "Erro na solicitação Groq: %s: %s",
            type(exc).__name__,
            str(exc),
        )
        return (
            "TECHNOCRACYSI encontrou um erro na solicitação. "
            "Consulte os logs da aplicação para identificar "
            "a causa exata."
        )


# ============================================================
# TESTE LOCAL
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TECHNOCRACYSI")
    print("SUPER INTELLIGENCE SYSTEM")
    print("=" * 70)

    if client is None:
        print("ERRO: configure uma chave válida da API Groq.")
    else:
        print("Modelo:", GROQ_MODEL)
        print("Digite 'sair' para encerrar.")

        while True:
            try:
                prompt = input("\nVocê > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nEncerrado.")
                break

            if prompt.lower() in {"exit", "quit", "sair"}:
                break

            if not prompt:
                continue

            print("\nTechnocracySI >")
            print(ask(prompt))
