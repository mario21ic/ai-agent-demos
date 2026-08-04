"""
Agente Orquestador — cliente A2A.

Descubre a los agentes Investigador y Redactor vía el protocolo A2A
(Agent2Agent, Google) usando A2AClientToolProvider, que convierte cada
agente remoto descubierto en una herramienta más del Orquestador. El LLM del
Orquestador decide en qué orden delegar y qué pasarle a cada uno.

Flujo esperado para el prompt de ejemplo:
  1. Orquestador -> Agente Investigador (A2A): "dame precio y noticias de AMZN"
     Agente Investigador -> Servidor MCP: obtiene los datos reales
  2. Orquestador -> Agente Redactor (A2A): "redacta un resumen con estos datos"

Ejecutar en este orden, cada uno en su propia terminal:
  1. python mcp_server.py
  2. python agente_investigador.py
  3. python agente_redactor.py
  4. python agente_orquestador.py
"""

import logging

from strands import Agent
from strands_tools.a2a_client import A2AClientToolProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

provider = A2AClientToolProvider(
    known_agent_urls=[
        "http://127.0.0.1:9001",  # Agente Investigador
        "http://127.0.0.1:9002",  # Agente Redactor
    ]
)

orquestador = Agent(
    name="Orchestrator Agent",
    system_prompt=(
        "Eres un orquestador de agentes especializados. Para preparar un "
        "informe financiero debes seguir este orden estrictamente:\n"
        "1. Delegar al Agente Investigador la obtención del precio actual y "
        "las noticias recientes de la acción solicitada.\n"
        "2. Delegar al Agente Redactor la redacción de un resumen ejecutivo, "
        "pasándole exactamente los datos que obtuviste del Investigador.\n"
        "Nunca inventes datos ni redactes tú mismo el resumen: ese es "
        "trabajo del Agente Redactor."
    ),
    tools=provider.tools,
)

if __name__ == "__main__":
    respuesta = orquestador(
        "Prepara un informe ejecutivo breve sobre la acción de Amazon (AMZN)."
    )
    logger.info(respuesta)
