"""Pattern 14: Context Management Pattern"""
from strands import Agent
from typing import List, Dict

class ContextManagementPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres gestor de contexto")
        self.context_stack: List[Dict] = []

    def push_context(self, goal: str, metadata: Dict):
        print(f"\n{'='*70}\nCONTEXT MANAGEMENT\n{'='*70}\n")
        frame = {"goal": goal, "metadata": metadata, "timestamp": "now"}
        self.context_stack.append(frame)
        print(f"✓ Context pushed")
        print(f"  Goal: {goal}")
        print(f"  Stack size: {len(self.context_stack)}\n")

    def pop_context(self):
        if self.context_stack:
            self.context_stack.pop()
            print(f"✓ Context popped. Stack size: {len(self.context_stack)}\n")

def main():
    pattern = ContextManagementPattern()
    pattern.push_context("Resolver problema", {"priority": "high"})
    pattern.push_context("Validar solución", {"priority": "medium"})
    pattern.pop_context()

if __name__ == "__main__":
    main()
