"""Pattern 20: Reflection & Self-Improvement Pattern"""
from strands import Agent
from typing import List

class ReflectionPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres reflexivo y autocrítico")
        self.improvements: List[str] = []

    def reflect_and_improve(self, task: str, result: str) -> str:
        print(f"\n{'='*70}\nREFLECTION & SELF-IMPROVEMENT\n{'='*70}\n")

        print(f"📌 Tarea: {task}")
        print(f"📊 Resultado: {result[:100]}...\n")

        # Reflexión
        print("🤔 Reflexionando...")
        reflection = str(self.agent(f"""
        Tarea: {task}
        Resultado: {result}

        Reflexiona:
        1. ¿Qué salió bien?
        2. ¿Qué podría mejorar?
        3. ¿Cómo actuar diferente próxima vez?
        """))

        print(f"Reflexión: {reflection[:150]}...\n")

        # Plan de mejora
        print("📈 Generando plan de mejora...")
        improvement = str(self.agent(f"""
        Basado en esta reflexión:
        {reflection[:200]}

        ¿Cuál es tu plan de mejora concreto?
        """))

        self.improvements.append(improvement)
        print(f"Plan: {improvement[:150]}...")
        print(f"Total de mejoras registradas: {len(self.improvements)}\n")

        return improvement

def main():
    pattern = ReflectionPattern()

    # Primera tarea
    pattern.reflect_and_improve(
        "Escribir código Python",
        "def hello(): return 'Hello World'"
    )

    # Segunda tarea
    pattern.reflect_and_improve(
        "Diseñar API REST",
        "GET /users, POST /users, DELETE /users/{id}"
    )

    print("="*70)
    print("REFLECTION & SELF-IMPROVEMENT CHARACTERISTICS")
    print("="*70)
    print("""
Ventajas:
  ✓ Mejora continua
  ✓ Autoaprendizaje
  ✓ Adaptación automática
  ✓ Evolución del agente

Desventajas:
  ✗ Complejidad adicional
  ✗ Overhead computacional
  ✗ Difícil de debuggear

Casos de Uso:
  • Sistemas que mejoran con tiempo
  • Aprendizaje continuo
  • Adaptación a nuevas situaciones
    """)

if __name__ == "__main__":
    main()
