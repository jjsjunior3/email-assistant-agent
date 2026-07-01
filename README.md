# 📧 Email Assistant Agent

Projeto de estudo e portfólio desenvolvido durante o curso **LangGraph: Orquestrando agentes e multiagentes** da Alura, parte da trilha **Engenharia de Agentes de IA**.

Um assistente inteligente de e-mail que combina **roteamento semântico**, **execução autônoma de ferramentas**, **memória semântica** e **Human in the Loop** em um único pipeline orquestrado com LangGraph.

---

## 🖥️ Demo

![Demo do Assistente](docs/demo.png)

---

## 🧠 Como funciona

```
Email recebido
      ↓
[ROTEADOR] → classifica: ignore / notify / respond
      ↓
  ignore → 🗑️ descartado
  notify → 🔔 notificação
  respond → [AGENTE EXECUTOR]
                  ↓
         usa ferramentas:
         ├── write_email
         ├── schedule_meeting
         ├── check_calendar_availability
         ├── manage_memory
         └── search_memory
                  ↓
         [HUMAN IN THE LOOP]
         ├── busca memória de reuniões anteriores
         ├── pergunta ao humano se deve agendar
         └── salva decisão na memória semântica
```

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| **Roteador inteligente** | Classifica e-mails em ignore/notify/respond usando Pydantic com saída estruturada |
| **Agente executor** | Usa `create_react_agent` do LangGraph para executar ferramentas autonomamente |
| **Memória semântica** | Armazena e recupera contexto por similaridade usando embeddings do Google |
| **Human in the Loop** | Pausa o fluxo e solicita aprovação humana antes de agendar reuniões |
| **Fallback robusto** | Retry automático para JSON truncado na classificação |

---

## 🛠️ Tecnologias

- **Python 3.12**
- **LangGraph** — orquestração do pipeline com grafos de estado
- **LangChain** — integração com LLMs e ferramentas
- **OpenRouter** — acesso ao Gemini 2.5 Flash via API compatível com OpenAI
- **Google Generative AI** — embeddings semânticos (`gemini-embedding-001`)
- **LangMem** — ferramentas de memória semântica para agentes
- **Pydantic** — validação e saída estruturada do roteador
- **python-dotenv** — gerenciamento de variáveis de ambiente

---

## 📁 Estrutura do Projeto

```
email-assistant-agent/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── docs/
│   └── demo.png
│
└── src/
    ├── main.py        # Ponto de entrada e cenários de teste
    ├── graph.py       # Grafo LangGraph com triage + agente executor
    ├── router.py      # Roteador com Pydantic e fallback para JSON truncado
    ├── agent.py       # Agente executor com e sem memória semântica
    ├── hitl.py        # Human in the Loop para agendamento de reuniões
    ├── memory.py      # Configuração de embeddings e InMemoryStore
    ├── tools.py       # Ferramentas agênticas (email, reunião, calendário)
    ├── prompts.py     # Templates de prompt para triage e agente
    └── config.py      # Perfil do usuário e regras de triagem
```

---

## 🚀 Como rodar

### Pré-requisitos
- Python 3.12+
- Conta no [OpenRouter](https://openrouter.ai/) com saldo
- Chave de API do Google ([AI Studio](https://aistudio.google.com/)) para embeddings

### 1. Clone o repositório
```bash
git clone https://github.com/jjsjunior3/email-assistant-agent.git
cd email-assistant-agent
```

### 2. Crie e ative o ambiente virtual
```bash
py -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
```
Edite o `.env`:
```env
OPENROUTER_API_KEY=sk-or-v1-sua_chave_aqui
GEMINI_API_KEY=sua_chave_google_aqui
```

### 5. Execute
```bash
py src/main.py
```

---

## 💡 Conceitos demonstrados

- **Roteamento com Pydantic** — saída estruturada com `Literal` para classificação confiável
- **`create_react_agent`** — agente ReAct em uma linha vs implementação manual das aulas anteriores
- **`Command`** — roteamento explícito entre nós do grafo
- **Memória semântica** — embeddings + `InMemoryStore` + `langmem`
- **Human in the Loop** com memória — decisão humana + aprendizado persistente
- **Fallback robusto** — retry automático para JSON truncado em saídas estruturadas
- Boas práticas: `.env`, `.gitignore`, estrutura modular, ambiente virtual

---

## 📚 Referências

- [Curso Alura — LangGraph: Orquestrando agentes e multiagentes](https://cursos.alura.com.br/)
- [Documentação LangGraph](https://langchain-ai.github.io/langgraph/)
- [LangMem — Memory for AI Agents](https://langchain-ai.github.io/langmem/)
- [OpenRouter](https://openrouter.ai/)

---

> Desenvolvido por **José João Santos Júnior** como projeto de portfólio durante os estudos de Engenharia de Agentes de IA.
>
> LinkedIn: [linkedin.com/in/jrsantosdev1](https://linkedin.com/in/jrsantosdev1) | GitHub: [github.com/jjsjunior3](https://github.com/jjsjunior3)