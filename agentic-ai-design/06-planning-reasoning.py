"""
Pattern 6: Planning & Reasoning Pattern
========================================
Agente que planifica antes de actuar.
"""

from strands import Agent


class PlanningReasoningPattern:
    def __init__(self):
        self.agent = Agent(
            system_prompt="Eres planificador estratégico. Planifica, razona, luego actúa."
        )

    def plan_and_execute(self, goal: str) -> str:
        print(f"\n{'='*70}")
        print(f"PLANNING & REASONING")
        print(f"{'='*70}\n")

        # Planificación
        print("📋 PLANNING:")
        plan = self.agent(f"Crea un plan detallado para: {goal}")
        plan_text = str(plan)
        print(f"{plan_text[:150]}...\n")

        # Razonamiento
        print("💭 REASONING:")
        reasoning = self.agent(f"Razona sobre este plan:\n{plan_text[:200]}")
        reasoning_text = str(reasoning)
        print(f"{reasoning_text[:150]}...\n")

        # Primer paso
        print("🎯 FIRST STEP:")
        action = self.agent(f"¿Cuál es el primer paso concreto?\n{reasoning_text[:200]}")
        action_text = str(action)
        print(f"{action_text[:150]}...\n")

        return action_text


def main():
    pattern = PlanningReasoningPattern()
    pattern.plan_and_execute("Mejorar eficiencia operacional en 30%")


if __name__ == "__main__":
    main()
