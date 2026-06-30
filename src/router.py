import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from pydantic import BaseModel, Field
from typing_extensions import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

from prompts import triage_system_prompt, triage_user_prompt
from config import profile, prompt_instructions, email

load_dotenv()

MODEL = "google/gemini-2.5-flash"


class Router(BaseModel):
    """Analisa o e-mail não lido e o roteia de acordo com seu conteúdo."""
    reasoning: str = Field(
        description="Raciocínio passo a passo por trás da classificação."
    )
    classification: Literal["ignore", "respond", "notify"] = Field(
        description="A classificação do e-mail: ignore, notify ou respond."
    )


def criar_llm_router() -> ChatOpenAI:
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model=MODEL,
        temperature=0,
    )
    return llm.with_structured_output(Router)


def testar_roteador():
    llm_router = criar_llm_router()

    system_prompt = triage_system_prompt.format(
        full_name=profile["full_name"],
        name=profile["name"],
        examples="Nenhum",
        user_profile_background=profile["user_profile_background"],
        triage_no_prompt_instructions=prompt_instructions["triage_rules"]["ignore"],
        triage_notify_prompt_instructions=prompt_instructions["triage_rules"]["notify"],
        triage_email_prompt_instructions=prompt_instructions["triage_rules"]["respond"],
    )

    user_prompt = triage_user_prompt.format(
        author=email["from"],
        to=email["to"],
        subject=email["subject"],
        email_thread=email["body"],
    )

    result = llm_router.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])

    print("\n📧 RESULTADO DA TRIAGEM:")
    print(f"   Classificação : {result.classification.upper()}")
    print(f"   Raciocínio    : {result.reasoning}")

    return result


if __name__ == "__main__":
    testar_roteador()