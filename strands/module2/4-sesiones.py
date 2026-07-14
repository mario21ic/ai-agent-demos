"""
Session Management = evitar que al cerrar script y todo se pierde. Para eso guardar estado y luego vuelvo a retomar.
    Incluye: historial de mensajes, estado del agente con agentstate y estado del conversation manager (resumen, otros, etc)
    step1: conversacion se termina y guarda en disco.
    step2: script se termina
    step3: conversacion se restaura y continua donde se quedo.

Para Prod: S3SessionManager o Redis
Para dev: FileSessionManager
"""

from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.session.file_session_manager import FileSessionManager

agent = Agent(
    system_prompt="""You are a Computer Science Subject Expert specializing
    in explaining technical concepts clearly and concisely...""",
    conversation_manager = SummarizingConversationManager(
        summary_ratio=0.3, # resumir el 30%
        preserve_recent_messages=10 # retener ultimos 10
    ),
    session_manager = FileSessionManager(
        session_id='user-1234',
        storage_dir="./sessions"
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
