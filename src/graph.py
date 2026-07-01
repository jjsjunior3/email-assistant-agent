import os
from dotenv import load_dotenv
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(_ROOT, '.env'))

import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from typing_extensions import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage

from prompts import triage_system_prompt, triage_user_prompt
from config import profile, prompt_instructions
from router import Router, classificar_email
from agent import criar_agente, criar_agente_com_memoria


class State(TypedDict):
    email_input: dict
    messages: Annotated[list, add_messages]


def triage_router(state: State) -> Command[Literal["response_agent", "__end__"]]:
    email = state["email_input"]

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
        author=email["author"],
        to=email["to"],
        subject=email["subject"],
        email_thread=email["email_thread"],
    )

    result = classificar_email([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    
    print(f"\n📊 Classificação: {result.classification.upper()}")
    print(f"   Raciocínio: {result.reasoning[:150]}...")

    if result.classification == "respond":
        print("✍️  Encaminhando para agente de resposta...")
        return Command(
            goto="response_agent",
            update={"messages": [HumanMessage(
                content=f"Responda ao seguinte e-mail:\n\n{email}"
            )]}
        )
    elif result.classification == "ignore":
        print("🗑️  Email ignorado.")
        return Command(goto=END, update=None)
    elif result.classification == "notify":
        print("🔔 Email marcado para notificação.")
        return Command(goto=END, update=None)
    else:
        raise ValueError(f"Classificação inválida: {result.classification}")


def build_email_graph(use_memory: bool = False):
    """
    use_memory=False → agente básico
    use_memory=True  → agente com memória semântica
    """
    agent = criar_agente_com_memoria() if use_memory else criar_agente()

    builder = StateGraph(State)
    builder.add_node("triage_router", triage_router)
    builder.add_node("response_agent", agent)
    builder.add_edge(START, "triage_router")

    return builder.compile()