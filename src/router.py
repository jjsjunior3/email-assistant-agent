import os
import re
import json
from dotenv import load_dotenv

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(_ROOT, '.env'))

import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from pydantic import BaseModel, Field
from typing_extensions import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

MODEL = "google/gemini-2.5-flash"


class Router(BaseModel):
    reasoning: str = Field(description="Raciocínio por trás da classificação.")
    classification: Literal["ignore", "respond", "notify"] = Field(
        description="Classificação do e-mail."
    )


def criar_llm_router():
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model=MODEL,
        temperature=0,
    )
    return llm.with_structured_output(Router)


def classificar_email(messages: list) -> Router:
    """Classifica com retry e fallback para JSON truncado."""

    # Tentativa 1: with_structured_output
    try:
        llm_router = criar_llm_router()
        return llm_router.invoke(messages)
    except Exception:
        pass

    # Tentativa 2: JSON manual via regex
    try:
        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model=MODEL,
            temperature=0,
        )
        fallback_messages = messages + [
            HumanMessage(content='Responda APENAS com JSON válido: {"reasoning": "...", "classification": "ignore|notify|respond"}')
        ]
        response = llm.invoke(fallback_messages)
        texto = response.content
        match = re.search(r'\{.*\}', texto, re.DOTALL)
        if match:
            dados = json.loads(match.group())
            return Router(
                reasoning=dados.get("reasoning", "fallback"),
                classification=dados.get("classification", "ignore")
            )
    except Exception:
        pass

    # Tentativa 3: padrão seguro
    return Router(reasoning="Erro na classificação", classification="ignore")