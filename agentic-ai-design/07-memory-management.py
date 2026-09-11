"""Pattern 7: Memory Management Pattern"""
from strands import Agent
from typing import List

class MemoryManagementPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres agente con memoria persistente")
        self.memory: List[str] = []

    def remember_and_use(self, input_text: str) -> str:
        print(f"\n{'='*70}\nMEMORY MANAGEMENT\n{'='*70}\n")
        self.memory.append(input_text)
        context = f"Recordatorio: {' | '.join(self.memory[-3:])}"
        response = self.agent(f"{context}\n\nNueva entrada: {input_text}")
        print(f"Memoria: {len(self.memory)} items")
        print(f"Respuesta: {str(response)[:150]}...\n")
        return str(response)

def main():
    pattern = MemoryManagementPattern()
    pattern.remember_and_use("Preferencia: User prefiere brevedad")
    pattern.remember_and_use("Contexto: Trabajamos en IA")
    pattern.remember_and_use("¿Cuál es mi preferencia de comunicación?")

if __name__ == "__main__":
    main()
