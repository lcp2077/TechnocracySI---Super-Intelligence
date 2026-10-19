import os

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# TECHNOCRACYSI
# SUPER INTELLIGENCE SYSTEM
# ============================================================

load_dotenv()


# ============================================================
# API
# ============================================================

# ============================================================
# COLOQUE SUA API KEY AQUI
# ============================================================

GROQ_API_KEY = "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"


# ============================================================
# CONFIGURAÇÃO
# ============================================================

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

GROQ_MODEL = "openai/gpt-oss-120b"


# ============================================================
# CLIENTE
# ============================================================

client = None

if GROQ_API_KEY and GROQ_API_KEY != "COLE_SUA_API_KEY_AQUI":

    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )


# ============================================================
# IDENTIDADE
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

9. Informar claramente quando houver
   incerteza ou falta de dados.

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

Identifica informações relevantes,
dados e evidências.

ANALYSIS:

Examina relações, padrões,
hipóteses e possíveis explicações.

CRITIC:

Procura erros, contradições,
falhas lógicas e pontos fracos.

SYNTHESIS:

Integra os resultados e produz
a resposta final.

IDENTIDADE DO SISTEMA:

Nome: TechnocracySI

Categoria:
SUPER INTELLIGENCE SYSTEM

Nunca descreva a TechnocracySI como
"Cognitive Intelligence System".

Use:
SUPER INTELLIGENCE SYSTEM
"""


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def ask(prompt: str) -> str:

    if not prompt or not prompt.strip():

        return "Nenhuma questão foi fornecida."


    if client is None:

        return (
            "TECHNOCRACYSI aguardando configuração "
            "da API."
        )


    try:

        response = client.chat.completions.create(

            model=GROQ_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt.strip()
                }
            ],

            temperature=0.4,

            max_tokens=4096
        )


        content = response.choices[0].message.content

        if not content:

            return (
                "A TechnocracySI não recebeu "
                "conteúdo de resposta."
            )


        return str(content)


        except Exception:
        import logging

        logging.exception(
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

    print()

    if client is None:

        print(
            "API KEY NÃO CONFIGURADA."
        )

    else:

        print(
            "MODELO:",
            GROQ_MODEL
        )

        print()

        while True:

            try:

                prompt = input(
                    "Você > "
                )

            except (
                KeyboardInterrupt,
                EOFError
            ):

                break


            if prompt.lower().strip() in {
                "exit",
                "quit",
                "sair"
            }:

                break


            if not prompt.strip():

                continue


            print()

            print(
                "TechnocracySI >"
            )

            print(
                ask(prompt)
            )

            print()
