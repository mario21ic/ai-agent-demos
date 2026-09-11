"""Pattern 8: Error Handling & Recovery Pattern"""
from strands import Agent

class ErrorHandlingPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres resiliente ante errores")
        self.max_retries = 3

    def execute_with_recovery(self, task: str) -> str:
        print(f"\n{'='*70}\nERROR HANDLING & RECOVERY\n{'='*70}\n")
        for attempt in range(1, self.max_retries + 1):
            try:
                result = self.agent(f"Intento {attempt}: {task}")
                print(f"✓ Éxito en intento {attempt}")
                return str(result)
            except Exception as e:
                print(f"✗ Intento {attempt} falló: {str(e)[:50]}")
                if attempt == self.max_retries:
                    return "Error recovered gracefully"
        return "Recovered"

def main():
    pattern = ErrorHandlingPattern()
    pattern.execute_with_recovery("Tarea que podría fallar")

if __name__ == "__main__":
    main()
