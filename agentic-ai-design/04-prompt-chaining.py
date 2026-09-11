"""
Pattern 4: Prompt Chaining Pattern
===================================
Encadena múltiples prompts para resolver problemas complejos.
Cada paso usa la salida del anterior.
"""

from strands import Agent
from typing import List


class PromptChainingAgent:
    """Encadena múltiples prompts secuencialmente"""

    def __init__(self):
        self.agent = Agent(
            system_prompt="""Eres un agente analítico que resuelve problemas complejos
            mediante encadenamiento de pasos. Cada paso construye sobre el anterior."""
        )
        self.chain_history: List[str] = []

    def chain_prompts(self, initial_task: str, num_steps: int = 3) -> str:
        """Ejecuta cadena de prompts"""

        print(f"\n{'='*70}")
        print(f"PROMPT CHAINING - {num_steps} steps")
        print(f"{'='*70}\n")

        print(f"Initial Task: {initial_task}\n")

        # Paso 1: Análisis inicial
        print("Step 1: Initial Analysis")
        print("-" * 70)
        step1_prompt = f"Analiza este problema: {initial_task}\nProvorciona análisis conciso."
        step1_result = self.agent(step1_prompt)
        step1_text = str(step1_result)
        self.chain_history.append(step1_text)
        print(f"Result: {step1_text[:150]}...\n")

        # Paso 2: Implicaciones
        print("Step 2: Implications")
        print("-" * 70)
        step2_prompt = f"""Basado en este análisis:
        {step1_text[:200]}

        ¿Cuáles son las implicaciones principales? (máximo 3)"""
        step2_result = self.agent(step2_prompt)
        step2_text = str(step2_result)
        self.chain_history.append(step2_text)
        print(f"Result: {step2_text[:150]}...\n")

        # Paso 3: Síntesis y recomendación
        print("Step 3: Synthesis & Recommendation")
        print("-" * 70)
        step3_prompt = f"""Basado en:
        Análisis: {step1_text[:100]}
        Implicaciones: {step2_text[:100]}

        Proporciona una recomendación final concreta."""
        step3_result = self.agent(step3_prompt)
        step3_text = str(step3_result)
        self.chain_history.append(step3_text)
        print(f"Result: {step3_text[:150]}...\n")

        return step3_text

    def print_chain_summary(self):
        """Imprime resumen de la cadena"""

        print(f"\n{'='*70}")
        print("CHAIN SUMMARY")
        print(f"{'='*70}\n")

        for i, result in enumerate(self.chain_history, 1):
            print(f"Step {i}: {result[:100]}...")

        print("\n" + "="*70)
        print("PROMPT CHAINING CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Descomposición de problemas complejos
  ✓ Razonamiento paso a paso
  ✓ Cada paso valida el anterior
  ✓ Resulta en mejores respuestas

Desventajas:
  ✗ Más llamadas al agente (lentitud)
  ✗ Costo computacional
  ✗ Errores se propagan

Casos de Uso:
  • Análisis profundo
  • Problem solving
  • Investigación compleja
  • Toma de decisiones
        """)


def main():
    """Ejecuta ejemplo de Prompt Chaining"""

    agent = PromptChainingAgent()

    task = "¿Cómo debería una startup validar su idea de producto antes de invertir?"
    result = agent.chain_prompts(task, num_steps=3)

    agent.print_chain_summary()


if __name__ == "__main__":
    main()
