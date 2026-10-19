import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# TECHNOCRACYSI
# SUPER INTELLIGENCE SYSTEM
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

load_dotenv(ROOT / ".env")


# ============================================================
# CONFIGURAÇÃO DA API GROQ
# ============================================================

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
).strip()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
).strip()


# ============================================================
# LOGS
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger("technocracysi")


# ============================================================
# CLIENTE
# ============================================================

client = None

if GROQ_API_KEY:
    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
            timeout=60.0,
            max_retries=2,
        )
    except Exception:
        logger.exception("Falha ao inicializar o cliente da API")
else:
    logger.warning("GROQ_API_KEY não configurada")


# ============================================================
# IDENTIDADE DO SISTEMA
# ============================================================

SYSTEM_PROMPT = """
Você é a TechnocracySI.

SUPER INTELLIGENCE SYSTEM.

Seu objetivo é analisar problemas de maneira
profunda, estruturada e rigorosa.

Você deve:

1. Diferenciar fatos de hipóteses.
2. Diferenciar evidências de inferências.
3. Identificar contradições.
4. Procurar explicações alternativas.
5. Questionar premissas frágeis.
6. Não inventar informações.
7. Não inventar fontes.
8. Não inventar acontecimentos.
9. Informar claramente quando houver incerteza
   ou falta de dados.
10. Priorizar precisão sobre confiança aparente.

ARQUITETURA:

RESEARCH
↓
ANALYSIS
↓
CRITIC
↓
SYNTHESIS

RESEARCH:
Identifica informações relevantes, dados e evidências.

ANALYSIS:
Examina relações, padrões, hipóteses e explicações.

CRITIC:
Procura erros, contradições, falhas lógicas e limitações.

SYNTHESIS:
Integra os resultados e produz a resposta final.

IDENTIDADE:

Nome: TechnocracySI
Categoria: SUPER INTELLIGENCE SYSTEM

Nunca descreva a TechnocracySI como
"Cognitive Intelligence System".
"""


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def ask(prompt: str) -> str:

    if not isinstance(prompt, str) or not prompt.strip():
        return "Nenhuma questão foi fornecida."

    if client is None:
        logger.error(
            "Solicitação recusada: cliente indisponível. "
            "Verifique a configuração da chave da API."
        )
        return (
            "TECHNOCRACYSI encontrou um problema "
            "ao processar a solicitação."
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
            max_tokens=4096,
        )

        if not response.choices:
            logger.error("A API retornou uma resposta sem opções.")
            return (
                "TECHNOCRACYSI encontrou um problema "
                "ao processar a solicitação."
            )

        content = response.choices[0].message.content

        if not content or not content.strip():
            logger.warning("A API retornou conteúdo vazio.")
            return (
                "TECHNOCRACYSI encontrou um problema "
                "ao processar a solicitação."
            )

        return content.strip()

    except Exception:
        logger.exception(
            "Erro real ao consultar a API da TechnocracySI"
        )
        return (
            "TECHNOCRACYSI encontrou um problema "
            "ao processar a solicitação."
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
        print(
            "\nAPI não configurada. Configure GROQ_API_KEY "
            "no arquivo .env."
        )
    else:
        print(f"\nModelo configurado: {GROQ_MODEL}")
        print("Digite 'sair' para encerrar.\n")

        while True:
            try:
                prompt = input("Você > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nEncerrando.")
                break

            if prompt.lower() in {"exit", "quit", "sair"}:
                break

            if not prompt:
                continue

            print("\nTechnocracySI >")
            print(ask(prompt))
            print()
