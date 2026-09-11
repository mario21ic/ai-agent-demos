"""Pattern 10: Parallel Execution Pattern"""
from strands import Agent
from concurrent.futures import ThreadPoolExecutor

class ParallelExecutionPattern:
    def __init__(self):
        self.agents = [Agent(system_prompt=f"Eres agente {i}") for i in range(3)]

    def parallel_tasks(self, tasks: list) -> list:
        print(f"\n{'='*70}\nPARALLEL EXECUTION\n{'='*70}\n")
        results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(agent, task) for agent, task in zip(self.agents, tasks)]
            for future in futures:
                result = str(future.result())
                results.append(result)
                print(f"✓ {result[:80]}...")
        print(f"\nEjecutadas {len(results)} tareas en paralelo\n")
        return results

def main():
    pattern = ParallelExecutionPattern()
    pattern.parallel_tasks(["Tarea 1", "Tarea 2", "Tarea 3"])

if __name__ == "__main__":
    main()
