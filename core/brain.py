
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

# ============================================================
# TECHNOCRACYSI — SUPER INTELLIGENCE SYSTEM
# ============================================================

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("technocracysi")

# ============================================================
# API GROQ — CONFIGURAÇÃO
# ============================================================
# CONFIGURE A CHAVE EM:
# 1. Streamlit Cloud: Settings > Secrets
# 2. Localmente: variável de ambiente GROQ_API_KEY
# 3. Opcionalmente: arquivo .env local
#
# Nunca publique sua chave no GitHub.

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1",
).strip()

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
).strip()

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
            max_retries=1,
        )
        logger.info("Cliente Groq inicializado.")
    except Exception:
        logger.exception("Falha ao inicializar cliente Groq.")
else:
    logger.error(
        "GROQ_API_KEY ausente. Configure a chave nos Secrets "
        "do Streamlit ou na variável de ambiente."
    )

# ============================================================
# IDENTIDADE DO SISTEMA
# ============================================================

SYSTEM_PROMPT = """
Você é a TechnocracySI.

SUPER INTELLIGENCE SYSTEM.

Analise cada solicitação de maneira profunda,
estruturada, crítica e rigorosa.

PRINCÍPIOS:
1. Diferencie fatos, hipóteses e inferências.
2. Avalie evidências e suas limitações.
3. Identifique contradições e falhas lógicas.
4. Considere explicações alternativas.
5. Não invente fatos, fontes ou resultados.
6. Declare incertezas quando necessário.
7. Priorize precisão, clareza e utilidade.

ARQUITETURA:
RESEARCH → ANALYSIS → CRITIC → SYNTHESIS

RESEARCH:
Identifique informações e evidências relevantes.

ANALYSIS:
Examine relações, padrões e explicações possíveis.

CRITIC:
Avalie inconsistências, premissas e alternativas.

SYNTHESIS:
Produza uma resposta final coerente e fundamentada.

Nome: TechnocracySI
Categoria: SUPER INTELLIGENCE SYSTEM

Não afirme ter realizado pesquisas externas,
executado ferramentas ou acessado dados que
não estejam realmente disponíveis.
"""

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def ask(prompt: str) -> str:
    if not isinstance(prompt, str) or not prompt.strip():
        return "Digite uma questão válida."

    if client is None:
        logger.error(
            "Cliente indisponível. Verifique GROQ_API_KEY."
        )
        return (
            "CONFIGURAÇÃO AUSENTE: configure GROQ_API_KEY "
            "nos Secrets do Streamlit ou no ambiente local."
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
            max_tokens=2048,
        )

        if not response.choices:
            logger.error("Resposta da API sem opções.")
            return "ERRO: a API não retornou nenhuma resposta."

        content = response.choices[0].message.content

        if not isinstance(content, str) or not content.strip():
            logger.error(
                "Resposta vazia. finish_reason=%s",
                response.choices[0].finish_reason,
            )
            return (
                "ERRO: a API retornou conteúdo vazio. "
                "Consulte os logs da aplicação."
            )

        logger.info("Resposta gerada com sucesso.")
        return content.strip()

    except Exception as exc:
        status = getattr(exc, "status_code", None)

        logger.exception(
            "Falha Groq | tipo=%s | HTTP=%s | detalhe=%s",
            type(exc).__name__,
            status if status is not None else "indisponível",
            str(exc),
        )

        status_text = (
            f"HTTP {status}"
            if status is not None
            else "sem código HTTP"
        )

        return (
            f"ERRO NA API: {type(exc).__name__} "
            f"({status_text}). Consulte os logs do Streamlit "
            "para ver o diagnóstico completo."
        )


# ============================================================
# TESTE LOCAL
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TECHNOCRACYSI")
    print("SUPER INTELLIGENCE SYSTEM")
    print("=" * 60)

    if client is None:
        print("Configure GROQ_API_KEY antes de executar.")
    else:
        print("Modelo:", GROQ_MODEL)
        print("Digite 'sair' para encerrar.")

        while True:
            try:
                prompt = input("\nVocê > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nEncerrado.")
                break

            if prompt.lower() in {"sair", "exit", "quit"}:
                break

            if prompt:
                print("\nTechnocracySI >")
                print(ask(prompt))
