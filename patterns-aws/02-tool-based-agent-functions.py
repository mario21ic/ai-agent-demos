"""
AWS Pattern: Tool-based Agent for Calling Functions
====================================================
Agente que llama funciones/herramientas para completar tareas.
Usa el protocolo de tool-use de Anthropic.

Principios AWS:
- Agencia: Ejecuta acciones mediante herramientas
- Autonomía: Decide qué herramienta usar y cuándo
"""

from strands import Agent
from strands_tools import current_time, http_request
from typing import Dict, List, Any
import json


class FunctionCallingAgent:
    """Agente que usa funciones/herramientas para resolver problemas"""

    def __init__(self):
        # Agente con acceso a herramientas
        self.agent = Agent(
            system_prompt="""Eres un agente que completa tareas usando herramientas.
            Cuando necesites información o realizar una acción:
            1. Identifica qué herramienta usar
            2. Llama la herramienta con parámetros correctos
            3. Procesa el resultado
            4. Proporciona el resultado al usuario

            Sé inteligente sobre qué herramientas usar y cuándo.""",
            tools=[current_time, http_request]
        )

        self.tool_calls_log: List[Dict] = []

    def complete_task_with_tools(self, task: str) -> str:
        """Completa una tarea usando herramientas disponibles"""

        print(f"\n{'='*70}")
        print(f"TOOL-BASED AGENT FOR FUNCTIONS")
        print(f"{'='*70}\n")

        print(f"Task: {task}\n")
        print("Execution:")
        print("-" * 70)

        # El agente determina qué herramientas usar
        execution_prompt = f"""
        Completa esta tarea: {task}

        Herramientas disponibles:
        1. current_time() - Obtiene la hora actual
        2. http_request(url) - Hace solicitudes HTTP

        Paso a paso:
        1. ¿Qué herramientas necesitas?
        2. Llama las herramientas necesarias
        3. Procesa los resultados
        4. Proporciona la solución
        """

        result = self.agent(execution_prompt)

        print(f"Result: {result}\n")

        self.tool_calls_log.append({
            "task": task,
            "result": result
        })

        return result

    def demonstrate_tool_use(self):
        """Demuestra uso de herramientas específicas"""

        print(f"\n{'='*70}")
        print("TOOL USE DEMONSTRATIONS")
        print(f"{'='*70}\n")

        # Demostración 1: Obtener hora
        print("🔧 Tool 1: Get Current Time")
        print("-" * 70)
        task1 = "¿Cuál es la hora actual? Considera la zona horaria."
        result1 = self.complete_task_with_tools(task1)

        # Demostración 2: Información técnica
        print("\n🔧 Tool 2: HTTP Request")
        print("-" * 70)
        task2 = """
        Obtén información técnica sobre la API de Claude.
        Necesito saber qué versiones están disponibles.
        """
        result2 = self.complete_task_with_tools(task2)

    def chain_tool_calls(self, complex_task: str) -> str:
        """Encadena múltiples llamadas de herramientas"""

        print(f"\n{'='*70}")
        print("CHAINING MULTIPLE TOOL CALLS")
        print(f"{'='*70}\n")

        print(f"Complex Task: {complex_task}\n")

        chaining_prompt = f"""
        Para completar esta tarea, es posible que necesites:
        1. Llamar una herramienta para obtener datos
        2. Procesar esos datos
        3. Llamar otra herramienta con los datos procesados
        4. Sintetizar el resultado final

        Tarea: {complex_task}

        Explica tu estrategia y ejecuta los pasos necesarios.
        """

        result = self.agent(chaining_prompt)
        return result

    def print_summary(self):
        """Imprime resumen de herramientas usadas"""

        print(f"\n{'='*70}")
        print("TOOL-BASED AGENT SUMMARY")
        print(f"{'='*70}\n")

        print(f"Total tasks completed: {len(self.tool_calls_log)}")

        print("\nAvailable Tools:")
        print("  1. current_time() - Get current time")
        print("  2. http_request(url) - Make HTTP requests")

        print("\nTasks executed:")
        for i, log in enumerate(self.tool_calls_log, 1):
            print(f"{i}. {log['task'][:60]}...")

        print("\n" + "="*70)
        print("TOOL-BASED AGENT CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Acceso a información en tiempo real
  ✓ Puede ejecutar acciones concretas
  ✓ Más capaz que razonamiento básico
  ✓ Determina automáticamente qué herramientas usar

Desventajas:
  ✗ Limitado a herramientas disponibles
  ✗ Puede haber latencia de red
  ✗ Errores en herramientas afectan al agente
  ✗ Seguridad: ¿Qué herramientas debería acceder?

AWS Pattern: TOOL-BASED AGENTS
  → Agentes que usan APIs y funciones
  → Permiten extensibilidad mediante herramientas
  → Clave para sistemas prácticos y productivos

Casos de Uso:
  • Obtención de datos en tiempo real
  • Integración con APIs externas
  • Ejecución de cálculos complejos
  • Automatización de procesos
        """)


def main():
    """Ejecuta ejemplo de Tool-based Agent"""

    agent = FunctionCallingAgent()

    # Demostración de uso de herramientas
    agent.demonstrate_tool_use()

    # Impresión de resumen
    agent.print_summary()


if __name__ == "__main__":
    main()
