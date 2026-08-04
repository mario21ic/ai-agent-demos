"""
Agente Investigador — servidor A2A y, a la vez, cliente MCP.

Este agente cumple doble rol, que es el punto central de este ejemplo:
  1. Cliente MCP: se conecta al servidor MCP (mcp_server.py) y obtiene sus
     herramientas de datos financieros vía streamable-HTTP.
  2. Servidor A2A: expone esas capacidades como un agente descubrible por el
     protocolo Agent2Agent (Google), para que otros agentes -como el
     Orquestador- puedan delegarle tareas en lenguaje natural.

Ejecutar primero mcp_server.py en otra terminal.
"""

import logging

from a2a.types import AgentSkill
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands.tools.mcp import MCPClient

logging.basicConfig(level=logging.INFO)

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

# El cliente MCP se abre una sola vez y se mantiene vivo durante toda la
# ejecución del proceso (ver el bloque `with mcp_client:` más abajo).
mcp_client = MCPClient(lambda: streamablehttp_client(MCP_SERVER_URL))

skill_financiera = AgentSkill(
    id="consultar_datos_financieros",
    name="Consultar datos financieros",
    description=(
        "Obtiene precio de acción y noticias recientes de una empresa "
        "usando herramientas MCP conectadas a fuentes de datos financieros."
    ),
    tags=["finanzas", "mcp"],
    examples=["¿Cuál es el precio de AMZN?", "Dame noticias recientes de MSFT"],
)


def create_agent(context_id: str) -> Agent:
    """Fábrica de agentes: A2AServer invoca esto una vez por conversación entrante."""
    herramientas_mcp = mcp_client.list_tools_sync()
    return Agent(
        name="Research Agent",
        description=(
            "Agente especializado en datos financieros (precios de acciones "
            "y noticias), respaldado por herramientas MCP."
        ),
        system_prompt=(
            "Eres un analista financiero. Usa siempre las herramientas "
            "disponibles para obtener precios y noticias; nunca inventes "
            "cifras ni titulares. Responde de forma breve y estructurada."
        ),
        tools=herramientas_mcp,
        callback_handler=None,
    )


if __name__ == "__main__":
    with mcp_client:
        a2a_server = A2AServer(
            agent_factory=create_agent,
            host="127.0.0.1",
            port=9001,
            skills=[skill_financiera],
        )
        print("Agente Investigador escuchando en http://127.0.0.1:9001 (A2A)")
        print(f"  usando herramientas MCP de {MCP_SERVER_URL}")
        a2a_server.serve()
