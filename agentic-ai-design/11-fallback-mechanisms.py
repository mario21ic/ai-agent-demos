"""
Pattern 11: Fallback Mechanisms Pattern
========================================
Múltiples estrategias para recuperación ante errores.
Primary → Fallback A → Fallback B → Default
"""

from strands import Agent


class FallbackMechanismsPattern:
    """Múltiples estrategias de fallback"""

    def __init__(self):
        self.primary = Agent(system_prompt="Eres estrategia principal")
        self.fallback_a = Agent(system_prompt="Eres fallback alternativo A")
        self.fallback_b = Agent(system_prompt="Eres fallback alternativo B")

    def with_fallback(self, task: str) -> str:
        """Intenta estrategias en orden"""

        print(f"\n{'='*70}")
        print(f"FALLBACK MECHANISMS")
        print(f"{'='*70}\n")

        strategies = [
            ("Primary", self.primary),
            ("Fallback A", self.fallback_a),
            ("Fallback B", self.fallback_b),
        ]

        for strategy_name, strategy_agent in strategies:
            try:
                print(f"Intentando: {strategy_name}...")
                result = str(strategy_agent(task))
                print(f"✓ Éxito con {strategy_name}")
                print(f"  Resultado: {result[:100]}...\n")
                return result
            except Exception as e:
                print(f"✗ {strategy_name} falló: {str(e)[:50]}")

        print("✗ Todas las estrategias fallaron. Retornando default.\n")
        return "Default response"


def main():
    """Ejecuta ejemplo de Fallback Mechanisms"""

    pattern = FallbackMechanismsPattern()
    result = pattern.with_fallback("Tarea desafiante que podría fallar")

    print("="*70)
    print("FALLBACK MECHANISMS CHARACTERISTICS")
    print("="*70)
    print("""
Ventajas:
  ✓ Múltiples opciones de recuperación
  ✓ Resiliencia ante fallos
  ✓ Garantiza una respuesta
  ✓ Fácil de mantener

Desventajas:
  ✗ Costo de intentos múltiples
  ✗ Posible degradación de calidad
  ✗ Complejidad en gestión

Casos de Uso:
  • Sistemas críticos
  • Recuperación ante errores
  • Garantía de respuesta
  • Escalabilidad
    """)


if __name__ == "__main__":
    main()
