"""
AWS Pattern: Memory-augmented Agent
====================================
Agente que mantiene y utiliza memoria de conversaciones previas,
aprendizajes y contexto histórico.

Principios AWS:
- Autonomía: Recuerda y aplica aprendizajes previos
- Agencia: Usa memoria para actuar mejor
"""

from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.session.file_session_manager import FileSessionManager
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MemoryEntry:
    """Una entrada en la memoria del agente"""
    timestamp: datetime
    category: str  # "learned", "preference", "fact", "mistake"
    content: str
    importance: int  # 1-10


class MemoryAugmentedAgent:
    """Agente que mantiene memoria persistente"""

    def __init__(self, agent_id: str = "memory-agent-1"):
        # Configurar persistence
        conversation_manager = SummarizingConversationManager(
            summary_ratio=0.3,
            preserve_recent_messages=10
        )

        session_manager = FileSessionManager(
            session_id=agent_id,
            storage_dir="./patterns-aws/sessions"
        )

        # Agente con memoria
        self.agent = Agent(
            system_prompt="""Eres un agente con memoria persistente.
            Tu tarea es:
            1. Recordar interacciones previas
            2. Aplicar aprendizajes
            3. Mejorar con experiencia
            4. Reconocer patrones

            Usa tu memoria para ser más efectivo con el tiempo.""",
            conversation_manager=conversation_manager,
            session_manager=session_manager
        )

        self.agent_id = agent_id
        self.memory: List[MemoryEntry] = []
        self.interaction_count = 0

    def learn_preference(self, user: str, preference: str):
        """Registra una preferencia aprendida"""
        entry = MemoryEntry(
            timestamp=datetime.now(),
            category="preference",
            content=f"{user} prefiere: {preference}",
            importance=8
        )
        self.memory.append(entry)
        print(f"  💾 Learned: {preference}")

    def record_fact(self, fact: str, importance: int = 5):
        """Registra un hecho importante"""
        entry = MemoryEntry(
            timestamp=datetime.now(),
            category="fact",
            content=fact,
            importance=importance
        )
        self.memory.append(entry)
        print(f"  💾 Recorded: {fact}")

    def remember_mistake(self, mistake: str):
        """Recuerda un error para no repetirlo"""
        entry = MemoryEntry(
            timestamp=datetime.now(),
            category="mistake",
            content=f"Evitar: {mistake}",
            importance=9
        )
        self.memory.append(entry)
        print(f"  ⚠️  Remembered mistake: {mistake}")

    def retrieve_relevant_memories(self, query: str) -> List[MemoryEntry]:
        """Busca memorias relevantes"""
        relevant = []
        query_lower = query.lower()

        for memory in self.memory:
            if any(word in memory.content.lower() for word in query_lower.split()):
                relevant.append(memory)

        return sorted(relevant, key=lambda m: m.importance, reverse=True)[:3]

    def interact_with_memory(self, user_input: str) -> str:
        """Interactúa considerando memoria"""

        self.interaction_count += 1

        print(f"\n{'='*70}")
        print(f"INTERACTION #{self.interaction_count}")
        print(f"{'='*70}\n")

        print(f"User: {user_input}\n")

        # Buscar memorias relevantes
        relevant_memories = self.retrieve_relevant_memories(user_input)

        memory_context = ""
        if relevant_memories:
            print("📚 Relevant Memories:")
            memory_context = "\n".join([
                f"- {m.content} (importance: {m.importance})"
                for m in relevant_memories
            ])
            print(memory_context)
            print()

        # Generar respuesta usando memoria
        prompt = f"""
        User input: {user_input}

        {f"Memorias relevantes:{memory_context}" if memory_context else "No hay memorias previas"}

        Basado en tu memoria y aprendizajes previos, responde:
        1. Considera tus memorias
        2. Aplica preferencias aprendidas
        3. Evita errores previos
        4. Proporciona una respuesta mejorada

        Después de responder, ¿hay algo nuevo que debería recordar?
        """

        response = self.agent(prompt)
        print(f"Agent: {response}\n")

        return response

    def interactive_session(self):
        """Sesión interactiva donde el agente aprende"""

        print(f"\n{'='*70}")
        print("MEMORY-AUGMENTED AGENT - INTERACTIVE SESSION")
        print(f"{'='*70}\n")

        interactions = [
            {
                "input": "¿Cuál es mi nombre? Soy Alex.",
                "learn": ("preference", "El usuario se llama Alex")
            },
            {
                "input": "¿Cuál es mi rol en la empresa?",
                "learn": ("fact", "Alex es Product Manager en TechCorp")
            },
            {
                "input": "Necesito ayuda con planning de features. ¿Recuerdas algo sobre mí?",
                "learn": ("preference", "Alex necesita ayuda con planning de features")
            },
            {
                "input": "El año pasado cometí el error de no validar con usuarios. ¿Puedes ayudarme a evitarlo?",
                "learn": ("mistake", "No validar features con usuarios antes de build")
            },
            {
                "input": "Estoy planificando nuevas features. ¿Qué debería considerar?",
                "learn": None
            },
        ]

        for interaction in interactions:
            # Interacción
            self.interact_with_memory(interaction["input"])

            # Aprendizaje
            if interaction["learn"]:
                category, content = interaction["learn"]
                if category == "preference":
                    self.learn_preference("Alex", content)
                elif category == "fact":
                    self.record_fact(content)
                elif category == "mistake":
                    self.remember_mistake(content)

    def print_memory_summary(self):
        """Imprime resumen de la memoria"""

        print(f"\n{'='*70}")
        print("AGENT MEMORY SUMMARY")
        print(f"{'='*70}\n")

        print(f"Total Interactions: {self.interaction_count}")
        print(f"Memories Stored: {len(self.memory)}\n")

        # Categorías
        categories = {}
        for memory in self.memory:
            if memory.category not in categories:
                categories[memory.category] = []
            categories[memory.category].append(memory)

        print("Memories by Category:")
        for category, memories in categories.items():
            print(f"\n  {category.upper()} ({len(memories)})")
            for memory in memories:
                print(f"    - {memory.content} (importance: {memory.importance})")

        print("\n" + "="*70)
        print("MEMORY-AUGMENTED AGENT CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Mejora con experiencia
  ✓ Personalización automática
  ✓ Contexto histórico
  ✓ Evita repetir errores
  ✓ Sesiones persistentes

Desventajas:
  ✗ Complejidad de gestión de memoria
  ✗ Conflicto con memorias antiguas
  ✗ Requiere almacenamiento
  ✗ Privacidad/confidencialidad

AWS Pattern: MEMORY-AUGMENTED
  → Integra contexto histórico
  → Soporta sesiones largas
  → Memorias recuperables
  → Base para personalizacion

Casos de Uso:
  • Asistentes personales
  • Chatbots de servicio al cliente
  • Tutores educativos
  • Análisis histórico
        """)


def main():
    """Ejecuta ejemplo de Memory-augmented Agent"""

    agent = MemoryAugmentedAgent("product-manager-assistant")

    # Sesión interactiva
    agent.interactive_session()

    # Resumen de memoria
    agent.print_memory_summary()


if __name__ == "__main__":
    main()
