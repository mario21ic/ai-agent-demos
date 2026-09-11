"""Pattern 16: Knowledge Graph Integration Pattern"""
from strands import Agent
from typing import List

class KnowledgeGraphPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres especialista en grafos de conocimiento")
        self.knowledge_graph = {
            "entities": ["Python", "Machine Learning", "Deep Learning", "NLP"],
            "relations": [
                ("Python", "se_usa_en", "Machine Learning"),
                ("Machine Learning", "incluye", "Deep Learning"),
                ("Deep Learning", "se_usa_en", "NLP"),
            ]
        }

    def query(self, entity: str) -> List[str]:
        print(f"\n{'='*70}\nKNOWLEDGE GRAPH INTEGRATION\n{'='*70}\n")
        related = [r[2] for r in self.knowledge_graph["relations"] if r[0] == entity]
        print(f"Entidad: {entity}")
        print(f"✓ Relacionado a: {related}\n")
        return related

def main():
    pattern = KnowledgeGraphPattern()
    pattern.query("Python")
    pattern.query("Machine Learning")
    pattern.query("Deep Learning")
    pattern.query("Rust")

if __name__ == "__main__":
    main()
