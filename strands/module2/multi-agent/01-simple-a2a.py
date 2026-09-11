"""
Simple Agent-to-Agent Communication
====================================
Ejemplo básico: Researcher Agent hace preguntas y Expert Agent responde
"""

from strands import Agent


def simple_a2a_demo():
    """Demostración simple de comunicación entre dos agentes"""

    # Agent 1: Investigador
    researcher = Agent(
        system_prompt="You are a curious researcher. Ask technical questions about AI."
    )

    # Agent 2: Experto
    expert = Agent(
        system_prompt="You are an AI expert. Answer questions with clear, concise explanations."
    )

    print("\n" + "="*60)
    print("SIMPLE AGENT-TO-AGENT COMMUNICATION")
    print("="*60 + "\n")

    # Paso 1: Researcher pregunta
    print("📚 RESEARCHER asking question...")
    question = researcher("Ask a technical question about neural networks")
    print(f"Question:\n{question}\n")

    # Paso 2: Expert responde
    print("🤖 EXPERT responding...")
    answer = expert(f"Answer this question: {question}")
    print(f"Answer:\n{answer}\n")

    # Paso 3: Researcher hace seguimiento
    print("📚 RESEARCHER follow-up...")
    follow_up = researcher(f"Based on this response, ask a deeper follow-up question:\n{answer}")
    print(f"Follow-up question:\n{follow_up}\n")

    # Paso 4: Expert responde nuevamente
    print("🤖 EXPERT responding to follow-up...")
    final_answer = expert(f"Answer this follow-up question: {follow_up}")
    print(f"Final answer:\n{final_answer}\n")


if __name__ == "__main__":
    simple_a2a_demo()
