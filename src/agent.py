import os
from dotenv import load_dotenv

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(_ROOT, '.env'))

import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

from tools import TOOLS
from prompts import agent_system_prompt, agent_system_prompt_memory
from config import profile, prompt_instructions
from memory import manage_memory_tool, search_memory_tool, store

MODEL = "google/gemini-2.5-flash"


def create_prompt(state: dict) -> list:
    """Prompt básico sem memória."""
    system = agent_system_prompt.format(
        instructions=prompt_instructions["agent_instructions"],
        **profile,
    )
    return [SystemMessage(content=system)] + state["messages"]


def create_prompt_with_memory(state: dict) -> list:
    """Prompt aprimorado com instruções de uso de memória."""
    system = agent_system_prompt_memory.format(
        instructions=prompt_instructions["agent_instructions"],
        **profile,
    )
    return [SystemMessage(content=system)] + state["messages"]


def criar_agente():
    """Agente básico sem memória."""
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model=MODEL,
        temperature=0,
    )
    return create_react_agent(
        model=llm,
        tools=TOOLS,
        prompt=create_prompt,
    )


def criar_agente_com_memoria():
    """Agente aprimorado com ferramentas de memória semântica."""
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model=MODEL,
        temperature=0,
    )

    tools_com_memoria = TOOLS + [manage_memory_tool, search_memory_tool]

    return create_react_agent(
        model=llm,
        tools=tools_com_memoria,
        prompt=create_prompt_with_memory,
        store=store,
    )