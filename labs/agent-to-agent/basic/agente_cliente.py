"""
Agente B (cliente A2A / orquestador).

Descubre al Agente A (agente_servidor.py) vía el protocolo A2A y le delega
preguntas usando A2AClientToolProvider, que expone el agente remoto como una
herramienta más dentro de este agente Strands.

Ejecutar primero agente_servidor.py en otra terminal.
"""

import logging

from strands import Agent
from strands_tools.a2a_client import A2AClientToolProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Registra de antemano la URL del Agente A. A2AClientToolProvider también
# puede descubrir agentes dinámicamente si no se le pasa known_agent_urls.
provider = A2AClientToolProvider(known_agent_urls=["http://127.0.0.1:9000"])

orquestador = Agent(
    name="Orchestrator Agent",
    system_prompt=(
        "Eres un agente orquestador. Cuando la pregunta del usuario requiera "
        "cálculos matemáticos, delega la tarea al agente remoto disponible "
        "vía A2A en lugar de calcularlo tú mismo."
    ),
    tools=provider.tools,
)

if __name__ == "__main__":
    respuesta = orquestador("¿Cuánto es 30 / 15 + 8? Usa el agente remoto disponible.")
    logger.info(respuesta)
