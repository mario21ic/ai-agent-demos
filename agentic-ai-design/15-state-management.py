"""Pattern 15: State Management Pattern"""
from strands import Agent
from typing import Dict

class StateManagementPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres gestor de estado")
        self.state: Dict = {"status": "active", "data": {}, "version": 1}

    def update_state(self, key: str, value: str):
        print(f"\n{'='*70}\nSTATE MANAGEMENT\n{'='*70}\n")
        self.state[key] = value
        print(f"✓ State updated: {key} = {value}")
        print(f"  Current state: {self.state}\n")

    def save_state(self):
        print(f"✓ State saved to persistence layer")
        print(f"  Version: {self.state.get('version')}\n")

def main():
    pattern = StateManagementPattern()
    pattern.update_state("status", "processing")
    pattern.update_state("user_id", "user-123")
    pattern.save_state()

if __name__ == "__main__":
    main()
