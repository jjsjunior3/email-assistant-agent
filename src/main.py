import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from router import testar_roteador
from config import email

def main():
    print("\n" + "="*60)
    print("📬 ASSISTENTE DE EMAIL — TRIAGEM")
    print("="*60)
    print(f"\nAnalisando email:")
    print(f"  De      : {email['from']}")
    print(f"  Assunto : {email['subject']}")

    resultado = testar_roteador()

    acoes = {
        "ignore":  "🗑️  Email ignorado — não requer ação",
        "notify":  "🔔 Email marcado para notificação",
        "respond": "✍️  Email encaminhado para resposta automática",
    }
    print(f"\n{acoes[resultado.classification]}")


if __name__ == "__main__":
    main()