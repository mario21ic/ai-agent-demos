"""
Session Management = Cierro script y todo se pierde
Conversation Managers = conversacion crece y el contexto tambien.
    SlidingWindow (default) = mantiene ultimos n mensajes, ideal para conversaciones normales
    Summarizing = resume mensajes viejos con el modelo, ideal para conversaciones largas donde el contexto importa.
    Null = no modificada nada, para conversaciones cortas, debugging
"""

from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager

agent = Agent(
    system_prompt="""You are a Computer Science Subject Expert specializing
    in explaining technical concepts clearly and concisely...""",
    conversation_manager=SummarizingConversationManager(
        summary_ratio=0.3, # resumir el 30%
        preserve_recent_messages=10 # retener ultimos 10
    )
)

def interactive_session():
    print("CS Subject Expert (type 'exit' to quit)")
    print("----------------------------------------")
    
    while True:
        user_input = input("\nYour question: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        print("\nThinking...\n")
        agent(user_input)

if __name__ == "__main__":
    interactive_session()
