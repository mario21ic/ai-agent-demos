"""
Agente A (servidor A2A).

Expone un agente Strands ("Agente Calculadora") como un servidor que habla el
protocolo A2A (Agent2Agent, desarrollado por Google) en http://127.0.0.1:9000.

Cualquier cliente A2A -incluido otro agente Strands- puede descubrirlo y
enviarle mensajes en lenguaje natural.

Requiere credenciales de AWS configuradas (Strands usa Amazon Bedrock con un
modelo Claude por defecto).
"""

import logging

from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands_tools.calculator import calculator

logging.basicConfig(level=logging.INFO)


def create_agent(context_id: str) -> Agent:
    """Fábrica de agentes: A2AServer crea una instancia nueva por conversación."""
    return Agent(
        name="Calculator Agent",
        description="Agente que realiza operaciones aritméticas básicas.",
        tools=[calculator],
        callback_handler=None,
    )


if __name__ == "__main__":
    a2a_server = A2AServer(agent_factory=create_agent, host="127.0.0.1", port=9000)
    print("Agente Calculadora escuchando en http://127.0.0.1:9000 (A2A)")
    a2a_server.serve()
