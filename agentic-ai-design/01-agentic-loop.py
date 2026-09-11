"""
Agentic Loop Pattern
====================
El patrón fundamental de un agente: Think → Act → Observe → Repeat
Bucle cerrado de percepción, razonamiento y acción.
"""

from strands import Agent
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class LoopIteration:
    """Una iteración del bucle agentico"""
    iteration: int
    thought: str
    action: str
    observation: str
    reasoning: str


class AgenticLoopAgent:
    """Implementación del bucle agentico fundamental"""

    def __init__(self, max_iterations: int = 5):
        self.agent = Agent(
            system_prompt="""Eres un agente con bucle agentico.
            Tu proceso es iterativo:
            1. THINK: Analiza la situación
            2. ACT: Realiza una acción basada en tu análisis
            3. OBSERVE: Observa los resultados
            4. REPEAT: Itera hasta resolver

            Sé reflexivo y adaptativo."""
        )

        self.max_iterations = max_iterations
        self.iterations: List[LoopIteration] = []

    def think(self, situation: str, context: str = "") -> str:
        """Fase THINK: Razonamiento y análisis"""
        prompt = f"""
        Situación: {situation}
        {f"Contexto previo: {context}" if context else ""}

        Piensa sobre esto:
        1. ¿Cuál es el problema?
        2. ¿Qué información necesitas?
        3. ¿Cuál es la mejor estrategia?
        4. ¿Qué acción deberías tomar?

        Proporciona tu pensamiento (máximo 2 frases).
        """
        return self.agent(prompt)

    def act(self, thought: str) -> str:
        """Fase ACT: Ejecutar acción"""
        prompt = f"""
        Basado en tu pensamiento:
        {thought}

        ¿Cuál es la acción específica que tomarías?
        Proporciona la acción concretamente.
        """
        return self.agent(prompt)

    def observe(self, action: str, situation: str) -> str:
        """Fase OBSERVE: Observar resultados"""
        prompt = f"""
        Acción tomada: {action}
        Situación original: {situation}

        Observa los resultados:
        1. ¿Qué cambió?
        2. ¿Fue efectiva la acción?
        3. ¿Hay nuevos desafíos?

        Proporciona tus observaciones.
        """
        return self.agent(prompt)

    def execute_loop(self, goal: str) -> List[LoopIteration]:
        """Ejecuta el bucle agentico completo"""

        print(f"\n{'='*70}")
        print(f"AGENTIC LOOP - GOAL: {goal}")
        print(f"{'='*70}\n")

        situation = goal
        iteration_count = 0

        while iteration_count < self.max_iterations:
            iteration_count += 1
            print(f"\n🔄 ITERATION {iteration_count}")
            print("-" * 70)

            # THINK
            print("\n💭 THINK")
            thought = self.think(situation)
            print(f"Thought: {thought}")

            # ACT
            print("\n🎯 ACT")
            action = self.act(thought)
            print(f"Action: {action}")

            # OBSERVE
            print("\n👁️  OBSERVE")
            observation = self.observe(action, situation)
            print(f"Observation: {observation}")

            # Registrar iteración
            loop_iter = LoopIteration(
                iteration=iteration_count,
                thought=thought,
                action=action,
                observation=observation,
                reasoning=thought
            )
            self.iterations.append(loop_iter)

            # Decidir si continuar
            should_continue = self.agent(
                f"""Basado en tu observación:
                {observation}

                ¿Necesitas otra iteración o has resuelto el problema?
                Responde: CONTINUAR o FINALIZAR"""
            )

            if "FINALIZAR" in should_continue.upper() or "STOP" in should_continue.upper():
                print("\n✓ Goal achieved!")
                break

            # Actualizar situación para siguiente iteración
            situation = observation

        return self.iterations

    def print_loop_summary(self):
        """Imprime resumen del bucle"""

        print(f"\n{'='*70}")
        print("AGENTIC LOOP SUMMARY")
        print(f"{'='*70}\n")

        print(f"Total Iterations: {len(self.iterations)}\n")

        for i, iteration in enumerate(self.iterations, 1):
            print(f"Iteration {i}:")
            print(f"  💭 Thought: {iteration.thought[:60]}...")
            print(f"  🎯 Action:  {iteration.action[:60]}...")
            print(f"  👁️  Observation: {iteration.observation[:60]}...")
            print()

        print("="*70)
        print("AGENTIC LOOP CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Patrón fundamental y universal
  ✓ Adaptativo y reflexivo
  ✓ Permite iteración y mejora
  ✓ Funciona con cualquier tarea
  ✓ Bien documentado

Desventajas:
  ✗ Lento (múltiples iteraciones)
  ✗ Costo computacional
  ✗ Puede converger a óptimos locales
  ✗ Requiere criterios de parada

Casos de Uso:
  • Cualquier tarea agentica
  • Problem solving
  • Research y análisis
  • Adaptación a nuevas situaciones
        """)


def main():
    """Ejecuta ejemplo del Agentic Loop"""

    agent = AgenticLoopAgent(max_iterations=5)

    goal = "Diseña una estrategia para mejorar la retención de clientes en una SaaS"

    iterations = agent.execute_loop(goal)
    agent.print_loop_summary()


if __name__ == "__main__":
    main()
