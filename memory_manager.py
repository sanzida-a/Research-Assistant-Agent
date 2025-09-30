from langchain_community.vectorstores import Chroma
from llm_config import get_embeddings


class MemoryManager:
    """
    Handles short-term and long-term memory.
    - Short-term: stored in memory (reset each session).
    - Long-term: persisted in Chroma DB.
    """
    def __init__(self, persist_directory="chroma_db"):
        self.short_term = []  # list of {"query": q, "answer": a}
        self.persist_directory = persist_directory
        self.embeddings = get_embeddings()
        self.vectordb = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def add_short_term(self, query, answer):
        self.short_term.append({"query": query, "answer": answer})

    def get_short_term_context(self):
        if not self.short_term:
            return ""
        return "\n".join([f"Q: {m['query']}\nA: {m['answer']}" for m in self.short_term])

    def reset_short_term(self):
        self.short_term = []

    def add_long_term_text(self, text: str):
        """
        Store insights or summaries into ChromaDB.
        """
        self.vectordb.add_texts([text])
        self.vectordb.persist()
