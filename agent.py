from langgraph.graph import StateGraph, END
from llm_config import get_llm


class ResearchAssistantAgent:
    """
    LangGraph-based research assistant agent.
    Combines retrieval, short-term memory, and long-term memory.
    """

    def __init__(self, retriever, long_term_summary, memory_manager):
        self.llm = get_llm()
        self.retriever = retriever
        self.memory_manager = memory_manager
        self.long_term_summary = long_term_summary
        self.graph = self._build_graph()

    def _build_graph(self):
        """
        Build LangGraph state graph with retrieval and answering nodes.
        """
        graph = StateGraph(dict)

        def retrieve_node(state):
            query = state["query"]
            docs = self.retriever.get_relevant_documents(query)
            return {**state, "docs": docs}

        def answer_node(state):
            query = state["query"]
            docs = state["docs"]

            short_term_context = self.memory_manager.get_short_term_context()
            context = "\n\n".join([d.page_content for d in docs])

            full_context = (
                f"Long-term summary:\n{self.long_term_summary}\n\n"
                f"Short-term context:\n{short_term_context}\n\n"
                f"Retrieved documents:\n{context}\n\n"
                f"Question: {query}"
            )

            response = self.llm.invoke(
                [("user", f"Answer using the context below:\n\n{full_context}")]
            )
            return {**state, "answer": response.content}

        graph.add_node("retrieve", retrieve_node)
        graph.add_node("answer", answer_node)
        graph.add_edge("retrieve", "answer")
        graph.add_edge("answer", END)
        graph.set_entry_point("retrieve")
        
        # CRITICAL: Compile the graph before returning
        return graph.compile()

    def ask(self, query: str):
        """
        Run the agent on a query and store in short-term memory.
        """
        result = self.graph.invoke({"query": query})
        self.memory_manager.add_short_term(query, result["answer"])
        return result["answer"]

    def end_session(self):
        """
        Summarize session and store in long-term memory.
        (Bonus: includes multi-PDF summary as well)
        """
        short_term_summary = self.memory_manager.get_short_term_context()
        if short_term_summary:
            self.memory_manager.add_long_term_text("Session summary:\n" + short_term_summary)
        self.memory_manager.reset_short_term()