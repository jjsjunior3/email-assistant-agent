from langchain_core.tools import tool


@tool
def write_email(to: str, subject: str, content: str) -> str:
    """Escreve e envia um e-mail para o destinatário especificado."""
    return f"✅ E-mail enviado para {to} com o assunto '{subject}'"


@tool
def schedule_meeting(
    attendees: list[str],
    subject: str,
    duration_minutes: int,
    preferred_day: str,
) -> str:
    """Agenda uma reunião no calendário com os participantes especificados."""
    return (
        f"✅ Reunião '{subject}' agendada para {preferred_day} "
        f"com {len(attendees)} participante(s) "
        f"— duração: {duration_minutes} minutos"
    )


@tool
def check_calendar_availability(day: str) -> str:
    """Verifica a disponibilidade do calendário para um determinado dia."""
    return f"📅 Horários disponíveis em {day}: 9:00, 14:00, 16:00"


# Lista de todas as ferramentas disponíveis
TOOLS = [write_email, schedule_meeting, check_calendar_availability]