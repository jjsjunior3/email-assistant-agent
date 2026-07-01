import os
from dotenv import load_dotenv

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(_ROOT, '.env'))

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool


# Embeddings do Google para busca semântica
google_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Armazenamento em memória RAM
# Em produção: substituir por PostgresStore ou similar
store = InMemoryStore(
    index={"embed": google_embeddings}
)

# Namespace por usuário — evita misturar memórias de usuários diferentes
NAMESPACE = ("email_assistant", "{langgraph_user_id}", "collection")

# Ferramentas de memória que o agente pode usar
manage_memory_tool = create_manage_memory_tool(
    store=store,
    namespace=NAMESPACE,
)

search_memory_tool = create_search_memory_tool(
    store=store,
    namespace=NAMESPACE,
)