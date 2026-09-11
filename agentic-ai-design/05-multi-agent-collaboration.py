"""
Pattern 5: Multi-Agent Collaboration Pattern
==============================================
Múltiples agentes especializados colaboran para resolver problemas.
"""

from strands import Agent
from typing import Dict


class MultiAgentCollaborationPattern:
    """Múltiples agentes colaboran"""

    def __init__(self):
        self.financial_agent = Agent(
            system_prompt="Eres experto en finanzas. Proporciona perspectiva financiera."
        )
        self.technical_agent = Agent(
            system_prompt="Eres experto técnico. Proporciona perspectiva técnica."
        )
        self.strategy_agent = Agent(
            system_prompt="Eres estratega. Sintetiza perspectivas en estrategia."
        )

    def collaborate(self, task: str) -> Dict[str, str]:
        """Colaboración entre agentes"""

        print(f"\n{'='*70}")
        print(f"MULTI-AGENT COLLABORATION")
        print(f"{'='*70}\n")

        print(f"Task: {task}\n")

        # Perspectiva financiera
        print("💰 Financial Perspective:")
        financial = self.financial_agent(f"Análisis financiero: {task}")
        financial_text = str(financial)
        print(f"{financial_text[:150]}...\n")

        # Perspectiva técnica
        print("🔧 Technical Perspective:")
        technical = self.technical_agent(f"Análisis técnico: {task}")
        technical_text = str(technical)
        print(f"{technical_text[:150]}...\n")

        # Síntesis estratégica
        print("🎯 Strategic Synthesis:")
        synthesis_prompt = f"""
        Perspectiva Financiera: {financial_text[:200]}
        Perspectiva Técnica: {technical_text[:200]}

        Sintetiza estas perspectivas en una estrategia coherente.
        """
        strategy = self.strategy_agent(synthesis_prompt)
        strategy_text = str(strategy)
        print(f"{strategy_text[:150]}...\n")

        return {
            "financial": financial_text,
            "technical": technical_text,
            "strategy": strategy_text
        }


def main():
    pattern = MultiAgentCollaborationPattern()
    result = pattern.collaborate("Lanzar nuevo producto SaaS")

    print("="*70)
    print("MULTI-AGENT COLLABORATION CHARACTERISTICS")
    print("="*70)
    print("""
Ventajas:
  ✓ Múltiples perspectivas
  ✓ Decisiones equilibradas
  ✓ Mejor cobertura de riesgos
  ✓ Soluciones más robustas

Desventajas:
  ✗ Costo computacional
  ✗ Lentitud
  ✗ Posible conflicto

Casos de Uso:
  • Decisiones estratégicas
  • Análisis complejos
  • Validación cruzada
    """)


if __name__ == "__main__":
    main()
