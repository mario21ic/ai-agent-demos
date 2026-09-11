"""Pattern 17: Meta-Reasoning Pattern"""
from strands import Agent
from typing import Dict

class MetaReasoningPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres especialista en meta-razonamiento")

    def meta_reason(self, task: str) -> Dict:
        print(f"\n{'='*70}\nMETA-REASONING\n{'='*70}\n")

        # Razonamiento directo
        print("💭 Direct Reasoning:")
        direct = str(self.agent(f"Resuelve: {task}"))
        print(f"{direct[:100]}...\n")

        # Meta-razonamiento
        print("🧠 Meta-Reasoning:")
        meta = str(self.agent(f"¿Tu razonamiento anterior es correcto y completo?: {direct[:150]}"))
        print(f"{meta[:100]}...\n")

        return {"direct": direct, "meta": meta}

def main():
    pattern = MetaReasoningPattern()
    pattern.meta_reason("¿Cuál es la mejor forma de optimizar código Python?")

if __name__ == "__main__":
    main()
