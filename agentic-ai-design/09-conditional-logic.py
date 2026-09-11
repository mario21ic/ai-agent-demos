"""Pattern 9: Conditional Logic Pattern"""
from strands import Agent

class ConditionalLogicPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres decisor inteligente")

    def conditional_execution(self, condition: str, task_a: str, task_b: str) -> str:
        print(f"\n{'='*70}\nCONDITIONAL LOGIC\n{'='*70}\n")
        decision = self.agent(f"¿Se cumple?: {condition}")
        decision_text = str(decision).lower()
        if "sí" in decision_text or "yes" in decision_text:
            result = self.agent(task_a)
            path = "A (SÍ)"
        else:
            result = self.agent(task_b)
            path = "B (NO)"
        print(f"Path ejecutado: {path}")
        print(f"Resultado: {str(result)[:150]}...\n")
        return str(result)

def main():
    pattern = ConditionalLogicPattern()
    pattern.conditional_execution(
        "¿Es urgente?",
        "Actúa rápido",
        "Planifica bien"
    )

if __name__ == "__main__":
    main()
