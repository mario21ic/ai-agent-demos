"""
Tool Use/Function Calling Pattern
==================================
Agentes que invocan herramientas y APIs externas
para completar tareas más allá de su conocimiento base.
"""

from strands import Agent
from strands_tools import current_time, http_request
from typing import Dict, List


class ToolUseAgent:
    """Agente que usa herramientas efectivamente"""

    def __init__(self):
        self.agent = Agent(
            system_prompt="""Eres un agente con acceso a herramientas.
            Tu trabajo es:
            1. Determinar qué herramientas necesitas
            2. Usarlas estratégicamente
            3. Procesar resultados
            4. Adaptar según feedback

            Sé inteligente sobre tool selection.""",
            tools=[current_time, http_request]
        )

        self.tool_calls: List[Dict] = []

    def execute_with_tools(self, task: str) -> str:
        """Ejecuta una tarea usando herramientas"""

        print(f"\n{'='*70}")
        print(f"TOOL USE PATTERN - TASK: {task}")
        print(f"{'='*70}\n")

        prompt = f"""
        Tarea: {task}

        Herramientas disponibles:
        - current_time() → Obtiene la hora actual
        - http_request(url) → Realiza solicitudes HTTP

        Completa la tarea:
        1. Identifica qué herramientas necesitas
        2. Úsalas para obtener información
        3. Procesa los resultados
        4. Proporciona una respuesta completa
        """

        result = self.agent(prompt)

        self.tool_calls.append({
            "task": task,
            "result": result,
            "timestamp": "logged"
        })

        print(f"Result:\n{result}\n")
        return result


def main():
    agent = ToolUseAgent()

    tasks = [
        "¿Cuál es la hora actual y qué puedo hacer con esa información?",
        "Busca información sobre Cloud Computing",
    ]

    for task in tasks:
        agent.execute_with_tools(task)


if __name__ == "__main__":
    main()
