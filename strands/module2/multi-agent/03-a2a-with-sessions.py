"""
Agent-to-Agent with Sessions
=============================
Comunicación A2A con persistencia de sesión para conversaciones largas
"""

from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.session.file_session_manager import FileSessionManager


class PersistentA2A:
    """A2A con sesiones persistentes"""

    def __init__(self, session_id: str = "a2a-session-1"):
        # Manager para sesiones
        session_manager = FileSessionManager(
            session_id=session_id,
            storage_dir="./a2a/sessions"
        )

        # Manager para conversación con resumen
        conversation_manager = SummarizingConversationManager(
            summary_ratio=0.3,
            preserve_recent_messages=5
        )

        # Agente 1: Mentor
        self.mentor = Agent(
            system_prompt="""You are a wise mentor teaching software engineering principles.
            You provide guidance, feedback, and deeper insights based on previous discussions.""",
            conversation_manager=conversation_manager,
            session_manager=session_manager
        )

        # Agente 2: Student
        self.student = Agent(
            system_prompt="""You are an eager student learning software engineering.
            You ask thoughtful questions and apply feedback from your mentor.""",
            conversation_manager=conversation_manager,
            session_manager=session_manager
        )

        self.session_id = session_id

    def interactive_lesson(self):
        """Sesión interactiva de aprendizaje A2A"""
        print(f"\n{'='*60}")
        print(f"INTERACTIVE A2A LEARNING SESSION: {self.session_id}")
        print(f"{'='*60}\n")

        topics = [
            "Design Patterns in Python",
            "API Design Best Practices",
            "Database Optimization"
        ]

        for i, topic in enumerate(topics, 1):
            print(f"\n--- ROUND {i}: {topic} ---\n")

            # Student pregunta
            print("👨‍🎓 STUDENT: Asking question...")
            student_question = self.student(
                f"Ask a specific technical question about {topic}"
            )
            print(f"Q: {student_question}\n")

            # Mentor responde
            print("👨‍🏫 MENTOR: Providing guidance...")
            mentor_response = self.mentor(
                f"A student asked: {student_question}\n\nProvide thoughtful guidance with examples."
            )
            print(f"A: {mentor_response}\n")

            # Student applies feedback
            print("👨‍🎓 STUDENT: Deepening understanding...")
            student_followup = self.student(
                f"Based on mentor feedback: {mentor_response}\n\n"
                f"Ask a more advanced follow-up question."
            )
            print(f"Follow-up: {student_followup}\n")

    def save_and_resume_info(self):
        """Muestra información sobre guardado y reanudación"""
        print(f"\n{'='*60}")
        print("SESSION PERSISTENCE")
        print(f"{'='*60}\n")
        print(f"Session ID: {self.session_id}")
        print(f"Saved at: ./a2a/sessions/")
        print("\nYou can resume this conversation by:")
        print(f"  • Running this script again with same session_id")
        print(f"  • Or instantiate with: PersistentA2A('{self.session_id}')")
        print("\nSession includes:")
        print("  ✓ Full conversation history")
        print("  ✓ Agent context and state")
        print("  ✓ Summarized long conversations")


def main():
    """Ejecuta lección A2A persistente"""
    session = PersistentA2A(session_id="mentorship-program")
    session.interactive_lesson()
    session.save_and_resume_info()


if __name__ == "__main__":
    main()
