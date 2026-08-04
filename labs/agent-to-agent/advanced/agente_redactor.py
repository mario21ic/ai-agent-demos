"""
Agente Redactor — servidor A2A.

Agente especializado en redactar resúmenes ejecutivos claros y concisos a
partir de datos que le proporcionan otros agentes vía A2A. No tiene
herramientas propias ni acceso a datos externos: su valor es puramente el
estilo y la calidad de redacción, y depende de que le pasen los datos
correctos (típicamente, los que obtuvo el Agente Investigador).
"""

import logging

from a2a.types import AgentSkill
from strands import Agent
from strands.multiagent.a2a import A2AServer

logging.basicConfig(level=logging.INFO)

skill_redaccion = AgentSkill(
    id="redactar_resumen_ejecutivo",
    name="Redactar resumen ejecutivo",
    description=(
        "Redacta un resumen ejecutivo breve y profesional en español a "
        "partir de datos ya provistos (precios, noticias, cifras, etc.)."
    ),
    tags=["redaccion", "reportes"],
    examples=[
        "Redacta un resumen ejecutivo con estos datos: precio AMZN 231.45 USD..."
    ],
)


def create_agent(context_id: str) -> Agent:
    """Fábrica de agentes: A2AServer invoca esto una vez por conversación entrante."""
    return Agent(
        name="Writer Agent",
        description="Agente que redacta resúmenes ejecutivos a partir de datos provistos.",
        system_prompt=(
            "Eres un redactor financiero. A partir de los datos que te "
            "entreguen, escribe un resumen ejecutivo de máximo 4 líneas, en "
            "tono profesional y en español. No inventes datos que no te "
            "hayan dado; si falta información, dilo explícitamente."
        ),
        callback_handler=None,
    )


if __name__ == "__main__":
    a2a_server = A2AServer(
        agent_factory=create_agent,
        host="127.0.0.1",
        port=9002,
        skills=[skill_redaccion],
    )
    print("Agente Redactor escuchando en http://127.0.0.1:9002 (A2A)")
    a2a_server.serve()
