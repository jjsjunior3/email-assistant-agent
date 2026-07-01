import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from graph import build_email_graph

EMAIL_EQUIPE = {
    "author": "Alice Smith <alice.smith@company.com>",
    "to": "Sarah Chen <sarah.chen@company.com>",
    "subject": "Dúvida rápida sobre a documentação da API",
    "email_thread": """Olá Sarah,

Eu estava revisando a documentação da API para o novo serviço de autenticação
e notei que alguns endpoints parecem estar faltando nas especificações.
Você poderia me ajudar a esclarecer se isso foi intencional ou se devemos
atualizar a documentação?

Especificamente, estou procurando por:
- /auth/refresh
- /auth/validate

Obrigada!
Alice""",
}

EMAIL_SPAM = {
    "author": "Equipe de Marketing <marketing@amazingdeals.com>",
    "to": "Sarah Chen <sarah.chen@company.com>",
    "subject": "🔥 OFERTA EXCLUSIVA: 80% de desconto!",
    "email_thread": "Prezado(a), não perca esta oferta INCRÍVEL! 80% OFF por 24h!",
}


def testar_email(email: dict, descricao: str, use_memory: bool = False):
    modo = "COM MEMÓRIA" if use_memory else "SEM MEMÓRIA"
    print(f"\n{'='*60}")
    print(f"📬 {descricao} [{modo}]")
    print(f"   De: {email['author']}")
    print(f"   Assunto: {email['subject']}")
    print("="*60)

    graph = build_email_graph(use_memory=use_memory)
    response = graph.invoke(
        {"email_input": email},
        config={"configurable": {"langgraph_user_id": "sarah_chen"}},
    )

    if response.get("messages"):
        print("\n💬 RESPOSTA DO AGENTE:")
        last = response["messages"][-1]
        print(str(last.content)[:500])
    else:
        print("✅ Fluxo encerrado sem resposta.")


def main():
    # Sem memória
    testar_email(EMAIL_SPAM, "SPAM", use_memory=False)
    testar_email(EMAIL_EQUIPE, "Email da Alice", use_memory=False)

    # Com memória semântica
    testar_email(EMAIL_EQUIPE, "Email da Alice", use_memory=True)


if __name__ == "__main__":
    main()