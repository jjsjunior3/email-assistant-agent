import sys
import os
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tools import write_email, schedule_meeting
from memory import manage_memory_tool, search_memory_tool


def human_in_the_loop_schedule(
    email_sender: str,
    email_recipient: str,
    email_subject: str,
    config: dict,
) -> None:
    """
    Implementa o Human in the Loop para agendamento de reuniões.

    Fluxo:
    1. Busca na memória se já existe reunião agendada
    2. Se sim → avisa por email
    3. Se não → pergunta ao humano
       - sim → agenda + salva memória + envia email
       - não → envia email de acompanhamento + salva memória
    """
    print("\n🔍 Buscando na memória reuniões anteriores...")

    # 1. Verifica memória
    try:
        search_results = search_memory_tool.invoke(
            {"query": f"Reunião agendada para {email_sender}"},
            config=config,
        )
        if isinstance(search_results, str):
            search_results = {}
    except Exception:
        search_results = {}

    # 2. Já existe reunião → avisa
    if search_results and search_results.get("results"):
        print("📋 Reunião já encontrada na memória — enviando aviso.")
        result = write_email.invoke({
            "to": email_sender,
            "subject": f"Re: {email_subject}",
            "content": "Olá, já temos uma conversa agendada para discutirmos esse assunto.",
        }, config=config)
        print(f"\n📧 write_email: {result}")
        return

    # 3. Pergunta ao humano
    print(f"\n⏸️  HUMAN IN THE LOOP")
    decisao = input(
        f"Deseja agendar uma reunião para discutir o pedido de {email_sender}? (sim/não): "
    ).strip().lower()

    if decisao == "sim":
        # Agenda reunião
        nome_remetente = email_sender.split('<')[0].strip()
        nome_destinatario = email_recipient.split('<')[0].strip()

        reuniao = schedule_meeting.invoke({
            "attendees": [nome_destinatario, nome_remetente],
            "subject": f"Acompanhamento: {email_subject}",
            "duration_minutes": 30,
            "preferred_day": "amanhã",
        }, config=config)
        print(f"\n📅 schedule_meeting: {reuniao}")

        # Salva na memória
        memoria = manage_memory_tool.invoke({
            "action": "create",
            "content": f"Reunião agendada para discutir pedido de {email_sender}",
        }, config=config)
        print(f"🧠 manage_memory: {memoria}")

        # Envia email confirmando
        email = write_email.invoke({
            "to": email_sender,
            "subject": f"Re: {email_subject}",
            "content": "Já agendei uma reunião para discutirmos esse assunto. Até lá!",
        }, config=config)
        print(f"📧 write_email: {email}")

    else:
        # Envia email de acompanhamento
        email = write_email.invoke({
            "to": email_sender,
            "subject": f"Re: {email_subject}",
            "content": "Estou acompanhando seu pedido e entrarei em contato assim que houver novidades.",
        }, config=config)
        print(f"📧 write_email: {email}")

        # Salva na memória
        memoria = manage_memory_tool.invoke({
            "action": "create",
            "content": f"Email de acompanhamento enviado para {email_sender}",
        }, config=config)
        print(f"🧠 manage_memory: {memoria}")