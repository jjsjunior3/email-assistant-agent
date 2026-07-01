import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from langchain_core.messages import ToolMessage
from graph import build_email_graph
from hitl import human_in_the_loop_schedule

# Config com user_id para namespace da memória
CONFIG = {"configurable": {"langgraph_user_id": "sarah_chen"}}

EMAIL_ACOMPANHAMENTO = {
    "author": "Alice Smith <alice.smith@company.com>",
    "to": "Sarah Chen <sarah.chen@company.com>",
    "subject": "Acompanhamento",
    "email_thread": "Olá Sarah, como está minha solicitação de reunião?",
}

EMAIL_SPAM = {
    "author": "Equipe de Marketing <marketing@amazingdeals.com>",
    "to": "Sarah Chen <sarah.chen@company.com>",
    "subject": "🔥 OFERTA EXCLUSIVA: 80% de desconto!",
    "email_thread": "Não perca esta oferta INCRÍVEL! 80% OFF por 24h!",
}

EMAIL_ALICE = {
    "author": "Alice Smith <alice.smith@company.com>",
    "to": "Sarah Chen <sarah.chen@company.com>",
    "subject": "Dúvida sobre a documentação da API",
    "email_thread": """Olá Sarah,
Notei que os endpoints /auth/refresh e /auth/validate estão faltando
na documentação. Foi intencional?
Obrigada, Alice""",
}


def testar_email(email: dict, descricao: str, use_memory: bool = False, usar_hitl: bool = False):
    modo = "COM MEMÓRIA" if use_memory else "SEM MEMÓRIA"
    print(f"\n{'='*60}")
    print(f"📬 {descricao} [{modo}]")
    print(f"   De: {email['author']}")
    print(f"   Assunto: {email['subject']}")
    print("="*60)

    graph = build_email_graph(use_memory=use_memory)
    response = graph.invoke({"email_input": email}, config=CONFIG)

    if response.get("messages"):
        for msg in response["messages"]:
            if isinstance(msg, ToolMessage):
                print(f"\n🔧 [{msg.name}]: {str(msg.content)[:200]}")
        ultima = response["messages"][-1]
        print(f"\n💬 RESPOSTA: {str(ultima.content)[:300]}")
    else:
        print("✅ Fluxo encerrado.")

    # HITL após o fluxo principal
    if usar_hitl and response.get("messages"):
        human_in_the_loop_schedule(
            email_sender=email["author"],
            email_recipient=email["to"],
            email_subject=email["subject"],
            config=CONFIG,
        )


def main():
    print("\n🤖 ASSISTENTE DE EMAIL — DEMO COMPLETO")

    # 1. Spam — ignora
    testar_email(EMAIL_SPAM, "SPAM")

    # 2. Dúvida técnica — responde automaticamente
    testar_email(EMAIL_ALICE, "Dúvida técnica", use_memory=False)

    # 3. Solicitação de reunião — HITL decide
    testar_email(EMAIL_ACOMPANHAMENTO, "Solicitação de reunião",
                 use_memory=True, usar_hitl=True)


if __name__ == "__main__":
    main()