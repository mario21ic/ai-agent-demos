"""
Retrieval Augmented Generation (RAG) Pattern
==============================================
Agente que busca información relevante antes de generar respuestas.
Combina búsqueda de documentos con generación de texto.
"""

from strands import Agent
from typing import List, Dict


class RAGAgent:
    """Agente con Retrieval Augmented Generation"""

    def __init__(self):
        self.retriever_agent = Agent(
            system_prompt="Eres especialista en búsqueda y recuperación de información"
        )

        self.generator_agent = Agent(
            system_prompt="Eres especialista en generar respuestas bien informadas"
        )

        self.knowledge_base = {
            "IA": ["Machine Learning", "Deep Learning", "NLP", "Computer Vision"],
            "Python": ["Variables", "Funciones", "Clases", "Decoradores"],
            "Bases de datos": ["SQL", "NoSQL", "Relacional", "Distribuida"],
        }

    def retrieve(self, query: str) -> List[str]:
        """Fase 1: RETRIEVE - Buscar documentos relevantes"""

        print("\n📚 RETRIEVE Phase")
        print("-" * 70)

        # Búsqueda simulada en knowledge base
        relevant_docs = []
        query_lower = query.lower()

        for topic, docs in self.knowledge_base.items():
            if any(word in query_lower for word in topic.lower().split()):
                relevant_docs.extend(docs)

        print(f"Query: {query}")
        print(f"Retrieved: {relevant_docs}\n")

        return relevant_docs

    def augment(self, query: str, documents: List[str]) -> str:
        """Fase 2: AUGMENT - Crear contexto aumentado"""

        print("📝 AUGMENT Phase")
        print("-" * 70)

        context = f"Documentos relevantes: {', '.join(documents)}"
        print(f"Contexto aumentado: {context}\n")

        return context

    def generate(self, query: str, context: str) -> str:
        """Fase 3: GENERATE - Generar respuesta informada"""

        print("🤖 GENERATE Phase")
        print("-" * 70)

        prompt = f"""
        Pregunta: {query}
        Contexto: {context}

        Genera una respuesta informada basada en el contexto.
        """

        response = self.generator_agent(prompt)
        print(f"Response: {response[:150]}...\n")

        return response

    def rag_query(self, query: str) -> str:
        """Ejecuta el pipeline RAG completo"""

        print(f"\n{'='*70}")
        print(f"RAG PATTERN - QUERY: {query}")
        print(f"{'='*70}\n")

        documents = self.retrieve(query)
        context = self.augment(query, documents)
        response = self.generate(query, context)

        return response


def main():
    agent = RAGAgent()

    queries = [
        "¿Cuáles son los conceptos clave en IA?",
        "¿Qué son las funciones en Python?",
    ]

    for query in queries:
        agent.rag_query(query)


if __name__ == "__main__":
    main()
